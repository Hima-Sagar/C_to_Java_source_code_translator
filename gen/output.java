public class Test {
	public static int search(int arr[],int  arr_len,int x){ 
		for( int  i=0;i<arr_len;i++){ 
			if( arr[i]==x){ 
				return i;
			}
		} 
		return -1;
	} 
	public static int verifyFactorial(int num){ 
		int fact=1 ; 
		if( num<0){ 
			fact=-1 ; 
		}
		else{ 
			if( num>1){ 
				do { 
					fact=fact*num ; 
					num=num-1 ; 
				} while( num>1); 
			}
			else{ 
				fact=1 ; 
			}
		}
		return fact;
	} 
	public static  void main(String[] args) { 
		int arr[]={1,2,3,4,5,6} ; 
		int num=6 ; 
		int result=search(arr,6,num) ; 
		System.out.println(result);
		result=factorial(num) ; 
		System.out.println(result);
	} 
	public static int factorial(int num){ 
		int copyNum=num ; 
		int fact=1 ; 
		if( num<0){ 
			fact=-1 ; 
		}
		else{ 
			while( num>1){ 
				fact=fact*num-- ; 
			} 
		}
		return fact==verifyFactorial(copyNum)?fact:-2;
	} 
}