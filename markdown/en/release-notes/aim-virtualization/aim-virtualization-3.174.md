# Jul 19, 2026: AIM-Virtualization 3.174

## New features

### Broader Teradata SQL compatibility

- Added support for QUALIFY, SELECT NORMALIZE, XMLEXTRACT, JSON\_CHECK, and EXISTVALUE

### Date and time

- Added TIMESTAMP WITH TIME ZONE support

### Functions

- Added EDITDISTANCE support via Damerau-Levenshtein UDF

### Stored procedure support

- Added JSON type in DECLARE and SQL/PSM class 45 SQLSTATE handlers

## Bug fixes

### Numeric and string formatting

- Fixed FLOAT-to-TEXT, DECIMAL dot placement, and trailing-zero formatting
- Corrected FORMAT directives (E4, X(N), Z(I)/9(I), leading-sign patterns)

### Function correctness

- Fixed TRY\_CAST with mixed types, LPAD/RPAD null handling, and case-insensitive INDEX/POSITION
- Corrected multi-character STRTOK delimiter handling

### Date and time

- Fixed INTERVAL HOUR TO SECOND handling and temporal precision propagation

### Identifier and metadata handling

- Fixed non-ASCII identifier resolution and special characters in SHOW commands
