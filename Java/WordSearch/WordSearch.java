/* Project 2 - WordSearch Solver
 * BB&N 2019-20 Advanced Topics in Computer Science
 * WordSearch.java - source file to solve word search puzzles.
 * See the Powerschool posting for guidelines and more.
 *
 * Name: Daniel Katz
 * Date: September 2019
 */
import java.util.*;
import java.io.*;


public class WordSearch {
    // Scanner to get user's input for minimum word length
    static Scanner scn = new Scanner(System.in); 

    public static void main(String[] args) {
        /* Frist four lines should remain the same */
        String[] dictionary = readDictionary(args);
        System.out.println("Length of dictionary: " + dictionary.length);
        String[][] puzzle = readPuzzle(args);
        System.out.println("Puzzle:");
        printPuzzle(puzzle);


        /* Add your code here */
        // Prompt user for minimum word length and loop until an int is provided
        
        System.out.print("What is the minimum word length to look for: ");
        while(!scn.hasNextInt()) {
            scn.nextLine();
            System.out.print("What is the minimum word length to look for: ");
        }
        int wordLength = scn.nextInt();

        System.out.println("\nUsing naive approach");

        // Take time in nanoseconds before first algorithm starts running
        double beforeAlg1Time = System.nanoTime();

        // Solve using algorithm 3. Track the runtime of alg2, print all words
        // that you find as well as their location in the puzzle, and finally
        // the total number of words that you find.
        solveAlg1(dictionary, puzzle, wordLength);

        double afterAlg1Time = System.nanoTime();
        double alg1Time = (afterAlg1Time - beforeAlg1Time) / 1000000000;

        System.out.println("Algorithim 1 (naive) took "+ alg1Time + " seconds\n");

        System.out.println("Using binary search approach");
        // Take time before algorithm 2
        double beforeAlg2Time = System.nanoTime();

        // Solve using algorithm 2. Track the runtime of alg2, print all words
        // that you find as well as their location in the puzzle, and finally
        // the total number of words that you find.
        solveAlg2(dictionary, puzzle, wordLength);

        double afterAlg2Time = System.nanoTime();
        double alg2Time = (afterAlg2Time - beforeAlg2Time) / 1000000000;

        System.out.println("Algorithim 2 (binary search) took "+ alg2Time + " seconds\n");

        System.out.println("Using binary search with hash set approach");

        // Take time before algorithm 3
        double beforeAlg3Time = System.nanoTime();

        // Solve using algorithm 3. Track the runtime of alg3, print all words
        // that are found in dictionary as well as their location,
        // and print the total number of words found as well
        solveAlg3(dictionary, puzzle, wordLength);

        double afterAlg3Time = System.nanoTime();
        double alg3Time = (afterAlg3Time - beforeAlg3Time) / 1000000000;

        System.out.println("Algorithim 3 (binary search with hashset) took "+
                            alg3Time + " seconds");
    }

    public static void solveAlg1(String[] dictionary, String[][] puzzle, int minWordLength) {
        // Search through every word in dict, and if longer than minimum length
        // with a starting point at every point in the puzzle,
        // search in all direction to see if there is a match for the 
        // target word in the puzzle
        int matches = 0;
        for(String word : dictionary) {
            if(word.length() >= minWordLength) {
                for(int i = 0; i < puzzle.length; i++) {
                    for(int j = 0; j < puzzle[i].length; j++) {
                        if(findInPuzzle(puzzle, word, i, j, -1, -1)) matches++; 
                        if(findInPuzzle(puzzle, word, i, j, -1, +0)) matches++; 
                        if(findInPuzzle(puzzle, word, i, j, -1, +1)) matches++; 
                        if(findInPuzzle(puzzle, word, i, j, +0, -1)) matches++; 
                        if(findInPuzzle(puzzle, word, i, j, +0, +1)) matches++; 
                        if(findInPuzzle(puzzle, word, i, j, +1, -1)) matches++; 
                        if(findInPuzzle(puzzle, word, i, j, +1, +0)) matches++; 
                        if(findInPuzzle(puzzle, word, i, j, +1, +1)) matches++; 
                    }
                }
            }
        }
        System.out.println(matches + " matches were found");
    }

