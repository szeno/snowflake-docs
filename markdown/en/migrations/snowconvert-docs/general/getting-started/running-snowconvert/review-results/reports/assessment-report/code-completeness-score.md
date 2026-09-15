# SnowConvert AI - Code Completeness Score

[![The Code Completeness Score section of the assessment report for Teradata](/static/images/migrations/sc-assets/image(430).png "image")](/static/images/migrations/sc-assets/image(430).png)

## Code Completeness Score Value

This number represents the percentage of code units whose references to other code units are correctly addressed by SnowConvert AI. If the score is less than one hundred represents that there is at least one code unit referencing one or more code units not included in the source code.

### Formula

Copy code

```
((total_CU - impacted_CU) / total_CU ) * 100

total_CU = total number of Code Units
impacted_CU = Code Units with missing references
```

#### Sample

Copy code

```
-- Code Unit with no missing references
CREATE TABLE table1
(
    COL1 VARCHAR
)

-- Code Unit with no missing references
SELECT * from table1;

-- Code Unit with a missing reference
SELECT * from missing_table;
```

Copy code

```
-- Code Unit with no missing references
CREATE OR REPLACE TABLE table1
(
    COL1 VARCHAR
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

-- Code Unit with no missing references
SELECT
* from
table1;

-- Code Unit with a missing reference
SELECT
* from
missing_table;
```

**Expected Code Completeness Score:** 66.67

**Explanation:** In this case, we have 3 code units and only one of them has a missing reference. The `SELECT` in line 11 references another code unit called ‘missing\_table’ whose definition is not present in the source code, therefore this `SELECT` is considered a code unit with missing references.
