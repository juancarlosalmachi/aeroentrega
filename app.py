from pathlib import Path
import json
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from modelo import encuesta, calcular, DEFAULT, SECTORES

st.set_page_config(page_title='AeroEntrega | Diseño de Máquinas',page_icon='🚁',layout='wide')
st.markdown("""<style>
.stApp{background:#F4F7FB;color:#162D46}
[data-testid="stSidebar"]{background:#EAF0F6;color:#162D46}
h1,h2,h3,h4,p,label{color:#162D46}
[data-testid="stMetric"]{background:#FFFFFF;padding:20px;border-radius:12px;border:1px solid #DFE7EF;box-shadow:0 3px 12px #15365308}
[data-testid="stMetricValue"]{color:#102C50;font-size:1.8rem}
[data-testid="stMetricLabel"]{color:#52677C}
.block-container{padding-top:2rem;max-width:1500px}
</style>""",unsafe_allow_html=True)
import plotly.io as pio
pio.templates.default='plotly_white'
PALETA=['#176B86','#16A085','#E6A23C','#6E63A8','#D45D5D']
def grafico(fig):
    fig.update_layout(template='plotly_white',paper_bgcolor='#FFFFFF',plot_bgcolor='#FFFFFF',font=dict(color='#162D46',family='Arial',size=13),title_font=dict(size=18,color='#102C50'),colorway=PALETA,legend=dict(title=None,font=dict(color='#162D46'),orientation='h',y=-.22),margin=dict(l=25,r=25,t=65,b=85),hoverlabel=dict(bgcolor='#FFFFFF',font_color='#162D46'))
    fig.update_xaxes(gridcolor='#E8EDF3',zerolinecolor='#CBD5E1',tickfont_color='#52677C',title_font_color='#52677C')
    fig.update_yaxes(gridcolor='#E8EDF3',zerolinecolor='#CBD5E1',tickfont_color='#52677C',title_font_color='#52677C')
    st.plotly_chart(fig,theme=None,width='stretch')
st.title('AeroEntrega | evaluación de negocio')
st.caption('DISEÑO DE MÁQUINAS · DECISIONES DE PRODUCTO · HORIZONTE DE 4 AÑOS · USD')
st.info('SIMULACIÓN DOCENTE · Empresas y cifras ficticias. Modelo de venta de drones; las hipótesis no constituyen una previsión validada del mercado.')
if 'base' not in st.session_state: st.session_state.base=encuesta()
p=DEFAULT.copy()
with st.sidebar:
    st.header('Simulador de negocio')
    escenario=st.selectbox('Escenario',['Base','Conservador','Optimista'])
    p['empresas']=st.number_input('Empresas en mercado objetivo',1,100000,3500)
    p['conversion']=st.slider('Conversión de intención a compra',0.,1.,.65,.05)
    p['precio']=st.number_input('Precio por dron (USD)',100,50000,6000,100)
    p['variable']=st.number_input('Costo variable por dron (USD)',0,50000,3400,100)
    p['fijo']=st.number_input('Costos fijos mensuales (USD)',0,100000,6500,500)
    p['inversion']=st.number_input('Inversión inicial total (USD)',0,5000000,160000,10000)
    p['activo']=st.number_input('Activos depreciables incluidos (USD)',0,p['inversion'],min(100000,p['inversion']),1000)
    p['capacidad']=st.number_input('Capacidad de fabricación (drones/mes)',0,1000,14)
    p['inflacion']=st.slider('Crecimiento anual de costos',0.,.3,.04,.01)
    p['precio_var']=st.slider('Variación anual del precio',-.3,.3,-.02,.01)
    p['descuento']=st.slider('Tasa de descuento anual',0.,.5,.12,.01)
    st.subheader('Ciclo de vida: meses')
    p['lanzamiento']=st.slider('Salida al mercado',2,12,7)
    p['madurez']=st.slider('Inicio de maduración',p['lanzamiento']+1,28,22)
    p['saturacion']=st.slider('Inicio de saturación',p['madurez']+1,38,32)
    p['declive']=st.slider('Inicio de declive',p['saturacion']+1,47,39)
    p['cola']=st.slider('Demanda relativa al final',0.,1.,.25,.05)
    st.subheader('Captación y operaciones')
    p['cuota']=st.slider('Cuota máxima frente a competidores',0.,1.,.4,.05)
    p['notoriedad']=st.slider('Notoriedad inicial de la marca',0.,1.,.35,.05)
    p['rezago']=st.slider('Plazo pedido → entrega (meses)',0,6,2)
    p['cancelacion']=st.slider('Cancelación mensual por retrasos',0.,.5,.08,.01)
    p['rampa']=st.slider('Meses para alcanzar capacidad',1,18,8)
    p['rendimiento']=st.slider('Rendimiento de fabricación',.5,1.,.94,.01)
    p['volatilidad']=st.slider('Variabilidad mensual del mercado',0.,.4,.12,.02)
    p['seed']=st.number_input('Semilla reproducible',0,100000,42)
    if escenario=='Conservador':
        p['conversion']*=.8; p['cuota']*=.75; p['variable']*=1.12
    if escenario=='Optimista':
        p['conversion']=min(1,p['conversion']*1.15);p['cuota']=min(1,p['cuota']*1.2);p['variable']*=.92
