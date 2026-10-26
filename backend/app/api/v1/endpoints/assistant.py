from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.models.entities import StudentProfile, CareerRole, ChatSession, ChatMessage
from backend.app.schemas.career_schemas import ChatMessageCreate, ChatMessageResponse
from backend.app.services.ai_assistant_service import AIAssistantService

router = APIRouter(prefix="/assistant", tags=["AI Career Assistant"])

@router.post("/chat", response_model=ChatMessageResponse)
def chat_with_assistant(chat_in: ChatMessageCreate, db: Session = Depends(get_db)):
    # 1. Resolve or create chat session
    session = None
    if chat_in.session_id:
        session = db.query(ChatSession).filter(ChatSession.id == chat_in.session_id).first()

    if not session:
        session = ChatSession(
            student_profile_id=chat_in.student_profile_id,
            title="Guidance Session",
            selected_role_slug=chat_in.career_role_slug
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    # 2. Retrieve student and career role context if available
    student = None
    if chat_in.student_profile_id:
        student = db.query(StudentProfile).filter(StudentProfile.id == chat_in.student_profile_id).first()

    role = None
    if chat_in.career_role_slug:
        role = db.query(CareerRole).filter(CareerRole.slug == chat_in.career_role_slug).first()

    # 3. Save student's incoming message
    user_msg = ChatMessage(
        session_id=session.id,
        role="user",
        content=chat_in.message
    )
    db.add(user_msg)
    db.commit()

    # 4. Invoke AI assistant service
    ai_result = AIAssistantService.generate_reply(
        user_message=chat_in.message,
        student=student,
        role=role
    )

    # 5. Save assistant reply
    assistant_msg = ChatMessage(
        session_id=session.id,
        role="assistant",
        content=ai_result["reply"],
        is_fallback=ai_result["is_fallback"]
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    return ChatMessageResponse(
        session_id=session.id,
        role="assistant",
        content=assistant_msg.content,
        is_fallback=assistant_msg.is_fallback,
        timestamp=assistant_msg.timestamp,
        sources=ai_result.get("sources", [])
    )
