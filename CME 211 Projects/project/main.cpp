#include <iostream>
#include <string>

#include "heat.hpp"

//--run_1
//--CGSolver fails to converge even on input0.txt
//--END

//--functionality_1
//--Cannot get program to work for any of input[012].txt
//--END

//--output_1
//--CGSolver endlessly writes intermediate guesses to disk,
//--and has no termination condition.
//--END

//--performance_1
//--Code runs forever, unless manually stopped.
//--END

//--compile_0.5
//--CGSolver had several modifications required before it could compile.
//--Notably, lines 59-60 were problematic.
//--END

//--code:read_0.1
//--Non-standard indentation in matvecops.cpp
//--END

//--design_0.5
//--Heat.cpp should have additional sub-routines to make code both
//--more compact and also more computationally efficient; see comments in script.
//--CGSolver doesn't return the correct value, according to your own code!
//--See comment for two-wongs don't make a right.
//--Matvecops should allow addvec and subtract_vec to share code.
//--END

//--code:extra_1
//--END

//--doc:extra_1
//--END

int main(int argc, char *argv[])
{
  //command line args 
  if (argc != 3)
  {
    std::cout << "Usage:" << std::endl;
    std::cout << "  " << argv[0] << " <input file> <solution file>" << std::endl;
    return 0;
  }

  /* Setup 2D heat equation system */
  HeatEquation2D sys;

  int solver = sys.Setup(argv[1]);
  if (solver)
  {
    std::cerr << "ERROR: System setup was unsuccessful" << std::endl;
    return 1;
  }
  
  //solve 
  solver = sys.Solve(argv[2]);
  if (solver)
  {
    std::cerr << "ERROR: System solve was unsuccessful" << std::endl;
    return 1;
  }

  return 0;
}
