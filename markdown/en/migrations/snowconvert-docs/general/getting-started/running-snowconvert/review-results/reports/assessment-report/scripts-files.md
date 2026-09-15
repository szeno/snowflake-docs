# SnowConvert AI - Scripts - Files

Note

This page of the documentation is for Teradata only.

[![The Scripts - Files section of the assessment report for Teradata.](/static/images/migrations/sc-assets/image(396).png "image")](/static/images/migrations/sc-assets/image(396).png)

## Conversion Rate - Files Generated

Indicates the file generation percentage grouped by valid file extension (shown in the image above).

Note

You can refer to further information about this topic in the [Conversion Rate Modes](../../../../../getting-started/running-snowconvert/review-results/reports/assessment-report/README#conversion-rate-modes) section of our documentation.

### Formula

Copy code

```
(successfully_generated_files / total_valid_files) * 100
```

#### Associated CSV Field names

- **BTEQ Files Conversion Rate:** BTEQFilesConversionRate
- **FastLoad Files Conversion Rate:** FastLoadFilesConversionRate
- **MultiLoad Files Conversion Rate**: MultiLoadFilesConversionRate
- **TPT Files Conversion Rate**: TPTFilesConversionRate
- **TPump Files Conversion Rate**: TPumpFilesConversionRate

## Conversion Rate - Lines of Code (LOC)

Indicates the Lines of Code conversion percentage per file extension.

### Formula

Copy code

```
(successfully_converted_lines / total_line_amount_per_file_extension) * 100
```

#### Associated CSV Field names

- **BTEQ LOC Conversion Rate:** BTEQLoCConversionRate
- **FastLoad LOC Conversion Rate**: FastLoadLoCConversionRate
- **MultiLoad LOC Conversion Rate**: MultiLoadLoCConversionRate
- **TPT LOC Conversion Rate**: TPTLoCConversionRate
- **TPump LOC Conversion Rate**: TPumpLoCConversionRate

## Total File Quantity

Indicates the total amount of files of each type. It is used to calculate the `Files Generated` conversion rate.

### Associated CSV Field names

- **BTEQ Total File Quantity**: BTEQFileCount
- **FastLoad Total File Quantity:** FastLoadFileCount
- **MultiLoad Total File Quantity:** MultiLoadFileCount
- **TPT Total File Quantity:** TPTFileCount
- **TPump Total File Quantity:** TPumpFileCount

#### Sample

Copy code

```
input folder
  ├> one.bteq
  ├> two.tpt
  ├> three.doc
  └> readme.txt
```

Copy code

```
output folder
  ├> one_bteq.py
  └> two_tpt.py
```

From the previous, we will get:

- Number of BTEQ files: 1
- Number of TPT files: 1

## Total LOC

Indicates the total amount of lines of code per file extension. It is used to calculate the `Lines of Code` conversion..

### Associated CSV Field names

- **BTEQ Total LOC:** BTEQLinesCount
- **FastLoad Total LOC:** FastLoadLinesCount
- **MultiLoad Total LOC:** MultiLoadLinesCount
- **TPT Total LOC:** TPTLinesCount
- **TPump Total LOC:** TPumpLinesCount

Indicates the total amount of parsing errors per file extension.

#### Associated CSV Field names

- **BTEQ Total Parsing Errors:** BTEQTotalParsingErrors
- **FastLoad Total Parsing Errors:** FastLoadTotalParsingErrors
- **MultiLoad Total Parsing Errors:** MultiLoadTotalParsingErrors
- **TPT Total Parsing Errors:** TPTTotalParsingErrors
- **TPump Total Parsing Errors:** TPumpTotalParsingErrors

#### Sample

Copy code

```
CREATE TABLE TABLE_INVALID [
  first_column INTEGER
];
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
  snowconvert.helpers.quit_application()

if __name__ == "__main__":
  main()

#** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '1' COLUMN '1' OF THE SOURCE CODE STARTING AT 'CREATE'. EXPECTED 'STATEMENT' GRAMMAR. LAST MATCHING TOKEN WAS 'CREATE' ON LINE '1' COLUMN '1'. CODE '81'. **
#--CREATE TABLE TABLE_INVALID [
#--  first_column INTEGER
#--]
```

**Explanation**: In the above example, there is a parsing error when creating the table due to the incorrect use of the square brackets (`[]`), lines 1 and 3. This will be shown in the report as 1 parsing error in the TPT files row.
