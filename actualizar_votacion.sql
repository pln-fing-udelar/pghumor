DELETE FROM corpus.votos;
INSERT INTO corpus.votos SELECT * FROM chistesdb.audit_table;
