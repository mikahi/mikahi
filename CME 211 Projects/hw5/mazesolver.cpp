#include <iostream>
#include <fstream>
#include <string>


enum direction { // initialize north, west, south, east directions to be used in switch statemnet later
	South,
	East,
	North,
	West
};

int main(int argc, char* argv[]) {
	int maze[300][300] = {};
	
//Conﬁrms that appropriate command line arguments were provided and if not provides a usage message and exits
	if (argc < 3) {
		std::cout << "Usage:" << std::endl;
		std::cout << " " << argv[0] << "<maze file> <solution file>" << std::endl;
		return 0;
	}

	int row = 0;
	int column = 0;

// read in number of row and column of the maze
// print an error message and exit if the maze is too big

	std::ifstream filein;

	filein.open(argv[1]);
	if (filein.is_open()) {

		filein >> row >> column;
		if (row > 300 or column > 300) {
        	std::cout << "Not enough storage available." << std::endl;
        	return 0;
    	}

// input 1 into a maze matrix if the coordinates exist on the maze file
		int i, j;
		while(filein >> i >> j) {
			maze[i][j] = 1;
		}
		filein.close();
	}

// find the position of the entrance at the top of the maze matrix
	int entrance;
	for(int i = 0; i < column; i++) {
        if (maze[0][i] == 0) {
			entrance = i;
        }
	}

	int x = 0;
	int y = entrance;
	int d = 0;

//use switch case to do different movements depending on where the player is facing (North, West, South, or East)
//based on where the player is facing, the player will go through a series of if statements to determine
//where it should go based on where the walls are (the order of directions checked are right wall, forward wall, then left wall 
//in order for the player to follow the right hand solver algorithm)
	std::ofstream fileout;
	fileout.open(argv[2]);
	if (fileout.is_open()) {
		fileout << x << " " << y << std::endl;
		while (x < row - 1) {
			switch(d) {
				case South: {
					if (maze[x][y - 1] == 0) {
						y-= 1;
						d = West;
					}
					else if (maze[x + 1][y] == 0){
						x += 1;		
						d = South;
					}
                	else if (maze[x][y+1]==0){
                    	y+=1;
                    	d = East;	
                    } 
                    else{
                    	x-=1;
                    	d = North;
                    }
                    break; 
				}
				case East: {
					if (maze[x+1][y] == 0) {
						x += 1;
						d = South;
					}
					else if (maze[x][y + 1] == 0) {
						y +=1;
						d = East;
					}
					else if (maze[x-1][y] ==0){
						x-=1;
						d = North;
					}
					else {
						y-=1;
						d = West;
					}
					break; 
				}
				case North: {
					if (maze[x][y + 1] == 0) {
						y += 1;
						d = East;
					}
					else if (maze[x - 1][y] == 0) {
						x -= 1;	
						d = North;
					}
					else if (maze[x][y-1]==0) {
						y-=1;
						d = West;
					}
					else {
						x+=1;
						d = South;
					}
					break; 
				}
				case West: {
					if (maze[x-1][y] == 0) {
                    	x -= 1;
                    	d = North;
                	}
                	else if (maze[x][y - 1] == 0) {
                		y-=1;
                		d = West;
                	}
                	else if (maze[x+1][y]==0) {
                		x+=1;
                		d = South;
                	}
                	else {
                		y+=1;
                		d = East;
                	}
                	break; 
				}
			}
			fileout << x << " " << y << std::endl;
		}
		fileout.close();
	}
    return 0;
}
