/* Project 2 - A Bit Puzzling
 * BB&N 2019-20 Advanced Topics in Computer Science
 * BitPuzzles.java - source file with your puzzle solutions.
 * See the Powerschool posting for guidelines, rules, and hints.
 *
 * Name:
 * Date:
 */
public class BitPuzzles {
	/*
	 * Helper function notLogical because Java doesn't have ! built in
	 * for non boolean variables.
	 * Please still complete the "not" function with the required
	 * limited operators.
	 */
	public static int notLogical(int a) {
		return !(a == 0) ? 0 : 1;
	}

	/*
	 * maxVal - return maximum possible number
	 * 	Legal operations: ! ~ & ^ | + << >>
	 *  Maximum operations: 5
	 *  Difficulty: 1
	 *  Explanation: Worked backwards from first bit to fill all but
	 *  first bit with zeros, then flipped all bits so that
	 *  it was the biggest positive integer
	 */
	public static int maxVal() {
	    int x = 0b0001;
	    x = x << 31;
        x = ~x;
        return x;
	}

	/*
	 * bitAnd - a&b using only ~ and |
	 *  Example: bitAnd(6, 5) = 4
	 *  Legal operations: ~ |
	 *  Maximum operations: 8
	 *  Difficulty: 1
	 *  Explanation: And is checking if two bits are one. To do with or and bitwise not requires 
	 *  the use of De Morgan's Laws. Since not a or not b is the same as the not (a and b)
	 *  we can get not (a and b) by orring not a and not b, then notting the
	 *  result to get a and b.
	 */
	 public static int bitAnd(int a, int b) {
        a = ~a;
        b = ~b;
	    int x = a | b;
	    x = ~x;
	    return x;
	 }

	 /*
 	 * bitXor - a^b using only ~ and &
 	 *  Example: bitXor(4, 5) = 1
 	 *  Legal operations: ~ &
 	 *  Maximum operations: 14
 	 *  Difficulty: 1
 	 *  Explanation: To get a^b I worked backwards. The first step backwards is to 
 	 *  find (aOrB & notAAndB). To find notAAndB is pretty simple by using ~(a & b).
 	 *  To find (a or b) I used De Morgan's laws. According to the laws ~(a or b) is the
 	 *  same as (~a & ~b). Then to find (a or b) I just negated ~(a or b).
 	 */
 	 public static int bitXor(int a, int b) {
 	     int notA = ~a;
 	     int notB = ~b;
 	     int notAorB = notB & notA;
 	     int aOrB = ~notAorB;
 	     int aAndB = a & b;
 	     int notAAndB = ~aAndB;
 	     int aXorB = aOrB & notAAndB;
 	     return aXorB;
 	 }

	 /*
 	 * checkSign - return 1 if a < 0, return 0 otherwise
 	 *  Example: checkSign(-1) = 1
 	 *  Legal operations: ! ~ & ^ | + << >>
 	 *  Maximum operations: 6
 	 *  Difficulty: 1
 	 *  Explanation: If a number is positive, I should return 0, which is the 
 	 *  sign bit of a positive number. If a number is negative, I should return 1, which
 	 *  is the sign bit of a negative number. To get the sign bit I shifted the input by
 	 *  31 to get the sign bit into the first bit place. Then and by 1 to make sure that the other
 	 *  31 bits are zero. 
 	 */
 	 public static int checkSign(int a) {
 	     int sign = a >> 31;
 	     sign = sign & 1;
 	     return sign;
 	 }

	 /*
 	 * setThirdBits - return word with every third bit set to 1
 	 *  (i.e.: setThirdBits() = 0100 1001 0010 0100 1001 0010 0100 1001)
 	 *  Legal operations: ! ~ & ^ | + << >>
 	 *  Maximum operations: 8
 	 *  Difficulty: 2
 	 *  Explanation: Wrote an external program to find what is the optimal number to left
 	 *  shift to the get the smallest remainder. I did that three times until the remainder
 	 *  left from the sum of previous steps and the number with every
 	 *  third bit set to 1 was between 255 and 0, which allowed me to add up
 	 *  all the previus steps plus the remainder to get the number where every
 	 *  third bit is set to one. 
 	 */
 	 public static int setThirdBits() {
        int firstStep = 146<<23;
        int secondStep = 146<<14;
        int thirdStep = 146<<5;
        int fourthStep = 9;
        int out = firstStep + secondStep;
        out = out + thirdStep;
        out = out + fourthStep;
        return out;
 	 }

	 /*
 	 * byteExtract - Extract byte n from word a
	 *  Bytes numbered from 0 (LSB) to 3 (MSB)
	 *  Examples: byteExtract(0x12345678,1) = 0x56
	 *  Legal operations: ! ~ & ^ | + << >>
	 *  Max operations: 6
	 *  Difficulty: 2
	 *  Explanation: Getting the first eight bits is done by anding a number by 255 to mask it.
	 *  To shift the word so the desired byte is the first one is done by shifting the
	 *  number of the desired byte by three to the right.
	 *  Then shift a to the right by the result of the previous operation to 
	 *  get the desired byte in front, and mask it to get the byte.
 	 */
 	 public static int byteExtract(int a, int n) {
 	     int shiftBy = n << 3;
 	     a = a >> shiftBy;
 	     return a & 0b11111111;
 	 }

