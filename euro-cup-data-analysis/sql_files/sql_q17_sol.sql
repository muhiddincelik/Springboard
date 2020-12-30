/* 17. Write a SQL query to find the country where the most assistant referees come from,
	   and the count of the assistant referees. */
	
SELECT
	country_name,
    COUNT(DISTINCT ﻿ass_ref_id) AS number_of_asst_refs
FROM euro_cup_2016.asst_referee_mast AS a
INNER JOIN euro_cup_2016.soccer_country AS c ON a.country_id = c.﻿country_id
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1