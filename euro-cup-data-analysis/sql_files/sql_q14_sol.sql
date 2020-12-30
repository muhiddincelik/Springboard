/* 14. Write a SQL query to find referees and the number of bookings they made for the
entire tournament. Sort your answer by the number of bookings in descending order. */

WITH bookings AS
(SELECT
m.referee_id,
COUNT(*) AS booking_count
FROM euro_cup_2016.match_mast AS m
INNER JOIN euro_cup_2016.player_booked AS b ON m.﻿match_no = b.﻿match_no
GROUP BY 1)

SELECT
	r.referee_name,
	SUM(b.booking_count) AS total_bookings
FROM bookings AS b INNER JOIN euro_cup_2016.referee_mast AS r
		 ON b.referee_id = r.﻿referee_id
GROUP BY 1
ORDER BY 2 DESC

