from __future__ import annotations

from row import Row
from enum import Enum
from dataclasses import dataclass


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


class Matrix:
    def __init__(self, *rows: Row):
        self.__rows: list[Row] = []

        for row in rows:
            self._add_row(row)
        
    @property
    def order(self) -> MatrixOrder:
        return MatrixOrder(
            rows=len(self.__rows),
            columns=len(self.__rows[0])
        )
    
    @property
    def rows(self) -> list[Row]:
        return self.__rows
    
    @property
    def columns(self) -> list[list[int]]:
        columns: list[list[int]] = []
        
        for _ in range(self.order.columns):
            columns.append([])

        for row in self.__rows:
            row_elem_idx = 0
            
            for col_idx in range(self.order.columns):
                columns[col_idx].append(row.nums[row_elem_idx])
                row_elem_idx += 1
        
        return columns
    
    def _add_row(self, row: Row):
        """
        Don't confuse this with `add_rows`. This function
        "adds" a row to the matrix, increasing its number of rows.
        """

        if len(self.__rows) > 0 and len(row) != len(self.__rows[0]):
            raise Exception("Inconsistent number of columns.")
        
        self.__rows.append(row)
            
    def add_rows(self, row1_idx: int, row2_idx: int):
        """
        Don't confuse this with `_add_row`. This function
        adds two rows present in the current matrix
        """

        self.__rows[row1_idx] += self.__rows[row2_idx]
        
    def interchange_rows(self, row1_idx: int, row2_idx: int):
        temp = self.__rows[row1_idx]
        self.__rows[row1_idx] = self.__rows[row2_idx]
        self.__rows[row2_idx] = temp
    
    def scalar_multiply(self, scalar: int):
        for row in self.__rows:
            row.mul_by_scalar(scalar)
    
    @classmethod
    def dot_multiply(cls, first: Matrix, second: Matrix) -> Matrix:
        new_mat_rows: list[Row] = []
        
        for row in first.rows:
            formed_row: list[int] = []
            
            for column in second.columns:
                formed_row.append(row.mul_by_col(column))
            
            new_mat_rows.append(Row(*formed_row))
        
        return cls(*new_mat_rows)
        
    def as_latex(self, brackets: BracketsType) -> str:
        latex = f"\\begin{{{brackets.value}matrix}}\n"
        rows_latex: list[str] = []
        
        for row in self.__rows:
            rows_latex.append(row.as_latex())
        
        # add double slash ("\\") at the end of each latex row
        latex += "\\\\\n".join(rows_latex)
        
        latex += f"\n\\end{{{brackets.value}matrix}}"
        
        return latex
        
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

    print(mat.as_latex(BracketsType.SQUARE))