	 /*
 	 * byteSwitch - Swaps the nth byte and mth byte
	 *  Bytes numbered from 0 (LSB) to 3 (MSB)
	 *  Examples: byteSwitch(0x12345678, 1, 3) = 0x56341278
	 *            byteSwitch(0xDEADBEEF, 0, 2) = 0xDEEFBEAD
	 *  You may assume that 0 <= n <= 3, 0 <= m <= 3
	 *  Legal operations: ! ~ & ^ | + << >>
	 *  Max operations: 25
	 *  Difficulty: 3
	 *  Explanation: First, I extracted the two bytes that I am switching.
	 *  Then, I found out to how much to shift each byte by to take the place of the other one. 
	 *  Then, I shifted masks to the places where the bytes that are switching are. 
	 *  After, I flipped the masks and anded them with a so that the places where the 
	 *  bytes go are all filled with ones. 
	 *  Then, I shifted the bytes by the neccesary amount so that they can take eachothers places.
	 *  After, I ored the bytes with a so that they blended with a. 
 	 */
 	 public static int byteSwitch(int a, int n, int m) {
        int byteN = byteExtract(a, n); // three operations
        int byteM = byteExtract(a, m); // three operations
        int shiftByteN = m << 3;
        int shiftByteM = n << 3;
        int maskN = 0b11111111 << shiftByteN;
        int maskM = 0b11111111 << shiftByteM;
        maskN = ~maskN;
        maskM = ~maskM;
        a = a & maskM;
        a = a & maskN;
        byteN = byteN << shiftByteN;
        byteM = byteM << shiftByteM;
        a = a | byteM;
        a = a | byteN;
        return a;
 	 }

	 /*
 	 * addOverflow - Determine if it is possible to compute a+b without overflow.
	 *							 Return 1 if overflow will not occur and 0 otherwise.
 	 *  Example: addOverflow(0x80000000,0x80000000) = 0,
	 *           addOverflow(0x80000000,0x70000000) = 1,
 	 *  Legal operations: ! ~ & ^ | + << >>
 	 *  Maximum operations: 20
 	 *  Difficulty: 3
 	 *  Explanation: There are two comparisons to make to determine if overflow occurs.
 	 *  First, if the sign bits of the two inputs are different, then overflow does not occur.
 	 *  Second, if the sign bits of sum and inputs are the same, then overflow does not occur.
 	 *  To check if the sign bits of the inputs are different I isolated them and xored them.
 	 *  This will return a one if the bits are different and 0 if they are the same.
 	 *  Jumping to the end, if the xor returns a 1, the program will always return a 1, 
 	 *  The second step is to check if the sign bits of the sum and 
 	 *  one of the inputs are the same. It is only neccesary to check one of the 
 	 *  input's signed bits, because if the input's signed bits are different then the 
 	 *  method will already return 1. 
 	 *  To check if sign of the sum and the sign of one of the inputs is the 
 	 *  same you xor and then logical not it because those two 
 	 *  operations will return a one if two bits are the same. Going to the end again, if either
 	 *  the first of second step return a one, then overflow will not occur. 
 	 */
 	 public static int addOverflow(int a, int b) {
        int signA = a >> 31;
        signA = signA & 1;
        int signB = b >> 31;
        signB = signB & 1;
        // if isSignDif is 1, then the sign bits are different, if 0 then they are the same
        int aXorB  = signA ^ signB;
        int sum = a + b;
        int signSum = sum >> 31;
        signSum = signSum & 1;
        int signAXorSignSum = signA ^ signSum;
        signAXorSignSum = notLogical(signAXorSignSum);
        return aXorB | signAXorSignSum;
 	 }

	 /*
 	 * not - Compute !a without using !
 	 *  Example: not(3) = 0, not(0) = 1
 	 *  Legal operations: ~ & ^ | + << >>
 	 *  Maximum operations: 12
 	 *  Difficulty: 3
 	 *  Explanation: The key piece of logic is that if a number is not 0, the opposite of 
 	 *  a number and the number will have opposite signed bits. I then isolated the
 	 *  signed bits and xored them. If the xor produces a 1, then the signed bits
 	 *  are opposite, which means that the input was not 0. If the xor produces a 0, then
 	 *  the input is a zero. Then I have to flip the bits since I should return 1 if the
 	 *  input is zero and zero if it is not zero. Then after flipping the bits, I masked by
	 *  one to isolate the first bit, and returned it. 
 	 */
 	 public static int not(int a) {
        int sign = a >> 31;
        sign = sign & 1;
        int oppositeA = ~a;
        oppositeA = oppositeA + 1;
        int oppositeSign = oppositeA >> 31;
        oppositeSign = oppositeSign & 1;
        int signXorSign = sign ^ oppositeSign;
        signXorSign = ~signXorSign;
        signXorSign = signXorSign & 1;
        return signXorSign;
 	 }
}
