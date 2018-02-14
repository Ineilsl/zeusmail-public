#!/bin/csh

# INFO
######

# ============================================================================
# |                               ZEUS.SH                                    |
# ============================================================================
# | Este Script es público, esta bajo una licencia CC. esto es lo que puedes |
# | hacer: Copiarlo y Distribuirlo. En ningun caso permito la compra venta o |
# | edicion de este codigo. La distribucion de este, implica la citación del |
# | autor. En el caso de que no se cite al autor se dara como incumplida la  |
# | la licencia de software, al igual que la venta o modificacion del mismo. |
# |                                                 Youtube: @NeilsADM       |
# ============================================================================

# PATH
######
set PATH = "/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin:/root/bin"

# VERSION
#########
set ver = "0.2"

# AUTOR
#######
set autor = "INeilsl"

# VARIABLES GLOBALES
####################
set data = "/scripts/zeusmail/data" # path de tu directorio donde colocamos el analisis de php
set log = "/var/log" # ruta del log
set scripts = "/scripts/zeusmail/scripts" # path de este script
set date = `date +"%Y%m%d;%H%M%S"`
set i = 1 # numero de linea
set b = 1 # numero lineas a coger
set ok = 0
set ko = 0

# SCRIPT START
###############

if ("$1" != "-v") then

	# COMPROBACION DE PRIMERA INSTALACION
	####################################

	if ( -f "$scripts/zeusmail.cfg" ) then
		set firstinstall = `cat $scripts/zeusmail.cfg | grep -o "firstinstall=FALSE"`
	else
		set firstinstall = "firstinstall=TRUE"
	endif

	if ( "$firstinstall" == 'firstinstall=FALSE' ) then
		set date = `date +"%Y%m%d;%H%M%S"`
		echo "$date - [WELLCOME\!] Soy zeusmail bienvenido de nuevo, estamos alimentando al hamster" | tee -a $log/zeusmail.log
		set date = `date +"%Y%m%d;%H%M%S"`
		echo "$date -  [INFO] Zeus ha empezado a correr en la rueda\!\!\!" | tee -a $log/zeusmail.log
		set lines = `wc -l "$data/database/url.db" | cut -d "/" -f "1"`
		set date = `date +"%Y%m%d;%H%M%S"`
		echo "$date - $lines webs detectadas\!" | tee -a $log/zeusmail.log

		# ANALISIS DE URL | EXTRACCION XML
		##################################

		while ( $i <= $lines )

			set line = `head -$i "$data/database/url.db" | tail -$b`

			# ASIGNANDO UN HASH A LA URL ( PREVIENE DUPLICACION DE DOMINIO EJ VARIOS FEEDS DE UNA MISMA WEB )
			#################################################################################################
			
			set urlhashed = `echo "$line" | md5` # hasheamos el url obtenido de la db
			if ( -f "/scripts/zeusmail/data/database/$urlhashed.db" ) then
				echo "se ha detectado url conocida" | tee -a $log/zeusmail.log
			else
				touch /scripts/zeusmail/data/database/$urlhashed.db
			endif
			
			
			# DESCARGA DEL XML Y PROCESAMIENTO DE ESTE CON EL ULTIMO HASH
			#############################################################

			set site = `echo "$line" | cut -d"/" -f"3"` # devuelve el nombre web
			set date = `date +"%Y%m%d;%H%M%S"`
			echo "$date - [INFO] Primera vuelta de Zeus: $site" | tee -a $log/zeusmail.log
			curl -s "$line" > "/tmp/$site.xml" # descarga del xml
			if ( "$status" == "0" ) then
				set analiz = `echo "$site" | cut -d"." -f "2"`
				set analizar = "$analiz.php"

				# CONTROL POST PARA SABER SI SE HA COMPROBADO O NO EL FEED Y CUANDO
				###################################################################
				# Pasar el hash y la url

				php -f "$data/sintaxis/$analizar" $urlhashed

				@ i = $i + 1
				@ ok = $ok + 1
			else
				set date = `date +"%Y%m%d;%H%M%S"`
				echo "$date - [ERROR] La descarga de: $site Ha fallado [COD:000]" | tee -a $log/zeusmail.log
				@ i = $i + 1
				@ ko = $ko + 1
			endif
			rm "/tmp/$site.xml"
		end
		set date = `date +"%Y%m%d;%H%M%S"`
		echo "$date - Hola de nuevo, script finalizado OK: $ok KO: $ko \n" | tee -a $log/zeusmail.log
		echo "$date - [BYE\!] El hamster se ha cansado de correr e ira a descansar, espero que nos llames de nuevo\!" | tee -a $log/zeusmail.log
	else
		# PRIMERA INSTSALACION
		######################

		echo "¡Hola! Soy ZeusMail, veo que es la primera vez que me ejecutas\n porfavor permiteme que en esta primera vez te aconseje;" | tee -a $log/zeusmail.log
		echo "Debes de añadir la ejecucion de este script en tu crontab para automatizarlo:\n Ejemplo:" | tee -a $log/zeusmail.log
		echo "#* * * * * root /bin/csh /scripts/zeus.sh > /dev/null" | tee -a $log/zeusmail.log
		echo "Esta pantalla no se volvera a mostrar, relanzando el script..." | tee -a $log/zeusmail.log
		echo "firstinstall=FALSE" > "$scripts/zeusmail.cfg"
		echo "Tiene 2 segundos para cancelar la ejecucion con Crl+C" | tee -a $log/zeusmail.log
		sleep 2
		csh $scripts/zeus.sh
	endif
	exit
else
	echo "* ZeusMail * [ PUBLIC - $ver ] - $autor" 
endif
exit
