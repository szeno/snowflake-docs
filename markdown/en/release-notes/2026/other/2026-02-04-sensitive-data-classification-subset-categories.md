# Feb 04, 2026: Sensitive data classification: Classify a subset of native semantic categories (*Preview*)

You can now configure sensitive data classification to limit which types of data are classified as sensitive.
By default, Snowflake classifies data into all [native semantic categories](/user-guide/classify-native) whenever Snowflake identifies
sensitive data. You can now specify a subset of semantic categories so Snowflake classifies data only if it belongs
to the categories you specify.

You can specify a subset of semantic categories in the following ways:

- **Based on the semantic category**: For example, configure sensitive data classification so tax identifiers (the TAX\_IDENTIFIER semantic
  category) are classified as sensitive, but other semantic categories (for example, POSTAL\_CODE) are not.
- **Based on a country**: For example, configure Snowflake to classify identifiers in the United States
  as sensitive data, but not identifiers in other countries.

For more information, see [Classify data using a subset of native semantic categories](/user-guide/classify-auto#label-classify-auto-subset).
