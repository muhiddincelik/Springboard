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

-- 3. List the names of students who have taken course v4 (crsCode).
 SELECT name FROM Student s INNER JOIN Transcript t ON s.id = t.studId WHERE crsCode = @v4;

-- ● What was the bottleneck?
	-- Full table scan to find the student in a certain id range.
-- ● How did you identify it?
	-- I have looked into execution plan. Access type was ALL.
-- ● What method you chose to resolve the bottleneck?
	-- I have converted studId column in the transcript table into foreign key which refers to the primary key (id) in the student table.
    -- I have also added an index for crsCode column in the course table.
    -- I have used JOIN instead of IN operator.