pmodelo=p.copy()
tabla,k=calcular(st.session_state.base,pmodelo)
st.subheader('Resumen ejecutivo · versión 2')
cols=st.columns(4)
for col,label,value in zip(cols,['Drones vendidos · 4 años','Ingresos · USD','VAN · USD','Recuperación simple'],[f'{tabla.Ventas.sum():,}',f'{tabla.Ingresos.sum():,.0f}',f'{k["van"]:,.0f}',f'Mes {k["payback"]}' if k['payback'] else 'No recupera en 48 meses']): col.metric(label,value)
res=st.columns(4)
res[0].metric('Inversión inicial',f'USD {p["inversion"]:,.0f}')
res[1].metric('Captación de pedidos / mercado',f'{k["captacion"]:.1%}')
res[2].metric('Déficit máximo de caja',f'USD {k["capital_requerido"]:,.0f}')
res[3].metric('Utilidad operativa · 4 años',f'USD {tabla["Utilidad operativa"].sum():,.0f}')
if k['van']>=0:
    st.success(f"El escenario genera valor según los supuestos: VAN USD {k['van']:,.0f}. La viabilidad técnica y comercial debe verificarse por separado.")
else:
    st.warning(f"El escenario no cubre la rentabilidad exigida: VAN USD {k['van']:,.0f}. Revise captación, margen y costos antes de comprometer inversión.")
st.caption(f"Pedidos pendientes al cierre: {k['pendientes']} · cancelados por demora: {tabla.Cancelaciones.sum()} · sin valor terminal ni ingreso por pedidos aún no entregados.")
left,right=st.columns([1.25,1])
with left:
    grafico(px.line(tabla,x='Mes',y=['Demanda','Pedidos','Ventas'],color_discrete_sequence=PALETA,title='Mercado → pedidos → entregas',labels={'value':'Drones / mes','variable':'Serie'}))
with right:
    caja=pd.concat([pd.DataFrame({'Mes':[0],'Caja acumulada':[-p['inversion']]}),tabla[['Mes','Caja acumulada']]])
    fig=px.area(caja,x='Mes',y='Caja acumulada',color_discrete_sequence=['#176B86'],title='Recuperación de la inversión',labels={'Caja acumulada':'USD'})
    fig.add_hline(y=0,line_color='#D45D5D',line_dash='dash');grafico(fig)
st.divider()
tabs=st.tabs(['1 · Encuesta','2 · Mercado','3 · Demanda y ciclo','4 · Costos y ganancias','5 · Sensibilidad','6 · Diseño y clase'])
with tabs[0]:
    st.subheader('Encuesta empresarial ficticia')
    st.write('Producto: compra de un dron de reparto, con capacitación inicial. Seleccione una empresa hipotética y complete el formulario; sus respuestas se incorporan al análisis.')
    with st.form('encuesta'):
        a,b=st.columns(2)
        sector=a.selectbox('1. Sector de la empresa',SECTORES)
        entregas=a.number_input('2. Entregas diarias',1,10000,50)
        distancia=a.number_input('3. Radio de servicio requerido (km)',1,500,10)
        carga=a.number_input('4. Carga útil requerida (kg)',.1,100.,3.)
        autonomia=a.number_input('5. Autonomía mínima (min)',1,300,30)
        intencion=b.selectbox('6. ¿Compraría drones de reparto?',['Sí','Tal vez','No'])
        unidades=b.number_input('7. Unidades que adquiriría en cuatro años',1,1000,2)
        presupuesto=b.number_input('8. Presupuesto máximo por dron (USD)',0,100000,6000)
        prioridad=b.selectbox('9. Principal criterio de compra',['Autonomía','Seguridad','Precio','Carga útil','Mantenimiento'])
        barrera=b.selectbox('10. Principal barrera',['Costo','Regulación','Seguridad','Infraestructura','Aceptación'])
        if st.form_submit_button('Añadir respuesta ficticia'):
            fila=dict(empresa=f'Respuesta de clase {len(st.session_state.base)+1}',sector=sector,entregas_dia=entregas,distancia_km=distancia,carga_kg=carga,autonomia_min=autonomia,intencion=intencion,unidades=unidades,presupuesto_usd=presupuesto,prioridad=prioridad,barrera=barrera)
            st.session_state.base=pd.concat([st.session_state.base,pd.DataFrame([fila])],ignore_index=True)
            st.rerun()
    st.info('Respuestas de clase conservadas solo durante esta sesión. Descargue el CSV para guardarlas.')
    if st.button('Restablecer las 120 empresas simuladas'): st.session_state.base=encuesta(); st.rerun()
    st.dataframe(st.session_state.base,hide_index=True)
    st.download_button('Descargar encuesta CSV',st.session_state.base.to_csv(index=False).encode('utf-8-sig'),'encuesta_ficticia.csv','text/csv')
