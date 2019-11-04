import java.util.Random;
import java.util.Arrays;
public class ArrayTest {
    public static void main(String[] args) {
        int[] arr = genRanArr(Integer.parseInt(args[0]));
        int[] out = minMax(arr);
        System.out.println(Arrays.toString(arr));
        System.out.println("Max = " + out[0]);
        System.out.println("Min = " + out[1]);
    }
    public static int[] minMax(int[] in){
        int min = Integer.MAX_VALUE;
        int max = Integer.MIN_VALUE;
        int[] out = new int[2];
        for(int i : in){
            if(i > max) max = i;
            if(i < min) min = i;
        }
        out[0] = max;
        out[1] = min;
        return out;
    }
    public static int[] genRanArr(int size){
        int[] out = new int[size];
        Random rand = new Random();
        for(int i = 0; i < size; i++) {
            out[i] = rand.nextInt(1000000);
        }
        return out;
    }
}