    // Given a start index in the puzzle array, and a direction to go in 
    // both the x and y direction, this method returns true if the target word is found
    // and false if it not found. If the target word is found, it is printed
    public static boolean findInPuzzle(String[][] puzzle, String targetWord, int xStart, 
                                       int yStart, int xDifference, int yDifference) {
 
        // Get length of target word, puzzle row length, and puzzle column length to
        // prevent multiple calls and increase efficiency
        int targetWordLength = targetWord.length();
        int puzHorLen = puzzle.length;
        int puzVertLen = puzzle[0].length;

        // horDif and vertDif is the length and dirction that the array is searching
        // in for the target word. 
        int horDif = xStart + (targetWordLength * xDifference);
        int vertDif = yStart + (targetWordLength * yDifference);

        // if starting for the starting indexs and going in the specified 
        // directions will be out of bounds, return false
        if(horDif < 0 || horDif > puzHorLen || vertDif < 0 || vertDif > puzVertLen) {
            return false;
        }

        StringBuilder builder = new StringBuilder();
        int xIndex = xStart, yIndex = yStart;

        // For loop that iterates for the number of charachters in the targer word
        for(int i = 0; i < targetWordLength; i++) {

            String currChar = puzzle[xIndex][yIndex];

            // Check to see if at the current index, the charachters of the
            // target word and current charachter in the array match, 
            // if not return false
            if(!currChar.equalsIgnoreCase(targetWord.substring(i,i+1))) return false;

            builder.append(currChar);
            String currString = builder.toString(); 

            if(targetWord.equalsIgnoreCase(currString)) {
                currString = "Found \""+currString+"\" at ("+xStart+","+yStart+")";
                currString = currString+" to ("+xIndex+","+yIndex+")"; 
                System.out.println(currString);
                return true;
            }
            xIndex += xDifference;
            yIndex += yDifference;
        } 
        return false;
    }

    public static void solveAlg2(String[] dictionary, String[][] puzzle, int minWordLength) {
        // Starting from every index in the puzzle, build a string in every direction 
        // going outward. If a match is found in the dictionary, print it out
        // and increment add the number of matches to the "matches" variable
        int matches = 0;
        for(int i = 0; i < puzzle.length; i++) {
            for(int j = 0; j < puzzle[0].length; j++) {
                matches += buildAndSearch(dictionary, puzzle, minWordLength, i, j, -1, -1);
                matches += buildAndSearch(dictionary, puzzle, minWordLength, i, j, -1, +0);
                matches += buildAndSearch(dictionary, puzzle, minWordLength, i, j, -1, +1);
                matches += buildAndSearch(dictionary, puzzle, minWordLength, i, j, +0, -1);
                matches += buildAndSearch(dictionary, puzzle, minWordLength, i, j, +0, +1);
                matches += buildAndSearch(dictionary, puzzle, minWordLength, i, j, +1, -1);
                matches += buildAndSearch(dictionary, puzzle, minWordLength, i, j, +1, +0);
                matches += buildAndSearch(dictionary, puzzle, minWordLength, i, j, +1, +1);
            }
        }
        System.out.println(matches + " matches were found");
        return;
    }

    public static int buildAndSearch(String[] dictionary, String[][] puzzle, int minWordLength,
                                      int xStart, int yStart, int xDifference, int yDifference) {


        // Get length of target word, puzzle row length, and puzzle column length to
        // prevent multiple calls and increase efficiency
        int puzHorLen = puzzle.length;
        int puzVertLen = puzzle[0].length;

        // horDif and vertDif is the length and dirction that the array is searching
        // in for the target word. 
        int horDif = xStart + (minWordLength * xDifference);
        int vertDif = yStart + (minWordLength * yDifference);

        // if there is not enough space from the start index to the end of the puzzle
        // to reach the minimum word length, then return.
        if(horDif < 0 || horDif > puzHorLen || vertDif < 0 || vertDif > puzVertLen) {
            return 0;
        }

        // number of result found from starting index going in specified direction
        int out = 0;

        String currString = "";
        int xIndex = xStart, yIndex = yStart;

        while(xIndex >= 0 && xIndex < puzHorLen && yIndex >= 0 && yIndex < puzVertLen) {
            currString = currString + puzzle[xIndex][yIndex];

            if(currString.length() >= minWordLength &&  binSearchDict(dictionary, currString)) {
                String outString = "Found \""+currString+"\" at ("+xStart+","+yStart+")";
                outString = outString+" to ("+xIndex+","+yIndex+")"; 
                out++; 
                System.out.println(outString);
            }

            xIndex += xDifference;
            yIndex += yDifference;
        }
        return out;
    }

    public static boolean binSearchDict(String[] dictionary, String targetWord) {
        int l = 0, r = dictionary.length-1;
        while(l<=r) {
            int mid = (l+r) / 2;
            int compare = targetWord.compareToIgnoreCase(dictionary[mid]);
            if(compare == 0) {
                return true;
            }
            else if(compare < 0) {
                r = mid - 1;
            }
            else {
                l = mid+1;
            }
        }
        return false;
    }

    public static void solveAlg3(String[] dictionary, String[][] puzzle, int minWordLength) {
        // Starting from every index in the puzzle, build a string in every direction 
        // going outward. If a match is found in the dictionary, print it out
        // and increment add the number of matches to the "matches" variable
        // If a current word is found in the hash set of words that are not in the dictionary,
        // do not binary search the dictionary.
        int matches = 0;
        for(int i = 0; i < puzzle.length; i++) {
            for(int j = 0; j < puzzle[0].length; j++) {
                matches += buildAndSearchHash(dictionary, puzzle, minWordLength, i, j, -1, -1);
                matches += buildAndSearchHash(dictionary, puzzle, minWordLength, i, j, -1, +0);
                matches += buildAndSearchHash(dictionary, puzzle, minWordLength, i, j, -1, +1);
                matches += buildAndSearchHash(dictionary, puzzle, minWordLength, i, j, +0, -1);
                matches += buildAndSearchHash(dictionary, puzzle, minWordLength, i, j, +0, +1);
                matches += buildAndSearchHash(dictionary, puzzle, minWordLength, i, j, +1, -1);
                matches += buildAndSearchHash(dictionary, puzzle, minWordLength, i, j, +1, +0);
                matches += buildAndSearchHash(dictionary, puzzle, minWordLength, i, j, +1, +1);
            }
        }
        System.out.println(matches + " matches were found");
        return;
    }

