/* 20. Write a SQL query to find the substitute players who came into the field in the first
half of play, within a normal play schedule. */

SELECT
	p.player_name
FROM player_in_out AS i
INNER JOIN player_mast AS p ON i.player_id = p.﻿player_id
WHERE i.in_out = 'I' AND i.play_half = 1 AND i.play_schedule = 'NT'