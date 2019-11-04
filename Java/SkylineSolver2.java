// A divide and conquer based C++ program to find skyline of given
// buildings
import java.lang.Math;
public class SkylineSolver2Answer {
  final static int NUM_BUILDINGS = 2;
  final static int MAX_X = 50;
  final static int MAX_WIDTH = 7;
  final static int MAX_HEIGHT = 10;
  public static void main(String[] args) {
    Building[] buildings = new Building[NUM_BUILDINGS];
    for (int i = 0; i < NUM_BUILDINGS; i++) {
      int min = i + (int)(MAX_X/NUM_BUILDINGS);

      int height = (int)(Math.random() * (MAX_HEIGHT + 1));
      int leftX = min + (int)(Math.random() * (MAX_X - min + 1));
      int rightX = leftX + 1 + (int)(Math.random() * (MAX_WIDTH + 1));

      buildings[i] = new Building(leftX, rightX, height);
    }
    printBuildings(buildings);
    SkylinePoint[] skyline = cleanSkyline(getSkyline(buildings, 0, buildings.length-1));
    printSkyline(skyline);
  }

  // Method for governing the recursive structure of the program.
  // This method is the same as the "mergeSort" method in my
  // implementation of mergeSort.
  public static SkylinePoint[] getSkyline(Building[] arr, int l, int r) {
    // deal with base case of one building
    // this will produce a skyline with two points that define it.
    if (l == r)
    {
      SkylinePoint[] skl = new SkylinePoint[2];
      skl[0] = new SkylinePoint(arr[l].leftXCord, arr[l].height);
      skl[1] = new SkylinePoint(arr[l].rightXCord, 0);
      return skl;
    }

    int mid = (l + r)/2;

    // Recurse on left and right halves
    SkylinePoint[] lSkl = getSkyline(arr, l, mid);
    SkylinePoint[] rSkl = getSkyline(arr, mid+1, r);
    // Merge results
    SkylinePoint[] merged = merge(lSkl, rSkl);

    return merged;
  }

  public static SkylinePoint[] merge(SkylinePoint[] lSkl, SkylinePoint[] rSkl) {
    /* WRITE THIS METHOD */
    return null; // CHANGE THIS
  }

  // removes redundant points in a skyline and returns a new array
  private static SkylinePoint[] cleanSkyline(SkylinePoint[] sk) {
    int numCritPts = 0;
    for (int i = 1; i < sk.length; i++) {
      int prev = sk[i-1].height;
      if (prev != sk[i].height) {
        numCritPts++;
      }
    }

    SkylinePoint[] newSk = new SkylinePoint[numCritPts+2];
    int j = 1;
    newSk[0] = sk[0];
    for (int i = 1; i < sk.length; i++) {
      int prev = sk[i-1].height;
      if (prev != sk[i].height) {
        newSk[j] = sk[i];
        j++;
      }
    }
    newSk[numCritPts+1] = sk[sk.length-1];

    return newSk;
  }

  // Skyline printer helper method
  private static void printSkyline(SkylinePoint[] sk) {
    for (int i = 0; i < sk.length; i++) {
      System.out.printf("(%d, %d) ", sk[i].xCord, sk[i].height);
    }
    System.out.println();
  }
  // Buidlings printer helper method
  private static void printBuildings(Building[] bd) {
    for (int i = 0; i < bd.length; i++) {
      System.out.printf("(%d, %d, %d) ", bd[i].leftXCord, bd[i].rightXCord, bd[i].height);
    }
    System.out.println();
  }
}



class SkylinePoint {
  int xCord;
  int height;
  public SkylinePoint(int x, int h) {
    xCord = x;
    height = h;
  }
}

class Building {
  int leftXCord;
  int rightXCord;
  int height;
  public Building(int l, int r, int h) {
    leftXCord = l;
    rightXCord = r;
    height = h;
  }
}
