package start;

import java.io.*;
import java.util.*;

public class PropLoader {

	public Properties defecto() throws IOException{
    	
		Properties prop = new Properties();
		
		try {
			prop.load(this.getClass().getClassLoader().getResourceAsStream("resources/config.properties"));
		} catch(IOException e) {
			System.out.println(e.toString());
		}
		return prop;
		
	}

	public Properties custom() throws IOException{
			Properties prop = new Properties();
			InputStream fichero = null;			
			try {
				fichero = new FileInputStream("cfg/config.cfg");
				prop.load(fichero);
			} catch(IOException e) {
				System.out.println(e.toString());
			}
			return prop;
	}
}