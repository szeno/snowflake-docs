# Code Conversion - Sybase IQ Functional Differences

Note

**Conversion Scope**

For Sybase IQ, the assessment and translation capabilities primarily focus on TABLES, VIEWS, STORED PROCEDURES, and FUNCTIONS.
While other types of ANSI-standard statements are recognized, they are not yet fully supported for conversion. The tool may identify them, but will not perform a complete translation for these unsupported code units.

## SSC-FDM-SY0001

Calling stored procedure in FROM might have compilation errors

### Description

Snowflake supports calling a stored procedure in the FROM clause when the procedure meets certain [conditions](https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-selecting-from#limitations-for-selecting-from-a-stored-procedure) otherwise the query fails.

#### Code Example

##### Input Code:

##### Sybase

Copy code

```
 SELECT * FROM MyProcedure(1, 'test');
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
  *
FROM
  --** SSC-FDM-SY0001 - CALLING STORED PROCEDURE IN FROM CLAUSE MIGHT HAVE COMPILATION ERRORS **
  TABLE(MyProcedure(1, 'test'));
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-SY0002

Calling stored procedure in FROM might have compilation errors

### Description

Snowflake does not contain indexes for query optimization.

#### Code Example

##### Input Code:

##### Sybase

Copy code

```
 SELECT * FROM TABLE1 FORCE INDEX (MyIndex);
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
  *
FROM
  TABLE1
--         --** SSC-FDM-SY0002 - FORCE INDEX IS NOT SUPPORTED IN SNOWFLAKE **
--         FORCE INDEX(MyIndex)
                             ;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
