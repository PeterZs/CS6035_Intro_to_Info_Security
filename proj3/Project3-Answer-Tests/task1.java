import java.io.IOException;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.lang.management.ManagementFactory;
import java.lang.management.ThreadMXBean;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.charset.Charset;
import java.security.InvalidKeyException;
import java.util.Arrays;
import javax.xml.bind.DatatypeConverter;


public class task1 {
	public static byte[] padding = new byte[]{(byte)128, 0, 0, 0, 0, 0, 0, 0};

	public static String toHexString(byte[] array) {
		return DatatypeConverter.printHexBinary(array);
	}

	public static byte[] toByteArray(String s) {
		return DatatypeConverter.parseHexBinary(s);
	}
	
	public static byte[] arraySub(byte[]a, int start, int end) {
		byte[] result = new byte[end - start];
		System.arraycopy(a, start, result, 0, end - start);
		return result;
	}

	public static byte[] arrayConcat(byte[] a, byte[] b) {
		if (a == null) {
			if (b == null) {
				return null;
			} else {
				return b;
			}
		} else if (b == null) {
			return a;
		}
		byte[] result = new byte[a.length + b.length];
		System.arraycopy(a, 0, result, 0, a.length);
		System.arraycopy(b, 0, result, a.length, b.length);
		return result;
	}

	public static byte[] cbc_encrypt(byte[] message, String key, String iv) {
		// TODO: Add your code here.
		// Padding
		int messageSize = message.length;
		System.out.println(toHexString(message));
		if (messageSize % 8 != 0) {
			System.out.println(toHexString(Arrays.copyOfRange(padding, 0, 8 - (messageSize % 8))));
			message = arrayConcat(message, Arrays.copyOfRange(padding, 0, 8 - (messageSize % 8)));
		} else {
			message = arrayConcat(message, padding);
		}
		messageSize = message.length;

		// Initialize DES object.
		iv = iv.replace("\n", "");
		key = key.replace("\n", "");
		byte[] ivBytes = toByteArray(iv);
		byte[] keyBytes = toByteArray(key);

		DES des = new DES();
		Object k;
		byte[] result = null;
		try {
			k = des.makeKey(keyBytes, des.KEY_SIZE);
			for (int i=0; i<messageSize; i+=8) {
				// IV Xor Plaintext
				System.out.println(i);
				System.out.println(i+8);
				// System.out.println(message.substring(i, i+8));
				byte[] temp = Arrays.copyOfRange(message, i, i+8);
				System.out.println("before");
				System.out.println(toHexString(temp));

				for (int j=0; j<8; j++) {
					temp[j] = (byte) ( ivBytes[j] ^ temp[j] );
				}
				byte[] output = toByteArray(des.encrypt(k, temp));
				System.out.println("after");
				System.out.println(toHexString(output));

				ivBytes = output;
				System.out.println(ivBytes);
				result = arrayConcat(result, output);
			}
		} catch (InvalidKeyException e) {
			System.out.println("Invalid Key.");
		}
		return result;
	}

	public static byte[] cbc_decrypt(byte[] message, String key, String iv) {
		// TODO: Add your code here.
		int messageSize = message.length;
		// Initialize DES object.
		iv = iv.replace("\n", "");
		key = key.replace("\n", "");
		byte[] ivBytes = toByteArray(iv);
		byte[] keyBytes = toByteArray(key);

		DES des = new DES();
		Object k;
		byte[] result = null;
		try {
			k = des.makeKey(keyBytes, des.KEY_SIZE);
			for (int i=0; i<messageSize; i+=8) {
				// IV Xor Plaintext
				System.out.println(i);
				System.out.println(i+8);
				// System.out.println(message.substring(i, i+8)); 
				byte[] temp = Arrays.copyOfRange(message, i, i+8);
				System.out.println("before");
				System.out.println(toHexString(temp));

				byte[] output = toByteArray(des.decrypt(k, temp));
				for (int j=0; j<8; j++) {
					output[j] = (byte) ( ivBytes[j] ^ output[j] );
				}				
				System.out.println("after");
				System.out.println(toHexString(output));
				ivBytes = temp;
				System.out.println(ivBytes);
				result = arrayConcat(result, output);
			}
		} catch (InvalidKeyException e) {
			System.out.println("Invalid Key.");
		}
		// Discard padding.
		int result_index = result.length-1;
		byte lastByte = result[result_index];
		while (lastByte != padding[0]) {
			result_index --;
			lastByte = result[result_index];			
		}
		result = arraySub(result, 0, result_index);
		return result;
	}

