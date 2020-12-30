/* 8. Write a SQL query to find the match number for the game with the highest number of
   penalty shots, and which countries played that match. */
WITH highest_penalty AS
(SELECT
	match_no,
    COUNT(*) AS number_of_penalty_goals
FROM euro_cup_2016.penalty_shootout
WHERE score_goal = 'Y'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1)

SELECT
	d.﻿match_no,
    GROUP_CONCAT(country_name SEPARATOR ', ') AS countries
FROM euro_cup_2016.match_details AS d
	INNER JOIN soccer_country AS c ON d.team_id = c.﻿country_id
WHERE d.﻿match_no = (SELECT match_no FROM highest_penalty)
    