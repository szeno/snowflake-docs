# SnowConvert AI - Scripts - Identified Objects

Note

This page of the documentation is for Teradata only.

The breakdown of all the database objects created or modified in all script files (BTEQ, BTQ, FL, ML, TPUMP, TPT).

[![The Scripts - Identified Objects section of the assessment report for Teradata.](/static/images/migrations/sc-assets/Screenshot2023-08-29at8.04.34AM.png "image")](/static/images/migrations/sc-assets/Screenshot2023-08-29at8.04.34AM.png)

## Conversion Rate - Object

Note

An object is considered successfully migrated if it does not have issues with medium, high, or critical severity.

Represents the percentage of identified objects by SnowConvert AI that were successfully migrated. This helps determine the number of objects that were successfully migrated and the objects that need manual work to complete the migration of the objects to Snowflake. If `N/A` is listed in the column, it means that the object type is not supported in Snowflake. A “`-`” could also be listed in this column. This means that the set of files migrated by SnowConvert AI did not contain objects of the specific type that could be identified.

### Formula

Copy code

```
(successfully_converted_scripts_objects / total_scripts_objects) * 100
```

#### CSV Associated Field Names

- **Tables:** ScriptTableObjectConversionRate
- **Views:** ScriptViewObjectConversionRate
- **Join Index:** ScriptJoinIndexObjectConversionRate
- **Macro:** ScriptMacroObjectConversionRate
- **Procedures:** ScriptProcedureObjectConversionRate
- **Functions:** ScriptFunctionObjectConversionRate
- **Triggers**: ScriptTriggerObjectConversionRate
- **Indexes:** N/A

#### Sample

Copy code

```
CREATE SET TABLE Tables_Database.Employee
   (Associate_Id     INTEGER)
UNIQUE PRIMARY INDEX (Associate_Id);

CRATE SET TABLE Tables_Database.Employee2
   (Associate_Id     INTEGER)
UNIQUE PRIMARY INDEX (Associate_Id);
```

Copy code

```
#*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***

import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  exec("""
    --** SSC-FDM-TD0024 - SET TABLE FUNCTIONALITY NOT SUPPORTED. TABLE MIGHT HAVE DUPLICATE ROWS **
    CREATE OR REPLACE TABLE Tables_Database.Employee (
      Associate_Id INTEGER,
      UNIQUE (Associate_Id)
    )
    """)
  #** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '5' COLUMN '1' OF THE SOURCE CODE STARTING AT 'CRATE'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'CRATE' ON LINE '5' COLUMN '1'. CODE '81'. **
  #
  #--CRATE SET TABLE Tables_Database.Employee2
  #--   (Associate_Id     INTEGER)
  #--UNIQUE PRIMARY INDEX (Associate_Id)

  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

**Expected Object Conversion Rate:** 50%

**Explanation:** With the previous sample code we will have a 50% Object Conversion Rate because only 1 of the 2 identified tables were successfully migrated to Snowflake.

## Conversion Rate - Lines of Code (LOC)

Indicates the Lines of Code conversion percentage per file extension.

### Formula

Copy code

```
(script_success_lines / script_total_lines) * 100
```

#### Associated CSV Field names

- **Tables:** ScriptTableLoCConversionRate
- **Views:** ScriptViewLocConversionRate
- **Join Index:** ScriptJoinIndexLoCConversionRate
- **Macros:** ScriptMacroLoCConversionRate
- **Procedures:** ScriptProcedureLoCConversionRate
- **Functions:** ScriptFunctionLoCConversionRate
- **Triggers**: ScriptTriggerLoCConversionRate
- **Indexes:** N/A

#### Sample

Copy code

```
CREATE SET TABLE Tables_Database.Employee
   (Associate_Id     INTEGER)
UNIQUE PRIMARY INDEX (Associate_Id);

CREATE SET TABLE Tables_Database.Employee2
   (Associate_Id     ANYTYPE!)
UNIQUE PRIMARY INDEX (Associate_Id);
```

Copy code

```
#*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***

