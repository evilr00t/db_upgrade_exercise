create database if not exists testdb;
CREATE USER 'karol'@'localhost' IDENTIFIED BY 'test123';
grant usage on *.* to karol@localhost identified by 'test123';
grant all privileges on testdb.* to karol@localhost;

use testdb;

create table if not exists users (
	id int auto_increment not null,
	login varchar(255),
	name varchar(255),
	password varchar(255),
	primary key (id)
);

create table if not exists migrations (
	id int auto_increment not null,
	version int,
	time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	primary key(id)
);

insert into migrations (version) values (0);
