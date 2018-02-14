<?php
// para comprimir texto si las lineas superan 70
$body = wordwrap($body,70);

// envio de email
$status = mail("sergioloscast@gmail.com","¡Alerta de Empleo! - $head",$body);
echo $status;
if ( $status != "FALSE" ){
	echo "[INFO] - Oferta: $head - Ha sido notificado por email";
}else{
	echo "no se ha podido mandar el email de $head";
}
?> 