	public static void main (String[] args) {
		if (args.length != 5) {
			System.out.println("Wrong number of arguments!\njava task1 $MODE $INFILE $KEYFILE $IVFILE $OUTFILE.");
			System.exit(1);
		} else {
			String mode = args[0];
			String infile = args[1];
			String keyfile = args[2];
			String ivfile = args[3];
			String outfile = args[4];
			byte[] input = readFromFile(infile);
			String key = readFromFile(keyfile, Charset.defaultCharset());
			String iv = readFromFile(ivfile, Charset.defaultCharset());
			byte[] output = null;

			double start = getCpuTime();
			// Calculate the CPU cycles.
			if (mode.equals("enc")) {
				output = cbc_encrypt(input, key, iv);
			} else if (mode.equals("dec")) {
				output = cbc_decrypt(input, key, iv);
			} else {
				System.out.println(mode);
				System.out.println("Wrong mode!");
				System.exit(1);
			}
			double end = getCpuTime();
			System.out.printf("Consumed CPU time=%f\n", end - start);
			writeToFile(outfile, output);
		}
	}

	static String readFromFile(String path, Charset encoding) {
		try {
			byte[] encoded = Files.readAllBytes(Paths.get(path));
			return new String(encoded, encoding);
		} catch (IOException e) {
			System.out.println("File Not Found.");
			return null;
		}
	}

	static byte[] readFromFile(String path) {
		try {
			byte[] encoded = Files.readAllBytes(Paths.get(path));
			return encoded;
		} catch (IOException e) {
			System.out.println("File Not Found.");
			return null;
		}
	}

	static void writeToFile(String path, byte[] data) {
		try {
			Files.write(Paths.get(path), data);
		} catch (FileNotFoundException e) {
			System.out.println("File Not Found.");
		} catch (IOException e) {
			System.out.println("File Not Found.");
		}
	}

	// Helper functions.
	private static double getCpuTime () {
		ThreadMXBean bean = ManagementFactory.getThreadMXBean();
		// getCurrentThreadCpuTime() returns the total CPU time for the current thread in nanoseconds.
		return bean.isCurrentThreadCpuTimeSupported() ? ((double)bean.getCurrentThreadCpuTime() / 1000000000): 0L;
	}

	static void testDES(String key, String message) {
		DES des = new DES();
		Object k;
		try {
			k = des.makeKey(key.getBytes(), des.KEY_SIZE);
			String output = des.encrypt(k, message.getBytes());
			// suppress output
			// System.out.println(output);
		} catch (InvalidKeyException e) {
			System.out.println("Invalid Key.");
		}
	}
	
	static void test() {
		// This function is for test and illustration purpose.
		char[] chars1 = new char[8];
		char[] chars2 = new char[8];
		Arrays.fill(chars1, '\0');
		Arrays.fill(chars2, '\0');
		String key = new String(chars1);
		String message = new String(chars2);
		testDES(key, message);
		chars2[7] = '\1';
		message = new String(chars2);
		testDES(key, message);
		chars1[7] = '\2';
		chars2[7] = '\0';
		key = new String(chars1);
		message = new String(chars2);
		testDES(key, message);
		chars2[7] = '\1';
		message = new String(chars2);
		testDES(key, message);		
	}
}
