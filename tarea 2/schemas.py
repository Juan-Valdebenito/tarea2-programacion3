from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models import EstadoVuelo

class Vuelo(BaseModel):
    codigo: str
    estado: EstadoVuelo
    hora: datetime
    origen: str
    destino: str

    class Config:
        orm_mode = True
