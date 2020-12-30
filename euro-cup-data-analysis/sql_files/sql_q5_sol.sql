-- 5. Write a SQL query to find the number of bookings that happened in stoppage time.
SELECT
	COUNT(*) AS number_of_stop_bookings
FROM euro_cup_2016.player_booked
WHERE play_schedule = 'ST'