# SnowConvert CLI - Renaming feature

Renaming objects during a database migration process is something that a lot of users need to do. For this reason, SnowConvert CLI enables the Renaming feature to allow defining new names for the following types of user-defined objects:

Note

This feature is supported for Teradata, SQL Server, and Redshift **ONLY**.

- Schemas
- Tables
- Views
- Materialized Views
- Procedures
- Functions
- Macros

Note

The renaming feature will apply to both the object definition and the object’s uses.

These objects are usually qualified within a schema or a database, so, depending on the database platform, the object `Table1` might be referenced simply as `Table1`, as `MySchema.Table1` or as `MyDatabase.MySchema.Table1`. It is **essential** to fully qualify each object in the renaming file to avoid ambiguity.

The new object names are specified via a .json file with the following format.

Note

Note that this example contains a “Macros” section. This is a **Teradata-specific** element and may vary depending on the specified language.

Copy code

```
{
  "Schemas": {
    "SchemaName": "NewSchema"
  },
  "Tables": {
    "SchemaName.TableName": "NewSchema.TableNameChanged",
    "Table1": "Table2"
  },
  "TablesRegex": [
    {
      "RegexExpr": "(Schema1)\\.(.*)",
      "RegexReplace": "Prefix_$1.$2"
    }
  ],

  "Views": {
    "ViewName": "ViewNameChanged",
    "MaterializedViewName": "MaterializedViewNameChanged"
  },
  "ViewsRegex": [
    {
      "RegexExpr": "(Schema1)\\.(.*)",
      "RegexReplace": "$2.$1"
    }
  ],

  "Procedures": {
    "ProcedureName": "ProcedureNameChanged"
  },
  "ProceduresRegex": [
    {
      "RegexExpr": "(Schema1)\\.(.*)",
      "RegexReplace": "$2.$1"
    }
  ],

  "Macros": {
    "SchemaName.MacroName": "MacroNameChanged",
    "SimpleMacro": "SimpleMacroSf"
  },
  "MacrosRegex": [
    {
      "RegexExpr": "(Schema1)\\.(.*)",
      "RegexReplace": "$2.$1"
    }
  ],

  "Functions": {
    "SchemaName.FunctionName": "FunctionNameChanged",
    "SimpleFunction": "SimpleFunctionSf"
  },
  "FunctionsRegex": [
    {
      "RegexExpr": "(Schema1)\\.(.*)",
      "RegexReplace": "$2.$1"
    }
  ]
}
```

## Usage

To use the renaming feature, you have to execute the SnowConvert CLI with the following argument `--RenamingFile` and provide the path to the .json file containing the renaming information. An example of the command can look like this:

> snowct.exe -i “somePath/input” -o “somePath/output” –RenamingFile “somePath/renamings.json”

### Renaming modes

Notice there are two fields for each kind of object: `"Tables"` and `"TablesRegex"`, `"Views"` and `"ViewsRegex"`, and so on. This is because there are two ways in which renamings can be specified.

#### Object by object (line by line)

In this mode, each line represents an object, and it must contain the original fully qualified name and the new name. So, if we want to move an object named “Table1” inside the schema *“OriginalSchema”* to the schema *“SchemaSF”*, the line must be like this:

Copy code

```
"OriginalSchema.Table1": "SchemaSF.Table1"
```

If we also want to rename it to “Table2”, the line should be like this:

Copy code

```
"OriginalSchema.Table1": "SchemaSF.Table2"
```

This information has to be specified in the `"Tables"`, `"Views"`, `"Procedures"`, `"Macros"`, and `"Functions"` sections of the .json file and each line must be separated with a comma. Let’s take a look at an example:

**TableExample1**

Copy code

```
"Tables": {
    "Schema1.Table1": "SF_Schema1.SF_Table1",
    "Schema1.Table2": "SF_Schema1.SF_Table2",
    "Schema1.Table3": "SF_Schema1.SF_Table3"
  },
```

