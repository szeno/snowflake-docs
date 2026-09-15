# Code Conversion - Spark Functional Differences

Note

For Spark SQL, SnowConvert AI translates supported SQL statements and reports functional differences where Snowflake behavior can diverge. Review each generated marker and validate the converted statement against the target schema.

## SSC-FDM-SPK0001

Columns automatically extracted for INSERT BY NAME

#### Description

Spark `INSERT ... BY NAME` matches source expressions to target columns by name without requiring an explicit target list. SnowConvert AI extracts the projected names and adds them to the generated `INSERT`, then emits this FDM because aliases, schema drift, or missing columns can make the inferred list differ from the intended target structure.

#### Code Example

##### Input Code:

##### Spark

Copy code

```
INSERT INTO TABLE students BY NAME SELECT name, address FROM persons;
```

##### Output Code:

##### Snowflake

Copy code

```
INSERT
       --** SSC-FDM-SPK0001 - COLUMNS WERE AUTOMATICALLY EXTRACTED FROM THE SELECT STATEMENT FOR INSERT BY NAME. PLEASE VERIFY THAT THE COLUMN LIST MATCHES YOUR TARGET TABLE STRUCTURE AND THAT ALL REQUIRED COLUMNS ARE INCLUDED **
       INTO students (name, address)
SELECT
  name,
  address
FROM
  persons;
```

#### Best Practices

- Compare the generated column list with the target table schema, including required columns and expected ordering.
- Add an explicit target column list when the inferred list does not match the intended load.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
