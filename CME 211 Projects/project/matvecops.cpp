#include <vector>
#include <math.h>
#include "matvecops.hpp"

//The CSR sparse-matrix-vector multilication Ax with A's CSR values
//Initialises an iterator for the non-zero elements of the matrix, A.
//Gets the next non-zero element of the matrix, A[i,j]
//the equation for the values in the product matrix will be y[i] += A[i,j]*x[j]

std::vector<double> multiply_vec(std::vector<double> &value,
									std::vector<int>    &col_idx,
									std::vector<int>    &row_ptr,
									std::vector<double> &x) 
{
	std::vector<double> result_vec;

	int vec_size = row_ptr.size()-1; 

		for (unsigned int i = 0; i<vec_size; i++) {
			double m =0;
			for (int j = int(row_ptr[i]); j<int(row_ptr[i+1]); j++) {
				m+= value[j] * x[col_idx[j]];
			}
			result_vec.push_back(m);
		}
		return result_vec;
}

//The dot product of vectors a and b

//--code:read_0
//--This indentation not standard.
double dot_product(std::vector<double> &a, 
								std::vector<double> &b) {
  //--END
	double result = 0;
	for (unsigned int i = 0; i<a.size(); i++) {
		result+= a[i]*b[i];
	}
	return result;
}  


// multiplies vector x
std::vector<double> multiply_coeff(double x,
								std::vector<double> &y) {
	std::vector<double> result;
	for (unsigned int i = 0; i<y.size(); i++) {
		result.push_back(x*y[i]);
	}
	return result;
}

//The 2-norm of a vector x

double l2normer(std::vector<double> &a) {
	return sqrt(dot_product(a, a));
}

//adds vectors

//--design_0
//--It hurts to see so much code duplicated (all but one character: +/-)
std::vector<double> add_vec(std::vector<double> &a, 
								std::vector<double> b) 
{
	std::vector<double> sum;
	for (unsigned int i = 0; i < a.size(); i++) {
		sum.push_back(a[i] + b[i]);
	}

	return sum;
}

//subtracts vectors

std::vector<double> subtract_vec(std::vector<double> &a, 
								std::vector<double> &b) 
{
	std::vector<double> diff;
	for (unsigned int i = 0; i < a.size(); i++) {
		diff.push_back(a[i] - b[i]);
	}

	return diff;
}
//--END
