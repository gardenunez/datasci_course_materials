import MapReduce
import sys

"""
Join example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

order_table = u'order'
line_item_table = u'line_item'

def mapper(record):
    """ Mapper of table records:
    table id, (table name , record)
    """
    table = record[0]
    table_id = record[1]
    mr.emit_intermediate(table_id, (table, record))

def reducer(key, list_of_values):
    """ Reduce function"""
    order = []
    items = []
    for v in list_of_values:
        if v[0] == order_table:
            order = v[1]
        elif v[0] == line_item_table:
            items.append(v[1])
    for line_item in items:
        mr.emit(order + line_item)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
