#ifndef CGSOLVER_HPP
#define CGSOLVER_HPP

#include <string>
#include <vector>


#include "sparse.hpp"

/* implements the CG algorithm for a linear system
 *
 * Ax = b, A is in CSR format. This algorithm runs the max number of iterations
 * equal to the size of the linear system.  
 * My solver returns the number of iterations needed for
 * the solution to converge in realtion to the predermined
 * tolerance
 *if solution does not converge, then -1 is returned 
 */

int CGSolver(std::vector<double> &val,
             std::vector<int>    &row_ptr,
             std::vector<int>    &col_idx,
             std::vector<double> &b,
             std::vector<double> &x,
             double              tol,
             std::string         soln_prefix);

#endif 
