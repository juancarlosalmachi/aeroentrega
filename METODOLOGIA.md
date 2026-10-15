### 1. Caso y alcance
Se diseña un dron de reparto para venderlo a empresas. No se modela un servicio de entrega por paquete. Las empresas, respuestas, parámetros y resultados son ficticios; no son una encuesta de Ecuador. Correlaciones introducidas: empresas con más entregas piden más unidades; recorridos mayores requieren más autonomía; carga y distancia elevadas reducen intención. Los parámetros se eligen para enseñar decisiones, no para representar tasas observadas.

### 2. Mercado y embudo comercial
- Mercado objetivo: número de empresas editable; sin fuente empírica.
- Segmento atendible preliminar: carga ≤ 5 kg y radio ≤ 15 km. Son límites de la especificación conceptual, no prestaciones demostradas.
- Peso de intención: Sí = conversión; Tal vez = 0,30 × conversión; No = 0.
- Potencial del horizonte = empresas × promedio(unidades × peso × segmento × presupuesto ≥ USD 6.000).
- USD 6.000 es un precio de referencia sectorial fijo. Nuestro precio no cambia la curva del sector.
- El potencial se distribuye en 48 meses con una curva de ciclo de vida, estacionalidad de amplitud 13% y perturbaciones lognormales reproducibles. La distribución se normaliza: variabilidad y etapas cambian el momento, no el potencial total.
- Cuota propia = cuota máxima × notoriedad. La notoriedad parte del valor elegido y se aproxima exponencialmente a 100% con constante de diez meses; la cuota cae hasta 75% de su nivel durante el declive. Son supuestos docentes.
- La aceptación de nuestro precio es la razón entre unidades ponderadas asequibles a ese precio y las asequibles a USD 6.000, limitada a 1. Bajar el precio aumenta captación dentro del mercado de referencia; no amplía el universo sectorial.
- Pedidos = demanda del sector × cuota propia × aceptación del precio, redondeados por diferencias acumuladas.

### 3. Pedidos y entregas
Los pedidos se vuelven entregables después del plazo elegido. La capacidad efectiva crece con la rampa de fabricación y se multiplica por rendimiento. Cada mes se cancelan al porcentaje elegido pedidos vencidos anteriores; se acumulan fracciones hasta completar unidades enteras. Luego llegan pedidos cuyo plazo se cumple y se entregan hasta el límite de capacidad. El resto permanece en cartera vencida.

Identidad acumulada verificable: pedidos = entregas + cancelaciones + cartera vencida + pedidos aún en plazo. La demanda que se lleva otro fabricante no es cartera nuestra. Las entregas pueden superar los pedidos de un mes al atender cartera antigua. No se fuerza una brecha artificial entre pedidos y entregas: con plazo cero, capacidad suficiente y sin retrasos pueden coincidir legítimamente.

### 4. Ciclo de vida
Desarrollo hasta lanzamiento; introducción y crecimiento hasta madurez; maduración hasta saturación; saturación hasta declive; después disminución. La demanda normalizada pasa por niveles 0,12 al lanzamiento, 0,92 en madurez, 1 en saturación y 0,95 al inicio del declive. Cuatro años es una compresión docente; la encuesta no permite estimar estas fechas. La inversión es un desembolso en t=0, no una fase de ventas.

### 5. Finanzas
Ingresos = entregas × precio. Costo variable = entregas × costo unitario. Se supone fabricación contra pedido con gasto y cobro al entregar; no hay inventario ni cuentas por cobrar. EBITDA = ingresos − costos variables − costos fijos. Los costos fijos continúan durante desarrollo. Depreciación = activos / 48 mensuales desde lanzamiento: vida depreciable de 48 meses a partir de puesta en uso; parte queda fuera del horizonte.

Utilidad operativa = EBITDA − depreciación; no equivale a utilidad neta. La inversión total incluye activos y preparación del proyecto. No se suman activos otra vez. El VAN considera inversión completa en t=0 y EBITDA como aproximación del flujo operativo al cierre de cada mes. Tasa mensual = (1 + tasa anual)^(1/12) − 1. Recuperación simple = primer mes de caja acumulada ≥ 0; no garantiza que la caja no vuelva a caer.

La tabla mensual incluye inversión en la fila del mes 1 para agregarla; la gráfica muestra el desembolso en mes 0. Fondos requeridos = máximo déficit de caja acumulada incluyendo inversión inicial. No incluye reserva adicional.

Sin impuestos, deuda, capital de trabajo, valor terminal, valor residual, reinversión ni ingresos recurrentes por mantenimiento. No hay certificación o permiso presupuestados explícitamente fuera del costo fijo/preparación. No es un plan financiero de inversión real.

### 6. Sensibilidad y decisiones
La tabla precio–conversión mantiene la semilla común para comparar supuestos, no es una probabilidad de éxito. La envolvente de 100 simulaciones muestra percentiles condicionales a variabilidad mensual, sin incertidumbre sobre tamaño del mercado o costos: no es un intervalo de confianza del mercado real.

Los puntajes de la matriz de conceptos son juicios docentes, no prestaciones medidas. Las prioridades de la encuesta sirven de referencia; los estudiantes deben justificar pesos, verificar requisitos excluyentes, presupuestos de masa/energía, cargas y riesgos antes de seleccionar una solución.
