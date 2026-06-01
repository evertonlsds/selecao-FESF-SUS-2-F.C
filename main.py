from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List


from schemas import FuncionarioCreate, FuncionarioResponse, PacienteCreate, PacienteResponse

app = FastAPI(title="Sistema de Gestão Clínica FESF-SUS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


db_funcionarios = []
db_pacientes = []
id_funcionario_counter = 1
id_paciente_counter = 1



def get_current_user(token: str = Depends(oauth2_scheme)):
    if token == "admin-token-secreto":
        return {"username": "admin", "role": "admin"}
    
    for f in db_funcionarios:
        if f["username"] == token:
            return {"username": f["username"], "role": "funcionario", "nome": f["nome"]}
            
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

def verify_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas o Administrador pode realizar esta ação."
        )
    return current_user



@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "admin" and form_data.password == "admin":
        return {"access_token": "admin-token-secreto", "token_type": "bearer"}
    
    for f in db_funcionarios:
        if f["username"] == form_data.username and f["password"] == form_data.password:
            return {"access_token": f["username"], "token_type": "bearer"}
            
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Usuário ou senha incorretos"
    )

@app.post("/funcionarios/", response_model=FuncionarioResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_funcionario(funcionario: FuncionarioCreate, admin: dict = Depends(verify_admin)):
    global id_funcionario_counter
    
    for f in db_funcionarios:
        if f["username"] == funcionario.username:
            raise HTTPException(status_code=400, detail="Este nome de usuário já está em uso")

    novo_funcionario = {
        "id": id_funcionario_counter,
        "nome": funcionario.nome,
        "data_nascimento": funcionario.data_nascimento,
        "cargo": funcionario.cargo,
        "username": funcionario.username,
        "password": funcionario.password,
        "ativo": True
    }
    db_funcionarios.append(novo_funcionario)
    id_funcionario_counter += 1
    return novo_funcionario

@app.get("/funcionarios/", response_model=List[FuncionarioResponse])
def listar_funcionarios(current_user: dict = Depends(get_current_user)):
    return db_funcionarios

@app.post("/pacientes/", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_paciente(paciente: PacienteCreate, current_user: dict = Depends(get_current_user)):
    global id_paciente_counter
    
    novo_paciente = {
        "id": id_paciente_counter,
        "nome": paciente.nome,
        "data_nascimento": paciente.data_nascimento,
        "sintomas": paciente.sintomas,
        "nivel_sintoma": paciente.nivel_sintoma,
        "cadastrado_por": current_user["username"]
    }
    db_pacientes.append(novo_paciente)
    id_paciente_counter += 1
    return novo_paciente

@app.get("/pacientes/", response_model=List[PacienteResponse])
def listar_pacientes(current_user: dict = Depends(get_current_user)):
    return db_pacientes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)