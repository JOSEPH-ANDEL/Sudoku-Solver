import tkinter as tk
from amplpy import AMPL
import os

class SudokuUI:
    def __init__(self, root):
        self.root = root
        self.entries = []
        self.create_grid()

        solve_btn = tk.Button(root, text="Solve", command=self.solve_sudoku)
        solve_btn.grid(row=10, column=0, columnspan=9, pady=10)

    def create_grid(self):
        for r in range(9):
            row_entries = []
            for c in range(9):
                e = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                e.grid(row=r, column=c, padx=2, pady=2)
                row_entries.append(e)
            self.entries.append(row_entries)

    def get_data(self):
        data = []
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                if val.isdigit() and 1 <= int(val) <= 9:
                    data.append((i+1, j+1, int(val)))  # 1-indexed
        return data

    def write_dat_file(self, data, filename="sudoku.dat"):
        with open(filename, "w") as f:
            f.write("set FIXED :=\n")
            for row, col, val in data:
                f.write(f"  {row} {col} {val}\n")
            f.write(";\n")

    def solve_sudoku(self):
        given_data = self.get_data()
        self.write_dat_file(given_data)

        ampl = AMPL()
        ampl.eval("option solver gurobi;")
        ampl.read("sudoku.mod")  # your AMPL model
        ampl.readData("sudoku.dat")
        ampl.solve()

        x = ampl.getVariable("x")  # x[i,j,k] = 1 if cell (i,j) is value k
        # Populate the grid with solution
        for i in range(1, 10):
            for j in range(1, 10):
                for k in range(1, 10):
                    if x[i, j, k].value() == 1:
                        self.entries[i-1][j-1].delete(0, tk.END)
                        self.entries[i-1][j-1].insert(0, str(k))
                        break

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sudoku Solver")
    app = SudokuUI(root)
    root.mainloop()
