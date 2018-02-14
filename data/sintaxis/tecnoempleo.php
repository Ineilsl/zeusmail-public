<?php
	function analisisxml($urlhashed) {
		$i=0;
		$f=0;
		$first="TRUE";
		$database="/scripts/zeusmail/data/database";
		if(!$xml = simplexml_load_file("/tmp/www.tecnoempleo.com.xml")){
			echo "No se ha encontrado el fichero";
		} else {
			$titulo_xml = $xml->channel->title;
			$descripcion_xml = $xml->channel->description;
			$fecha_xml = $xml->channel->pubDate;
			$link_xml = $xml->channel->link;
			foreach($xml->children() as $channel) {
				foreach($channel as $item) {
					$title = $item->title;
					$old_description = strip_tags("$item->description");
					$description = str_replace("&nbsp;", '', $old_description);
					$link_ofer = $item->link;
					$pubDate = $item->pubDate;
					if ( $first != "TRUE" ) { // Controlará la primera noticia valida TRUE la primera, luego ira a false asi que procesara la informacion para enviarla por email
						if ( $title != "" && $description != "" && $link_ofer != "" && $pubDate != "" ){ // tiene que contener estas variables ya analizadas para poder enviar el email
							$body = $description . "\n" . $link_ofer;
                            				$head = $title;
                            				include('/scripts/zeusmail/data/tools/email.php');
                            				$f++;
						} else {
							// echo "Noticia no valida\n";
							$f++;
							$i++;
						}
					} else { // si es la primera noticia entra aqui
						if ( $title != "" && $description != "" && $link_ofer != "" && $pubDate != "" ){ // tiene que contener estas variables sino...
								if (file_exists("$database/$urlhashed.db")) { // comprobamos que exista el hash de la url que contiene el hash de la primera noticia
									$file = fopen("$database/$urlhashed.db", "r") or exit("Error abriendo fichero! esta corrupto o no se encuentra.\n");
										$hashfichero = fgets($file);
									fclose($file);
									if ( $hashfichero == md5($link_ofer) ){ // una vez sepa que existe el fichero hay que comprobar el hash de dentro con el hash de la noticia
										echo "Feed Actualizado!\n";
                                                                                break 2;
									} else {
										$fichero= fopen("$database/$urlhashed.db", "w"); // creamos el dichero hash
										fputs($fichero, md5($link_ofer)); // Grabamos el hash de la primera noticia
										fclose($fichero); // cerramos el archivo
										$body = $description . "\n" . $link_ofer; // enviamos el email
										$head = $title;
										include('/scripts/zeusmail/data/tools/email.php');
										$f++;
										$first="FALSE";
									}
								} else {
									$fichero= fopen("$database/$urlhashed.db", "w");
									fwrite($fichero, md5($link_ofer));
									fclose($fichero);
									$body = $description . "\n" . $link_ofer;
									$head = $title;
									include('/scripts/zeusmail/data/tools/email.php');
									$f++;
									$first="FALSE";
								}
							$e = "FALSE";
							$f++;
						} else { # si es la primera noticia y no tiene los datos correctos
							// echo "Noticia no valida\n";
							$f++;
							$i++;
						}
				  	}
				}
			}
			if ( $i > 0){
				echo "No se han podido procesar: " . $i . " consultas\n";
			}
			if ( $f > 0){
				echo "Se han procesado: " . $f . "consultas\n";
			}
		}
	}
	$urlhashed = $argv[1];
	analisisxml($urlhashed);
?>
