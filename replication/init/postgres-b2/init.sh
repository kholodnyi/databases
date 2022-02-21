#!/bin/bash

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE TABLE products (
    id bigint not null,
    category_id int not null,
    CONSTRAINT category_id_check CHECK (category_id = 2),
    brand_id int not null,
    title character varying not null,
    description character varying not null
  );

  CREATE INDEX idx_id ON products(id);

  CREATE INDEX idx_category_id ON products(category_id);

  CREATE INDEX idx_brand_id ON products(brand_id);
EOSQL