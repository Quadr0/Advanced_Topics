/* Bleckel's advice
 for each building
    for each x coordinate
        set the skyline height to the max of bulding height and current height @ x
 */
import java.lang.Math;
import java.util.*;

public class SkylineSolver1 {

  /* Constants */
  final static int NUM_BUILDINGS = 15;
  final static int MAX_X = 50;
  final static int MAX_WIDTH = 7;
  final static int MAX_HEIGHT = 10;

  /* Main method. Sets up the building array and calls
   * methods that build the skyline array
   */
  public static void main(String[] args) {
    // Initialize the buildings array and fill with
    // random width and height buildings
    
    Building[] buildings = new Building[3];
    
    buildings[0] = new Building(1,3,5);
    buildings[1] = new Building(2,5,3);
    buildings[2] = new Building(5,7,9);
    
    /*
    for (int i = 0; i < NUM_BUILDINGS; i++) {
      int min = i + (int)(MAX_X/NUM_BUILDINGS);

      int height = (int)(Math.random() * (MAX_HEIGHT)) + 1;
      int leftX = min + (int)(Math.random() * (MAX_X - min + 1));
      int rightX = leftX + (int)(Math.random() * (MAX_WIDTH )) + 1;

      buildings[i] = new Building(leftX, rightX, height);
    }
    */
    // Print building array
    printBuildings(buildings);

    // Calculate skyline with redundant points removed
    SkylinePoint[] skyline = getSkyline(buildings);
    // Print skyline
    printSkyline(skyline);
  }

  /* IMPLEMENT THIS
   * This function takes the buildings array and calculates the
   * skyline. The returned skyline should have no redundant points
   * and is an array of Skyline objects. Each object in the array
   * is compromised of a x coordinate indicating a change in height,
   * and the associated height that results at that point.
   */
  public static SkylinePoint[] getSkyline(Building[] buildings) {
    ArrayList<SkylinePoint> list = new ArrayList<>();
    ArrayList<SkylinePoint> semiFiltered = new ArrayList<>();
    int maxRight = -1;

    for(int i = 0; i < buildings.length; i++) {
        Building curr = buildings[i];
        if(curr.rightXCord > maxRight) maxRight = curr.rightXCord;
        for(int j = curr.leftXCord; j <= curr.rightXCord; j++) {
            list.add(new SkylinePoint(j, curr.height, curr.leftXCord, curr.rightXCord));
        }
    }
    
    semiFiltered.add(maxAtX(heightsAtX(maxRight, list)));
    semiFiltered.add(maxAtX(heightsAtX(0, list)));
    for(int i = 0; i < maxRight; i++) {
        ArrayList<SkylinePoint> pointsAtX = heightsAtX(i, list);
        SkylinePoint highestPoint = maxAtX(pointsAtX);
        if(i == highestPoint.buildRightX) {
            semiFiltered.add(secondMaxAtX(pointsAtX));
        }
        semiFiltered.add(highestPoint);
    }

    SkylinePoint[] tempArr = new SkylinePoint[semiFiltered.size()];
    for(int i = 0; i < semiFiltered.size(); i++) {
        tempArr[i] = semiFiltered.get(i);
    }
    sortSky(tempArr);
    return tempArr;
  }

  
  private static ArrayList<SkylinePoint> heightsAtX(int currX, ArrayList<SkylinePoint> in) {
    ArrayList<SkylinePoint> out = new ArrayList<>();

    for(SkylinePoint i : in) {
        if(i.xCord == currX) out.add(i);
    }
    out.add(new SkylinePoint(currX, 0, -1, Integer.MAX_VALUE));

    return out;
  }

  private static SkylinePoint maxAtX(ArrayList<SkylinePoint> currX) {
      SkylinePoint temp = new SkylinePoint(-1, -1, -1, -1);
      for(SkylinePoint i : currX) {
          if(i.height >= temp.height) temp = i;  
      }
      return temp;
  }

  private static SkylinePoint secondMaxAtX(ArrayList<SkylinePoint> in) {
    SkylinePoint max = maxAtX(in);
    in.remove(max);
    SkylinePoint secondMax = maxAtX(in);

    return secondMax;
  }
  
  /**************************
  ***************************
  ***** HELPER METHODS ******
  ***************************
  **************************/

  // sorts the array by left point
  private static void sortSky(SkylinePoint[] points) {
    for(int i = 1; i < points.length; i++){
        SkylinePoint curr = points[i];
        int j = i - 1;
        while(j >= 0 && points[j].xCord> curr.xCord) {
            points[j+1] = points[j];
            j--;
        }
        points[j+1] = curr;
    }
  }
  // removes redundant points in a skyline and returns a new array
  // you can decide to use this if you like, but feel free to
  // implement the same thing in the getSkyline method
  private static SkylinePoint[] cleanSkyline(SkylinePoint[] sk) {
    return sk;
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


// SkylinePoint class holds the critical points for describing a
// skyline.
class SkylinePoint {
  int xCord;
  int height;
  int buildRightX, buildLeftX;
  public SkylinePoint(int x, int h, int l, int r) {
    xCord = x;
    height = h;
    buildRightX = r;
    buildLeftX = l;
  }
}

// Building class holds the values that describe each building.
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
