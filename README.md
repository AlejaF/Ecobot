# Ecobot

## Descripción
El proyecto aborda el reto de identificar materiales en movimiento dentro de un entorno de computación de borde (edge computing), utilizando hardware de bajos recursos como la Raspberry Pi 3.

En la fase inicial, se evalúa la implementación de un sistema de visión artificial aplicado a la clasificación automatizada de residuos sólidos (botellas PET, envases rígidos, empaques flexibles y Tetra Pak) para las estaciones de reciclaje Ecobot.

## Características
- Clasificación automatizada de residuos sólidos mediante visión artificial.
- Configuración personalizable a través del archivo `config.yaml`.
- Procesamiento por lotes con parámetros ajustables.
- Integración con una base de datos para almacenamiento y recuperación de datos.
- Optimización para hardware de bajos recursos.

## Estructura del Proyecto
- config.yaml: Archivo de configuración para personalizar el comportamiento del sistema.
- data/: Directorio para almacenar archivos de datos.
- database.py: Módulo para la interacción con la base de datos.
- dataset/: Directorio para almacenar conjuntos de datos.
- main.py: Punto de entrada principal del proyecto.
- test.py: Archivo que contiene las pruebas unitarias del proyecto.
- README.md: Documentación del proyecto.