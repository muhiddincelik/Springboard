-- 15. Write a SQL query to find the referees who booked the most number of players.

SELECT
	r.referee_name,
    COUNT(DISTINCT b.player_id) AS distinct_players
FROM euro_cup_2016.match_mast AS m
INNER JOIN euro_cup_2016.player_booked AS b ON m.﻿match_no = b.﻿match_no
INNER JOIN euro_cup_2016.referee_mast AS r ON m.referee_id = r.﻿referee_id
GROUP BY 1
ORDER BY 2 DESC


    

