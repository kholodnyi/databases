CREATE TABLE IF NOT EXISTS isolation_db.my_table (
    id INT,
    name VARCHAR(31),
    amount INT
);

INSERT INTO isolation_db.my_table (id, name, amount)
VALUES (1, 'Bob', 0);