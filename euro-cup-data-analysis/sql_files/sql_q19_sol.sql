-- 19. Write a SQL query to find the number of captains who were also goalkeepers.

SELECT
	COUNT(*) AS gk_captains
FROM euro_cup_2016.match_captain
WHERE player_captain IN (SELECT 
							﻿player_id
                        FROM euro_cup_2016.player_mast
                        WHERE posi_to_play = 'GK')