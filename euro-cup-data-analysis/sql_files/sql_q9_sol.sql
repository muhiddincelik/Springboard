/* 9. Write a SQL query to find the goalkeeper’s name and jersey number,
	playing for Germany, who played in Germany’s group stage matches. */
WITH country AS
(SELECT
	﻿country_id
FROM euro_cup_2016.soccer_country
WHERE country_name = 'Germany'),

group_match_gk AS
(SELECT
	DISTINCT player_gk
FROM euro_cup_2016.match_details
WHERE team_id = (SELECT * FROM country) AND play_stage = 'G')

SELECT
player_name,
jersey_no
FROM euro_cup_2016.player_mast
WHERE ﻿player_id IN (SELECT * FROM group_match_gk)

