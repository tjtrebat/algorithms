__author__ = 'Tom'

from Tkinter import *
from matrix_chain_multiply import Matrix

class MatrixCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Calculator")
        self.root.resizable(0, 0)
        self.frame = Frame(self.root)
        self.left_frame = Frame(self.frame, padx=15, pady=15)
        self.right_frame = Frame(self.frame, padx=15, pady=15)
        self.product_frame = Frame(self.frame, padx=15, pady=15)
        self.bottom_frame = Frame(self.root)
        self.txt_matrix = Text(self.left_frame, width=40, height=20)
        self.txt_matrix1 = Text(self.right_frame, width=40, height=20)
        self.txt_matrix2 = Text(self.product_frame, state=DISABLED, width=40, height=20)
        self.btn_calc = Button(self.bottom_frame, command=self.calculate_product, text="Calculate")
        self.add_frames()

    def add_frames(self):
        Label(self.left_frame, text="Matrix 1").pack()
        Label(self.right_frame, text="Matrix 2").pack()
        Label(self.product_frame, text="Product Matrix").pack()
        self.txt_matrix.pack()
        self.txt_matrix1.pack()
        self.txt_matrix2.pack()
        self.btn_calc.pack()
        self.left_frame.grid(row=0, column=0)
        Label(self.frame, text="X").grid(row=0, column=1)
        self.right_frame.grid(row=0, column=2)
        Label(self.frame, text="=").grid(row=0, column=3)
        self.product_frame.grid(row=0, column=4)
        self.bottom_frame.pack(side=BOTTOM)
        self.frame.pack()

    def calculate_product(self):
        matrix = Matrix.read_matrix(self.txt_matrix.get(1.0, END))
        matrix1 = Matrix.read_matrix(self.txt_matrix1.get(1.0, END))
        product = matrix * matrix1
        self.txt_matrix2.configure(state=NORMAL)
        self.txt_matrix2.delete(1.0, END)
        self.txt_matrix2.insert(END, product.write_matrix())
        self.txt_matrix2.configure(state=DISABLED)

if __name__ == "__main__":
    root = Tk()
    mc = MatrixCalculator(root)
    root.mainloop()
