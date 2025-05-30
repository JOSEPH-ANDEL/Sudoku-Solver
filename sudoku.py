import tkinter as tk
from amplpy import AMPL
import os

class SudokuUI:
    def __init__(self, root):
        self.root = root
        self.entries = [[] for _ in range(9)]
        self.create_grid()

        solve_btn = tk.Button(root, text="Solve", command=self.solve_sudoku)
        solve_btn.grid(row=10, column=0, columnspan=9, stick = 'nsew', pady=10)

        clear_button = tk.Button(self.root, text="Clear", command=self.clear_grid)
        clear_button.grid(row=20, column=0, columnspan=9, sticky='nsew', pady=10)

    #Create Grid UI
    def create_grid(self):
        for r in range(9):
            self.entries.append([])
            self.root.grid_rowconfigure(r, weight=1)
            for c in range(9):
                self.root.grid_columnconfigure(c, weight=1)

                # Determine border thicknesses
                top = .3
                left = .3
                bottom = 6 if (r + 2) % 3 == 1 and r < 8 else 1
                right = 6 if (c + 2) % 3 == 1 else 1

                # Surround each Entry with a Frame that controls the border
                cell_frame = tk.Frame(
                    self.root,
                    highlightbackground="black",
                    highlightcolor="black",
                    highlightthickness=0,
                    bd=0,
                    bg="black",  
                    padx=left,
                    pady=top
                )
                cell_frame.grid(row=r, column=c, sticky='nsew')

                e = tk.Entry(
                    cell_frame,
                    font=('Calibri', 20),
                    justify='center',
                    borderwidth=0,
                    highlightthickness=0,
                    relief='flat',
                    fg = 'red'
                )
                e.pack(fill='both', expand=True, padx=(0, right), pady=(0, bottom))
                self.entries[r].append(e)


    #Get data from the grid
    def get_data(self):
        data = []
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                if val.isdigit() and 1 <= int(val) <= 9:
                    data.append((i+1, j+1, int(val)))  
        return data

    #Write to the data file
    def write_dat_file(self, data, filename="sudoku.dat"):
        with open(filename, "w") as f:
            f.write("set FIXED :=\n")
            for row, col, val in data:
                f.write(f"  {row} {col} {val}\n")
            f.write(";\n")

    def solve_sudoku(self):
        given_data = self.get_data()
        self.write_dat_file(given_data)

        #Use AMPL Model
        ampl = AMPL()
        ampl.eval("option solver gurobi;")
        ampl.read("sudoku.mod")
        ampl.readData("sudoku.dat")
        ampl.solve()

        x = ampl.getVariable("x")  
        # Populate the grid with solution
        for i in range(1, 10):
            for j in range(1, 10):
                for k in range(1, 10):
                    if x[i, j, k].value() == 1:
                        if(self.entries[i-1][j-1].get() == ""):
                            self.entries[i-1][j-1].insert(0, str(k))
                            self.entries[i-1][j-1].config(fg='black')  
                        break
    #Clear the grid
    def clear_grid(self):
        for r in range(9):
            for c in range(9):
                self.entries[r][c].config(state='normal') 
                self.entries[r][c].delete(0, tk.END)      
                self.entries[r][c].config(fg='red')     


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sudoku Solver")
    app = SudokuUI(root)
    root.mainloop()