    public static int buildAndSearchHash(String[] dictionary, String[][] puzzle, int minWordLength,
                                      int xStart, int yStart, int xDifference, int yDifference) {

        

        // Get length of target word, puzzle row length, and puzzle column length to
        // prevent multiple calls and increase efficiency
        int puzHorLen = puzzle.length;
        int puzVertLen = puzzle[0].length;

        // horDif and vertDif is the length and dirction that the array is searching
        // in for the target word. 
        int horDif = xStart + (minWordLength * xDifference);
        int vertDif = yStart + (minWordLength * yDifference);

        // if there is not enough space from the start index to the end of the puzzle
        // to reach the minimum word length, then return.
        if(horDif < 0 || horDif > puzHorLen || vertDif < 0 || vertDif > puzVertLen) {
            return 0;
        }

        // Use hash set to see if a current word is the same as a previous word
        // that is not in the dictionary. Looking up if a hash set contains a 
        // value is more efficient than binary search. 
        HashSet<String> notInDict = new HashSet<>();
        
        // number of result found from starting index going in specified direction
        int out = 0;

        String currString = "";
        int xIndex = xStart, yIndex = yStart;

        while(xIndex >= 0 && xIndex < puzHorLen && yIndex >= 0 && yIndex < puzVertLen) {
            currString = currString + puzzle[xIndex][yIndex];

            // If the current string is not in the hash set, continue and increment x and y index
            if(notInDict.contains(currString)) {
                xIndex += yDifference;
                yIndex += yDifference;
                continue;
            }
            else if(currString.length() >= minWordLength && binSearchDict(dictionary, currString)) {
                String outString = "Found \""+currString+"\" at ("+xStart+","+yStart+")";
                outString = outString+" to ("+xIndex+","+yIndex+")"; 
                out++; 
                System.out.println(outString);
            }
            else {
                notInDict.add(currString);
            }

            xIndex += xDifference;
            yIndex += yDifference;
        }
        return out;
    }
    /*****************************************
    DON'T MESS WITH THESE METHODS
    ******************************************/
    private static void printPuzzle(String[][] puzzle) {
        /* Private method for printing sudoku puzzles (i.e. 9X9 array of ints) */
        for (int r = 0; r < puzzle.length; r++) {
            for (int c = 0; c < puzzle[r].length; c++) {
                if (c < puzzle.length-1)
                    System.out.printf("%s ", puzzle[r][c]);
                else
                    System.out.printf("%s\n", puzzle[r][c]);
            }
        }
        System.out.printf("\n");
    }

    private static String[][] readPuzzle(String[] args) {
        String filepath = "pz.txt";
        if (args.length > 1) {
            filepath = args[1];
        }
        List<List<String>> puzzle = new ArrayList<List<String>>();

        try { // try to open file
          File file = new File(filepath);
          Scanner sc = new Scanner(file);
          // fill in puzzle array with file contents
          while (sc.hasNextLine()) {
              String line = sc.nextLine();
              List<String> curRow = new ArrayList<String>();
              for (int i = 0; i < line.length(); i++) {
                 curRow.add(String.valueOf(line.charAt(i)));
              }
              puzzle.add(curRow);
          }
        } catch (FileNotFoundException e) { // filepath is illegal
          System.out.println("FileNotFoundException. Please try again with a valid"
            + "filename");
            System.exit(0);
        }

        String[][] puzzleAsArray = new String[puzzle.size()][puzzle.get(0).size()];
        for (int i = 0; i < puzzle.size(); i++) {
            puzzleAsArray[i] = puzzle.get(i).toArray(new String[puzzle.get(i).size()]);
        }

        return puzzleAsArray;
    }

    private static String[] readDictionary(String[] args) {
        // Takes input from the command line, or defaults to d.txt
        // Returns an array that contains all the words from the dictionary file
        String filepath = "d.txt";
        if (args.length > 0) {
            filepath = args[0];
        }

        List<String> dictionary = new ArrayList<String>();
        try { // try to open file
          File file = new File(filepath);
          Scanner sc = new Scanner(file);
          // fill in dictionary array with file contents
          while (sc.hasNextLine()) {
            dictionary.add(sc.nextLine());
          }
          return dictionary.toArray(new String[dictionary.size()]);
        } catch (FileNotFoundException e) { // filepath is illegal
          System.out.println("FileNotFoundException. Please try again with a valid"
            + "filename");
            System.exit(0);
        }
        return dictionary.toArray(new String[dictionary.size()]);
    }
}
