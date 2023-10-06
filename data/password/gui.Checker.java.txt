import java.util.*;
import java.io.*;
import java.lang.*;
import java.math.*;

public class Checker {
	/* password checker
	 * Following conditions should be considered
	 * 1. Length of password
	 * 2. If it has special characters
	 * 3. If it has sequential strings or numbers (ex. 12345, abcde)
	 * 4. If it has repetitive strings (ex. abc12abc90abc)
	 * 5. If is has same character or number sequentially more than 3 times (ex. 11111, aaaaa)
	 * 6. If it has both numbers and characters (Cannot make password that has only numbers or only characters)
	 */
	public int checker(String st) {
		int score = 0;
		int containsNum = 0;
		int containsUpper = 0;
		int containsLower = 0;
		int containsSp = 0;
		int consecNumCnt = 0;
		int consecCharCnt = 0;
		int consecSpCnt = 0;
		String strNum = new String("0123456789");
		String strChar = new String("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ");
		String strSp = new String("@#$%^&*()-_=+|[]{};:/?.><.");

		char ch;

		/* Check if it is using common password to prevent dictionary attack
		 * "common.txt" has about 14 thousands common password
		 */ 
		FileReader fr = null;
		try {
			fr = new FileReader("common.txt");
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		BufferedReader br = new BufferedReader(fr);
		String tempStr = "";
		try {
			while ((tempStr = br.readLine()) != null) {
				if (st.contains(tempStr)) {
					score -= 10;
				}
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		try {
			fr.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		// Calculate score
		
		// Score rule for length
		score += st.length() * 4;

		// Count number of letters, numbers, and special characters
		for (int i = 0; i < st.length(); i++) {
			ch = st.charAt(i);
			Character cr = new Character(ch);
			if (strChar.substring(26).contains(cr.toString())) {
				containsUpper++;
			} else if (strChar.substring(0, 26).contains(cr.toString())) {
				containsLower++;
			} else if (strNum.contains(cr.toString())) {
				containsNum++;
			} else if (strSp.contains(cr.toString())) {
				containsSp++;
			}
		}

		// Score rule for number of letters, numbers, and special characters
		if (containsUpper > 0) {
			score += (st.length() - containsUpper) * 2;
		}
		if (containsLower > 0) {
			score += (st.length() - containsLower) * 2;
		}
		if (containsNum > 0) {
			score += containsNum * 4;
		}
		if (containsSp > 0)
			score += containsSp * 6;

		if (containsNum == 0 && containsSp == 0) {
			score -= (containsUpper + containsLower);
		}

		// Check consecutive chars
		for (int i = 0; i < st.length(); i++) {
			ch = st.charAt(i);
			Character cr = new Character(ch);
			if (strChar.contains(cr.toString())) {
				for (int j = i + 1; j < st.length(); j++) {
					if (strChar.contains(st.substring(j - 1, j))) {
						consecCharCnt++;
					} else {
						i = j;
						break;
					}
				}
			} else if (strNum.contains(cr.toString())) {
				for (int j = i + 1; j < st.length(); j++) {
					if (strNum.contains(st.substring(j - 1, j))) {
						consecNumCnt++;
					} else {
						i = j;
						break;
					}
				}
			} else if (strSp.contains(cr.toString())) {
				for (int j = i + 1; j < st.length(); j++) {
					if (strSp.contains(st.substring(j - 1, j))) {
						consecSpCnt++;
					} else {
						i = j;
						break;
					}
				}
			}
		}

		// Deduct score for each consecutive chars
		score -= consecCharCnt * 2;
		score -= consecNumCnt * 2;
		score -= consecSpCnt * 2;

		// Deduct score if a number, a number, or a special character is used consecutively more than 3 times
		for (int i = 0; i < st.length() - 2; i++) {
			if (st.charAt(i) == st.charAt(i + 1)) {
				score -= 10;
			}
		}

		// Set the score to 0 if it has only characters or numbers
		if ((containsUpper == 0 && containsLower == 0) || containsNum == 0)
			score = 0;
		
		// return final score
		return score;
	}
}
