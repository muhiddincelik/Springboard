/* 11. Write a SQL query to find the players, their jersey number, and playing club who
were the goalkeepers for England in EURO Cup 2016. */

WITH country AS
(SELECT
	﻿country_id
FROM euro_cup_2016.soccer_country
WHERE country_name = 'England'),

match_gk AS
(SELECT
	player_gk
FROM euro_cup_2016.match_details
WHERE team_id = (SELECT * FROM country))

SELECT
player_name,
jersey_no,
playing_club
FROM euro_cup_2016.player_mast
WHERE ﻿player_id IN (SELECT * FROM match_gk)
