import hashlib
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Sessions, User


def createSession(session: Session, username_email: str) -> str:
    session_id = uuid4().hex

    stmt = select(User).where(
        (User.username == username_email) | (User.email == username_email)
    )
    user = session.scalar(stmt)

    if user is None:
        return None

    # Delete existing session for user (if any)
    stmt_existing = select(Sessions).where(Sessions.userId == user.id)
    existing_session = session.scalar(stmt_existing)

    if existing_session:
        session.delete(existing_session)
        session.commit()

    # Create new session
    new_session = Sessions(sessionId=session_id, userId=user.id)
    session.add(new_session)
    session.commit()

    return session_id


def isUserValid(session: Session, username_email: str, password: str) -> bool:
    stmt = select(User).where(
        (User.username == username_email) | (User.email == username_email)
    )
    user = session.scalar(stmt)

    if user is None or user.password_hash != hashFunction(password):
        return False

    return True


def hashFunction(password):
    m = hashlib.sha1()
    salt = 'gvUiUR88'
    b = bytes(password + salt, 'utf-8')
    m.update(b)
    hashed = m.hexdigest()
    return hashed
