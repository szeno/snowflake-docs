# SnowConvert AI - Embedded Code Units Report

## What is a Embedded Code Unit?

A Code Unit, as the name suggests, is the most atomic, standalone executable element. In most cases, these are statements, but they also include script files as well because those are executed as a single element.

So according to the previous definition, an embedded code unit is when a Code Unit is inside a Top Level Code Unit. For more information please refer to [Top-Level Code Units Report](top-level-code-units-report).

## Examples of Embedded Code Units

In the following section, we can see some examples of Embedded Code Units.

### Packages

A package can define multiple elements inside its body. The package body is considered the Top-Level Code Unit because those elements cannot be created individually without creating the entire package body. Elements or code units inside a package will count as Embedded Code Units.

The following statements will be counted as embedded code units in `packages`:

- Functions
- Procedures
- Types
- Cursors
- Constants
- Variables
- Exceptions
- Pragmas

Copy code

```
:force:
CREATE OR REPLACE PACKAGE my_package1 IS
    PROCEDURE outer_procedure(input_value NUMBER);
END my_package1;
/

CREATE OR REPLACE PACKAGE BODY my_package1 IS
    FUNCTION outer_function(value NUMBER) RETURN NUMBER IS
        BEGIN
            RETURN value * 2;
        END inner_function;

    PROCEDURE outer_procedure(input_value NUMBER) IS
    BEGIN
        DBMS_OUTPUT.PUT_LINE('Result of inner function: ' || inner_function(input_value));
        DBMS_OUTPUT.PUT_LINE('Input Value: ' || input_value);
    END outer_procedure;
END my_package1;
```

For this case the embedded function `"outer_function(NUMBER)"` and the embedded procedure `"outer_procedure(NUMBER)"` will be counted.

## Information in the Embedded Code Units Report

| Column | Description |
| --- | --- |
| Partition Key | The unique identifier of the conversion. |
| File Type | The type of the file that the Embedded Code Unit is in. (SQL, BTEQ, etc…) |
| ParentCategory | The Category of the Top Level Code Unit in which the code unit is embedded. |
| ParentID | The fully qualified name of the Top Level Code Unit in which the code unit is embedded. |
| Category | The broader class or type each Embedded Code Unit belongs to. |
| Code Unit | The type of Embedded Code Unit that this element belongs to. |
| Code Unit Name | The name of the Embedded Code Unit if it has one such as tables or procedures. It will be N/A for elements without a name. |
| File Name | The name of the file in which the Embedded Code Unit is located. Uses the relative path starting from the input directory. |
| Line Number | The line number inside the file where the Embedded Code Unit is located. |
| Lines of Code | The total lines of code that the Embedded Code Unit has. |
| EWI Count | The amount of EWIs found within the code unit. You can learn more about EWIs [here](../../../../technical-documentation/issues-and-troubleshooting/conversion-issues/README). |
| FDM Count | The amount of FDMs found within the code unit. You can learn more about FDMs [here](../../../../technical-documentation/issues-and-troubleshooting/functional-difference/README). |
| PRF Count | The amount of PRFs found within the code unit. You can learn more about PRFs [here](../../../../technical-documentation/issues-and-troubleshooting/performance-review/README). |
| Highest EWI Severity | The highest EWI severity found within the Embedded Code Unit. The severity order is the following:   - N/A (when there are not any EWIs) - Low - Medium - High - Critical |
| UDFs Used | The names of all the user defined functions found within the Embedded Code Unit. The name of the UDFs used are separated by a pipe if there is more than one. |
| EWI | The codes of all the EWIs found within the code unit. These codes are separated by pipes and do not include repeated codes. |
| FDM | The codes of all the FDMs found within the code unit. These codes are separated by pipes and do not include repeated codes. |
| PRF | The codes of all the PRFs found within the code unit. These codes are separated by pipes and do not include repeated codes. |
| Conversion Status | The final status of the conversion of the code unit.  The possible conversion statuses are:   - **NotSupported:** When the Embedded Code Unit has a 0% conversion rate. - **Partial:** When the conversion rate of the Embedded Code Unit is between 0% and 100%. - **Success:** When the Embedded Code Unit conversion rate is 100%. |
| LoC Conversion Percentage | The conversion percentage is based on Lines of Code. A single line of code may have supported and unsupported fragments depending on how the input code was formatted. In these cases, the entire line is considered as not supported. |
| Deployment Order | The deployment order is the topological level of each code unit based on its dependencies. It shows the right order in which the code units should be deployed to avoid missing dependencies during the deployment phase. |

