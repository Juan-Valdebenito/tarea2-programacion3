from sqlalchemy import Column, String, DateTime, Enum as SqlEnum
from database import Base
import enum

class EstadoVuelo(enum.Enum):
    programado = "programado"
    emergencia = "emergencia"
    retrasado = "retrasado"

class VueloDB(Base):
    __tablename__ = "vuelos"
    codigo = Column(String, primary_key=True, index=True)
    estado = Column(SqlEnum(EstadoVuelo), nullable=False)
    hora = Column(DateTime)
    origen = Column(String)
    destino = Column(String)
