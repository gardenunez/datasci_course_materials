select A.docid, B.docid, sum(A.count * B.count)
FROM frequency A, frequency B
WHERE A.term = B.term AND A.docid < B.docid
GROUP BY A.docid, B.docid;
