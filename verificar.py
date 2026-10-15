import numpy as np
from modelo import encuesta,calcular,DEFAULT
b=encuesta();t,k=calcular(b,DEFAULT)
assert len(t)==48
assert (t.Ventas<=t['Capacidad efectiva']).all()
assert (t.Pedidos.cumsum()>=t.Ventas.cumsum()).all()
assert (t.loc[t.Mes<DEFAULT['lanzamiento'],'Ventas']==0).all()
assert np.all(t.Pedidos.cumsum()==t.Ventas.cumsum()+t.Cancelaciones.cumsum()+t['Cartera vencida']+t['Pedidos en plazo'])
assert np.isclose(t['Flujo neto'].sum(),t.EBITDA.sum()-DEFAULT['inversion'])
assert np.isclose(k['van'],-DEFAULT['inversion']+sum(t.EBITDA/(1+DEFAULT['descuento'])**(t.Mes/12)))
assert t.Demanda.sum()>t.Pedidos.sum()>=t.Ventas.sum()
for caso in [dict(capacidad=0),dict(conversion=0),dict(cuota=0),dict(rezago=0),dict(cancelacion=.5),dict(lanzamiento=12,madurez=28,saturacion=38,declive=47)]:
 p={**DEFAULT,**caso};z,_=calcular(b,p)
 assert np.all(z.Pedidos.cumsum()==z.Ventas.cumsum()+z.Cancelaciones.cumsum()+z['Cartera vencida']+z['Pedidos en plazo'])
 if caso.get('capacidad')==0 or caso.get('conversion')==0 or caso.get('cuota')==0: assert z.Ventas.sum()==0
p={**DEFAULT,'precio':8000};z,_=calcular(b,p)
assert np.array_equal(t.Demanda,z.Demanda)
assert z.Pedidos.sum()<=t.Pedidos.sum()
print('CORRECTO: embudo comercial, balance de cartera, escenarios extremos, capacidad, caja y VAN.')
print(t.groupby('Año')[['Demanda','Pedidos','Ventas']].sum().to_string())
print('VAN:',round(k['van']))
