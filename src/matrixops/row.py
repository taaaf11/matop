from __future__ import annotations

from collections.abc import Callable, MutableSequence, Iterator, Sequence

from matrixops.exceptions import ZeroScalarMultiplication


class Row:
    def __init__(self, *nums: int | float) -> None:
        self.__nums: MutableSequence[int | float] = list(nums)
        
    @property
    def nums(self) -> MutableSequence[int | float]:
        return self.__nums
    
    def mul_by_col(self, column: Sequence[int | float]) -> int | float:
        product: int | float = 0
        
        for row_idx in range(len(self)):
            product += self.__nums[row_idx] * column[row_idx]
        
        return product
    
    def mul_by_scalar(self, scalar: int | float) -> None:
        if scalar == 0:
            raise ZeroScalarMultiplication("Cannot multiply by scalar 0.\n")
        if scalar == 1:
            return
        
        is_fractional_zero: Callable[[float | int], float] = lambda n: isinstance(n, float) and str(n).split(".")[1] == "0"

        if is_fractional_zero(scalar):
            scalar = int(scalar)

        for index in range(len(self.__nums)):
            product = round(self.__nums[index] * scalar, 1)

            if is_fractional_zero(product):
                product = int(product)

            self.__nums[index] = product
        
    def as_latex(self) -> str:
        return " & ".join(map(str, self.__nums))
    
    def __add__(self, other: Row) -> Row:
        new_row: MutableSequence[int | float] = []
        
        for (index, num) in enumerate(self.__nums):
            new_row.append(num + other.nums[index])
            
        return Row(*new_row)
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Row):
            return NotImplemented
        return self.__nums == value.nums
    
    def __len__(self) -> int:
        return len(self.__nums)
    
    def __iter__(self) -> Iterator[int | float]:
        for num in self.__nums:
            yield num
            
    # def __delitem__(self, index: int):
        # del self.__nums[index]
    
    def __repr__(self) -> str:
        return "Row(" + ", ".join(map(str, self.__nums)) + ")"

 
if __name__ == "__main__":
    row = Row(1,2,3)
    # print | float(row.as_latex())
    
    # iter toest
    # fr num in row:
    #     print | float(num)
    
    # print | float(f"{row * 2=}")
    # print | float(f"{row * 2 + Row(9, 10, 11)=}")
