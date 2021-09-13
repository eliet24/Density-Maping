package DensityMapping;
import java.lang.Math;
import java.util.HashMap;
import java.util.Map;

public class Square {
double length;
//Point square_center;
//double diagonal;
int index_row;
int index_column;
double value;
//int [] num_business; //array in size of number of business for each square to tell how many business use it
Map<String, Integer> businessOnSquare = new HashMap<>();

	public Square(double length, int index_row, int index_column, double value) {
	this.length=length;
	this.index_row=index_row;
	this.index_column=index_column;
	this.value=value;
	businessOnSquare.put("food", 0);
	businessOnSquare.put("fashion", 0);
	businessOnSquare.put("health", 0);
	businessOnSquare.put("electronics", 0);
	//this.square_center=this.calc_SquareCenter();
	//this.diagonal=this.calc_diagonal();
	}

	public Map<String, Integer> getBusinessOnSquare() {
        return businessOnSquare ;
	}
        
	public double getLength() {
	return this.length;
	}
	
	public double getValue() {
		return this.value;
		}
		

//	public Point getSquare_center() {
//		return this.square_center;
//	}

	public double getRow() {
		return this.index_row;
	}
	
	public double getColumn() {
		return this.index_column;
	}
	
	public Point calc_singleSquareCenter() {         // return the center point(Coordinates) of single square
		double x=((this.length*this.index_column+this.length*this.index_column-1)/2);
		double y=((this.length*this.index_row+this.length*this.index_row-1)/2);
		Point center=new Point(x,y);
		return center;
	}
	
	
	public double calc_diagonal() {                      // return the length of the diagonal of single square;
		return Math.sqrt(2*Math.pow(this.length, 2));
	}
}
 