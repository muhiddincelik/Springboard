CREATE TABLE Patient (
  id INT,
  patient_name VARCHAR(50),
  email VARCHAR(30),
  address VARCHAR(200),
  PRIMARY KEY (id)
);

CREATE TABLE Specialty (
  id INT,
  specialty_name VARCHAR(30),
  description VARCHAR(300),
  PRIMARY KEY (id)
);

CREATE TABLE Disease (
  id INT,
  disease_name VARCHAR(30),
  description VARCHAR(300),
  PRIMARY KEY (id)
);

CREATE TABLE Doctor (
  id INT,
  doctor_name VARCHAR(50),
  specialty_id INT,
  PRIMARY KEY (id),
  FOREIGN KEY (specialty_id)
	REFERENCES Specialty(id)
);

CREATE TABLE Diagnosis (
  disease_id INT,
  visit_code INT,
  notes VARCHAR(300),
  FOREIGN KEY (visit_code)
      REFERENCES Visit(visit_code),
  FOREIGN KEY (disease_id)
      REFERENCES Disease(id)
);

CREATE TABLE Visit (
  visit_code INT,
  doctor_id INT,
  patient_id INT,
  visit_time DATETIME,
  PRIMARY KEY (visit_code),
  FOREIGN KEY (doctor_id)
      REFERENCES Doctor(id),
  FOREIGN KEY (patient_id)
      REFERENCES Patient(id)
);

