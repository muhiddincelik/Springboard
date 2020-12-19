CREATE TABLE Region (
  id INT,
  region_name VARCHAR(30),
  PRIMARY KEY (id)
);

CREATE TABLE Category (
  id INT,
  category_name VARCHAR(20),
  description VARCHAR(300),
  PRIMARY KEY (id)
);

CREATE TABLE Users (
  id INT,
  full_name VARCHAR(50),
  email VARCHAR(40),
  pref_region INT,
  PRIMARY KEY (id),
  FOREIGN KEY (pref_region)
	REFERENCES Region(id)
);

CREATE TABLE Post (
  id INT,
  title VARCHAR(30),
  post_text VARCHAR(300),
  user_id INT,
  location VARCHAR(20),
  region_id INT,
  category_id INT,
  created_at DATETIME,
  PRIMARY KEY (id),
  FOREIGN KEY (region_id)
	REFERENCES Region(id),
  FOREIGN KEY (user_id)
	REFERENCES Users(id),
  FOREIGN KEY (category_id)
	REFERENCES Category(id)
);

