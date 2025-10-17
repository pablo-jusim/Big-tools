import json
from collections import Counter

RUTA_BASE_CONOCIMIENTO = 'base_hidrolavadora.json'

def cargar_base_conocimiento(ruta_archivo):
    """Carga la base de conocimiento desde un archivo JSON."""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            print("✅ Base de conocimiento cargada correctamente.")
            return json.load(archivo)
    except FileNotFoundError:
        print(f"🚨 Error: No se encontró el archivo '{ruta_archivo}'.")
        return None
    except json.JSONDecodeError:
        print(f"🚨 Error: El archivo '{ruta_archivo}' no tiene un formato JSON válido.")
        return None

def extraer_atributos_iniciales(mensaje, mapeo):
    """
    Analiza el mensaje de texto libre del usuario y extrae los atributos conocidos.
    """
    atributos_encontrados = set()
    mensaje_lower = mensaje.lower()
    for atributo, palabras_clave in mapeo.items():
        for palabra in palabras_clave:
            if palabra in mensaje_lower:
                atributos_encontrados.add(atributo)
                break # Pasa al siguiente atributo una vez que se encuentra una coincidencia
    return atributos_encontrados

def diagnostico_guiado():
    """
    Motor de inferencia que primero analiza el texto del usuario y luego
    realiza preguntas adicionales para refinar el diagnóstico.
    """
    CONOCIMIENTO = cargar_base_conocimiento(RUTA_BASE_CONOCIMIENTO)
    if not CONOCIMIENTO:
        return

    # --- FASE 1: ENTRADA DE TEXTO LIBRE Y EXTRACCIÓN DE ATRIBUTOS ---
    print("\n--- 🛠️ Asistente de Diagnóstico Avanzado para Hidrolavadora 🛠️ ---")
    mensaje_usuario = input("Por favor, describe el problema con tus propias palabras: ")

    atributos_iniciales = extraer_atributos_iniciales(mensaje_usuario, CONOCIMIENTO['mapeo_palabras_clave'])
    
    if atributos_iniciales:
        print("\n✔️ Entendido. He identificado las siguientes características del problema:")
        for attr in atributos_iniciales:
            print(f"  - {attr}")
    else:
        print("\n🤔 No he podido extraer pistas iniciales. Empezaré con preguntas generales.")

    # --- FASE 2: DIAGNÓSTICO DIFERENCIAL ---
    posibles_fallas = list(CONOCIMIENTO['fallas'])
    preguntas = CONOCIMIENTO['preguntas']
    atributos_conocidos = set(atributos_iniciales) # Atributos confirmados (iniciales + respuestas)

    print("\nAhora haré algunas preguntas para confirmar y precisar el diagnóstico. Responde con 'si' o 'no'.")

    while len(posibles_fallas) > 1:
        contador_atributos = Counter()
        for falla in posibles_fallas:
            for atributo in falla['atributos']:
                if atributo not in atributos_conocidos:
                    contador_atributos[atributo] += 1
        
        if not contador_atributos:
            break

        mejor_atributo, _ = contador_atributos.most_common(1)[0]
        
        # Saltamos la pregunta si ya la inferimos del texto inicial.
        if mejor_atributo in atributos_iniciales:
            # Confirmamos el atributo y filtramos la lista de fallas.
            posibles_fallas = [f for f in posibles_fallas if mejor_atributo in f['atributos']]
            atributos_conocidos.add(mejor_atributo)
            continue # Pasamos a la siguiente iteración del bucle

        # Hacemos la pregunta al usuario.
        pregunta_texto = preguntas.get(mejor_atributo, f"¿Se cumple la condición '{mejor_atributo}'?")
        respuesta = input(f"\n❓ {pregunta_texto} (si/no): ").lower().strip()

        if respuesta == 'si':
            posibles_fallas = [f for f in posibles_fallas if mejor_atributo in f['atributos']]
            atributos_conocidos.add(mejor_atributo)
        elif respuesta == 'no':
            posibles_fallas = [f for f in posibles_fallas if mejor_atributo not in f['atributos']]
            atributos_conocidos.add(mejor_atributo) # También lo marcamos para no volver a preguntar
        else:
            print("Respuesta no válida. Intente de nuevo.")

    # --- FASE 3: RESULTADO FINAL ---
    print("\n------------------ Diagnóstico Final ------------------")
    if len(posibles_fallas) == 1:
        falla_final = posibles_fallas[0]
        print(f"💡 El problema más probable es: **{falla_final['nombre']}**")
        print(f"✅ **Solución sugerida:** {falla_final['solucion']}")
        print(f"*(Referencia del manual: {falla_final.get('referencia', 'N/A')})*")
    elif len(posibles_fallas) > 1:
        print("🤔 No pude llegar a una única conclusión. Las fallas más probables son:")
        for falla in posibles_fallas:
            print(f"  - {falla['nombre']}")
    else:
        print("🤷‍♂️ No pude encontrar una falla que coincida con la información proporcionada.")

if __name__ == '__main__':
    diagnostico_guiado()