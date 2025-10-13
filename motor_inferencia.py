import json
import difflib
from typing import List, Dict

class MotorInferencia:
    def __init__(self, ruta_base: str):
        with open(ruta_base, "r", encoding="utf-8") as f:
            self.base_conocimiento = json.load(f)

    def buscar_falla(self, descripcion_usuario: str, umbral: float = 0.4) -> List[Dict]:
        """
        Analiza la descripción del usuario y busca coincidencias en la base.
        Retorna una lista ordenada de posibles fallas (por similitud).
        """
        resultados = []
        descripcion_usuario = descripcion_usuario.lower()

        for falla in self.base_conocimiento:
            # Unimos todos los textos relevantes de la falla
            texto_falla = (
                falla["falla"] + " " +
                " ".join(falla["sintomas"]) + " " +
                " ".join(falla["causas"])
            ).lower()

            # Medir similitud semántica (aproximada).
            similitud = difflib.SequenceMatcher(None, descripcion_usuario, texto_falla).ratio()

            if similitud >= umbral:
                resultados.append({
                    "id": falla["id"],
                    "falla": falla["falla"],
                    "similitud": round(similitud, 2),
                    "causas": falla["causas"],
                    "soluciones": falla["soluciones"]
                })

        resultados.sort(key=lambda x: x["similitud"], reverse=True)
        return resultados

    def diagnosticar(self, descripcion_usuario: str):
        """
        Devuelve la falla más probable según la descripción del usuario.
        """
        posibles = self.buscar_falla(descripcion_usuario)
        if not posibles:
            return {"mensaje": "No se encontraron coincidencias. Intenta describir el problema con más detalle."}

        mejor = posibles[0]
        return {
            "falla_probable": mejor["falla"],
            "similitud": mejor["similitud"],
            "causas_probables": mejor["causas"],
            "soluciones_sugeridas": mejor["soluciones"]
        }
