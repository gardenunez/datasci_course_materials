SELECT count(*) FROM (
      SELECT docid, sum(frequency.count) as count_term 
      from frequency
      group by docid
      having count_term > 300
       
) x
;
