import numpy as np


def vectors_to_dbn(num_rows, num_cols, h_, v_):
    """
    Constructs a string as follows : 
    [b | for r in [0,num_rows+1], for c in [0,num_cols]:
         b=1 if horizontal line[r,c] set else 0] 
    ++
    [b | for r in [0,num_rows_], for c in [0,num_cols+1]:
         b=1 if vertical line[r,c] set else 0]
    """
    dbn = ""

    for r in range(num_rows + 1):
        for c in range(num_cols):
            dbn += "1" if h_[r][c] else "0"

    for r in range(num_rows):
        for c in range(num_cols + 1):
            dbn += "1" if v_[r][c] else "0"

    return dbn


def dbn_to_vectors(num_rows, num_cols, dbn:str):
    """
    Create horizontal and vertical edge vectors from the Dots-and-Boxes Notation.
    """
    
    h_ = [[0] * num_cols for _ in range(num_rows + 1)]
    v_ = [[0] * (num_cols + 1) for _ in range(num_rows)]
    num_moves = 0
    
    idx = 0
    for row in range(num_rows + 1):
        for col in range(num_cols):
            if dbn[idx] == '1':
                h_[row][col] = 1
                num_moves += 1
            idx += 1
    
    for row in range(num_rows):
        for col in range(num_cols + 1):
            if dbn[idx] == '1':
                v_[row][col] = 1
                num_moves += 1
            idx += 1
    
    max_moves = (num_rows + 1) * num_cols + num_rows * (num_cols + 1)
    assert num_moves <= max_moves, "Number of moves exceeds maximum possible moves"

    return h_, v_

# // Create initial board from the Dots-and-Boxes Notation.
# // A vector with:
# // [b | for r in [0,num_rows+1], for c in [0,num_cols]:
# //      b=1 if horizontal line[r,c] set else 0] +
# // [b | for r in [0,num_rows_], for c in [0,num_cols+1]:
# //      b=1 if vertical line[r,c] set else 0]
# DotsAndBoxesState::DotsAndBoxesState(std::shared_ptr<const Game> game,
#                                      int num_rows, int num_cols,
#                                      bool utility_margin,
#                                      const std::string& dbn)
#     : State(game),
#       num_rows_(num_rows),
#       num_cols_(num_cols),
#       num_cells_((1 + num_rows) * (1 + num_cols)),
#       utility_margin_(utility_margin) {

#   /* std::cout << "Init dots and boxes state with dbn\n"; */
#   SPIEL_CHECK_GE(num_rows_, 1);
#   /* SPIEL_CHECK_LE(num_rows_, 1000); */
#   SPIEL_CHECK_GE(num_cols_, 1);
#   /* SPIEL_CHECK_LE(num_cols_, 1000); */

#   h_.resize(num_cells_);
#   v_.resize(num_cells_);
#   p_.resize(num_cells_);

#   std::fill(begin(h_), end(h_), CellState::kEmpty);
#   std::fill(begin(v_), end(v_), CellState::kEmpty);
#   std::fill(begin(p_), end(p_), CellState::kEmpty);
#   std::fill(begin(points_), end(points_), 0);

#   int cell = 0;
#   int idx = 0;

#   for (int row = 0; row < num_rows_ + 1; ++row) {
#     for (int col = 0; col < num_cols_; ++col) {
#       if (dbn[idx] == '1') {
#         h_[cell] = CellState::kSet;
#         num_moves_++;
#       }
#       idx++;
#       cell++;
#     }
#     cell++;
#   }
#   cell = 0;
#   for (int row = 0; row < num_rows_; ++row) {
#     for (int col = 0; col < num_cols_ + 1; ++col) {
#       if (dbn[idx] == '1') {
#         v_[cell] = CellState::kSet;
#         num_moves_++;
#       }
#       idx++;
#       cell++;
#     }
#   }
#   int max_moves = (num_rows_ + 1) * num_cols_ + num_rows_ * (num_cols_ + 1);
#   SPIEL_CHECK_LE(num_moves_, max_moves);
# }