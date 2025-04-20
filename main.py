from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, VueloDB
from schemas import Vuelo
from estructuras import ListaVuelos

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    global lista
    db = next(get_session())
    lista = ListaVuelos(db)

@app.post("/vuelos/")
def agregar_vuelo(vuelo: Vuelo):
    vuelo_db = VueloDB(**vuelo.dict())
    if vuelo.estado.value == "emergencia":
        lista.insertar_al_frente(vuelo_db)
    else:
        lista.insertar_al_final(vuelo_db)
    return {"mensaje": "Vuelo agregado"}

@app.get("/vuelos/total")
def total_vuelos():
    return {"total": lista.longitud()}

@app.get("/vuelos/proximo")
def vuelo_proximo():
    return lista.obtener_primero()

@app.get("/vuelos/ultimo")
def vuelo_ultimo():
    return lista.obtener_ultimo()

@app.post("/vuelos/insertar/{posicion}")
def insertar_vuelo(vuelo: Vuelo, posicion: int):
    vuelo_db = VueloDB(**vuelo.dict())
    lista.insertar_en_posicion(vuelo_db, posicion)
    return {"mensaje": f"Vuelo insertado en la posición {posicion}"}

@app.get("/vuelos/extraer/{posicion}")
def extraer_vuelo(posicion: int):
    vuelo = lista.extraer_de_posicion(posicion)
    if vuelo:
        return vuelo
    return {"mensaje": "Posición no válida"}

@app.get("/vuelos/lista")
def listar_vuelos():
    return lista.listar_vuelos()

@app.patch("/vuelos/reordenar")
def reordenar():
    lista.reordenar_por_retraso()
    return {"mensaje": "Vuelos reordenados por prioridad"}
