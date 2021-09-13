package DensityMapping;
import java.io.File;  // Import the File class
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.Map;
import java.util.Scanner; // Import the Scanner class to read text files

public class MapGrid {
Square[][] grid;
int x_length;
int y_length;
double square_length;

	public MapGrid() 
	{
		Scanner input = new Scanner(System.in);  // Create a Scanner object
	    System.out.println("Enter size of each square in grid");
	    double square_size = input.nextDouble();
	    System.out.println("Enter x_length of the grid");
	    int x_length = input.nextInt();
	    System.out.println("Enter y_length of the grid");
	    int y_length = input.nextInt();
	    this.x_length = x_length;
	    this.y_length = y_length;
	    this.square_length=square_size;
	    input.close();
		try {
		      File file = new File("מיפוי_צפיפות.txt");
		      Scanner myReader = new Scanner(file);
		      int i=0;
		      int j=0;
		      while (myReader.hasNextLine()) {
		        double data = myReader.nextDouble();	        
		        if(j>=x_length) {
		        	i++;
		            j=0;
		        }
		        grid[i][j]=new Square(square_size,i, j, data);
		        j++;
		      }
		      myReader.close();
			 } 
		catch (FileNotFoundException e) {
		 System.out.println("An error occurred.");
		e.printStackTrace();
		}
	}
	
	public double calc_dist(int i, int j, int k, int l) {   //calculate distance between the centers of two squares in the grid
		Square a=grid[i][j];
		Square b= grid[k][l];
		Point center_a= a.calc_singleSquareCenter();
		Point center_b=b.calc_singleSquareCenter();
		double dist= Math.abs(Math.sqrt(Math.pow(center_a.getY()-center_b.getY(), 2)+Math.pow(center_a.getX()-center_b.getX(), 2)));
		return dist;
	}
	
	public double[][] calc_gridSums(int size, String kind)  //return double array of all the sums in grid for the buisness square size and kind
	{
	  double [][] sums=new double[y_length-size+1][x_length-size+1];
	  for(int i=0; i<y_length; i=i++)                        /// Initialize array
		  {
			  for(int j=0; j<x_length; j++)
			  {
				  sums[i][j]=this.calc_squareSum(size, i, j, kind);
			  }
		  }
      return sums;
	}
	
	public double calc_squareSum(int size, int i, int j, String kind) {  //return sum of 1 wanted size square in the grid 
		double rowSum=0;
		double squareSum=0;
		for(int k=i; k<size+i; k++)                            
			  {
				  rowSum=0;
			   	for(int l=j; l<size+j; l++)
				{  
				  rowSum=rowSum+(grid[k][l].value)/(grid[k][j].getBusinessOnSquare().get(kind)+1);
				}	
			   	squareSum=squareSum+rowSum;
			  }
	 return squareSum;
		}
	
	public String max_arrayIndex(double [][] sums) {   //return the index (only upper left square of the big buisness square) of the max sum value of the sums array 
		double max=0;
		String max_index = null;
		for (int i=0; i<sums[0].length; i++)
		{
			for(int j=0; j<sums.length; j++)
			{
				if (sums[i][j]>max) {
					max=sums[i][j];
					max_index=String.valueOf(i) + ',' + String.valueOf(j);
				}
			}
		}
		return max_index;
		
	}
	

}

