// KLADWERK. 

#include <iostream>
#include <tuple>
using namespace std;

enum class CellOrientation {
  kHorizontal,  // = 0
  kVertical,    // = 1
};

tuple<int, int> move(int action, int rows, int cols);
int GetCell(int row_, int num_cols_, int col_);

int main() {
    int rows = 3;    
    int cols = 3;    

    for(int i = 0; i < 24; i++){  
        cout << i << endl;

        tuple<int,int> result = move(i, rows, cols);

        int row = get<0>(result);
        int col = get<1>(result);

        cout << "Row: " << row << ", Column: " << col << endl;

        cout << "GetCell: " << GetCell(row, cols, col) << endl;
    }


    return 0;
}

tuple<int, int> move(int action, int rows, int cols) {
  int num_rows_ = rows;
  int num_cols_ = cols;
  int row_;
  int col_;
  int maxh = (num_rows_ + 1) * num_cols_;
  if (action < maxh) {
    // Horizontal
    cout << "orientation_ = CellOrientation::kHorizontal" << endl;
    // CellOrientation orientation_ = CellOrientation::kHorizontal;

    row_ = action / num_cols_;
    col_ = action % num_cols_;
  } else {
    // Vertical
    action -= maxh;
    cout << "orientation_ = CellOrientation::kVertical" << endl;
    // CellOrientation orientation_ = CellOrientation::kVertical;

    cout << action << endl;
    row_ = action / (num_cols_ + 1);
    col_ = action % (num_cols_ + 1);
  }
  return make_tuple(row_, col_);
}


int GetCell(int row_, int num_cols_, int col_) { 
    return row_ * (num_cols_ + 1) + col_; }
