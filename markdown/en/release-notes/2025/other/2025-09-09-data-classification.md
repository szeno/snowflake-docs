# Sep 09, 2025: Sensitive data classification

## Classifying views automatically (*General availability*)

You can now configure sensitive data classification so the views in a database are automatically classified at regular intervals.
Previously, only tables could be classified automatically.

## Excluding objects from automatic classification (*Preview*)

By default, Snowflake automatically classifies all sensitive data in a database that has a classification profile set on it. You can now
configure Snowflake to exclude schemas, tables, or columns from automatic classification so that they are skipped during the classification
process.

For more information, see [Excluding data from sensitive data classification](/user-guide/classify-auto-exclude).
