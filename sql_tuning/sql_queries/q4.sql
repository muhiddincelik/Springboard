USE springboardopt;

-- -------------------------------------
SET @v1 = 1612521;
SET @v2 = 1145072;
SET @v3 = 1828467;
SET @v4 = 'MGT382';
SET @v5 = 'Amber Hill';
SET @v6 = 'MGT';
SET @v7 = 'EE';			  
SET @v8 = 'MAT';

-- 4. List the names of students who have taken a course taught by professor v5 (name).

SELECT name FROM Student,
	(SELECT studId FROM Transcript,
		(SELECT crsCode, semester FROM Professor
			JOIN Teaching
			WHERE Professor.name = @v5 AND Professor.id = Teaching.profId) as alias1
	WHERE Transcript.crsCode = alias1.crsCode AND Transcript.semester = alias1.semester) as alias2
WHERE Student.id = alias2.studId;

SELECT
	s.name
FROM student s
	JOIN transcript t1 ON s.id = t1.studId
	JOIN teaching t2 ON  t2.crsCode = t1.crsCode AND t2.semester = t1.semester
	JOIN professor p ON p.id = t2.profId
WHERE p.name = @v5;

-- ● What was the bottleneck?
	-- Full table scan on profesor and teaching tables.
-- ● How did you identify it?
	-- I have looked into execution plan. Access type was ALL.
-- ● What method you chose to resolve the bottleneck?
	-- I have converted id column in the professor table into primary key.
    -- I have also added an index for the name column in the professor table.
    -- I have defined prof_id column in the teaching table as a foreign key referencing to the id column in the professor table. 
    -- I have used JOIN(s) instead of IN and complex subqueries.