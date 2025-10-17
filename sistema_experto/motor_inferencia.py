import json
import os
from collections import Counter

class MotorDiagnostico:
    """
    Clase que encapsula la lógica del sistema experto de diagnóstico diferencial.
    """
    def __init__(self, nombre_archivo_conocimiento):
        ruta_script = os.path.dirname(__file__)
        ruta_completa = os.path.join(ruta_script, nombre_archivo_conocimiento)
        
        self.conocimiento = self._cargar_base_conocimiento(ruta_completa)

        if self.conocimiento:
            self.mapeo_palabras_clave = self.conocimiento.get('mapeo_palabras_clave', {})
            self.fallas = self.conocimiento.get('fallas', [])
            self.preguntas = self.conocimiento.get('preguntas', {})
            print("✅ Motor de diagnóstico listo.")
        else:
            print("🚨 Error: El motor de diagnóstico no pudo inicializarse.")
    
    def _cargar_base_conocimiento(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except Exception as e:
            print(f"🚨 Error crítico al cargar la base de conocimiento en '{ruta_archivo}': {e}")
            return None

    def _extraer_atributos_iniciales(self, mensaje):
        atributos = set()
        mensaje_lower = mensaje.lower()
        for atributo, palabras_clave in self.mapeo_palabras_clave.items():
            if any(palabra in mensaje_lower for palabra in palabras_clave):
                atributos.add(atributo)
        return list(atributos)

    def _calcular_siguiente_paso(self, posibles_fallas_indices, atributos_preguntados):
        # Si llegamos a una o ninguna falla, el diagnóstico termina.
        if len(posibles_fallas_indices) <= 1:
            resultado_final = None
            if posibles_fallas_indices:
                resultado_final = self.fallas[posibles_fallas_indices[0]]
            # Si hay más de una falla pero no más preguntas, se muestran las opciones restantes.
            elif len(posibles_fallas_indices) > 1:
                 resultado_final = [self.fallas[i] for i in posibles_fallas_indices]

            return {"tipo": "solucion", "resultado": resultado_final}

        contador_atributos = Counter()
        posibles_fallas_obj = [self.fallas[i] for i in posibles_fallas_indices]

        for falla in posibles_fallas_obj:
            for atributo in falla['atributos']:
                if atributo not in atributos_preguntados:
                    contador_atributos[atributo] += 1
        
        # Si no hay más preguntas que hacer, se devuelve la lista de fallas restantes.
        if not contador_atributos:
            return {"tipo": "solucion", "resultado": posibles_fallas_obj}

        mejor_atributo = contador_atributos.most_common(1)[0][0]
        pregunta_texto = self.preguntas.get(mejor_atributo, f"¿Se cumple la condición '{mejor_atributo}'?")
        
        return {"tipo": "pregunta", "pregunta": pregunta_texto, "atributo_actual": mejor_atributo}

    def iniciar_diagnostico(self, descripcion):
        if not self.conocimiento:
            return {"error": "Base de conocimiento no cargada."}

        atributos_iniciales = self._extraer_atributos_iniciales(descripcion)
        posibles_fallas_indices = list(range(len(self.fallas)))

        if atributos_iniciales:
            # Filtro inicial: nos quedamos con las fallas que tienen AL MENOS UNO de los atributos mencionados.
            fallas_filtradas_indices = set()
            for attr in atributos_iniciales:
                for i, falla in enumerate(self.fallas):
                    if attr in falla['atributos']:
                        fallas_filtradas_indices.add(i)
            posibles_fallas_indices = list(fallas_filtradas_indices)

        siguiente_paso = self._calcular_siguiente_paso(posibles_fallas_indices, atributos_iniciales)
        
        # Construimos el estado inicial que se enviará al front-end.
        estado = {
            "posibles_fallas_indices": posibles_fallas_indices,
            "atributos_preguntados": atributos_iniciales,
            # **CLAVE**: Incluimos el 'atributo_actual' de la pregunta que estamos haciendo.
            "atributo_actual": siguiente_paso.get('atributo_actual')
        }
        siguiente_paso['estado'] = estado
        
        return siguiente_paso

    def procesar_respuesta(self, estado, respuesta_usuario):
        if not self.conocimiento:
            return {"error": "Base de conocimiento no cargada."}

        posibles_fallas_indices = estado.get('posibles_fallas_indices', [])
        atributos_preguntados = set(estado.get('atributos_preguntados', []))
        atributo_actual = estado.get('atributo_actual') # El atributo de la pregunta que se acaba de responder.

        if atributo_actual:
            atributos_preguntados.add(atributo_actual) # Marcamos la pregunta como hecha.
            
            if respuesta_usuario == 'si':
                posibles_fallas_indices = [i for i in posibles_fallas_indices if atributo_actual in self.fallas[i]['atributos']]
            else:
                posibles_fallas_indices = [i for i in posibles_fallas_indices if atributo_actual not in self.fallas[i]['atributos']]

        siguiente_paso = self._calcular_siguiente_paso(posibles_fallas_indices, list(atributos_preguntados))
        
        # Construimos el NUEVO estado para el siguiente turno.
        nuevo_estado = {
            "posibles_fallas_indices": posibles_fallas_indices,
            "atributos_preguntados": list(atributos_preguntados),
            # **CLAVE**: Incluimos el 'atributo_actual' de la NUEVA pregunta que vamos a hacer.
            "atributo_actual": siguiente_paso.get('atributo_actual')
        }
        siguiente_paso['estado'] = nuevo_estado
        
        return siguiente_paso

