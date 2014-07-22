SELECT count(*) FROM (
      SELECT docid from frequency where term = 'parliament'
)x;

