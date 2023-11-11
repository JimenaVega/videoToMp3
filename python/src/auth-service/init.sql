CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin'; -- usuario que puede modificar la DB
CREATE DATABASE auth;

GRANT ALL PRIVILEGIES ON auth.* TO 'admin'@'localhost';

USE auth;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES  ('jimena.vega.cuevas@gmail.com', 'admin');  -- usuario que puede pegarle a la API

-- mysql -uroot -e "DROP DATABASE auth;"
-- mysql -uroot -e "DROP USER auth_user@localhost;"
-- describe user; -- para ver los atributos
--  ALTER TABLE user MODIFY email VARCHAR(255) NOT NULL UNIQUE; -- modificar atributos de la tabla