with tabs[1]:
    df=st.session_state.base
    a,b=st.columns(2)
    with a: grafico(px.histogram(df,x='sector',color='intencion',barmode='group',title='Intención por sector',color_discrete_sequence=PALETA))
    with b: grafico(px.histogram(df,x='presupuesto_usd',title='Presupuesto máximo por dron',color_discrete_sequence=PALETA))
    st.dataframe(df.groupby('sector').agg(empresas=('empresa','count'),entregas_dia=('entregas_dia','mean'),carga_kg=('carga_kg','median'),autonomia_min=('autonomia_min','median'),presupuesto=('presupuesto_usd','median')))
    st.write(f'Mercado potencial a 4 años: {k["potencial"]:,.1f} drones de todos los fabricantes, al precio sectorial de referencia USD 6.000. Extrapolación docente de una muestra sintética.')
with tabs[2]:
    grafico(px.line(tabla,x='Mes',y=['Demanda','Pedidos','Ventas','Capacidad efectiva'],color_discrete_sequence=PALETA,title='Demanda sectorial, pedidos propios y entregas'))
    st.dataframe(tabla.groupby(['Año','Etapa'],sort=False)[['Demanda','Pedidos','Ventas','Cancelaciones']].sum().reset_index(),hide_index=True)
    anual=tabla.groupby('Año')[['Demanda','Pedidos','Ventas','Cancelaciones','Ingresos','Costo variable','Costo fijo','EBITDA','Utilidad operativa','Flujo neto']].sum()
    st.subheader('Proyección a cuatro años'); st.dataframe(anual.style.format('{:,.0f}'))
    st.download_button('Descargar tabla anual',anual.to_csv().encode('utf-8-sig'),'proyeccion_cuatro_anos.csv','text/csv')
    ciclo=px.line(tabla,x='Mes',y='Demanda',title='Ciclo de vida del producto · demanda sectorial',color_discrete_sequence=['#176B86'])
    limites=[1,p['lanzamiento'],p['madurez'],p['saturacion'],p['declive'],49]
    for i,nombre in enumerate(['Desarrollo','Crecimiento','Maduración','Saturación','Declive']):
        ciclo.add_vrect(x0=limites[i],x1=limites[i+1],fillcolor=PALETA[i],opacity=.09,line_width=0,annotation_text=nombre,annotation_position='top left',annotation_font_color='#162D46')
    grafico(ciclo)
    grafico(px.line(tabla,x='Mes',y=['Pedidos','Ventas','Cartera vencida','Pedidos en plazo'],title='Operación comercial y cartera',color_discrete_sequence=PALETA))
    st.caption('Demanda: compras del mercado objetivo para todos los fabricantes. Pedidos: fracción captada por nuestra empresa. Ventas: drones entregados tras el plazo comercial, sujetos a capacidad y rampa. La cartera puede permitir ventas superiores a los pedidos de un mes; la competencia no es demanda insatisfecha.')
