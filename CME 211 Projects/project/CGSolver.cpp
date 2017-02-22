#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <cmath>
#include "matvecops.hpp"
#include "CGSolver.hpp"



//writes the solution to the solution file
void WriteSoln(std::vector<double> &x, std::string name) {
    std::ofstream f(name);
	std::size_t dim = x.size();
	// write the solution line by line
	if (f.is_open()) {
		for (std::size_t i = 0; i < dim; i++) {
			f << x[i] << std::endl;
		}

		f.close();
	}
	else {
		std::cerr << "ERROR: Unable to write solution file!" << std::endl;
		exit(1);
	}
}


//solves the CG algorithm 
int CGSolver(std::vector<double> &val,
             std::vector<int>    &row_ptr,
             std::vector<int>    &col_idx,
             std::vector<double> &b,
             std::vector<double> &x,
             double              tol,
             std::string 		 soln_prefix)
{
	//initializes variables


	std::vector<double> r;
	std::vector<double> Ax = multiply_vec(val, col_idx, row_ptr, x); //make multiply vec
	double l2norm0;
	r=subtract_vec(b,Ax);
	l2norm0 = l2normer(r);// finds norm of l 
	std::vector<double> p=r;
	int niter = 1;


	// write the initial guess
    std::stringstream s;
    s << std::setfill('0') << std::setw(3) << 0;
    //--compile_0
    //--Originally, this was left `std::string filename = soln_` where soln_ undefined
    //--and the line missing a closing semi-colon. Also, `ix` not defined below...
    std::string filename = soln_prefix;
    //ix + s.str() + ".txt"; // This line was left-in (not commented upon submission) but it doesn't perform any assignment or operation!
    WriteSoln(x, filename);
    //--END

	while (niter<row_ptr.size()){
		niter = niter +1;
		//multiply p from first 3 inpouts
		std::vector<double> Ap = multiply_vec(val, col_idx, row_ptr,p); 

		//get dot product 
		double r_initial = dot_product(r,r); 
		double alpha = r_initial/dot_product(p,Ap);
		//multiply vector by coeffifient alpha, also single for loop
		x= add_vec(x, multiply_coeff(alpha,p)); 

		// add vector adds two vectors . will be similar to dot product but will add instead
		r = add_vec(r,multiply_coeff(-alpha,Ap));
		double l2normr=l2normer(r); 
		//returns the number of iterations 
		if (l2normr/l2norm0 < tol){

			std::stringstream s;
            s << std::setfill('0') << std::setw(3) << niter;
            std::string filename = soln_prefix + s.str() + ".txt";
            WriteSoln(x, filename);

			return int(niter);
		}
		double beta = dot_product(r,r)/r_initial;

		p=add_vec(r, multiply_coeff(beta,p));

		if (niter % 10==0) {

			std::stringstream s;
            s << std::setfill('0') << std::setw(3) << niter;
            std::string filename = soln_prefix + s.str() + ".txt";
            WriteSoln(x, filename);
		}


	}
	// otherwise the algorithm diverges
	return -1;
}
