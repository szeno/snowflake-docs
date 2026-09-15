# Jul 31, 2026: AIM-Virtualization 3.175

## New features

### SQL compatibility

- Added IDENTITY column support with the CYCLE option
- Added multi-column UNPIVOT support
- Added TABLE VARYING USING FUNCTION for polymorphic table functions

### Functions

- Added JSONExtractValue method support
- Added FROM\_BYTES function support
- Added HASHBUCKET() function support
- Added BYTE/VARBYTE argument support in BITAND, BITOR, and BITXOR functions

### Date and time

- Added CAST support for TIME WITH TIME ZONE using numeric timezone offsets
- Added AM/PM and timezone format codes in date formatting

## Bug fixes

### Query correctness

- Fixed incorrect column reference resolution
- Fixed GROUP BY errors when SELECT uses both aggregates and aliases
- Fixed errors on scalar subqueries without a FROM clause using forward aliases
- Fixed QUALIFY incorrectly referencing SELECT-list aliases
- Fixed column extraction errors in subqueries containing QUALIFY, SAMPLE, and WINDOW clauses
- Fixed parse errors on non-ASCII characters in SQL comments

### Date and time

- Fixed return type mismatch for functions returning timezone-aware timestamps
- Applied session date format settings at connection time
- Fixed TIME type format conversion errors
- Fixed crash on unrecognized date format tokens

### Function correctness

- Fixed ASCII() returning incorrect values for multi-byte characters
- Fixed precision loss in FLOAT-returning stored functions
- Fixed errors on BYTEINT column operations
- Fixed FLOAT precision loss and overflow crash on Iceberg tables
- Improved REGEXP performance for repeated patterns

### Security

- Restricted admin commands to authorized Snowflake roles

### Connectivity

- Fixed errors in ODBC catalog metadata commands
