-- Creates users table with ENUM of countries

CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULLL UNIQUE,
	name VARCHAR(255),
	country ENUM("US", "CO", "TN") NOT NULL DEFAULT "US"
	);
