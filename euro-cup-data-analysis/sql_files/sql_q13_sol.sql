-- 13. Write a SQL query to find all the defenders who scored a goal for their teams.

SELECT
p.player_name,
COUNT(g.﻿goal_id) AS total_goals
FROM euro_cup_2016.goal_details AS g
INNER JOIN euro_cup_2016.player_mast AS p ON g.player_id = p.﻿player_id
WHERE p.posi_to_play = 'DF'
GROUP BY 1
