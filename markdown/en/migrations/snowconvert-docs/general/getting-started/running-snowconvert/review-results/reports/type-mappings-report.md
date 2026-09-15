# SnowConvert AI - TypeMappings Report

## What is the TypeMappings Report?

The TypeMappings report shows the data type transformations that were applied based on your [Data Type Customization](/migrations/snowconvert-docs/translation-references/oracle/basic-elements-of-oracle-sql/data-types/README#data-type-customization) file. This report only includes transformations specified in the customization file. Use this report to verify that your custom rules were applied correctly to the expected columns and objects.

## Where can I find it?

The TypeMappings report can be found in a folder named *“reports”*, in the output folder of your conversion. The file is named **TypeMappings.csv**.

Note

This report is generated when data type customization is enabled (using the `--dataTypeCustomizationFile` argument). If no customization file is provided, this report may not be generated or may be empty.

## What information does it contain?

The TypeMappings report is presented in a CSV table format and contains the following columns:

| Column | Description |
| --- | --- |
| ObjectType | The type of object where the data type was found (e.g., `TABLE_COLUMN`, `PROCEDURE_PARAMETER`, `FUNCTION_PARAMETER`, `VARIABLE`). |
| ObjectId | The fully qualified identifier of the object (e.g., `Schema.Table.Column`). |
| FileName | The name of the source file where the data type was found. |
| LineNumber | The line number in the source file where the data type is defined. |
| OriginalType | The original data type in the source code (e.g., `NUMBER(10, 2)`). |
| TargetType | The resulting data type after transformation (e.g., `DECFLOAT`, `NUMBER(18, 2)`). |

Expand

Show lessSee more

## Example Output

Here is an example of what the TypeMappings report might contain:

| ObjectType | ObjectId | FileName | LineNumber | OriginalType | TargetType |
| --- | --- | --- | --- | --- | --- |
| TABLE\_COLUMN | SALES.ORDERS.TOTAL\_AMOUNT | orders.sql | 15 | NUMBER(15, 2) | DECFLOAT |
| TABLE\_COLUMN | SALES.ORDERS.ORDER\_ID | orders.sql | 12 | NUMBER(10, 0) | NUMBER(18, 0) |
| TABLE\_COLUMN | HR.EMPLOYEES.SALARY | employees.sql | 8 | NUMBER | NUMBER(18, 2) |

Expand

Show lessSee more

## Using the Report

### Verifying Customization Rules

Use this report to verify that your data type customization rules in the JSON configuration file were applied as expected. Compare the `OriginalType` and `TargetType` columns to ensure the transformations match your requirements.

### Identifying Affected Objects

The report helps you identify all database objects affected by data type customizations, making it easier to:

- Review the scope of changes before deployment
- Plan testing strategies for affected tables and procedures
- Document the migration changes for compliance purposes

### UI Integration

In SnowConvert AI’s graphical interface, the TypeMappings report is integrated into the **Code Units Summary** tab of the conversion report. For Oracle conversions using data type customization, you will see a “Data type mappings” section that shows:

- The total count of affected data types
- A link to open the full TypeMappings.csv report

## Related Documentation

- [Data Type Customization](/migrations/snowconvert-docs/translation-references/oracle/basic-elements-of-oracle-sql/data-types/README#data-type-customization): Learn how to configure data type transformation rules.
- [Oracle CLI Arguments](/migrations/snowconvert-docs/general/user-guide/snowconvert/command-line-interface/oracle): Details on the `--dataTypeCustomizationFile` argument.
- [DB2 DECFLOAT](/migrations/snowconvert-docs/translation-references/db2/db2-data-types#decfloat-data-type): Information about DECFLOAT transformation in DB2.
