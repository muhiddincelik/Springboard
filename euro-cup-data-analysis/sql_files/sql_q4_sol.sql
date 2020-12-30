/* 4. Write a SQL query to compute a list showing the number of substitutions
   that happened in various stages of play for the entire tournament. */
SELECT
	m.play_stage,
	COUNT(s.in_out) number_of_subs
FROM euro_cup_2016.player_in_out AS s
	INNER JOIN match_mast AS m ON s.﻿match_no = m.﻿match_no
WHERE s.in_out = 'I'
GROUP BY play_stage
