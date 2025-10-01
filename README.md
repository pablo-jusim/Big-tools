# 🛠️ Sistema Experto para Mantenimiento de Motores

Proyecto académico desarrollado en la materia Prácticas Profesionalizantes.
Este sistema experto tiene como objetivo asistir en la gestión de mantenimiento preventivo y correctivo de motores, clasificando fallos, proponiendo acciones y generando un historial de consultas. <br /> <br />

<p align="center">
<img width="225" height="225" alt="image" src="https://github.com/user-attachments/assets/266eae85-3c09-46b7-b60b-3cbf29bb9f10" />
<p/>

## 📌 Contexto

El proyecto fue realizado para la empresa Big Tools como parte de un trabajo práctico de integración. El sistema busca mejorar la eficiencia en la detección y
resolución de incidencias relacionadas con motores, combinando reglas predefinidas y un modelo de machine learning básico para casos ambiguos. <br /> <br />


## 🎯 Objetivos

Detectar hechos de entrada (palabras clave en consultas técnicas).

Clasificar los reclamos/solicitudes en distintas categorías.

Implementar reglas de decisión y machine learning para mayor precisión.

Exponer un endpoint con FastAPI que reciba un mensaje y devuelva una categoría.

Incorporar un historial de consultas para mejorar las reglas o el modelo con el tiempo. <br /> <br />


## 🏗️ Tecnologías utilizadas

Python 3.11+

FastAPI para la API REST

scikit-learn para el modelo de clasificación

pandas para manejo de datos

Uvicorn como servidor de desarrollo  <br /> <br />


## 📜 Licencia

Este proyecto se distribuye bajo la Licencia MIT.
© 2025, desarrollado por estudiantes de Prácticas Profesionalizantes II del Politécnico Malvinas Argentinas para Big Tools.
