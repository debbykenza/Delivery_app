from app.core.database import SessionLocal
from app.core.security import create_access_token
from fastapi import Depends, HTTPException, status  
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/inscription", response_model=RegisterResponse)
def inscription_utilisateur(
    user_data: RegisterRequest,
    db: Session = Depends(lambda: SessionLocal())
):
    """
    Endpoint to register a new user.
    """
    from app.services.utilisateur import creer_utilisateur 
    
    nouvel_utilisateur = creer_utilisateur(db, user_data)

    return RegisterResponse(
        id=str(nouvel_utilisateur.id),
        email=nouvel_utilisateur.email,
        nom=nouvel_utilisateur.nom,
        # role: nouvel_utilisateur.role,
        # is_active: bool
    )
    
@router.post("/connexion", response_model=LoginResponse)
def connexion_utilisateur(
    user_data: LoginRequest,
    db: Session = Depends(lambda: SessionLocal())
):
    """
    Endpoint to login a user.
    """
    from app.services.utilisateur import authentifier_utilisateur
    utilisateur = authentifier_utilisateur(db, user_data.email, user_data.mot_de_passe)
    
    if not utilisateur:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if utilisateur.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    
    
    access_token = create_access_token(data={"sub": str(utilisateur.id)})
    
    return LoginResponse(access_token=access_token, token_type="bearer")
