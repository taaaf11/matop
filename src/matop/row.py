from __future__ import annotations

from collections.abc import Iterator


class Row:
    def __init__(self, *nums: int) -> None:
        self.__nums: list[int] = list(nums)
        
    @property
    def nums(self) -> list[int]:
        return self.__nums
    
    def mul_by_col(self, column: list[int]) -> int:
        product: int = 0
        
        for row_idx in range(len(self)):
            product += self.__nums[row_idx] * column[row_idx]
        
        return product
    
    def mul_by_scalar(self, scalar: int) -> None:
        for index in range(len(self.__nums)):
            self.__nums[index] *= scalar
        
    def as_latex(self) -> str:
        return " & ".join(map(str, self.__nums))
    
    def __add__(self, other: Row) -> Row:
        new_row: list[int] = []
        
        for (index, num) in enumerate(self.__nums):
            new_row.append(num + other.nums[index])
            
        return Row(*new_row)
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Row):
            return NotImplemented
        return self.__nums == value.nums
    
    def __len__(self) -> int:
        return len(self.__nums)
    
    def __iter__(self) -> Iterator[int]:
        for num in self.__nums:
            yield num
    
    def __repr__(self) -> str:
        return "Row(" + ", ".join(map(str, self.__nums)) + ")"

 
if __name__ == "__main__":
    row = Row(1,2,3)
    print(row.as_latex())
    
    # iter toest
    # fr num in row:
    #     print(num)
    
    # print(f"{row * 2=}")
    # print(f"{row * 2 + Row(9, 10, 11)=}")
