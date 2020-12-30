-- 7. Write a SQL query to find all the venues where matches with penalty shootouts were played.

SELECT
	m.venue_id,
	v.venue_name
FROM euro_cup_2016.match_mast AS m
	INNER JOIN euro_cup_2016.soccer_venue AS v
		ON m.venue_id = v.﻿venue_id
WHERE m.decided_by = 'P'