CREATE DATABASE snaver;

CREATE TABLE IF NOT EXISTS account (
    id INT AUTO_INCREMENT,
    acc_name VARCHAR (127) NOT NULL,
    income DECIMAL(38,2),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS transfers (
    id INT AUTO_INCREMENT,
    tr_name VARCHAR (127) NOT NULL,
    transfers DECIMAL(38,2),
    spendings DECIMAL(38,2),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT,
    cat_name VARCHAR (127) NOT NULL,
    spendings_by_category DECIMAL(38,2),
    budget_by_category DECIMAL(38,2),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS budget (
    id INT AUTO_INCREMENT,
    budget_name VARCHAR (127) NOT NULL,
    amount DECIMAL(38,2),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS spending (
    id INT AUTO_INCREMENT,
    spending_name VARCHAR (127) NOT NULL,
    account_id INT,
    category_name VARCHAR (127) NOT NULL,
    PRIMARY KEY (id)
);