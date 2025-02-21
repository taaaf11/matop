"""
Function for finding determinant of matrix.
"""

from matop.matrix import Matrix
from matop.row import Row

from copy import deepcopy
from typing import cast


def calculate_cofactor_sign(row_pos: int, col_pos: int) -> int:
    return (-1) ** (row_pos + col_pos)


def next_minor(col_pos: int, matrix: Matrix, row_pos: int = 1) -> int | float:
    element: int | float = matrix.columns[col_pos - 1][row_pos - 1]
    sign = calculate_cofactor_sign(row_pos, col_pos)
    return sign * element
    

def next_submatrix(col_pos: int, matrix: Matrix, row_pos: int = 1) -> Matrix:
    row_to_del = row_pos - 1
    col_to_del = col_pos - 1
    
    alter_matrix = deepcopy(matrix)
    
    del alter_matrix.rows[row_to_del]

    for row in alter_matrix.rows:
        del row[col_to_del]   

    return alter_matrix


def determinant(matrix: Matrix) -> float | None:
    if matrix.order.rows != matrix.order.columns:
        return
    
    det = 0
    
    if matrix.order.rows == 2 == matrix.order.columns:
        a = matrix.columns[0][0]
        d = matrix.columns[1][1]

        b = matrix.columns[1][0]
        c = matrix.columns[0][1]
        
        det += a * d - b * c

        return det

    if matrix.order.columns > 2:
        for col_index in range(1, len(matrix.columns) + 1):
            det += next_minor(col_index, matrix) * cast(float, determinant(next_submatrix(col_index, matrix)))
        
    return det


def get_cofactor_matrix(matrix: Matrix) -> Matrix:
    # i = 0
    # j = 0
    
    new_rows: list[Row] = []
    new_row_interim = []
    
    for i in range(1, len(matrix.rows) + 1):
        for j in range(1, len(matrix.columns) + 1):
            print(f"{i=} {j=}")
            value = calculate_cofactor_sign(i, j) * cast(float, determinant(next_submatrix(j, matrix, i)))
            print(f"{value=}")
            new_row_interim.append(
                calculate_cofactor_sign(i, j) * cast(float, determinant(next_submatrix(j, matrix, i)))
            )
            print()

        new_rows.append(Row(*new_row_interim))
        new_row_interim.clear()
    
    return Matrix(*new_rows)


# def inverse()
