from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from backend.app.db.session import get_db
from backend.app.agents.workflow import AgenticCareerWorkflow

router = APIRouter(prefix="/workflow", tags=["Agentic Workflow Orchestrator"])

class WorkflowRunRequest(BaseModel):
    student_profile_id: int
    selected_role_slug: Optional[str] = None

@router.post("/run")
def run_orchestrated_career_workflow(
    request: WorkflowRunRequest,
    db: Session = Depends(get_db)
):
    """
    Triggers the controlled multi-component agentic planning pipeline:
    Profile Analysis -> Recommendation -> Skill-Gap -> Roadmap Planning -> Quality Review -> Human Review Step.
    """
    result = AgenticCareerWorkflow.run_planning_workflow(
        db=db,
        student_id=request.student_profile_id,
        selected_role_slug=request.selected_role_slug
    )
    if result.get("status") == "error":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message")
        )
    return result
