# SnowConvert AI CLI - Oracle

## Specific CLI arguments

### `--disableSnowScript`

Flag to indicate whether SnowConvert AI CLI should migrate the procedures to Javascript and Python. By default, it is set to **false**.

#### `--disableSynonym`

Flag to indicate whether or not Synonyms should be transformed. By default, it’s set to **true**.

#### `--disablePackagesAsSchemas`

Flag to indicate whether or not the Packages should be transformed to new Schemas.

Please check the naming of the procedure enabling and disabling the flag:

Copy code

```
CREATE OR REPLACE PACKAGE emp_mgmt AS
PROCEDURE remove_emp (employee_id NUMBER );
END emp_mgmt;

CREATE OR REPLACE PACKAGE BODY emp_mgmt AS
PROCEDURE remove_emp (employee_id NUMBER) IS
   BEGIN
      DELETE FROM employees
      WHERE employees.employee_id = remove_emp.employee_id;
      tot_emps := tot_emps - 1;
   END;
END emp_mgmt;
```

Copy code

```
CREATE SCHEMA IF NOT EXISTS emp_mgmt
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE emp_mgmt.remove_emp (employee_id NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      DELETE FROM
         employees
         WHERE employees.employee_id = remove_emp.employee_id;
         tot_emps :=
                     !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN unknown AND Number ***/!!!
                     tot_emps - 1;
   END;
$$;
```

Copy code

```
-- Additional Params: --disablePackagesAsSchemas
CREATE OR REPLACE PROCEDURE EMP_MGMT_REMOVE_EMP (employee_id NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      DELETE FROM
         employees
         WHERE employees.employee_id = remove_emp.employee_id;
         tot_emps :=
                     !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN unknown AND Number ***/!!!
                     tot_emps - 1;
   END;
$$;
```

#### `--outerJoinsToOnlyAnsiSyntax`

Flag to indicate whether Outer Joins should be transformed to only ANSI syntax.

#### `--disableDateAsTimestamp`

Flag to indicate whether `SYSDATE` should be transformed into `CURRENT_DATE` *or* `CURRENT_TIMESTAMP`. This will also affect all `DATE` columns that will be transformed to `TIMESTAMP`.

Copy code

```
CREATE TABLE DATE_TABLE(
    DATE_COL DATE
);

SELECT SYSDATE FROM DUAL;
```

Copy code

```
CREATE OR REPLACE TABLE DATE_TABLE (
        DATE_COL TIMESTAMP /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;

    SELECT
        CURRENT_TIMESTAMP()
    FROM DUAL;
```

Copy code

```
-- Additional Params: --disableDateAsTimestamp
CREATE OR REPLACE TABLE DATE_TABLE (
        DATE_COL DATE /*** SSC-FDM-OR0042 - DATE TYPE COLUMN HAS A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;

SELECT
    CURRENT_DATE()
FROM DUAL;
```

#### `--arrange`

Flag to indicate whether the input code should be processed before parsing and transformation.

Learn more about this step on our **Processing the code** page.

#### `--dataTypeCustomizationFile`

The path to a .json file that specifies rules of data type transformation considering data type origin and column name. This feature allows you to customize how data types are transformed during migration, including support for transforming `NUMBER` columns to `DECFLOAT`.

When this argument is provided, SnowConvert AI CLI generates a [TypeMappings Report](/migrations/aim-for-datawarehouses/manual-migration/technical-documentation/type-mappings-report) that shows all data type transformations applied, making it easy to verify your customization rules were applied correctly.

Navigate to the [Data Type Customization](/migrations/snowconvert-docs/translation-references/oracle/basic-elements-of-oracle-sql/data-types/README#data-type-customization) documentation to learn more about configuring data type transformation rules.
