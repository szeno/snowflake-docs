# SnowConvert AI - Issues Report

## What is an “Issue”?

An issue is a message that provides relevant information about the transformations done by SnowConvert AI.

### Where can I find it?

The issues report can be found in a folder named *“Reports”*, in the output folder of your conversion. The name of the file itself starts with *“Issues”* so it can easily be located.

The format of the file is **.CSV**.

### What information does it contain?

The issues report contains the following information about all the issues added during the conversion:

| Column | Description |
| --- | --- |
| Session ID | The session ID of the transformation. This is a unique identifier for the transformation session. |
| Severity | One of the following values: Critical, High, Medium, Low, or None. This is an indicator of how much effort it takes to manually solve the problem. The None severity does not punish the conversion rate of the code unit. |
| Code | A unique identifier for the issue. |
| Name | The name of the issue message. |
| Description | The final message that was added to the output code. Something important to take into account is that some of the issues might have slightly different descriptions even though they have the same issue code, this happens because some of the descriptions have dynamic values. |
| Parent File | The relative path of the file where the issues is generated. |
| Line | The text line within the parent file where the issue is generated. |
| Column | The column within the line where the issue is generated. |
| Code Unit Database | The database name (if applicable) of the code unit that contains the issue message. It might be empty because the generated issue has no explicit database name or it is not generated inside a code unit with a name that identifies it. |
| Code Unit Schema | The schema name (if applicable) of the code unit that contains the issue message. It might be empty because the generated issue has no explicit schema name or it is not generated inside a code unit with a name that identifies it. |
| Code Unit Package | The package name (if applicable) of the code unit that contains the issue message. It might be empty because the generated issue has no explicit schema name or it is not generated inside a code unit with a name that identifies it. This column only applies to Oracle SQL migrations. |
| Code Unit Name | The name of the code unit, without database and or schema qualification. This column only applies to code units that have a name that identifies them. |
| Code Unit ID | A string that uniquely identifies the code unit. The name of the object, without database and or schema qualification. |
| Code Unit | The code unit that contains the issue. |
| Code Unit Size | A size classification of the code unit, based on its line of code. The available measurements are XS, S, M, L, and XL. |
| Language | The programming language or SQL dialect of the source code unit. |

### Report Example

Given the following Oracle SQL input code, SnowConvert AI will add the SSC-FDM-OR0035 conversion issue.

Copy code

```
:force:
CREATE OR REPLACE PROCEDURE schema1.procedure1
AS
BEGIN
  DBMS_OUTPUT.PUT_LINE('hello world');
END;
```

Copy code

```
CREATE OR REPLACE PROCEDURE schema1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  BEGIN
    --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
    CALL DBMS_OUTPUT.PUT_LINE_UDF('hello world');
  END;
$$;
```

The row in the issues report for the SSC-FDM-OR0035 conversion issue will have the following information:

| Column | Value |
| --- | --- |
| Session ID | Not available |
| Severity | Low |
| Code | SSC-FDM-OR0035 |
| Name | Custom UDF inserted |
| Description | CUSTOM UDF ‘DBMS\_OUTPUT.PUT\_LINE\_UDF’ INSERTED. |
| Parent File | sample.sql |
| Line | 4 |
| Column | 3 |
| Code Unit Database | N/A |
| Code Unit Schema | schema1 |
| Code Unit Package | N/A |
| Code Unit Name | procedure1 |
| Code Unit Id | schema1.procedure1 |
| Code Unit | CREATE PROCEDURE |
| Code Unit Size | XS |

Expand

Show lessSee more
