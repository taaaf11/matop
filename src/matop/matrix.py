from __future__ import annotations

from .row import Row
from enum import Enum
from dataclasses import dataclass

from collections.abc import MutableSequence, Sequence


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
    def __init__(self, op: str, i = None, j = None, k = None) -> None:
        match op:
            case "ADD_ROWS":
                self.message = fr"R_{i} + {k}R_{j} \rightarrow R_{i}"
            case "INTERCHANGE":
                self.message = fr"R_{i} \leftrightarrow R_{j}"
            case "SCALAR_MULTIPLY":
                self.message = fr"{k}R_{i} \rightarrow R_{i}"
            case _:
                self.message = "Unsupported."


class Matrix:
    def __init__(self, *rows: Row) -> None:
        self.__rows: MutableSequence[Row] = []
        self.brackets_type: BracketsType = BracketsType.SQUARE
        self.print_notation = False
        self.auto_print = False

        for row in rows:
            self._add_row(row)
        
    @property
    def order(self) -> MatrixOrder:
        return MatrixOrder(
            rows=len(self.__rows),
            columns=len(self.__rows[0])
        )
    
    @property
    def rows(self) -> Sequence[Row]:
        return self.__rows
    
    @property
    def columns(self) -> Sequence[Sequence[int | float]]:
        columns: Sequence[list[int | float]] = []
        
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
            raise Exception("Inconsistent number of columns.")
        
        self.__rows.append(row)
            
    def add_rows(self, row1_idx: int, row2_idx: int) -> None:
        """
        Don't confuse this with `_add_row`. This function
        adds two rows present in the current matrix
        """

        self.__rows[row1_idx] += self.__rows[row2_idx]
        
        if self.auto_print:
            print(self.as_latex(MatrixOperation("ADD_ROWS", i=row1_idx + 1, j=row2_idx + 1, k=1)))
        
    def interchange_rows(self, row1_idx: int, row2_idx: int) -> None:
        temp = self.__rows[row1_idx]
        self.__rows[row1_idx] = self.__rows[row2_idx]
        self.__rows[row2_idx] = temp

        if self.auto_print:
            print(self.as_latex(MatrixOperation("INTERCHANGE", i=row1_idx + 1, j=row2_idx + 1)))
    
    def scalar_multiply(self, scalar: int) -> None:
        for row in self.__rows:
            row.mul_by_scalar(scalar)
    
    def scalar_multiply_row(self, row_idx: int, scalar: int) -> None:
        self.__rows[row_idx].mul_by_scalar(scalar)
        
        if self.auto_print:
            print(self.as_latex(MatrixOperation("SCALAR_MULTIPLY", i=row_idx + 1, k=scalar)))
        
    @classmethod
    def dot_multiply(cls, first: Matrix, second: Matrix) -> Matrix:
        new_mat_rows: MutableSequence[Row] = []
        
        for row in first.rows:
            formed_row: MutableSequence[int | float] = []
            
            for column in second.columns:
                formed_row.append(row.mul_by_col(column))
            
            new_mat_rows.append(Row(*formed_row))
        
        return cls(*new_mat_rows)
        
    def as_latex(self, operation: MatrixOperation | None = None) -> str:
        latex = ""
        
        if self.print_notation and operation is not None:
            latex += operation.message + "\n"

        latex += f"\\begin{{{self.brackets_type.value}matrix}}\n"
        rows_latex: list[str] = []
        
        for row in self.__rows:
            rows_latex.append(row.as_latex())
        
        # add double slash ("\\") at the end of each latex row
        latex += "\\\\\n".join(rows_latex)
        
        latex += f"\n\\end{{{self.brackets_type.value}matrix}}"
        
        return latex
    
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

    # print(mat.as_latex(BracketsType.SQUARE))