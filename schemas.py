from pydantic import BaseModel
from datetime import date


class FuncionarioCreate(BaseModel):
    nome: str
    data_nascimento: date
    cargo: str
    username: str
    password: str

class FuncionarioResponse(BaseModel):
    id: int
    nome: str
    data_nascimento: date
    cargo: str
    username: str
    ativo: bool


class PacienteCreate(BaseModel):
    nome: str
    data_nascimento: date
    sintomas: str
    nivel_sintoma: int  # 1 = Moderado, 2 = Grave

class PacienteResponse(BaseModel):
    id: int
    nome: str
    data_nascimento: date
    sintomas: str
    nivel_sintoma: int
    cadastrado_por: str