with tabs[3]:
    grafico(px.line(tabla,x='Mes',y=['Ingresos','Costo variable','Costo fijo','Utilidad operativa'],title='Resultados mensuales · USD'))
    caja=pd.concat([pd.DataFrame({'Mes':[0],'Caja acumulada':[-p['inversion']]}),tabla[['Mes','Caja acumulada']]])
    grafico(px.line(caja,x='Mes',y='Caja acumulada',title='Caja acumulada, incluida inversión inicial'))
    margen=p['precio']-p['variable']
    st.write(f'Margen unitario inicial: USD {margen:,.0f}.')
    st.write(f'Punto de equilibrio operativo inicial: {int(np.ceil(p["fijo"]/margen))} drones/mes.' if margen>0 else 'Sin punto de equilibrio: margen unitario no positivo.')
    grafico(px.bar(tabla.groupby('Año')[['Ingresos','EBITDA','Utilidad operativa']].sum().reset_index(),x='Año',y=['Ingresos','EBITDA','Utilidad operativa'],barmode='group',color_discrete_sequence=PALETA,title='Resultados de los cuatro años'))
    if margen>0 and np.ceil(p['fijo']/margen)>np.floor(p['capacidad']*p['rendimiento']):
        st.warning('La capacidad efectiva máxima no alcanza el equilibrio operativo inicial, incluso si hubiera suficientes pedidos.')
    st.metric('Utilidad operativa total (sin impuestos)',f'USD {tabla["Utilidad operativa"].sum():,.0f}')
    st.dataframe(tabla,hide_index=True)
    st.download_button('Descargar resultados mensuales',tabla.to_csv(index=False).encode('utf-8-sig'),'resultados_48_meses.csv','text/csv')
    st.download_button('Descargar supuestos',json.dumps(p,indent=2,ensure_ascii=False),'supuestos.json','application/json')
with tabs[4]:
    filas=[]
    for precio_factor in [.8,.9,1.,1.1,1.2]:
        for conversion_factor in [.6,.8,1.,1.2,1.4]:
            q=pmodelo.copy();q['precio']*=precio_factor;q['conversion']=min(1,q['conversion']*conversion_factor)
            _,r=calcular(st.session_state.base,q)
            filas.append({'Precio relativo':precio_factor,'Conversión relativa':conversion_factor,'VAN':r['van']})
    sens=pd.DataFrame(filas)
    grafico(px.density_heatmap(sens,x='Precio relativo',y='Conversión relativa',z='VAN',histfunc='avg',text_auto='.0f',color_continuous_scale=['#F5C9C9','#F7F7F2','#B9E0D5'],title='VAN ante precio y conversión').update_traces(textfont=dict(color='#102C50'))) 
    st.caption('La disposición de pago se vuelve a filtrar en cada precio; subir precio puede reducir compradores. Escenarios deterministas, sin probabilidades ni intervalos de confianza.')
    st.dataframe(sens,hide_index=True)
    st.subheader('Variabilidad de las entregas')
    st.caption('100 trayectorias con semillas diferentes y los mismos supuestos. Banda P10–P90 condicional; no es una validación ni un intervalo de confianza del mercado.')
    if st.button('Simular 100 trayectorias'):
        import plotly.graph_objects as go
        sims=[]
        for seed in range(100):
            q=pmodelo.copy();q['seed']=seed;sims.append(calcular(st.session_state.base,q)[0].Ventas.to_numpy())
        sims=np.array(sims);lo,med,hi=np.percentile(sims,[10,50,90],axis=0)
        fig=go.Figure()
        fig.add_scatter(x=tabla.Mes,y=hi,line=dict(width=0),name='P90')
        fig.add_scatter(x=tabla.Mes,y=lo,line=dict(width=0),fill='tonexty',fillcolor='rgba(23,107,134,.18)',name='P10–P90')
        fig.add_scatter(x=tabla.Mes,y=med,line=dict(color='#176B86',width=3),name='Mediana')
        fig.update_layout(title='Entregas mensuales · variabilidad simulada',yaxis_title='Drones / mes',xaxis_title='Mes');grafico(fig)
