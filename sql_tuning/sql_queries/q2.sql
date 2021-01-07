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

-- 2. List the names of students with id in the range of v2 (id) to v3 (inclusive).

SELECT name FROM Student WHERE id BETWEEN @v2 AND @v3;

-- ● What was the bottleneck?
	-- Full table scan to find the student in a certain id range.
-- ● How did you identify it?
	-- I have looked into execution plan. Access type was ALL.
-- ● What method you chose to resolve the bottleneck?
	-- I have converted id column in the student table into a primary key. By default, primary key is the clustered index.



