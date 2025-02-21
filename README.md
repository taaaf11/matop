# matop
A package for doing matrix operations easily.


## IPython kernel friendly
When running in ipython kernel (jupyter lab or google colab), the functions automatically display the applied operation and the resultant matrix.


## How to use
1. Import required objects
```python
from matop.row import Row
from matop.matrix import Matrix, MatrixOperation
```
2. Creating `Matrix` object
```python
mat1 = Matrix(
    Row(1, 2, 3),
    Row(4, 5, 6),
    Row(7, 8, 9)
)
```
3. Perform required operations such as:
```python
# for interchanging rows
# interchanges rows 0 and 1 (rows are zero-indexed)
mat1.interchange_rows(0, 1)

# for addition of rows
# adds row 1 to row 0
mat1.add_rows(0, 1)

# adds row 1 to row 0 after multiplying with scalar 2
mat1.add_rows(0, 1, 2)
```

More operations are demonstrated in [this google colab notebook](https://colab.research.google.com/drive/1NuTzW1Ogtwq4X8HT-3cjqe_VEIAP8gfa?usp=sharing).