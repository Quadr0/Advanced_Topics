import java.util.Arrays;
public class MergeSort {


  //Will Carter and Daniel Katz 9/12/19

  // Crucial method in mergesort
  // Takes an array and the index of the left, the middle,
  // and the right and merges them into a sorted array.
  // Main assumption is that an array of size 1 is sorted
  // and that we can efficiently merge the two subarrays.
  public static void merge(int[] arr, int l, int m, int r) {
    // TO BE COMPLETED
    int[] temp = new int[r-l+1];
    int tempL = l, tempR = m+1;
    int i;
    for(i = 0; i < temp.length; i++){
      int atR = arr[tempR], atL = arr[tempL];
      if(atR > atL){
        temp[i] = atL;
        tempL++;
      }
      else{
        temp[i] = atR;
        tempR++;
      }
      if(tempL > m || tempR > r)
      {
        i++;
        break;
      }

    }

    if(tempL > m)
    {
      while(i < temp.length)
      {
        temp[i] = arr[tempR];
        i++;
        tempR++;
      }

    }
    else if(tempR > r)
    {
      while(i < temp.length)
      {
        temp[i] = arr[tempL];
        i++;
        tempL++;
      }

    }

    for(int v = 0; v < temp.length; v++) {
      arr[l+v] = temp[v];
    }

  }

  public static void mergeSort(int arr[], int l, int r) {
    if (l < r)
    {
      // Find the middle point
      int m = (l+r)/2;

      // Sort first and second halves
      mergeSort(arr, l, m);
      mergeSort(arr , m+1, r);

      // Merge the sorted halves
      merge(arr, l, m, r);
    }
  }

  public static void main(String[] args) {
    int arr[] = {12, 11, 13, 5, 6, 7, 19};

    System.out.println("Given Array");
    System.out.println(Arrays.toString(arr));

    mergeSort(arr, 0, arr.length-1);

    System.out.println("\nSorted array");
    System.out.println(Arrays.toString(arr));
  }
}
