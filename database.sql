create database flask_product_db;

use flask_product_db;

create table users (
	id int not null primary key auto_increment,
    username varchar(200),
    password varchar(200)
);

create table products (
	id int not null primary key auto_increment,
	name varchar(200),
    price float, 
    description longtext,
    category varchar(200)
);