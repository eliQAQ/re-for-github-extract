import java.util.Random;
import java.util.Scanner;

public class Main {
 
    public static void main(String[] args) throws Exception {

    	Scanner scan = new Scanner(System.in);
        System.out.println("1-새로 key를 생성해서 그걸 토대로 비밀번호 암호화하기\n2-기존의 key를 입력받아서 그걸 토대로 비밀번호 복호화하기");
        int i=scan.nextInt();
        if(i==1){
        	StringBuffer keyBuff = new StringBuffer();
        	String key = new String();
        	String keySource = 
        			new String("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*?/");
        	while(keyBuff.length()<16){
        		Random r = new Random();
        		int index=r.nextInt(keySource.length());
        		keyBuff.append(keySource.charAt(index));
        	}
        	key=keyBuff.toString();
            		// 원본 혹은 encrypt된 비밀번호
            Encrypter aes256 = new Encrypter(key);
            String text =new String("여기에다 비밀번호 대입하면 돼");
            String encText = aes256.aesEncode(text);
            System.out.println("암호화할 문자 : " + text);
            System.out.println("암호화할 키    : " + key);
            System.out.println("암호화된 문자 : " + encText);
            
            //text, key 랑 encText를 이용하면 된다
        }
        
     
        else{
        String key = new String();		//복호화에 쓰이는 key값
        String encText = new String();
        System.out.println("Enter key: ");
        key="sBe4JC/T@I3gC$0R";
        //key=scan.nextLine();
        /*암호화할 키    : sBe4JC/T@I3gC$0R
		암호화된 문자 : q/3tDI33Da/ZFpUByTnSyj5h0WiimVhnXQ6SopF3irUbRWIiaTp4gYQaGDaI1/iY*/
        Encrypter aes256 = new Encrypter(key);
        System.out.println("Enter password : ");
        //encText=scan.nextLine();
        encText="q/3tDI33Da/ZFpUByTnSyj5h0WiimVhnXQ6SopF3irUbRWIiaTp4gYQaGDaI1/iY";
    	String decText = aes256.aesDecode(encText);
        System.out.println("암호화된 문자 : " + encText);
    	System.out.println("복호화된 문자 : " + decText);
        }
    }
 
}
