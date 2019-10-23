package start;

import java.io.File;

import basicOps.operations;

public class start {

	public static void main(String[] args) {
		// INIT
		String path = "./cfg";
		File file = new File(path);
		if (file.isDirectory()) {
			path = path+"/config.cfg";
			file = new File(path);
			if (file.isFile()) {
				System.out.print("Normally Init");
			}else {
				System.out.print("Config Not Found");
			}
		}else {
			System.out.print("First Init");
		}
	}
	
}
