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

-- 5. List the names of students who have taken a course from department v6 (deptId), but not v7.

SELECT * FROM Student, 
	(SELECT studId FROM Transcript, Course WHERE deptId = @v6 AND Course.crsCode = Transcript.crsCode
	AND studId NOT IN
	(SELECT studId FROM Transcript, Course WHERE deptId = @v7 AND Course.crsCode = Transcript.crsCode)) as alias
WHERE Student.id = alias.studId;


-- ● What was the bottleneck?
	-- Full table scan on course table (for PRIMARY and DEPENDENT SUBQUERY select types on Course table)
-- ● How did you identify it?
	-- I have looked into execution plan. Access type was ALL.
-- ● What method you chose to resolve the bottleneck?
	-- I have created a composite key using crsCode and crsName. (composite key instead of PK on crsCode due to duplicate values in crsCode)
    -- I have also added an index for the deptId column.