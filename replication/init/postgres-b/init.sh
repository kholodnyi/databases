#!/bin/bash

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE EXTENSION postgres_fdw;

  /* configure shard 1 */
  CREATE SERVER products_server_1
  FOREIGN DATA WRAPPER postgres_fdw
  OPTIONS(host 'postgres-b1', port '5432', dbname 'mydb');

  CREATE USER MAPPING FOR user
  SERVER products_server_1
  OPTIONS (user 'user', password 'password');

  CREATE FOREIGN TABLE products_1 (
    id bigint not null,
    category_id int not null,
    brand_id int not null,
    title character varying not null,
    description character varying not null
  ) SERVER products_server_1
    OPTIONS (schema_name 'public', table_name 'products');

  /* configure shard 2 */
  CREATE SERVER products_server_2
  FOREIGN DATA WRAPPER postgres_fdw
  OPTIONS(host 'postgres-b2', port '5432', dbname 'mydb');

  CREATE USER MAPPING FOR user
  SERVER products_server_2
  OPTIONS (user 'user', password 'password');

  CREATE FOREIGN TABLE products_2 (
    id bigint not null,
    category_id int not null,
    brand_id int not null,
    title character varying not null,
    description character varying not null
  ) SERVER products_server_2
    OPTIONS (schema_name 'public', table_name 'products');

  /* configure a view */
  CREATE VIEW products AS
    SELECT * FROM products_1
    UNION
    SELECT * FROM products_2;

  CREATE RULE products_insert AS ON INSERT TO products DO INSTEAD NOTHING;
  CREATE RULE products_update AS ON UPDATE TO products DO INSTEAD NOTHING;
  CREATE RULE products_delete AS ON DELETE TO products DO INSTEAD NOTHING;
  CREATE RULE products_insert_to_1 AS ON INSERT TO products WHERE new.category_id = 1 DO INSTEAD INSERT INTO products_1 VALUES (NEW.*);
  CREATE RULE products_insert_to_2 AS ON INSERT TO products WHERE new.category_id = 2 DO INSTEAD INSERT INTO products_2 VALUES (NEW.*);

  /* create table for source data */
  CREATE TABLE products_source_data (
    id bigint not null,
    category_id int not null,
    brand_id int not null,
    title character varying not null,
    description character varying not null
  );

  CREATE INDEX idx_products_source_data_id ON products_source_data(id);

  /* create table without sharding */
  CREATE TABLE products_without_sharding (
    id bigint not null,
    category_id int not null,
    brand_id int not null,
    title character varying not null,
    description character varying not null
  );

  CREATE INDEX idx_products_without_sharding_id ON products_without_sharding(id);

  CREATE INDEX idx_products_without_sharding_category_id ON products_without_sharding(category_id);

  CREATE INDEX idx_products_without_sharding_brand_id ON products_without_sharding(brand_id);
EOSQL