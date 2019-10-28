package start;

import java.io.IOException;
import java.util.Properties;
import start.PropLoader;

public class Start {

	public static void main(String[] args) throws IOException {
		PropLoader propiedad = new PropLoader();
		Properties prop;
		prop = propiedad.defecto();
		System.print.out(prop);
	}
}
