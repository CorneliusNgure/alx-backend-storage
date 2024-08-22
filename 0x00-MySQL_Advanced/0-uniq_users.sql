--check if the table exits and create one if it donesn't

CREATE TABLE IF NOT EXISTS user (
	id INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(80) NOT NULL UNIQUE,
	name VARCHAR(50),
	PRIMARY KEY (id)
);
