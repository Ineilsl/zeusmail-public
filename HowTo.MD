# Bienvenido al How To de ZeusMail [<img src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png">](http://creativecommons.org/licenses/by-nc-nd/4.0/)

Esta obra está bajo una licencia de Creative Commons, Reconocimiento-NoComercial-SinObraDerivada 4.0 Internacional

Antes que nada, te recomiendo pasarte por el README.TXT y continuar con este MarkDown.

# 1. Componentes de ZeusMail

ZeusMail tiene los siguientes ficheros:

 1. HowTo.MD
 2. README.TXT
 3. Scripts/
	 1. zeus.sh
	 3. zeusmail.cfg
 4. DATA /
	 1. Database/
        1.Url.db
        2.#hash#.db
	 2. Tools/
		1. email.php
	3. Sintaxis/
        1.tecnoempleo.php

## Descripcion de los ficheros

- El HowTo.MD Expone toda la información necesaria para instalar usar ZeusMail.
- README.TXT Muestra toda la informacion de ZeusMail como la version, tipo de licencia y creador.
- La carpeta Scripts contiene los Scripts que se ejecutan a nivel de shell y pueden realizarse a traves de un cron. 
- zeus.sh Es el script principal de esta version de prueba de ZeusMail. Lo he realizado asi para mezclar y mostrar que podemos mezclar Shell y PHP en la ejecucion de código. Este script es recomendable leerlo y ponerlo en un cron ya que si queremos que la deteccion de ofertas sea instantanea y automatica debemos hacer que se ejecute solo.
- zeusmail.cfg Este fichero contiene 1 variable, le dice a zeusmail si es la primera vez que lo ejecutamos.
- DATA es la carpeta que contiene los ficheros que descarga Download.sh y los ficheros que procesan estos últimos y ademas nos lo notifican.
- Database es una carpeta donde zeusmail almacena los ficheros de datos.
- Url.db Es un fichero en el que almacenamos las url de las webs que queremos procesar, de las que queremos obtener las ofertas de empleo. 1 url por línea.
- #hash#.db #hash# me refiero a la url que hemos puesto en url.db (la que procesamos) y este fichero contendrá el link hasheado de la primera oferta de empleo que encontrara zeusmail para poder usarlo en el fichero de sintaxis y saber si ya se ha procesado o no (si procesa notifica nuevas ofertas, sino sabra que esta actualizado y ya notifico las ofertas antiguas).
- Tools contiene las herramientas utilizadas por ZeusMail. (En esta version solo esta disponible la notificacion de una oferta de empleo por email.).
- Email.php Es un script en php que tiene declarado el email al que se va a enviar un email de notificacion cuando se encuentre una oferta de trabajo.
- Sintaxis esta carpeta que esta dentro de data, contiene los ficheros que interpretarán los datos que hemos descargado de las url almacenadas en url.db.
- tecnoempleo.php es el fichero que contiene la programacion para poder interpretar los datos descargados de la url de tecnoempleo almacenada en url.db.

## Ubicacion e instalacion de ZeusMail

Todas las variables de localizacion pueden cambiarse por lo que ZeusMail es muy versatil a la hora de implantarlo, aquí voy a mostrar una ubicacion estandar (Yo que uso FreeBSD lo voy a hacer de esta forma. Se puede implantar en cualquier sistema puesto que las rutas son las mismas si quereis.):
1º La carpeta Zeusmail la ponemos en /Scripts (Con permiso para Root, porque en el cron lo vamos a ejecutar asi ya que estamos en un entorno DEMO y nos da igual los riesgos de seguridad ¡¡¡¡DEMO!!!!).
2º Tendremos la ruta de carpetas así:
/
/scripts
/scripts/zeusmail
/scripts/zeusmail/scripts
/scripts/zeusmail/data
/scripts/zeusmail/datadatabase
/scripts/zeusmail/datatools
/scripts/zeusmail/datasintaxis
3º Si no tenemos instalado y configurado sendmail o PHP no se enviarán los emails ni se ejecutará ZeusMail.
4º Si tenemos esto configurado e instalado, ¡ya tenemos todo listo para la ejecución!.
5º RECOMIENDO AGREGAR zeus.sh AL CRON PARA QUE SALTEN LAS ALERTAS LO MAS RAPIDO POSIBLE.

## Ejecucion de ZeusMail:

Para ejecutar Zeusmail simplemente ejecuta en Cshell el fichero zeus.sh; csh zeus.sh || ./zeus.sh (si estamos en su directorio).

## Diagramas de ejecucion.

Este seria un diagrama de ejecucion de ZeusMail para enviar un email al descubrir una oferta de empleo.

```mermaid
sequenceDiagram
Cron ->> zeus.sh: Ejecuta
zeus.sh ->> zeusmail.cfg: Combrueba si es la primera instalacion 
zeus.sh ->> url.db: Busca en
url.db ->> zeus.sh: devuelve la url a descargar
zeus.sh ->> www.url.com.XML: Descarga la informacion
Note right of url.db: El XML contiene una URL que hashearemos para saber si hay nuevas ofertas
tecnoempleo.php ->> www.url.com.XML: Toma la informacion de
tecnoempleo.php ->> #hash#.db: Comprueba el ultimo hash analizado
tecnoempleo.php ->> email.php: Si el hash es diferente ejecuta / Sino, notifica "ACTUALIZADO" y se para zeus.
email.php ->> usuario_final: Envia un email al usuario si != || ~=
```
Sergio Neils Losa 				2018(c)
