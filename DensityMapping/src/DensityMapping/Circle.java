package DensityMapping;
import java.lang.Math;

public class Circle {
	double radius;
	//Point circle_center;
	
	public Circle(double radius) {
		this.radius=radius;
		//this.circle_center=center;
	}
	
	public double circleToSquare(double radius) {   // return length of edge of the equivalent square
		double edge_of_square=Math.sqrt(2)*radius;
		return edge_of_square;
	}
}
