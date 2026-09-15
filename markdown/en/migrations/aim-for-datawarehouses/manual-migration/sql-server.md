# SnowConvert AI CLI - SQL Server

## Specific CLI arguments

### `-u, --usedatabase`

Flag to indicate whether the Transact-SQL USE statement should be translated.

### `-p, --arrange <ARRANGE OPTION>` [`<ARRANGE OPTION>`]

Flag to indicate whether to preprocess or arrange the source code before its transformation. By default, it’s set to FALSE.

| Arrange Option | Description |
| --- | --- |
| prettyprint | Applies indentation to the original code and gets it well organized. |
| generatereports | Generates extra reports after the arrangement. |
| multiple | Applies arrangement to multiple databases represented as multiple folders, and keeps their original structure. |
