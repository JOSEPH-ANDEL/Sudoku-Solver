set ROWS := 1..9;
set COLS := 1..9;
set DIGITS := 1..9;
set FIXED within ROWS cross COLS cross DIGITS;


# Binary decision variables
var x{ROWS, COLS, DIGITS} binary;

# Constraints
subject to cell_constraint{i in ROWS, j in COLS}:
    sum{k in DIGITS} x[i, j, k] = 1;

subject to row_constraint{i in ROWS, k in DIGITS}:
    sum{j in COLS} x[i, j, k] = 1;

subject to column_constraint{j in COLS, k in DIGITS}:
    sum{i in ROWS} x[i, j, k] = 1;

subject to subgrid_constraint{i_subgrid in 0..2, j_subgrid in 0..2, k in DIGITS}:
    sum{a in 1..3, b in 1..3} x[i_subgrid*3+a, j_subgrid*3+b, k] = 1;
    
# Constraint to fix the cells
subject to fixed_constraint{i in ROWS, j in COLS, k in DIGITS: (i,j,k) in FIXED}:
    x[i, j, k] = 1;