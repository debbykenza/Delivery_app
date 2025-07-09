from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    mot_de_passe: str
    # role: str  

class ChangePasswordRequest(BaseModel):
    ancien_mot_de_passe: str
    nouveau_mot_de_passe: str
    confirmation_nouveau_mot_de_passe: str

class RegisterRequest(BaseModel):
    nom: str
    email: EmailStr
    mot_de_passe: str
    role: str  
    is_active: bool = True  

class RegisterResponse(BaseModel):
    id: str
    nom: str
    email: EmailStr
    # role: str
    # is_active: bool

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
