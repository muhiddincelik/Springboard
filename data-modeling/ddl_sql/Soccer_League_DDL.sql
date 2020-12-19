CREATE TABLE Stadium (
  id INT,
  stadium_name VARCHAR(50),
  address VARCHAR(150),
  capacity INT,
  PRIMARY KEY (id)
);

CREATE TABLE Referee (
  id INT,
  referee_name VARCHAR(100),
  age INT,
  PRIMARY KEY (id)
);

CREATE TABLE Match_Week (
  week_number INT,
  week_start DATETIME,
  week_start DATETIME,
  PRIMARY KEY (week_number)
);

CREATE TABLE Team (
  id INT,
  team_name VARCHAR(50),
  stadium_id INT,
  founded DATE,
  PRIMARY KEY (id),
  FOREIGN KEY (stadium_id)
      REFERENCES Stadium(id)
);

CREATE TABLE Result (
  fixture_id INT,
  home_team_score INT,
  away_team_score INT,
  FOREIGN KEY (fixture_id)
	REFERENCES Fixture(id)
);

CREATE TABLE Player (
  id INT,
  player_name VARCHAR(100),
  age INT,
  player_position VARCHAR(20),
  team_id INT,
  PRIMARY KEY (id),
  FOREIGN KEY (team_id)
	REFERENCES Team(id)
);

CREATE TABLE Fixture (
  id INT,
  home_team_id INT,
  away_team_id INT,
  match_time DATETIME,
  stadium_id INT,
  week_number INT,
  referee_id INT,
  PRIMARY KEY (id),
  FOREIGN KEY (home_team_id)
	REFERENCES Team(id),
  FOREIGN KEY (away_team_id)
	REFERENCES Team(id),
  FOREIGN KEY (stadium_id)
	REFERENCES Stadium(id),
  FOREIGN KEY (week_number)
	REFERENCES Match_Week(week_number),
  FOREIGN KEY (referee_id)
	REFERENCES Referee(id)
);

CREATE TABLE Player_Match (
  match_id INT,
  player_id INT,
  goals INT,
  own_goals INT,
  assists INT,
  min_played INT,
  yellow_card INT,
  red_card INT,
  FOREIGN KEY (match_id)
	REFERENCES Fixture(id),
  FOREIGN KEY (player_id)
	REFERENCES Player(id)
);

