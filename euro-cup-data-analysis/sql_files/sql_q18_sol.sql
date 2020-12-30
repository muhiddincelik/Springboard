-- 18. Write a SQL query to find the highest number of foul cards given in one match.

SELECT
	﻿match_no,
    COUNT(*) AS number_of_cards
FROM euro_cup_2016.player_booked
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1