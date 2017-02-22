#ifndef HEAT_HPP
#define HEAT_HPP

#include <string>
#include <vector>

#include "sparse.hpp"

class HeatEquation2D
{
  private:
    SparseMatrix A;
    std::vector<double> b; 
    std::vector<double> x;
    std::vector<double> hot;
    std::vector<double> cold;

  public:
    //sets Ax=b 
    int Setup(std::string inputfile);
    //solve using CGsolver
    int Solve(std::string soln_prefix);
};

//initialize the matrix A, based on the coordinats of points.
int indx(int x, int y, int col);

#endif /* HEAT_HPP */
