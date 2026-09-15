# SnowConvert AI - Output Code

## Source Code

Suppose this is the input source code you’ve migrated:

Copy code

```
CREATE TABLE! TABLE_Invalid
(
  COL1 VARCHAR2(255),
  COL2 VARCHAR2
);

CREATE TABLE TABLE1
(
  COL1 INT,
  COL2 VARCHAR2!
);

CREATE OR REPLACE VIEW VIEW1
AS
    SELECT
        UNKOWN_FUNCTION(1),
        COL1,
        COL2
    FROM TABLE1
;
```

## Output code

Copy code

```
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '1' COLUMN '0' OF THE SOURCE CODE STARTING AT 'CREATE'. EXPECTED 'Create table Statement' GRAMMAR. LAST MATCHING TOKEN WAS 'TABLE' ON LINE '1' COLUMN '7'. FAILED TOKEN WAS '!' ON LINE '1' COLUMN '12'. CODE '63'. **
--CREATE TABLE! TABLE_Invalid
--(
--  COL1 VARCHAR2(255),
--  COL2 VARCHAR2
--)
 ;

        CREATE OR REPLACE TABLE TABLE1
        (
          COL1 INT
--                  ,
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '10' COLUMN '3' OF THE SOURCE CODE STARTING AT 'COL2'. EXPECTED 'Column Definition' GRAMMAR. LAST MATCHING TOKEN WAS 'VARCHAR2' ON LINE '10' COLUMN '8'. CODE '15'. **
--  COL2 VARCHAR2!
)
        COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;

        --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "UNKOWN_FUNCTION" **
        CREATE OR REPLACE VIEW VIEW1
        COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
        AS
        SELECT
          !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'UNKOWN_FUNCTION' NODE ***/!!!
          UNKOWN_FUNCTION(1),
          COL1,
          COL2
    FROM
          TABLE1
;
```

### How to interpret the output code?

- There is one parsing error in line number one. This is because of an invalid token `CREATE TABLE!`
- There is another parsing error on line 10. This is because of an invalid token`VARCHAR2!`
- There is an unknown function `UNKNOWN_FUNCTION` , which is translated as is, but warning SSC-EWI-0073 is added to indicate that this is something that has not been checked yet and therefore, the functional equivalence cannot be assured.
