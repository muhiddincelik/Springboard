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

-- 1. List the name of the student with id equal to v1 (id).
SELECT name FROM Student WHERE id = @v1; 

-- ● What was the bottleneck?
	-- Full table scan to find the student with the id 1612521.
-- ● How did you identify it?
	-- I have looked into execution plan. Access type was ALL.
-- ● What method you chose to resolve the bottleneck?
	-- I have created an index on 'id' column in the student table.
