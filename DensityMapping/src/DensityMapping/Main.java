package DensityMapping;

import java.util.Map;
import java.util.Scanner;

public class Main {
	
	public static void main(String[] args){
		MapGrid mapGrid=new MapGrid();
		while(true) {
			Scanner input = new Scanner(System.in);  // Create a Scanner object
		    System.out.println("Enter the kind of new business:(food, fashion, health or electronics)");
		    String kind = input.nextLine();
		    System.out.println("Enter imapct radius of business");
		    double radius = input.nextDouble();
		    System.out.println("Enter business required profit");
		    double reqProfit = input.nextDouble();
		    input.close();
			Business biz=new Business(radius, reqProfit, kind);
			int size=biz.find_sizeRatio(mapGrid);
			double [][] sums=mapGrid.calc_gridSums(size, kind);
			String upperLeft=mapGrid.max_arrayIndex(sums);
			String[] parts = upperLeft.split(",");
			int i=Integer.parseInt(parts[0]); 
			int j=Integer.parseInt(parts[1]); 
			for(int k=i; k<i+size; k++) {
				for(int l=j; l<j+size; l++) {
					Map<String, Integer> squareMap=mapGrid.grid[i][j].getBusinessOnSquare();
					squareMap.put(kind, squareMap.get(kind) + 1);
				}
				 System.out.println("Business added to map successfully!");
			}
				
		}
	}
}
