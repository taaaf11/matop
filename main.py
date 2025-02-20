from matrix import Matrix, Row


mat = Matrix(
    Row(1, 2, 3),
    Row(7, 8, 9),
    Row(3, 5, 7),
)

# add row 2 to 1
# mat.add_rows(0, 1)

mat1 = Matrix(
    Row(1,2,3),
    Row(4,5,6),
)

mat2 = Matrix(
    Row(7, 8),
    Row(9, 10),
    Row(11, 12),
)

print(Matrix.dot_multiply(mat1, mat2))

# print(mat.as_latex(BracketsType.SQUARE))
# print(mat.columns)