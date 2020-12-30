-- 16. Write a SQL query to find referees and the number of matches they worked in each venue.

SELECT
    r.referee_name,
    v.venue_name,
    COUNT(m.﻿match_no) AS number_of_matches
FROM euro_cup_2016.soccer_venue AS v
INNER JOIN euro_cup_2016.match_mast AS m ON v.﻿venue_id = m.venue_id
INNER JOIN euro_cup_2016.referee_mast AS r ON m.referee_id = r.﻿referee_id
GROUP BY 1, 2
ORDER BY 1
