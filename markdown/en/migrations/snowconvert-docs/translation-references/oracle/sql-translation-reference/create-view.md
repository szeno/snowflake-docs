# Oracle - Create View

In this section, you could find information about Oracle Views and their Snowflake equivalent. The syntax of subquery used to create the view can be found in the SELECT section

Note

Some parts in the output code are omitted for clarity reasons.

## Create View

Copy code

```
CREATE OR REPLACE VIEW View1 AS SELECT Column1 from Schema1.Table1;
```

Copy code

```
CREATE OR REPLACE VIEW View1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
SELECT Column1 from
Schema1.Table1;
```

The following clauses for Create View are removed:

- No Force/ Force
- Edition Clause
- Sharing Clause
- Default collation
- Bequeath clause
- Container clause

Copy code

```
CREATE OR REPLACE
NO FORCE
NONEDITIONABLE
VIEW Schema1.View1
SHARING = DATA
DEFAULT COLLATION Collation1
BEQUEATH CURRENT_USER
AS SELECT Column1 from Schema1.Table1
CONTAINER_MAP;
```

Copy code

```
CREATE OR REPLACE VIEW Schema1.View1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
AS
SELECT Column1 from
Schema1.Table1;
```

## Alter View

Alter is not yet supported.

## Drop View

The CASCADE CONSTRAINT clause is not supported yet.

Copy code

```
DROP VIEW Schema1.View1;

DROP VIEW Schema1.View1
CASCADE CONSTRAINTS;
```

Copy code

```
DROP VIEW Schema1.View1;

DROP VIEW Schema1.View1
CASCADE CONSTRAINTS !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'DropBehavior' NODE ***/!!!;
```

### Related EWIs

1. [SSC-EWI-0073](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.
