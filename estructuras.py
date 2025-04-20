from typing import Optional
from models import VueloDB
from sqlalchemy.orm import Session

class Nodo:
    def __init__(self, vuelo: VueloDB):
        self.vuelo = vuelo
        self.anterior: Optional['Nodo'] = None
        self.siguiente: Optional['Nodo'] = None

class ListaVuelos:
    def __init__(self, session: Session):
        self.cabeza: Optional[Nodo] = None
        self.cola: Optional[Nodo] = None
        self.size = 0
        self.session = session

    def insertar_al_frente(self, vuelo: VueloDB):
        nodo = Nodo(vuelo)
        if not self.cabeza:
            self.cabeza = self.cola = nodo
        else:
            nodo.siguiente = self.cabeza
            self.cabeza.anterior = nodo
            self.cabeza = nodo
        self.size += 1
        self.session.add(vuelo)
        self.session.commit()

    def insertar_al_final(self, vuelo: VueloDB):
        nodo = Nodo(vuelo)
        if not self.cola:
            self.cabeza = self.cola = nodo
        else:
            nodo.anterior = self.cola
            self.cola.siguiente = nodo
            self.cola = nodo
        self.size += 1
        self.session.add(vuelo)
        self.session.commit()

    def obtener_primero(self) -> Optional[VueloDB]:
        return self.cabeza.vuelo if self.cabeza else None

    def obtener_ultimo(self) -> Optional[VueloDB]:
        return self.cola.vuelo if self.cola else None

    def longitud(self) -> int:
        return self.size

    def insertar_en_posicion(self, vuelo: VueloDB, posicion: int):
        if posicion <= 0:
            return self.insertar_al_frente(vuelo)
        elif posicion >= self.size:
            return self.insertar_al_final(vuelo)

        nodo = Nodo(vuelo)
        actual = self.cabeza
        for _ in range(posicion):
            actual = actual.siguiente

        nodo.anterior = actual.anterior
        nodo.siguiente = actual
        actual.anterior.siguiente = nodo
        actual.anterior = nodo
        self.size += 1
        self.session.add(vuelo)
        self.session.commit()

    def extraer_de_posicion(self, posicion: int) -> Optional[VueloDB]:
        if posicion < 0 or posicion >= self.size:
            return None
        actual = self.cabeza
        for _ in range(posicion):
            actual = actual.siguiente

        if actual.anterior:
            actual.anterior.siguiente = actual.siguiente
        else:
            self.cabeza = actual.siguiente

        if actual.siguiente:
            actual.siguiente.anterior = actual.anterior
        else:
            self.cola = actual.anterior

        self.size -= 1
        self.session.delete(actual.vuelo)
        self.session.commit()
        return actual.vuelo

    def listar_vuelos(self):
        vuelos = []
        actual = self.cabeza
        while actual:
            vuelos.append(actual.vuelo)
            actual = actual.siguiente
        return vuelos

    def reordenar_por_retraso(self):
        vuelos = self.listar_vuelos()
        self.cabeza = self.cola = None
        self.size = 0

        # Prioridad: emergencia > retrasado > programado
        orden = {"emergencia": 0, "retrasado": 1, "programado": 2}
        vuelos.sort(key=lambda v: orden[v.estado.value])

        for vuelo in vuelos:
            self.insertar_al_final(vuelo)
