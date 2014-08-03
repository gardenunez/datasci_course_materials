import MapReduce
import sys

"""
Matrix multiplication example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

A_MATRIX = 'a'
B_MATRIX = 'b'
A_ROWS = 5 # number of rows in matrix A
B_COLS = 5 #  number of columns in matrix B

def mapper(record):
    """Matrix Multiplication Mapper.
    For each element mij of M, produce a key-value pair
    ((i, k), (M, j,mij )) for k = 1, 2,..., up to the number of columns of N. 
    Also, for each element njk of N, 
    produce a key-value pair ((i, k), (N, j, njk))for
    i = 1, 2, . . ., up to the number of rows of M. """
    matrix, row, col, value = record
    if matrix == A_MATRIX:
        # For all A(i,j) emit key (j, k) for k=1 to number of columns in B
        for k in range(0, B_COLS):
            mr.emit_intermediate((row, k), [matrix, col, value])
    else:
        # For all B(j, k) emit key (j, i) for i=1 to number of rows in B
        for i in range(0, A_ROWS):
            mr.emit_intermediate((i, col), [matrix, row, value])

def reducer(key, list_of_values):
    """Matrix Multiplication Reducer.
    Each key (i, k) will have an associated list with all
    the values (M, j,mij ) and (N, j, njk), for all possible values of j. 
    The Reduce function needs to connect the two values 
    on the list that have the same value of j, for each j."""
    a_values = filter(lambda cell: cell[0] == A_MATRIX, list_of_values)
    b_values = filter(lambda cell: cell[0] == B_MATRIX, list_of_values)

    # Generate sets and take the intersection of indeces from
    # row vectors (A) and column vectors (B).
    a_set = set(map(lambda s: s[1], a_values))
    b_set = set(map(lambda s: s[1], b_values))
    a_b_set = a_set & b_set

    # Filter matching values
    b_rows = filter(lambda row: row[1] in a_b_set, b_values)
    a_cols = filter(lambda row: row[1] in a_b_set, a_values)
    
    # Multiply the a_value * b_values
    mult = map(lambda x: x[0][2] * x[1][2], zip(b_rows, a_cols))
 
    # Sum the results
    mr.emit((key[0], key[1], sum(mult)))


# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
