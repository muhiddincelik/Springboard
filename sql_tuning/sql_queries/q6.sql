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

-- 6. List the names of students who have taken all courses offered by department v8 (deptId).

SELECT
	s.name
FROM student s
	JOIN transcript t ON s.id = t.studId 
	JOIN course c ON c.crsCode = t.crsCode
WHERE c.deptId = @v8
GROUP BY 1
HAVING COUNT(t.crsCode) = (SELECT COUNT(*) FROM course WHERE deptId = @v8)


-- ● What was the bottleneck?
	-- Full table scan on teaching table
-- ● How did you identify it?
	-- I have looked into execution plan. Access type was ALL.
-- ● What method you chose to resolve the bottleneck?
	-- I have defined crsCode column in the teaching table as a foreign key referring to the crsCode column in the course table.
    -- I have replaced IN operators and subqueries with JOIN(s).