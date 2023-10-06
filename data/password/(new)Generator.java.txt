import java.util.Random;


public class Generator {
	int self_password=0;
	int type=1;
	int length=10;
	String password;

	private StringBuffer sb = new StringBuffer();
	
	void setSelfPassword(int n){
		this.self_password=n;
	}
	int getSelfPassword(){
		return this.self_password;
	}
	void setLength(int length){
		this.length=length;
	}
	int getLength(){
		return this.length;
	}
	void setPassword(){
		
	}
	String getPassword(){
		
		return createRandomPassword();
	}
	
	public static int randInt(int min, int max) {//두 개의 숫자를 받아 랜덤값을 반환하는 함수

	    Random rand = new Random();
	    // nextInt is normally exclusive of the top value,
	    // so add 1 to make it inclusive
	    int randomNum = rand.nextInt((max - min) + 1) + min;
	    return randomNum;
	}


	String createRandomPassword(){
		String stra=new String("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ");
		String strn=new String("0123456789");
		String strsp=new String("!@#$%^&*");//(),.?/[]{};:|-=_+은 생략
		String digits = "[0-9]+";
		String chars = "[A-Za-z]+";
		String spChars = "[!@#$%^&*]+";
		int tea=0;
		int ten=0;
		int tes=0;
		int rand1;
		Random r = new Random();

		if(type==1){
    		//type 1: 특수문자 가능, 제약 없음
    		while(sb.length()<length){
           		tea=r.nextInt(stra.length());
           		ten=r.nextInt(strn.length());
           		tes=r.nextInt(strsp.length());
           		rand1=randInt(1,2);
    			if(rand1==1){
    				sb.append(stra.charAt(tea));
    			}
    			else if(rand1==2){
    				sb.append(strn.charAt(ten));
    			}
//    			else if(rand1==3){
//      				sb.append(strsp.charAt(tes));
//      			}
    		}
    		System.out.println(sb.toString());
    	}
    	else if(type==2){
    		//type 2: 특수문자 가능, 문자or숫자or특수문자 중 2개 이상 혼합 필수
    		do{
    			sb=new StringBuffer(length);    
    			while(sb.length()<length){        		
    				tea=r.nextInt(stra.length());
    				ten=r.nextInt(strn.length());
    				tes=r.nextInt(strsp.length());
    				rand1=randInt(1,3);
    				if(rand1==1){
    					sb.append(stra.charAt(tea));
    				}
    				else if(rand1==2){
    					sb.append(strn.charAt(ten));
    				}
    				else if(rand1==3){
    					sb.append(strsp.charAt(tes));
    				}
    			}
    		}while(sb.toString().matches(digits)||sb.toString().matches(chars)
    				||sb.toString().matches(spChars));
    		System.out.println(sb.toString());
    	}
    	else if(type==3){
    		/*type 3: 특수문자 가능, 문자or숫자or특수문자 중 2개 이상 혼합 필수, 
    		 * 숫자 or 문자 등을 연속해서 3개 이상 사용 금지
    		 */
    		int numCounter=0;
    		int charCounter=0;
    		int spCounter=0;
			while(sb.length()<length){        		
				tea=r.nextInt(stra.length());
				ten=r.nextInt(strn.length());
				tes=r.nextInt(strsp.length());
				rand1=randInt(1,3);
				if(rand1==1){
					sb.append(stra.charAt(tea));
					charCounter++;
					numCounter=0;
					spCounter=0;
				}
				else if(rand1==2){
					sb.append(strn.charAt(ten));
					charCounter=0;
					numCounter++;
					spCounter=0;
				}
				else if(rand1==3){
					sb.append(strsp.charAt(tes));
					charCounter=0;
					numCounter=0;
					spCounter++;
				}
				if(numCounter>2||charCounter>2||spCounter>2){
					sb = new StringBuffer(length);
					charCounter=0;
					numCounter=0;
					spCounter=0;
				}
			}
		}
     	else{
    		System.out.println("Invalid password configuration");        		
    	}
		return sb.toString();
	}
	

}
