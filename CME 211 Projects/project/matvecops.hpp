#ifndef MATVECOPS_HPP
#define MATVECOPS_HPP

#include <vector>

//vector scalar multiplication, returns a vector of (x* y)
std::vector<double> multiply_coeff(double x,
	std::vector<double> &y); 

//adds vectors

std::vector<double> add_vec(std::vector<double> &a, 
								std::vector<double> b); 

//The dot product of  a and b
double dot_product(std::vector<double> &a, 
								std::vector<double> &b);

//The 2-norm of a vector a

double l2normer(std::vector<double> &a); 

// The CSR format sparse-matrix-vector multilication Ax with A
std::vector<double> multiply_vec(std::vector<double> &value,
									std::vector<int>    &col_idx,
									std::vector<int>    &row_ptr,
									std::vector<double> &x); 

std::vector<double> subtract_vec(std::vector<double> &a, 
								std::vector<double> &b); 


#endif /* MATVECOPS_HPP */