import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  exec("""
    --** SSC-FDM-TD0024 - SET TABLE FUNCTIONALITY NOT SUPPORTED. TABLE MIGHT HAVE DUPLICATE ROWS **
    CREATE OR REPLACE TABLE Tables_Database.Employee (
      Associate_Id INTEGER,
      UNIQUE (Associate_Id)
    )
    """)
  exec("""
    --** SSC-FDM-TD0024 - SET TABLE FUNCTIONALITY NOT SUPPORTED. TABLE MIGHT HAVE DUPLICATE ROWS **
    CREATE OR REPLACE TABLE Tables_Database.Employee2 (
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '6' COLUMN '5' OF THE SOURCE CODE STARTING AT 'Associate_Id'. EXPECTED 'Column Definition' GRAMMAR. LAST MATCHING TOKEN WAS 'ANYTYPE' ON LINE '6' COLUMN '22'. CODE '15'. **
--                                                       Associate_Id     ANYTYPE!,
      UNIQUE (Associate_Id)
    )
    """)
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

**Expected LOC Conversion Rate: 83.33**%

**Explanation:** With the previous sample code we will have a 83.33% LOC Conversion Rate because line 5 of the input code `(Associate_Id ANYTYPE!)` could not be migrated and only 5 of the 6 total lines of code were migrated successfully.

Note

