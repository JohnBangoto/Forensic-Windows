# backend/app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import auth, models, schemas, database
from fastapi import Query


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser agent Tkinter à communiquer
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur notre API !"}

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import auth, models, schemas, database

# ...

@app.post("/signup", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    # Vérifier si l'utilisateur existe déjà
    existing_user = auth.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un compte existe déjà avec cet e-mail."
        )
    # Créer un nouvel utilisateur
    return auth.create_user(user, db)


@app.post("/login", response_model=schemas.UserResponse)
def login(user: schemas.UserLogin, db: Session = Depends(auth.get_db)):
    db_user = auth.authenticate_user(user, db)  # renvoie l'utilisateur ou lève HTTPException
    return db_user

@app.post("/collections")
def create_collection(session: schemas.CollectionCreate, db: Session = Depends(auth.get_db)):
    new_session = schemas.CollectionSession(**session.dict())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@app.post("/session", status_code=201)
def record_collection(
    session: schemas.CollectionCreate,
    email: str = Query(..., description="Email de l'utilisateur"),
    db: Session = Depends(auth.get_db)
):
    user = auth.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    return auth.create_collection_session(
    db=db,
    user_id=user.id,
    hostname=session.hostname,
    system=session.system,
    filename=session.file_name,
    path=session.file_path,
    errors=session.error_count,
    drive_url=session.drive_url
)


