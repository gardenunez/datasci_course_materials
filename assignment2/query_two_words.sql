/*SELECT * FROM (
      ( SELECT * from frequency where term = 'transactions' ) as a
      INNER JOIN  
      ( SELECT * from frequency where term = 'world' ) as b on a.docid = b.docid 
)x;

*/

select count(*) 
from frequency q1
inner join frequency q2 on q1.docid = q2.docid
where q1.term = 'transactions' and q2.term = 'world';


