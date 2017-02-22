


#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <math.h>
#include <cmath> 
#include "heat.hpp"
#include "sparse.hpp"

/* Method to help initialize the matrix A, based on the coordinats of points.*/
int indx(int x, int y, int col){
    int id = (col)* (y-1) + x;
    return id;
}

int HeatEquation2D::Setup(std::string inputfile) {

    //initialize parameters
    double L, W, h, Tc, Th;
    std::ifstream input;
    SparseMatrix A;
    std::vector<int> hot;
    std::vector<int> cold;
    int row, col;


    input.open(inputfile);
    if (input.is_open()) {
        input >> L >> W >> h >> Tc >> Th;

        row = int(W/h) + 1;
        col = int(L/h) + 1;


        for (int i = 0; i < col; ++i){
            hot.push_back(Th);
            cold.push_back(-Tc * (std::exp(-10 * (h * i - L/2) * (h * i - L/2) )-2));
        }


            //resize A
            A.Resize((row-2)*(col-1), (row-2)*(col-1));



            //initialize sparse matrixA, vec b, and  vec x
            for(int y = 1; y < row - 1; ++y){
                for(int x = 0; x < col; ++x){
                  //--design_0
                  //--Would rather see this split into different methods.
                  //--One to populate interior points, another to populate isothermal
                  //--and periodic boundary conditions.
                  //--You could probably cut down this section by 1/2 and still retain functionality.
                    // For the points near the coldside. 
                    if(y == 1) {
                        if (x == 0){
                            A.AddEntry(indx(x,y,col), indx(x+1, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x, y+1, col), -1);
                            A.AddEntry(indx(x,y,col), indx(col-2, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x,y,col), 4);
                            b.push_back(cold[x]);
                        }
                        else if (x == col - 2){
                            A.AddEntry(indx(x,y,col), indx(x-1, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x, y+1, col), -1);
                            A.AddEntry(indx(x,y,col), indx(0, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x,y,col), 4);
                            b.push_back(cold[x]);
                        }
                        else{
                            A.AddEntry(indx(x,y,col), indx(x+1, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x, y+1, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x-1, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x,y,col), 4);
                            b.push_back(cold[x]);
                        }
                    }

                    //for points near hotside

                    else if (y == row-2) {
                        if (x==0) {
                            A.AddEntry(indx(x,y,col), indx(x+1, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x, y+1, col), -1);
                            A.AddEntry(indx(x,y,col), indx(col-2, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x,y,col), 4);
                            b.push_back(hot[x]);
                        }
                        else if (x == col - 2){
                            A.AddEntry(indx(x,y,col), indx(x-1, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x, y+1, col), -1);
                            A.AddEntry(indx(x,y,col), indx(0, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x,y,col), 4);
                            b.push_back(hot[x]);
                        }
                        else{
                            A.AddEntry(indx(x,y,col), indx(x+1, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x, y+1, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x-1, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x,y,col), 4);
                            b.push_back(hot[x]);
                        }
                    }

                    //for points in the middle 

                    else {
                        if (x == 0){
                            A.AddEntry(indx(x,y,col), indx(x, y+1, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x, y-1, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x+1, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(col-2, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x,y,col), 4);
                            b.push_back(0.0);
                        }
                        else if (x == col - 2){
                            A.AddEntry(indx(x,y,col), indx(x, y+1, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x, y-1, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x-1, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(0, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x,y,col), 4);
                            b.push_back(0.0);
                        }
                        else {
                            A.AddEntry(indx(x,y,col), indx(x, y+1, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x, y-1, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x+1, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x-1, y, col), -1);
                            A.AddEntry(indx(x,y,col), indx(x,y,col), 4);
                            b.push_back(0.0);
                        }
                    }
                    //--END
                }
            }
            // initial guess
            for (unsigned int i = 0; i<b.size(); i++) {
                x.push_back(0);
            }
            //convert COO matrix to CSR matrix
            A.ConvertToCSR();
            this->A = A;
            this->b = b;
            this->x = x;            
            return 0;
        

	} else {
		std::cerr << "Could not open input file." << std::endl;
		return 1;			
	}
}


int HeatEquation2D::Solve(std::string soln_prefix) {
  //--design_0
  //--Why not just adjust CG method to return the correct value?
  //--Two wrongs don't make a right!
	int CG_iter = this->A.CG(this->b, this->x, 1.e-5, soln_prefix);
//account for extra iter count in CGsolver
    CG_iter = CG_iter-1;
    //--END
	if (CG_iter >= 0) {
		std::cout << "SUCCESS: CG solver converged in "<< CG_iter << " iterations." << std::endl;
		return 0;
	}
	else {
		std::cout << "The CG algorithm does not converge." << std::endl;
		return 1;
	}
	return 1;
}
