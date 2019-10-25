package start;

import java.io.File;
import java.io.IOException;
import java.util.Properties;

public class Start {

	public static void main(String[] args) throws IOException {
		String path = "./cfg";
		File file = new File(path);
		PropLoader propiedad = new PropLoader();
		Properties prop;
		prop = propiedad.custom();
		if (file.isDirectory()) {
			path = path+"/config.cfg";
			file = new File(path);
			if (file.isFile()) {
				System.out.print("Cfg custom encontrada.");
				System.out.print("Tomando la configuracion personalizada.");

			}else {
				System.out.print("Cfg no encontrada.");
				System.out.print("Tomando la configuracion por defecto.");

			}
		}else {
			System.out.print("Cfg no encontrada.");
			System.out.print("Tomando la configuracion por defecto.");
			
		}
		System.out.print(prop);
	}

}
