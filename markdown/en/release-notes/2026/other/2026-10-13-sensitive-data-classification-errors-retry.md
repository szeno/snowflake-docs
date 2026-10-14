# Oct 13, 2026: Sensitive data classification error and retry updates

With this release, sensitive data classification provides more specific error messages when automatic classification fails.

The [DATA\_CLASSIFICATION\_LATEST](/sql-reference/account-usage/data_classification_latest) view now reports a defined set of
`ERROR_MESSAGE` values. When available, each message includes the originating Snowflake error code so you can identify why a table failed
classification.

For more information, see [Troubleshooting sensitive data classification](/user-guide/classify-troubleshooting) and [DATA\_CLASSIFICATION\_LATEST view](/sql-reference/account-usage/data_classification_latest).
