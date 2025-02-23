from __future__ import annotations

from collections.abc import MutableSequence, Sequence
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import Any, cast

from matop.row import Row
from matop.exceptions import InconsistentOrder

try:
    get_ipython  # check if imported into ipython is running
except NameError:
    Math = None
    display = None
else:
    from IPython.core.display import Math, display


class BracketsType(Enum):
    PLAIN = ""
    ROUND = "p"
    SQUARE = "b"
    CURLY = "B"
    PIPES = "v"
    DOUBLE_PIPES = "V"
    

@dataclass
class MatrixOrder:
    rows: int
    columns: int
    
    
class MatrixOperation:
    ADD_ROWS = "ADD_ROWS"
    INTERCHANGE = "INTERCHANGE"
    SCALAR_MULTIPLY = "SCALAR_MULTIPLY"
    TRANSPOSE = "TRANSPOSE"
    
    def __init__(self, op: str, i: float | None = None, j: float | None = None, k: float | None = None) -> None:
        match op:
            case MatrixOperation.ADD_ROWS:
                if k != 1:
                    self.message = fr"R_{i} + {k}R_{j} \rightarrow R_{i}"
                else:
                    self.message = fr"R_{i} + R_{j} \rightarrow R_{i}"
            case MatrixOperation.INTERCHANGE:
                self.message = fr"R_{i} \leftrightarrow R_{j}"
            case MatrixOperation.SCALAR_MULTIPLY:
                self.message = fr"{k}R_{i} \rightarrow R_{i}"
            case "DOT_MULTIPLY":
                ...
            case MatrixOperation.TRANSPOSE:
                self.message = ""
                ...
            case _:
                self.message = "Unsupported."


