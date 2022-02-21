INIT_INSERT = '''
    INSERT INTO products_source_data(id, category_id, brand_id, title, description)
    SELECT generate_series(1, 1000100)    AS id,
           floor(random() * 2 + 1)      category_id,
           floor(random() * 100 + 1) as brand_id,
           md5(random()::text)       AS title,
           md5(random()::text)       AS description;

    '''

INSERT_WO_SHARDING = 'INSERT INTO products_without_sharding SELECT * FROM products_source_data WHERE id <= 1000000;'
INSERT_WITH_SHARDING = 'INSERT INTO products SELECT * FROM products_source_data WHERE id <= 1000000;'

INSERT_WO_SHARDING_100 = 'INSERT INTO products_without_sharding SELECT * FROM products_source_data WHERE id > 1000000;'
INSERT_WITH_SHARDING_100 = 'INSERT INTO products SELECT * FROM products_source_data WHERE id > 1000000;'