The above sample is saying that the only three tables in the whole workload to be renamed are the ones called “Table1”, “Table2”, and “Table3”, all located inside the “Schema1” schema; they must be renamed to “SF\_Table1”, “SF\_Table2”, and “SF\_Table3”, respectively; and finally, they will be located under the “SF\_Schema1” schema in Snowflake.

#### Regular expressions

If there is a need to rename multiple objects in the same way, the feature also allows regular expressions to define patterns to apply to objects of the same kind. Two lines are required to specify each renaming, the first line is `"RegexExpr"` which is the matching expression and the second line is the `"RegexReplace"` which is the replacing expression. This information has to be provided in the `"TablesRegex"`, `"ViewsRegex"`, `"ProceduresRegex"`, `"MacrosRegex"`, and `"FunctionsRegex"` sections of the .json file. So, the previous example can also be written in the following manner, using the regular expression feature.

**TableExample2**

Copy code

```
"TablesRegex": [
    {
      "RegexExpr": "Schema1\\.(.*)",
      "RegexReplace": "SF_Schema1.SF_$1"
    }
  ],
```

The only difference is that this way applies to all tables located within the “Schema1” schema. The regular expression would match all tables defined within the “Schema1” schema and will create a capturing group with everything after the dot. The regex replace will move the tables to the “SF\_Schema1” schema and will add the “SF\_” prefix to all tables found referencing the first group created ($1) in the regex expression.

#### Renaming priority

There might be renamings that apply to the same object and only one of them is chosen. Within the same section, SnowConvert CLI will apply the first renaming that matches the current object’s name, and it will stop trying to rename that object. So in the following example, despite the fact that `"Tables"` section specifies renaming “Table1” to “Table1-a” and also to “Table1-b”, SnowConvert CLI will only rename it to “Table1-a”.

Copy code

```
"Tables": {
    "Schema1.Table1": "Schema1.Table1-a",
    "Schema1.Table1": "Schema1.Table1-b",
  },
```

Also, SnowConvert CLI will try to rename an object first checking the object by object renaming section before trying the regular expressions section. So, in the following example despite the fact that both renamings can apply to the same object “Schema1.Table1”, only the one defined in the `"Tables"` section is applied.

Copy code

```
"Tables": {
    "Schema1.Table1": "Schema1.TableA",
  },
  "TablesRegex": [
    {
      "RegexExpr": "Schema1\\.(.*)",
      "RegexReplace": "Schema1.SF_$1"
    }
  ],
```

#### Example

Let’s say we have the following input code.

**Input Code**

Copy code

```
CREATE TABLE CLIENT (
    ID INTEGER,
    NAME varchar(20));

CREATE TABLE TICKET (
    CLIENT_ID INTEGER,
    FOREIGN KEY (CLIENT_ID_FK) REFERENCES CLIENT(ID));

SELECT * FROM CLIENT;
```

And the following renaming information

**Renaming File (.JSON)**

Copy code

```
{
  "Tables": {
    "CLIENT": "USER"
  }
}
```

This would be the output code with and without renaming.

#### Snowflake output code

Copy code

```
CREATE OR REPLACE TABLE CLIENT (
    ID INTEGER,
    NAME varchar(20))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "11/13/2024",  "domain": "test" }}'
;

CREATE OR REPLACE TABLE TICKET (
    CLIENT_ID INTEGER,
       FOREIGN KEY (CLIENT_ID_FK) REFERENCES CLIENT (ID))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "11/13/2024",  "domain": "test" }}'
;

SELECT
    * FROM
    CLIENT;
```

Copy code

```
CREATE OR REPLACE TABLE USER (
    ID INTEGER,
    NAME varchar(20))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "11/13/2024",  "domain": "test" }}'
;

CREATE OR REPLACE TABLE TICKET (
    CLIENT_ID INTEGER,
       FOREIGN KEY (CLIENT_ID_FK) REFERENCES USER (ID))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "11/13/2024",  "domain": "test" }}'
;

SELECT
    * FROM
    USER;
```

Notice how all the references to “CLIENT” are renamed to “USER”.
