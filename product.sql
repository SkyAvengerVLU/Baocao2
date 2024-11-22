CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    product_price NUMERIC(10, 2) NOT NULL,
    category_id INT NOT NULL
);
