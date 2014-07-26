import MapReduce
import sys

"""
Asymmetric friendships in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    person = record[0]
    friend = record[1]
    mr.emit_intermediate((person, friend), 1)
    mr.emit_intermediate((friend, person), 1)

def reducer(key, list_of_values):
    if len(list_of_values) == 1:   
        mr.emit((key[0], key[1]))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
