#ifndef SPARSE_HPP
#define SPARSE_HPP

#include <string>
#include <vector>

class SparseMatrix
{
  private:
    std::vector<int> i_idx;
    std::vector<int> j_idx;
    std::vector<double> a;
    int ncols;
    int nrows;


  public:
    //modify sparse matrix dimensions
    void Resize(int nrows, int ncols);
    //  convert COO matrix to CSR format using provided function 
    void ConvertToCSR();
    //add entry in COO
    void AddEntry(int i, int j, double val);

    //perform sparse matrix vector multiplication using CSR formatted matrix 
    std::vector<double> MulVec(std::vector<double> &vec);

    // Method that actually solve the linear system using CG 
    int CG(std::vector<double> &b, std::vector<double> &x, double tol, std::string soln_prefix);
    
};

#endif /* SPARSE_HPP */
