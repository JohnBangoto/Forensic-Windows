from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas, database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_user(user: schemas.UserCreate, db: Session):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    new_user = models.User(
        email=user.email,
        password_hash=get_password_hash(user.password)  # ✅ correct
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(user: schemas.UserLogin, db: Session):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_collection_session(db: Session, user_id: int, hostname: str, system: str, filename: str, path: str, errors: int, drive_url: str = None):
    from . import models
    session = models.CollectionSession(
        user_id=user_id,
        hostname=hostname,
        system=system,
        file_name=filename,
        file_path=str(path),
        error_count=errors,
        uploaded_to_drive=bool(drive_url),
        drive_url=drive_url
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session