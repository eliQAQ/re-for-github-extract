package db_connec_test;

import java.io.UnsupportedEncodingException;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.Key;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
import java.util.Random;
import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class Encryptor {
	private String iv;
	private Key keySpec;

	public Encryptor(String key) throws UnsupportedEncodingException {
		this.iv = key.substring(0, 16);
		byte[] keyBytes = new byte[16];
		byte[] b = key.getBytes("UTF-8");
		int len = b.length;
		if (len > keyBytes.length)
			len = keyBytes.length;
		System.arraycopy(b, 0, keyBytes, 0, len);
		SecretKeySpec keySpec = new SecretKeySpec(keyBytes, "AES");

		this.keySpec = keySpec;
	}

	// Generate random key
	public String generateKey() {
		StringBuffer temp = new StringBuffer();
		Random r = new Random();
		String chars = "[A-Za-z]";
		String digits = "[0-9]";
		String spChars = "~!@#$%^&*(){}[]:;<>,./?";
		int rand = 0;
		int rc = 0;
		int rd = 0;
		int rsp = 0;
		while (temp.length() < 16) {
			rand = r.nextInt(2);
			rc = r.nextInt(chars.length());
			rd = r.nextInt(digits.length());
			rsp = r.nextInt(spChars.length());
			if (rand == 0)
				temp.append(chars.charAt(rc));
			else if (rand == 1)
				temp.append(digits.charAt(rd));
			else
				temp.append(spChars.charAt(rsp));
		}
		return temp.toString();
	}

	// Encrypt password
	public String aesEncode(String str)
			throws java.io.UnsupportedEncodingException, NoSuchAlgorithmException, NoSuchPaddingException,
			InvalidKeyException, InvalidAlgorithmParameterException, IllegalBlockSizeException, BadPaddingException {
		Cipher c = Cipher.getInstance("AES/CBC/PKCS5Padding");
		c.init(Cipher.ENCRYPT_MODE, keySpec, new IvParameterSpec(iv.getBytes()));

		byte[] encrypted = c.doFinal(str.getBytes("UTF-8"));
		String enStr = new String(Base64.getEncoder().encode(encrypted));

		return enStr;
	}

	// Decrypt password
	public String aesDecode(String str)
			throws java.io.UnsupportedEncodingException, NoSuchAlgorithmException, NoSuchPaddingException,
			InvalidKeyException, InvalidAlgorithmParameterException, IllegalBlockSizeException, BadPaddingException {
		Cipher c = Cipher.getInstance("AES/CBC/PKCS5Padding");
		c.init(Cipher.DECRYPT_MODE, keySpec, new IvParameterSpec(iv.getBytes("UTF-8")));

		byte[] byteStr = Base64.getDecoder().decode(str.getBytes());

		return new String(c.doFinal(byteStr), "UTF-8");
	}
}
