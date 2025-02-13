DROP INDEX idx_posts_barcode;
DROP INDEX idx_posts_product;
alter table Client_Lines drop clustering;
DROP INDEX idx_client_lines_01;


-- 1st querie
CREATE INDEX idx_posts_barcode ON posts (barcode);
-- Hint 1
SELECT /*+ INDEX(posts idx_posts_barcode) */ * FROM Posts WHERE barcode = 'OII04455O419282';


-- 2nd querie
CREATE INDEX idx_posts_product ON posts (product);
-- Hint 2
SELECT /*+ INDEX(Posts idx_posts_product) */ * FROM Posts WHERE product = 'Compromiso';


-- 3rd querie
-- CREATE INDEX idx_posts_score ON posts (score); 
-- ISN'T OPTIMAL 


-- 4th querie
-- WE USE A HINT
SELECT /*+ FULL(posts) PARALLEL(posts, 2) */ * from posts;


-- 5th querie
-- CREATE CLUSTER
ALTER TABLE Client_Lines add clustering by linear order (username); 
ALTER TABLE Client_Lines move online; 
-- CREATE INDEX FOR SUCH CLUSTER
CREATE INDEX idx_client_lines_01 ON client_lines (username);

-- CHECK
set autotrace off
column table_name format a30
column clustering format a10

select table_name,
       clustering
from   user_tables
where table_name='CLIENT_LINES'
order by table_name;

select index_name,column_name,column_position from all_ind_columns where table_name='CLIENT_LINES' order by index_name,column_position;
