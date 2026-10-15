# AeroEntrega 2 · Diseño de Máquinas

## Ejecutar en PyCharm
1. Descomprima el ZIP en una carpeta nueva y abra `drones_clase` como proyecto.
2. Utilice Python 3.11 o 3.12 con entorno virtual.
3. Abra la terminal de PyCharm en la carpeta que contiene app.py:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Abra http://localhost:8501. Detenga con Ctrl+C. No use la ejecución normal de app.py.
En Run Configuration: Module name = streamlit; Parameters = run app.py; Working directory = carpeta drones_clase.

IMPORTANTE: reinicie el servidor anterior; abra esta nueva carpeta, no la versión previa. Se incluye .streamlit/config.toml con tema claro. La carpeta de trabajo debe ser drones_clase para aplicar el tema a controles y tablas. Los gráficos también fuerzan fondo blanco, texto oscuro y desactivan la adaptación automática de Streamlit.

## Contenido
- app.py: resumen ejecutivo, encuesta, mercado, ciclo de vida, resultados, sensibilidad y taller.
- modelo.py: encuesta sintética correlacionada y simulación comercial/económica.
- METODOLOGIA.md: fórmulas, supuestos y límites.
- datos_ficticios.csv: 120 empresas reproducibles.
- resultados_ejemplo.csv: proyección base de 48 meses.
- verificar.py: identidades de cartera y verificaciones del modelo.
- requirements.txt y .streamlit/config.toml.

## Cambios de la versión 2
Tema claro uniforme, gráficos legibles, indicadores y conclusión financiera. Se separan demanda total del sector, pedidos de la empresa y entregas facturadas. Incluye competencia, notoriedad progresiva, aceptación del precio, plazos, cartera vencida, cancelaciones, rampa de producción y rendimiento. La curva sectorial tiene estacionalidad y perturbaciones reproducibles. No se introduce una brecha artificial para hacer diferentes las curvas.

La pestaña Diseño y clase incorpora funciones, alternativas, matriz de selección editable, requisitos, plan de verificación y taller de 100 minutos con evaluación. Se trata de diseño conceptual; no es un cálculo validado de un dron.

## Supuestos
Todo es ficticio y debe presentarse como simulación. Cuatro años es un horizonte docente que comprime el ciclo completo, no una vida comercial demostrada. Ventas significa drones entregados, no paquetes repartidos. Finanzas sin impuestos, deuda, capital de trabajo o valor residual. Consulte METODOLOGIA.md y la pestaña Diseño y clase antes de interpretar los indicadores.

Las respuestas se mantienen en la sesión; descargue el CSV para guardarlas. No hay persistencia multiusuario. La matriz permite editar pesos y puntajes; su resultado no se enlaza automáticamente con costos ni garantiza factibilidad. Es tarea del estudiante justificar las modificaciones económicas del concepto.

API de interfaz consultada: https://docs.streamlit.io/develop/api-reference
