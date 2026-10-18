MEDICION DE FOTOGRAMAS POR SEGUNDO
Medida de exito 5 - actividades AO.5 y QV.3
18 de octubre de 2026

ARCHIVO   fps_20261018_060703.json
EQUIPO    Meta Quest 3S, aplicacion autonoma
ESCENA    Cap04_Pad con el entorno de claro low-poly
DURACION  12949 fotogramas, unos 3 minutos de juego real

RESULTADO

  fps medio          71.9
  mediana            13.9 ms
  p95                13.9 ms
  p99                13.9 ms
  peor fotograma    194.4 ms
  en vsync          12946   (100.0 %)
  perdieron uno         2
  tirones               1
  vsync perdidos     0.02 %

  El criterio era menos del 5 %. Se cumple con 216 veces de margen.

COMO SE CUENTA UNA CAIDA, Y POR QUE IMPORTA

Una caida es haber PERDIDO UN VSYNC: el fotograma tardo mas de 1.5 intervalos y el visor
tuvo que repetir imagen. Eso es lo que se siente.

El primer criterio contaba todo lo que pasara de 1000/72 = 13.889 ms, y como el visor
entrega exactamente a ese intervalo, el redondeo de coma flotante mandaba la mitad de los
fotogramas a cada lado. Reporto un 60.6 % de caidas sobre una corrida que iba clavada a
72 fps. El defecto era del criterio, no del render.

La aritmetica de aquella corrida lo cierra: 213 ms de exceso total en 11007 fotogramas, y
194 de ellos eran un solo tropiezo. El resto repartia 0.0017 ms cada uno.

POR QUE SE REGISTRA EL TIEMPO DE CADA FOTOGRAMA Y NO UN PROMEDIO

Un promedio de 72 fps esconde las caidas, y en realidad virtual lo que arruina la
experiencia son justo las caidas: treinta fotogramas malos entre mil buenos se notan, y el
promedio no los ve. El volcado lleva ademas un histograma en multiplos de vsync, porque un
informe que solo lleva percentiles no se puede reanalizar -y reanalizar fue exactamente lo
que hizo falta para desmontar el falso 60 %-.

EL PRIMER SEGUNDO SE DESCARTA

La carga de escena produce fotogramas largos que no representan el funcionamiento normal.
El peor fotograma de 194.4 ms que si aparece es un tropiezo posterior, uno solo en tres
minutos.