You can refer to further information about this topic in the [Conversion Rate Modes](../assessment-report/README#conversion-rate-modes) section of our documentation.

## Total Object Quantity

Represents the total amount of objects identified by SnowConvert AI during the parsing phase.

### CSV Associated Field Names

- **Tables:** ScriptTableTotalOccurrences
- **Views:** ScriptViewTotalOccurrences
- **Join Index:** ScriptJoinIndexTotalOccurrences
- **Macros:** ScriptMacroTotalOccurrences
- **Procedures:** ScriptProcedureTotalOccurrences
- **Functions:** ScriptFunctionTotalOccurrences
- **Triggers**: ScriptTriggerTotalOccurrences
- **Indexes:** ScriptIndexTotalOccurrences

#### Sample

Copy code

```
-- Successfully parsed table.
CREATE SET TABLE Tables_Database.Employee
   (Associate_Id     INTEGER)
UNIQUE PRIMARY INDEX (Associate_Id);

-- Table with a parsing error that could not be identified.
CRATE SET TABLE Tables_Database.Employee2
   (Associate_Id     INTEGER)
UNIQUE PRIMARY INDEX (Associate_Id);
```

Copy code

```
#*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***

import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  # Successfully parsed table.
  exec("""
    --** SSC-FDM-TD0024 - SET TABLE FUNCTIONALITY NOT SUPPORTED. TABLE MIGHT HAVE DUPLICATE ROWS **
    CREATE OR REPLACE TABLE Tables_Database.Employee (
      Associate_Id INTEGER,
      UNIQUE (Associate_Id)
    )
    """)
  #** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '7' COLUMN '1' OF THE SOURCE CODE STARTING AT 'CRATE'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'CRATE' ON LINE '7' COLUMN '1'. CODE '81'. **
  #
  #---- Table with a parsing error that could not be identified.
  #--CRATE SET TABLE Tables_Database.Employee2
  #--   (Associate_Id     INTEGER)
  #--UNIQUE PRIMARY INDEX (Associate_Id)

  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

**Expected Total Object Quantity:** 1.

**Explanation:** One table was completely parsed by SnowConvert AI during the parsing phase but the other table has a parsing error that causes SnowConvert AI to not identify it as a table object.

## Lines of Code

Represents the total number of lines of code for the identified top-level objects. It is important to take into account that the lines of code of the top-level object, as well as the comments, are used for this column. On the other hand, empty lines will not be counted in this column.

### CSV Associated Field Names

- **Tables:** ScriptTableTotalLinesOfCode
- **Views:** ScriptViewTotalLinesOfCode
- **Join Index:** ScriptJoinIndexTotalLinesOfCode
- **Macros:** ScriptMacroTotalLinesOfCode
- **Procedures:** ScriptProcedureTotalLinesOfCode
- **Functions:** ScriptFunctionTotalLinesOfCode
- **Triggers**: ScriptTriggerTotalLinesOfCode
- **Indexes:** ScriptIndexTotalLinesOfCode

#### Sample

Copy code

```
-- Hello World
CREATE SET TABLE Tables_Database.Employee
   (Associate_Id     INTEGER)
UNIQUE PRIMARY INDEX (Associate_Id);

CREATE SET TABLE Tables_Database.Employee2
   (-- hello world
   Associate_Id     ANYTYPE!)
UNIQUE PRIMARY INDEX (Associate_Id);
```

Copy code

```
#*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***

import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  # Hello World
  exec("""
    --** SSC-FDM-TD0024 - SET TABLE FUNCTIONALITY NOT SUPPORTED. TABLE MIGHT HAVE DUPLICATE ROWS **
    CREATE OR REPLACE TABLE Tables_Database.Employee (
      Associate_Id INTEGER,
      UNIQUE (Associate_Id)
    )
    """)
  # hello world
  exec("""
    --** SSC-FDM-TD0024 - SET TABLE FUNCTIONALITY NOT SUPPORTED. TABLE MIGHT HAVE DUPLICATE ROWS **
    CREATE OR REPLACE TABLE Tables_Database.Employee2 (
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '8' COLUMN '4' OF THE SOURCE CODE STARTING AT 'Associate_Id'. EXPECTED 'Column Definition' GRAMMAR. LAST MATCHING TOKEN WAS 'ANYTYPE' ON LINE '8' COLUMN '21'. CODE '15'. **
--   Associate_Id     ANYTYPE!,
      UNIQUE (Associate_Id)
    )
    """)
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

**Expected Lines of Code:** 8

**Explanation:** In this case, we have 6 lines that come from the code used for the `CREATE TABLE` statements and 2 for comments that are inside of the top-level objects.

## Parsing Errors

Represents the number of parsing errors that are inside of the identified objects.

### CSV Associated Field Names

- **Tables:** ScriptTableTotalParsingErrors
- **Views:** ScriptViewTotalParsingErrors
- **Join Index:** ScriptJoinIndexTotalParsingErrors
- **Macros:** ScriptMacroTotalLinesOfCode
- **Procedures:** ScriptProcedureTotalParsingErrors
- **Functions:** ScriptFunctionTotalParsingErrors
- **Triggers**: ScriptTriggerTotalParsingErrors
- **Indexes:** ScriptIndexTotalParsingErrors

#### Sample

Copy code

```
-- Successfully parsed table.
CREATE SET TABLE Tables_Database.Employee
   (Associate_Id     INTEGER)
UNIQUE PRIMARY INDEX (Associate_Id);

-- Table with a parsing error that could not be identified.
CRATE SET TABLE Tables_Database.Employee2
   (Associate_Id     INTEGER)
UNIQUE PRIMARY INDEX (Associate_Id);
```

Copy code

```
#*** Generated code is based on the SnowConvert AI Python Helpers version 2.0.6 ***

import os
import sys
import snowconvert.helpers
from snowconvert.helpers import Export
from snowconvert.helpers import exec
from snowconvert.helpers import BeginLoading
con = None
def main():
  snowconvert.helpers.configure_log()
  con = snowconvert.helpers.log_on()
  # Successfully parsed table.
  exec("""
    --** SSC-FDM-TD0024 - SET TABLE FUNCTIONALITY NOT SUPPORTED. TABLE MIGHT HAVE DUPLICATE ROWS **
    CREATE OR REPLACE TABLE Tables_Database.Employee (
      Associate_Id INTEGER,
      UNIQUE (Associate_Id)
    )
    """)
  #** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '7' COLUMN '1' OF THE SOURCE CODE STARTING AT 'CRATE'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'CRATE' ON LINE '7' COLUMN '1'. CODE '81'. **
  #
  #---- Table with a parsing error that could not be identified.
  #--CRATE SET TABLE Tables_Database.Employee2
  #--   (Associate_Id     INTEGER)
  #--UNIQUE PRIMARY INDEX (Associate_Id)

  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()
```

**Expected Parsing Errors:** 1

**Explanation:** Only one parsing error will be reported in the **Parsing Errors** column because SnowConvert AI was able to only identify the first table. Since the second table was not identified, those parsing errors will not be counted in the **Parsing Errors** column.
