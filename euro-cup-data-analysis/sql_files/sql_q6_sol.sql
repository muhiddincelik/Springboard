/* 6. Write a SQL query to find the number of matches that were won by a single point, but
      do not include matches decided by penalty shootout. */

SELECT
	goal_score
FROM euro_cup_2016.match_mast
WHERE ABS(CAST(SUBSTR(goal_score, 1, 1) AS SIGNED) - 
		CAST(SUBSTR(goal_score, 3, 1) AS SIGNED)) = 1
      AND
		decided_by != 'P'