Expand

Show lessSee more

## Example

Assume that the following `CREATE PACKAGE` in ORACLE SQL is located in its file called Oracle\_01.sql.

Copy code

```
CREATE OR REPLACE PACKAGE my_package1 IS
    PROCEDURE calculate_salary(emp_id IN NUMBER);
END my_package1;
/

CREATE OR REPLACE PACKAGE BODY my_package1 IS
    PROCEDURE calculate_salary(emp_id IN NUMBER) IS
        emp_name VARCHAR2(100);
        emp_salary NUMBER;
    BEGIN
        SELECT name, salary INTO emp_name, emp_salary FROM employees WHERE employee_id = emp_id;
        DBMS_OUTPUT.PUT_LINE('Employee ID: ' || emp_id);
        DBMS_OUTPUT.PUT_LINE('Employee Name: ' || emp_name);
        DBMS_OUTPUT.PUT_LINE('Employee Salary: ' || emp_salary);
    END calculate_salary;
END my_package1;
```

Copy code

```
:force:
CREATE SCHEMA IF NOT EXISTS my_package1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "employees" **
CREATE OR REPLACE PROCEDURE my_package1.calculate_salary(emp_id NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        emp_name VARCHAR(100);
        emp_salary NUMBER(38, 18);
    BEGIN
        SELECT name, salary INTO
            :emp_name,
            :emp_salary
        FROM
            employees
        WHERE employee_id = :emp_id;
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        CALL DBMS_OUTPUT.PUT_LINE_UDF('Employee ID: ' || NVL(:emp_id :: STRING, ''));
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        CALL DBMS_OUTPUT.PUT_LINE_UDF('Employee Name: ' || NVL(:emp_name :: STRING, ''));
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        CALL DBMS_OUTPUT.PUT_LINE_UDF('Employee Salary: ' || NVL(:emp_salary :: STRING, ''));
    END;
$$;
```

The Embedded Code Units report will have only one embedded procedure.

Here are all the values that would be reported in the entry of this embedded procedure inside the package:

- The **Partition Key** value will depend on migration so the value here will vary.
- The **File Type** will be SQL because it was migrated on a file with the .sql extension.
- The **ParentCategory** will be `PACKAGE BODY` because the `PACKAGE BODY` is the top level code unit that contains the embedded procedure.
- The **ParentID** will be `my_package1` because is the top level code unit name that contains the embedded procedure.
- The **Category** for the embedded procedure will be `PROCEDURE` because the `CREATE PROCEDURE` statement is part of the `PROCEDURE` Code Unit Category.
- The **Code Unit** itself will be `CREATE PROCEDURE`.
- The **Code Unit** **Name** will be `calculate_salary(NUMBER)`.
- The **File Name** where this code unit was found would be Oracle\_01.sql.
- Assuming that the `CREATE PROCEDURE` statement is in the `PACKAGE BODY DEFINITION`, the **Line Number** will be 8.
- The **Lines of Code** number would be 9.
- The **EWI Count** column will report 0 because the output code does not have EWIs.
- The **FDM Count** column will report 3 because the output code has three FDM related to the UDFs that were added to the output code.
- The **PRF Count** column will report N/A because the output code does not have PRFs.
- The **Highest EWI Severity** in this case would be “N/A” because there are no EWIs.
- The **UDFs Used** column will be `DBMS_OUTPUT.PUT_LINE_UDF` because this custom User Defined Function was added to convert the `DBMS_OUTPUT.PUT_LINE`.
- The **EWI** column will show N/A because there are no EWI issues.
- The **FDM** column will show “`SSC-FDM-OR0035`” in this case.
- The **PRF** column will show N/A because there are no PRF issues.
- The **Conversion Status** will be “`Success`” .
- The **LoC Conversion Percentage** is `100%` because all the lines were converted successfully.

## Deployment Order

The deployment order column represents the correct order to deploy each code unit into Snowflake. For the embedded code units report, the deployment order is only available for `FUNCTIONS` and `STORED PROCEDURES`. Other embedded code units would have `N/A` deployment order. See Deployment Order in [Top-Level Code Units Report](./top-level-code-units-report#deployment-order) for more details.
