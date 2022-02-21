
-- cat shard-magic.sql | docker exec -i highload-homework-19_postgresql-b_1 psql postgresql://postgres:postgres@postgresql-b:5432/postgres
-- type shard-magic.sql | docker exec -i highload-homework-19_postgresql-b_1 psql postgresql://postgres:postgres@postgresql-b:5432/postgres

\c "host=postgresql-b port=5432 dbname=postgres password=postgres user=postgres"
DROP DATABASE IF EXISTS mybooks;
CREATE DATABASE mybooks;
\c "host=postgresql-b port=5432 dbname=mybooks password=postgres user=postgres"



-- Create table with constrain on a shard criteria
CREATE TABLE books (
	id bigint not null,
	category_id  int not null,
	CONSTRAINT category_id_check CHECK ( category_id = 1 ),
	author character varying not null,
	title character varying not null,
	year int not null );

-- Create index on a shard criteria field
CREATE INDEX books_category_id_idx ON books USING btree(category_id);

-- Turn on EXTENSION called foreign data wrapper (fdw): 
CREATE EXTENSION postgres_fdw;
CREATE SERVER books_1_server 
FOREIGN DATA WRAPPER postgres_fdw 
OPTIONS( host 'postgresql-b', port '5432', dbname 'mybooks' );

CREATE USER MAPPING FOR CURRENT_USER 
SERVER books_1_server
OPTIONS (user 'postgres', password 'postgres');


-- Create foreign table on main server:
CREATE FOREIGN TABLE books_1 (
	id bigint not null,
	category_id  int not null,
	author character varying not null,
	title character varying not null,
	year int not null )
SERVER books_1_server
OPTIONS (schema_name 'public', table_name 'books');


-- Setup other shards

-- In the same way we set up other shards:
-- 1. Create table with constraint on shard server
-- 2. Add SERVER and MAPPING to main server
-- 3. Create foreign table on main server


-- postgresql-b1
	\c "host=postgresql-b1 port=5432 dbname=postgres password=postgres user=postgres"
    DROP DATABASE IF EXISTS mybooks;
	CREATE DATABASE mybooks;
	\c "host=postgresql-b1 port=5432 dbname=mybooks password=postgres user=postgres"

	-- Create table with constrain on a shard criteria
	CREATE TABLE books (
		id bigint not null,
		category_id int not null,
		CONSTRAINT category_id_check CHECK ( category_id = 2 ),
		author character varying not null,
		title character varying not null,
		year int not null );

	-- Create index on a shard criteria field
	CREATE INDEX books_category_id_idx ON books USING btree(category_id);

	-- Turn on EXTENSION called foreign data wrapper (fdw): 
--	CREATE EXTENSION postgres_fdw;
--	CREATE SERVER books_2_server 
--	FOREIGN DATA WRAPPER postgres_fdw 
--	OPTIONS( host 'postgresql-b1', port '5432', dbname 'mybooks' );
--
--	CREATE USER MAPPING FOR CURRENT_USER
--	SERVER books_2_server
--	OPTIONS (user 'postgres', password 'postgres');


\c "host=postgresql-b port=5432 dbname=mybooks password=postgres user=postgres"

CREATE SERVER books_2_server 
FOREIGN DATA WRAPPER postgres_fdw 
OPTIONS( host 'postgresql-b1', port '5432', dbname 'mybooks' );

CREATE USER MAPPING FOR CURRENT_USER
SERVER books_2_server
OPTIONS (user 'postgres', password 'postgres');

-- Create foreign table on main server:
CREATE FOREIGN TABLE books_2 (
	id bigint not null,
	category_id  int not null,
	author character varying not null,
	title character varying not null,
	year int not null )
SERVER books_2_server
OPTIONS (schema_name 'public', table_name 'books');


-- postgresql-b2
		\c "host=postgresql-b2 port=5432 dbname=postgres password=postgres user=postgres"
		DROP DATABASE IF EXISTS mybooks;
		CREATE DATABASE mybooks;
		\c "host=postgresql-b2 port=5432 dbname=mybooks password=postgres user=postgres"

		-- Create table with constrain on a shard criteria
		CREATE TABLE books (
			id bigint not null,
			category_id int not null,
			CONSTRAINT category_id_check CHECK ( category_id = 3 ),
			author character varying not null,
			title character varying not null,
			year int not null );

		-- Create index on a shard criteria field
		CREATE INDEX books_category_id_idx ON books USING btree(category_id);

		-- Turn on EXTENSION called foreign data wrapper (fdw): 
--		CREATE EXTENSION postgres_fdw;
--		CREATE SERVER books_3_server 
--		FOREIGN DATA WRAPPER postgres_fdw 
--		OPTIONS( host 'postgresql-b2', port '5432', dbname 'mybooks' );
--
--		CREATE USER MAPPING FOR CURRENT_USER
--		SERVER books_3_server
--		OPTIONS (user 'postgres', password 'postgres');


\c "host=postgresql-b port=5432 dbname=mybooks password=postgres user=postgres"

CREATE SERVER books_3_server 
FOREIGN DATA WRAPPER postgres_fdw 
OPTIONS( host 'postgresql-b2', port '5432', dbname 'mybooks' );

CREATE USER MAPPING FOR CURRENT_USER
SERVER books_3_server
OPTIONS (user 'postgres', password 'postgres');

-- Create foreign table on main server:
CREATE FOREIGN TABLE books_3 (
	id bigint not null,
	category_id  int not null,
	author character varying not null,
	title character varying not null,
	year int not null )
SERVER books_3_server
OPTIONS (schema_name 'public', table_name 'books');



-- create a view on the main server:
CREATE VIEW books_view AS
    SELECT * FROM books_1
        UNION ALL
    SELECT * FROM books_2
        UNION ALL
    SELECT * FROM books_3;


-- setup rules:
CREATE RULE books_insert AS ON INSERT TO books_view
DO INSTEAD NOTHING;
CREATE RULE books_update AS ON UPDATE TO books_view
DO INSTEAD NOTHING;
CREATE RULE books_delete AS ON DELETE TO books_view
DO INSTEAD NOTHING;


-- add rules with specific criteria
CREATE RULE books_insert_to_1 AS ON INSERT TO books_view
WHERE ( category_id = 1 )
DO INSTEAD INSERT INTO books_1 VALUES (NEW.*);

CREATE RULE books_insert_to_2 AS ON INSERT TO books_view
WHERE ( category_id = 2 )
DO INSTEAD INSERT INTO books_2 VALUES (NEW.*);

CREATE RULE books_insert_to_3 AS ON INSERT TO books_view
WHERE ( category_id = 3 )
DO INSTEAD INSERT INTO books_3 VALUES (NEW.*);

\q
