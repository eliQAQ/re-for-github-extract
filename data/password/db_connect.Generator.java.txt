package db_connec_test;

import java.util.Random;

public class Generator {
	int self_password = 1;
	int type = 3;
	int length = 10;
	String password;
	String includeChar;
	String includeNum;
	int max = 15;
	int min = 10;

	// Predefine strings
	private String stra = new String("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ");
	private String strn = new String("0123456789");
	private String strsp = new String("!@#$%^&*");// (),.?/[]{};:|-=_+
	private String digits = "[0-9]+";
	private String chars = "[A-Za-z]+";
	private String spChars = "[!@#$%^&*]+";

	void setSelfPassword(int n) {
		this.self_password = n;
	}

	int getSelfPassword() {
		return this.self_password;
	}

	void setLength(int length) {
		this.length = length;
	}

	int getLength() {
		return this.length;
	}

	void setType(int type) {
		if (type == 2 || type == 3)
			this.type = type;
		else
			this.type = 1;
	}

	void setPassword() {

	}

	String getPassword() {
		if (self_password == 1)
			return createCustomPassword();
		else
			return createRandomPassword();
	}

	void setIncludeNum(int n) {
		this.includeNum = String.valueOf(n);
	}

	String getIncludeNum() {
		return this.includeNum;
	}

	void setIncludeChar(String includeChar) {
		this.includeChar = includeChar;
	}

	String getIncludeChar() {
		return this.includeChar;
	}

	// Generate random range between min and max
	public static int randInt(int min, int max) {
		Random rand = new Random();
		// nextInt is normally exclusive of the top value,
		// so add 1 to make it inclusive
		int randomNum = rand.nextInt((max - min) + 1) + min;
		return randomNum;
	}

	String createRandomPassword() {

		StringBuffer sb = new StringBuffer();

		int tea = 0;
		int ten = 0;
		int tes = 0;
		int rand1;
		Random r = new Random();

		if (type == 1) {
			// type 1: Able to use special chars, Without any condition
			while (sb.length() < length) {
				tea = r.nextInt(stra.length());
				ten = r.nextInt(strn.length());
				tes = r.nextInt(strsp.length());
				rand1 = randInt(1, 2);
				if (rand1 == 1) {
					sb.append(stra.charAt(tea));
				} else if (rand1 == 2) {
					sb.append(strn.charAt(ten));
				}

			}
		} else if (type == 2) {
			// type 2: Able to use special chars,
			// Must combine at least 2 categories among chars, numbers, special chars
			do {
				sb = new StringBuffer(length);
				while (sb.length() < length) {
					tea = r.nextInt(stra.length());
					ten = r.nextInt(strn.length());
					tes = r.nextInt(strsp.length());
					rand1 = randInt(1, 3);
					if (rand1 == 1) {
						sb.append(stra.charAt(tea));
					} else if (rand1 == 2) {
						sb.append(strn.charAt(ten));
					} else if (rand1 == 3) {
						sb.append(strsp.charAt(tes));
					}
				}
			} while (sb.toString().matches(digits) || sb.toString().matches(chars) || sb.toString().matches(spChars));
		} else if (type == 3) {
			/*
			 * type 3: Able to use special chars,
			 * Must combine at least 2 categories among chars, numbers, special chars
			 * Cannot use same character or number sequentially more than 3 times
			 */
			int numCounter = 0;
			int charCounter = 0;
			int spCounter = 0;
			while (sb.length() < length) {
				tea = r.nextInt(stra.length());
				ten = r.nextInt(strn.length());
				tes = r.nextInt(strsp.length());
				rand1 = randInt(1, 3);
				if (rand1 == 1) {
					sb.append(stra.charAt(tea));
					charCounter++;
					numCounter = 0;
					spCounter = 0;
				} else if (rand1 == 2) {
					sb.append(strn.charAt(ten));
					charCounter = 0;
					numCounter++;
					spCounter = 0;
				} else if (rand1 == 3) {
					sb.append(strsp.charAt(tes));
					charCounter = 0;
					numCounter = 0;
					spCounter++;
				}
				if (numCounter > 2 || charCounter > 2 || spCounter > 2) {
					sb = new StringBuffer(length);
					charCounter = 0;
					numCounter = 0;
					spCounter = 0;
				}
			}
		} else {
			System.out.println("Invalid password configuration");
		}
		return sb.toString();
	}

	String createCustomPassword() {
		StringBuffer sb = new StringBuffer();
		int numCount = 0;
		int charCount = 0;
		int rand1 = 0;
		int tea = 0;
		int ten = 0;
		int tes = 0;
		int outputLength;
		String stra = new String("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ");
		String strn = new String("0123456789");
		String strsp = new String("!@#$%^&*");// (),.?/[]{};:|-=_+은 생략
		String digits = "[0-9]+";
		String chars = "[A-Za-z]+";
		Random r = new Random();
		outputLength = length; // Save length for print out
		
		// type 1(without any condition, 
		// combine numbers and chars
		if (type == 1 || type == 2) {
			while (sb.length() < length) {
				if (numCount >= includeNum.length() && charCount >= includeChar.length()) {
					tea = r.nextInt(stra.length());
					ten = r.nextInt(strn.length());
					tes = r.nextInt(strsp.length());
					rand1 = randInt(1, 2);
					if (rand1 == 1) {
						sb.append(stra.charAt(tea));
					} else {
						sb.append(strn.charAt(ten));
					}
				} else if (numCount >= includeNum.length()) {
					sb.append(includeChar.charAt(charCount));
					charCount++;
				} else if (charCount >= includeChar.length()) {
					sb.append(includeNum.charAt(numCount));
					numCount++;
				} else {
					rand1 = randInt(1, 2);
					if (rand1 == 1) {
						sb.append(includeChar.charAt(charCount));
						charCount++;
					} else {
						sb.append(includeNum.charAt(numCount));
						numCount++;
					}
				}
			}
		} else if (type == 3) {
			// Prevent consecutive characters or numbers
			String tempString = new String();
			String tempString2 = new String();
			int temp = 2;
			while (sb.length() < length) {
				if (numCount >= includeNum.length() && charCount >= includeChar.length()) {
					tea = r.nextInt(stra.length());
					ten = r.nextInt(strn.length());
					tes = r.nextInt(strsp.length());
					rand1 = randInt(1, 2);
					if (rand1 == 1) {
						sb.append(stra.charAt(tea));
					} else {
						sb.append(strn.charAt(ten));
					}
				} else if (numCount >= includeNum.length()) {
					sb.append(includeChar.charAt(charCount));
					charCount++;
				} else if (charCount >= includeChar.length()) {
					sb.append(includeNum.charAt(numCount));
					numCount++;
				} else {
					rand1 = randInt(1, 2);
					if (rand1 == 1) {
						sb.append(includeChar.charAt(charCount));
						charCount++;
					} else {
						sb.append(includeNum.charAt(numCount));
						numCount++;
					}
				}
			}
			while (temp <= sb.length() - 1) {
				tempString = (sb.toString()).substring(temp - 2, temp + 1);
				if (tempString.matches(chars) || tempString.matches(digits)) {
					tempString2 = (sb.toString()).substring(temp, sb.length());
					sb.delete(temp, sb.length());
					tes = r.nextInt(strsp.length());
					sb.append(strsp.charAt(tes));
					sb.append(tempString2);
					temp = temp + 3;
				}
				temp = temp + 1;
			}
		}
		return sb.substring(0, outputLength);
	}
}