class Matrix:
    def __init__(self, *rows: Row) -> None:
        self.__rows: MutableSequence[Row] = []
        self.brackets_type: BracketsType = BracketsType.SQUARE
        self.print_notation = True
        self.auto_print = Math is not None  # of course this can be changed
        
        self.__last_operation: MatrixOperation | None = None

        for row in rows:
            self._add_row(row)
        
        # These two variables:
        # self.__last_rows_state
        # self.__last_operation_state
        #
        # store the state
        # of the matrix before the latest mutating
        # operation, such as add_rows, interchange_rows
        # etc.
        #
        # These values are used by self.undo() function
        # to undo the last action taken
        #
        # It is like the previous operation than
        # self.__last_operation
        self.__last_rows_state: MutableSequence[Row] = self.__rows    
        self.__last_operation_state: MatrixOperation | None = None
        
    def __getattribute__(self, name: str) -> Any:
        # instance methods that mutate the state of the matrix
        if name in "add_rows interchange_rows scalar_multiply_row dot_multiply transposify".split():
            self.__last_rows_state = self.__rows
            self.__last_operation_state = self.__last_operation

        return object.__getattribute__(self, name)
        
    @property
    def order(self) -> MatrixOrder:
        return MatrixOrder(
            rows=len(self.__rows),
            columns=len(self.__rows[0])
        )
        
    @property
    def transpose(self) -> Matrix:
        new_rows: MutableSequence[Row] = []
        
        for column in self.columns:
            new_rows.append(Row(*column))
            
        return Matrix(*new_rows)
    
    @property
    def inverse(self) -> Matrix | None:
        if not self.is_square:
            return None

        determinant: float = cast(float, Matrix.calculate_determinant(self))

        if determinant == 0:
            return None

        adjoint: Matrix = cast(Matrix, Matrix.get_cofactor_matrix(self)).transpose
        adjoint.scalar_multiply(1 / determinant)
        return adjoint
    
    def get_cofactor_matrix(self) -> Matrix | None:
        if self.order.rows != self.order.columns:
            return None
        
        new_rows: list[Row] = []
        new_row_interim: MutableSequence[float] = []
        
        for row_index in range(1, len(self.rows) + 1):
            for column_index in range(1, len(self.columns) + 1):
                new_row_interim.append(
                    Matrix.calculate_cofactor_sign(row_index, column_index) * cast(float, Matrix.calculate_determinant(Matrix.next_submatrix(row_index, column_index, self)))
                )

            new_rows.append(Row(*new_row_interim))
            new_row_interim.clear()
            
        new_matrix = Matrix(*new_rows)

        if self.auto_print:
            new_matrix._print_latex()
        
        return new_matrix
    
    @property
    def rows(self) -> Sequence[Row]:
        return self.__rows
    
    @rows.setter
    def rows(self, value: Sequence[Row]):
        self.__rows.clear()

        for row in value:
            self._add_row(row)
    
    @property
    def columns(self) -> Sequence[Sequence[int | float]]:
        columns: list[list[int | float]] = []
        
        for _ in range(self.order.columns):
            columns.append([])

        for row in self.__rows:
            row_elem_idx = 0
            
            for col_idx in range(self.order.columns):
                columns[col_idx].append(row.nums[row_elem_idx])
                row_elem_idx += 1
        
        return columns
    
    def _add_row(self, row: Row) -> None:
        """
        Don't confuse this with `add_rows`. This function
        "adds" a row to the matrix, increasing its number of rows.
        """

        if len(self.__rows) > 0 and len(row) != len(self.__rows[0]):
            raise InconsistentOrder("Inconsistent number of columns.")
        
        self.__rows.append(row)
            
    def add_rows(self, row1_idx: int, row2_idx: int, scalar: float = 1) -> None:
        """
        Don't confuse this with `_add_row`. This function
        adds two rows present in the current matrix
        """
        
        # for indices
        row1_idx -= 1
        row2_idx -= 1
        
        self.__rows[row2_idx].mul_by_scalar(scalar)
        self.__rows[row1_idx] += self.__rows[row2_idx]
        # reverse the process of multiplication after addition
        self.__rows[row2_idx].mul_by_scalar(1 / scalar)
        
        # for displaying
        row1_idx += 1
        row2_idx += 1
        
        self.__last_operation = MatrixOperation(MatrixOperation.ADD_ROWS, i=row1_idx, j=row2_idx, k=1)
        
        if self.auto_print:
            self._print_latex()
        
    def interchange_rows(self, row1_idx: int, row2_idx: int) -> None:
        # for indices
        row1_idx -= 1
        row2_idx -= 1
        
        temp = self.__rows[row1_idx]
        self.__rows[row1_idx] = self.__rows[row2_idx]
        self.__rows[row2_idx] = temp
        
        # for display
        row1_idx += 1
        row2_idx += 1
        
        self.__last_operation = MatrixOperation(MatrixOperation.INTERCHANGE, i=row1_idx, j=row2_idx)

        if self.auto_print:
            self._print_latex()
    
    def scalar_multiply(self, scalar: float) -> None:
        for row in self.__rows:
            row.mul_by_scalar(scalar)
    
    def scalar_multiply_row(self, row_idx: int, scalar: float) -> None:
        self.__rows[row_idx - 1].mul_by_scalar(scalar)

        self.__last_operation = MatrixOperation(MatrixOperation.SCALAR_MULTIPLY, i=row_idx, k=scalar)

        if self.auto_print:
            self._print_latex()
        
    def dot_multiply(self, other: Matrix) -> None:
        if self.order.columns != other.order.rows:
            raise InconsistentOrder("Inconsistent order for dot multiplication.")

        new_mat_rows: MutableSequence[Row] = []
        
        for row in self.rows:
            formed_row: MutableSequence[int | float] = []
            
            for column in other.columns:
                formed_row.append(row.mul_by_col(column))
            
            new_mat_rows.append(Row(*formed_row))
            
        self.__rows = new_mat_rows
        
        if self.auto_print:
            self._print_latex()
    
    @staticmethod
    def calculate_cofactor_sign(row_pos: int, col_pos: int) -> int:
        return (-1) ** (row_pos + col_pos)
    
    @staticmethod
    def next_submatrix(row_pos: int, col_pos: int, matrix: Matrix) -> Matrix:
        row_to_del = row_pos - 1
        col_to_del = col_pos - 1
        
        new_rows = cast(MutableSequence[MutableSequence[int | float]], [row.nums for row in deepcopy(matrix).rows])
        
        del new_rows[row_to_del]
        for row in new_rows:
            del row[col_to_del]

        return Matrix(*[Row(*row) for row in new_rows])
    
    @staticmethod
    def calculate_determinant(matrix: Matrix) -> float | None:
        if matrix.order.rows != matrix.order.columns:
            return None
        
        det: float = 0
        
        if matrix.order.rows == 2 == matrix.order.columns:
            a = matrix.columns[0][0]
            d = matrix.columns[1][1]

            b = matrix.columns[1][0]
            c = matrix.columns[0][1]
            
            det += a * d - b * c

            return det

        row_index = 1
        if matrix.order.columns > 2:
            for col_index in range(1, len(matrix.columns) + 1):
                det += Matrix.calculate_cofactor_sign(row_index, col_index) * matrix.columns[col_index - 1][row_index - 1] * cast(float, Matrix.calculate_determinant(Matrix.next_submatrix(row_index, col_index, matrix)))
            
        return det
     
    def transposify(self) -> None:
        self.rows = self.transpose.rows

        self.__last_operation = MatrixOperation(MatrixOperation.TRANSPOSE)

        if self.auto_print:
            self._print_latex()
            
    def inversify(self) -> None:
        if not self.is_square:
            raise InconsistentOrder("Inverse is not possible for non-square matrices.")
        
        if (inverse := self.inverse) is None:
            return
        
        self.rows = cast(Matrix, self.inverse).rows
        
    def as_latex(self) -> str:
        latex = ""
        operation = self.__last_operation
        
        if self.print_notation and operation is not None:
            latex += operation.message + "\n"

        latex += f"\\begin{{{self.brackets_type.value}matrix}}\n"
        rows_latex: list[str] = []
        
        for row in self.__rows:
            rows_latex.append(row.as_latex())
        
        # add double slash ("\\") at the end of each latex row
        # how it would appear: ...\\<newline>
        latex += "\\\\\n".join(rows_latex)
        
        latex += f"\n\\end{{{self.brackets_type.value}matrix}}"
        
        return latex
    
    def _print_latex(self) -> None:
        latex = self.as_latex()
        if Math is not None:
            display(Math(latex))
        else:
            print(latex)
            
    def undo(self):
        self.__rows = self.__last_rows_state
        self.__last_operation = self.__last_operation_state
        
        if self.auto_print:
            self._print_latex()
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return self.__rows == other.rows
        
    def __repr__(self) -> str:
        r = "Matrix(\n"
        for row in self.__rows:
            r += "  " + str(row) + "\n"
        r += ")"
        return r


if __name__ == "__main__":
    mat = Matrix(
        Row(1,2),
        Row(3,9)
    )
