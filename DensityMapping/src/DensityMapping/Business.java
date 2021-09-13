package DensityMapping;

public class Business extends Circle {
double reqProfit;
String businessKind;
	public Business(double radius, double reqProfit, String kind) {
		super(radius);
		this.reqProfit=reqProfit;
		this.businessKind=kind;
	}
  
	public int find_sizeRatio(MapGrid grid) {  //find square Representation for the business
		Square [][]map=grid.grid;
		//int x_length=grid.x_length;
		//int y_length=grid.y_length;
		double square_length=map[0][0].length;
		double buisness_inSquare=this.circleToSquare(radius);
		int size_ratio=(int)(Math.floor(buisness_inSquare/square_length));
			return size_ratio;	
	}
}
		
		
		

	
		


