
#include <string>
#include <vector>

#include "sparse.hpp"
#include "COO2CSR.hpp"
#include "matvecops.hpp"
#include "CGSolver.hpp"

//adds entry to sparse matrix
void SparseMatrix::AddEntry(int i_, int j_, double val_) {
	this->i_idx.push_back(i_);
	this->j_idx.push_back(j_);
	this->a.push_back(val_);


}
//converts sparse matrix to CSR
void SparseMatrix::ConvertToCSR(){
  std::vector<double> copy_a=this->a;
  std::vector<int> copy_i_idx=this->i_idx;
  std::vector<int> copy_j_idx=this->j_idx;
  
  COO2CSR(copy_a,copy_i_idx,copy_j_idx);
 
  this->i_idx=copy_i_idx;
  this->a=copy_a;
  this->j_idx=copy_j_idx;
}
//resizes sparse matrix
void SparseMatrix::Resize(int nrows_, int ncols_) {
	nrows = nrows_; 
	ncols = ncols_;
}

//multiplies a sparse matrix with a vector
std::vector<double> SparseMatrix::MulVec(std::vector<double> &vec) {
	return multiply_vec(this->a, this->i_idx, this->j_idx, vec);
}
//CG solves sparse matrix
int SparseMatrix::CG(std::vector<double> &b, std::vector<double> &x, double tol, std::string soln_prefix) {
	return CGSolver(this->a, this->i_idx, this->j_idx, b, x, tol, soln_prefix);
}
