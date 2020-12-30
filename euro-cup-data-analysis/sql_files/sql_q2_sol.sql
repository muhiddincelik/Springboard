-- 2. Write a SQL query to find the number of matches that were won by penalty shootout.
SELECT
	COUNT(DISTINCT ﻿match_no) AS matches_decided_by_penalty
FROM euro_cup_2016.match_mast
WHERE decided_by = 'P'