-- PostgreSQL用サンプルテーブル作成SQL
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

INSERT INTO items (name) VALUES ('item1'), ('item2');