with tabs[5]:
    st.subheader('Del requerimiento al concepto mecánico')
    requisitos=pd.DataFrame([
        ['Carga útil','Percentil 75 de encuesta',f'{df.carga_kg.quantile(.75):.1f} kg','Estructura, tren de aterrizaje, mecanismo de sujeción'],
        ['Radio de servicio','Percentil 75',f'{df.distancia_km.quantile(.75):.1f} km','Energía de ida, retorno y reserva'],
        ['Autonomía','Percentil 75',f'{df.autonomia_min.quantile(.75):.1f} min','Batería, motores y masa total'],
        ['Seguridad','Necesidad del sistema','Validar','Retención de carga, redundancia y aterrizaje'],
        ['Fabricación','Capacidad del escenario',f'{p["capacidad"]} unidades/mes','Proceso, tolerancias, ensamble y mantenimiento']
    ],columns=['Requisito','Criterio docente','Objetivo preliminar','Decisión de diseño'])
    st.dataframe(requisitos,hide_index=True)
    st.subheader('Arquitectura funcional y alternativas')
    st.dataframe(pd.DataFrame([
        ['Transportar la carga','Multirrotor','Ala fija','VTOL híbrido'],
        ['Almacenar energía','Batería intercambiable','Batería fija','Sistema híbrido'],
        ['Sujetar / entregar paquete','Caja enclavada','Pinza accionada','Cabrestante'],
        ['Apoyar / absorber impacto','Patines','Patas articuladas','Tren con amortiguación'],
        ['Facilitar mantenimiento','Brazos modulares','Estructura monobloque','Módulos reemplazables']
    ],columns=['Función','Alternativa A','Alternativa B','Alternativa C']),hide_index=True)
    st.subheader('Selección del concepto · matriz ponderada')
    st.caption('Edite pesos y puntajes de 1 a 5; 5 significa mejor cumplimiento. Valores iniciales didácticos. Un requisito excluyente debe comprobarse antes de puntuar.')
    matriz=pd.DataFrame({'Criterio':['Entrega puntual / aterrizaje vertical','Autonomía','Carga útil','Facilidad de fabricación','Facilidad de mantenimiento','Costo total'], 'Peso':[25,20,15,15,10,15], 'Multirrotor':[5,2,3,5,4,4], 'Ala fija':[1,5,3,3,3,4], 'VTOL híbrido':[5,4,4,2,2,2]})
    edit=st.data_editor(matriz,hide_index=True,disabled=['Criterio'],column_config={'Peso':st.column_config.NumberColumn(min_value=0,max_value=100),**{c:st.column_config.NumberColumn(min_value=1,max_value=5) for c in ['Multirrotor','Ala fija','VTOL híbrido']}},key='matriz')
    if edit['Peso'].sum()>0 and not edit.isna().any().any():
        ranking=pd.DataFrame({'Concepto':['Multirrotor','Ala fija','VTOL híbrido'],'Puntaje':[float((edit[c]*edit['Peso']).sum()/edit['Peso'].sum()) for c in ['Multirrotor','Ala fija','VTOL híbrido']]}).sort_values('Puntaje',ascending=False)
        grafico(px.bar(ranking,x='Concepto',y='Puntaje',range_y=[0,5],color_discrete_sequence=['#176B86'],title='Comparación de conceptos · escala 1–5'))
        st.write(f"Concepto mejor puntuado bajo estos juicios: **{ranking.iloc[0]['Concepto']}**. Revisar factibilidad y sensibilidad antes de elegir.")
    else: st.warning('Complete los valores y asigne al menos un peso positivo.')
    st.subheader('Plan de verificación del diseño')
    st.dataframe(pd.DataFrame([
        ['Carga útil','Masa total, resistencia y fijación','Ensayo estático y retención del paquete'],
        ['Alcance / autonomía','Misión de ida y retorno, reserva y viento','Balance de energía y ensayo controlado'],
        ['Fabricación','Proceso, tolerancias, ensamble y calidad','Prototipo de montaje y tiempos de ciclo'],
        ['Seguridad','Modos de fallo y consecuencias','Análisis de riesgos y pruebas de fallos'],
        ['Costo objetivo','Lista de materiales + mano de obra + rechazo','Cotizaciones y costeo por proceso']
    ],columns=['Requisito','Trabajo de ingeniería','Evidencia requerida']),hide_index=True)
    st.markdown("""**Taller de 100 minutos**
1. **15 min · Necesidad:** defina usuario, misión, problema y límites del sistema. Separe necesidades de soluciones.
2. **20 min · Especificación:** seleccione un segmento y convierta tres necesidades en requisitos medibles con criterios de aceptación. No combine máximos de toda la muestra sin justificar.
3. **20 min · Conceptos:** combine alternativas, dibuje tres propuestas y puntúe la matriz. Cambie un peso y explique la estabilidad de la elección.
4. **20 min · Viabilidad:** proponga presupuestos de masa y energía, proceso de fabricación y costo unitario. Compare con el margen y la capacidad del dashboard.
5. **15 min · Ciclo de vida:** interprete los cuatro años; explique captación, retrasos, pérdidas, inversión y cuándo rediseñar.
6. **10 min · Defensa:** entregue una lámina de concepto, tabla de requisitos, matriz justificada y resumen económico con dos escenarios.

**Evaluación:** definición y requisitos 25%; diversidad y selección de conceptos 25%; verificación técnica 25%; coherencia económica y argumentación 25%.""")
    with st.expander('Fórmulas, interpretación y límites',expanded=True):
        st.markdown(Path(__file__).with_name('METODOLOGIA.md').read_text(encoding='utf-8'))
