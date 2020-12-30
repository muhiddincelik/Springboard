/* 12. Write a SQL query that returns the total number of goals scored by each position on
each country’s team. Do not include positions which scored no goals. */

SELECT
	g.team_id,
    p.posi_to_play,
	COUNT(g.﻿goal_id) AS total_goals
FROM euro_cup_2016.goal_details as g
	INNER JOIN  euro_cup_2016.player_mast AS p ON g.player_id = p.﻿player_id
GROUP BY 1, 2
HAVING total_goals > 0