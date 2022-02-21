
-- cat simple-db.sql | docker exec -i highload-homework-19_postgresql-b_1 psql postgresql://postgres:postgres@postgresql-b:5432/postgres
-- type simple-db.sql | docker exec -i highload-homework-19_postgresql-b_1 psql postgresql://postgres:postgres@postgresql-b:5432/postgres

\c "host=postgresql-b port=5432 dbname=postgres password=postgres user=postgres"
DROP DATABASE IF EXISTS mybooks2;
CREATE DATABASE mybooks2;
\c "host=postgresql-b port=5432 dbname=mybooks2 password=postgres user=postgres"

-- Create table with constrain on a shard criteria
CREATE TABLE books (
	id bigint not null,
	category_id  int not null,
	author character varying not null,
	title character varying not null,
	year int not null );

\q
