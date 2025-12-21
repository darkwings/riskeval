"""
FastAPI application for the insurance risk evaluation system.

This API provides a REST endpoint to evaluate insurance policy risk
using the ADK agent system with parallel risk evaluators.
"""

import asyncio
import logging
import traceback
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from risk_evaluator.agent import root_agent
from risk_evaluator.shared_libraries.types import PolicyRequest, RiskEvaluation, RiskScore
from google.adk.apps import App
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Insurance Risk Evaluator API",
    description="API for evaluating insurance policy risk using parallel AI agents",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RiskEvaluationResponse(BaseModel):
    """Response model for risk evaluation"""
    geographic_risk: RiskEvaluation | None = None
    vehicle_risk: RiskEvaluation | None = None
    person_risk: RiskEvaluation | None = None
    global_risk: RiskEvaluation
    request: PolicyRequest


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Insurance Risk Evaluator API",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "agent": "root_agent",
        "evaluators": ["geographic", "vehicle", "person", "global"]
    }


@app.post("/evaluate", response_model=RiskEvaluationResponse)
async def evaluate_risk(policy_request: PolicyRequest):
    """
    Evaluate insurance policy risk.

    This endpoint runs parallel risk evaluators (geographic, vehicle, person)
    and combines their assessments into a final global risk score.

    Args:
        policy_request: Policy holder and vehicle information

    Returns:
        RiskEvaluationResponse with individual and global risk assessments

    Raises:
        HTTPException: If evaluation fails
    """
    try:
        # Create the ADK app and session service
        adk_app = App(name='risk_eval_api', root_agent=root_agent)
        session_service = InMemorySessionService()

        # Create session
        user_id = 'api_user'
        session_id = f'session_{id(policy_request)}'  # Unique session per request
        await session_service.create_session(
            user_id=user_id,
            session_id=session_id,
            app_name='risk_eval_api'
        )

        # Create runner
        runner = Runner(app=adk_app, session_service=session_service)

        # Create input message for the agent
        message = types.Content(
            role='user',
            parts=[types.Part(text=f"""
Please evaluate the insurance risk for the following policy application:

City: {policy_request.city}
Tariff ID: {policy_request.tariff_id}
Vehicle Brand: {policy_request.vehicle_brand}
Fiscal Code: {policy_request.fiscal_code}

Provide a complete risk evaluation.
""")]
        )

        # Collect results from agent events
        geographic_risk = None
        vehicle_risk = None
        person_risk = None
        global_risk = None

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message
        ):
            # Check for structured outputs in state_delta
            if event.actions and event.actions.state_delta:
                state_delta = event.actions.state_delta

                if "geographic_risk" in state_delta:
                    geographic_risk = RiskEvaluation(**state_delta["geographic_risk"])
                if "vehicle_risk" in state_delta:
                    vehicle_risk = RiskEvaluation(**state_delta["vehicle_risk"])
                if "person_risk" in state_delta:
                    person_risk = RiskEvaluation(**state_delta["person_risk"])
                if "global_risk" in state_delta:
                    global_risk = RiskEvaluation(**state_delta["global_risk"])

        # Ensure we have at least the global risk
        if global_risk is None:
            raise HTTPException(
                status_code=500,
                detail="Risk evaluation failed: No global risk assessment generated"
            )

        return RiskEvaluationResponse(
            geographic_risk=geographic_risk,
            vehicle_risk=vehicle_risk,
            person_risk=person_risk,
            global_risk=global_risk,
            request=policy_request
        )

    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        logger.error("Risk evaluation failed with exception:")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Risk evaluation failed: {str(e)}"
        )


@app.post("/evaluate/global-only")
async def evaluate_risk_global_only(policy_request: PolicyRequest):
    """
    Evaluate insurance policy risk and return only the global assessment.

    Lightweight endpoint that returns just the final risk score and evaluation.

    Args:
        policy_request: Policy holder and vehicle information

    Returns:
        Global risk evaluation only
    """
    result = await evaluate_risk(policy_request)
    return {
        "score": result.global_risk.score,
        "evaluation": result.global_risk.evaluation,
        "request": result.request
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
