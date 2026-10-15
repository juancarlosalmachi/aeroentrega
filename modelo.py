"""Simulación docente reproducible. No es una estimación validada de Ecuador."""
import numpy as np
import pandas as pd
SECTORES = ['Comercio electrónico', 'Farmacias', 'Alimentos', 'Logística', 'Agroindustria']

def encuesta(n=120, seed=42):
    r=np.random.default_rng(seed)
    sector=r.choice(SECTORES,n,p=[.28,.18,.22,.22,.10])
    size=r.choice([0,1,2],n,p=[.5,.35,.15])
    entregas=np.round(r.lognormal(3.2+size*.65,.45)).astype(int)
    distancia=np.clip(np.round(r.normal(7+size*3,3)),2,30).astype(int)
    carga=np.array([r.choice([1,2,3,5,8],p=[.05,.1,.2,.35,.3] if s=='Agroindustria' else [.2,.3,.3,.15,.05]) for s in sector])
    presupuesto=np.round(np.clip(r.normal(4800+size*1500,1200),2000,13000)/100)*100
    intención=np.array([r.choice(['Sí','Tal vez','No'],p=[.45,.4,.15] if d<=15 and c<=5 else [.2,.4,.4]) for d,c in zip(distancia,carga)])
    return pd.DataFrame(dict(empresa=[f'Empresa simulada {i+1:03}' for i in range(n)],sector=sector,entregas_dia=entregas,distancia_km=distancia,carga_kg=carga,autonomia_min=np.clip(np.ceil((distancia*2/40*60+10)/10)*10,20,120).astype(int),intencion=intención,unidades=np.clip(np.ceil(entregas/50),1,8).astype(int),presupuesto_usd=presupuesto.astype(int),prioridad=r.choice(['Autonomía','Seguridad','Precio','Carga útil','Mantenimiento'],n),barrera=r.choice(['Costo','Regulación','Seguridad','Infraestructura','Aceptación'],n)))

DEFAULT=dict(empresas=3500,conversion=.65,precio=6000,variable=3400,fijo=6500,inversion=160000,activo=100000,capacidad=14,inflacion=.04,precio_var=-.02,descuento=.12,lanzamiento=7,madurez=22,saturacion=32,declive=39,cola=.25,cuota=.4,notoriedad=.35,rezago=2,cancelacion=.08,rampa=8,rendimiento=.94,volatilidad=.12,seed=42)

def calcular(df,p):
    p={**DEFAULT,**p}
    meses=np.arange(1,49)
    peso=df.intencion.map({'Sí':p['conversion'],'Tal vez':p['conversion']*.3,'No':0}).fillna(0)
    # Mercado de referencia: la demanda sectorial no cambia al cambiar nuestro precio.
    elegible=(df.carga_kg<=5)&(df.distancia_km<=15)
    ref=(df.presupuesto_usd>=6000)&elegible
    potencial=p['empresas']*float((df.unidades*peso*ref).mean())
    curva=np.interp(meses,[1,p['lanzamiento'],p['madurez'],p['saturacion'],p['declive'],48],[0,.12,.92,1,.95,p['cola']])
    curva[meses<p['lanzamiento']]=0
    r=np.random.default_rng(p['seed'])
    estacion=1+.13*np.cos(2*np.pi*(meses-11)/12)
    ruido=r.lognormal(-p['volatilidad']**2/2,p['volatilidad'],48)
    bruto=curva*estacion*ruido
    acumulado=np.floor(np.cumsum(potencial*bruto/bruto.sum())+1e-9).astype(int)
    demanda=np.diff(np.r_[0,acumulado])
    edad=np.maximum(0,meses-p['lanzamiento'])
    conocimiento=p['notoriedad']+(1-p['notoriedad'])*(1-np.exp(-edad/10))
    cuota=p['cuota']*conocimiento
    cuota[meses>=p['declive']]*=np.linspace(1,.75,(meses>=p['declive']).sum())
    precio=p['precio']*(1+p['precio_var'])**((meses-1)//12)
    base=float((df.unidades*peso*ref).sum())
    aceptacion=np.array([min(1,float((df.unidades*peso*elegible*(df.presupuesto_usd>=v)).sum())/base) if base else 0 for v in precio])
    interesados=demanda*cuota*aceptacion
    pedidos=np.diff(np.r_[0,np.floor(np.cumsum(interesados)+1e-9)]).astype(int)
    disponibles=np.r_[np.zeros(p['rezago'],dtype=int),pedidos][:48]
    capacidad=np.floor(p['capacidad']*np.clip((edad+1)/p['rampa'],0,1)*p['rendimiento']).astype(int)
    capacidad[meses<p['lanzamiento']]=0
    ventas=[];cancelados=[];cartera=[];pendiente=0;residuo=0.
    for i in range(48):
        # Cancelan solo pedidos que ya vencieron y siguen pendientes, antes de nuevas llegadas.
        residuo+=pendiente*p['cancelacion']
        perdida=min(pendiente,int(residuo));residuo-=perdida
        pendiente-=perdida
        pendiente+=int(disponibles[i])
        v=min(pendiente,int(capacidad[i]));pendiente-=v
        ventas.append(v);cancelados.append(perdida);cartera.append(pendiente)
    ventas=np.array(ventas);cancelados=np.array(cancelados)
    pipeline=np.cumsum(pedidos)-np.cumsum(disponibles)
    costo=p['variable']*(1+p['inflacion'])**((meses-1)//12)
    fijo=p['fijo']*(1+p['inflacion'])**((meses-1)//12)
    ingresos=ventas*precio
    variable=ventas*costo
    ebitda=ingresos-variable-fijo
    depreciacion=np.where(meses>=p['lanzamiento'],p['activo']/48,0)
    utilidad=ebitda-depreciacion
    flujo=ebitda.copy();flujo[0]-=p['inversion']
    caja=np.cumsum(flujo)
    tasa=(1+p['descuento'])**(1/12)-1
    van=-p['inversion']+sum(ebitda/(1+tasa)**meses)
    rec=np.flatnonzero(caja>=0)
    etapa=np.select([meses<p['lanzamiento'],meses<p['madurez'],meses<p['saturacion'],meses<p['declive']],['Desarrollo','Introducción / crecimiento','Maduración','Saturación'],default='Declive')
    tabla=pd.DataFrame({'Mes':meses,'Año':(meses-1)//12+1,'Etapa':etapa,'Demanda':demanda,'Pedidos':pedidos,'Ventas':ventas,'Capacidad efectiva':capacidad,'Cancelaciones':cancelados,'Cartera vencida':cartera,'Pedidos en plazo':pipeline,'Cuota comercial':cuota,'Precio':precio,'Ingresos':ingresos,'Costo variable':variable,'Costo fijo':fijo,'EBITDA':ebitda,'Depreciación':depreciacion,'Utilidad operativa':utilidad,'Flujo neto':flujo,'Caja acumulada':caja})
    return tabla,dict(potencial=potencial,van=van,payback=int(rec[0]+1) if len(rec) else None,capital_requerido=max(0,-float(caja.min())),captacion=pedidos.sum()/max(1,demanda.sum()),pendientes=int(cartera[-1]+pipeline[-1]))
