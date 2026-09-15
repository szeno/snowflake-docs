# Jul 18, 2025: Sensitive data classification

## Automatic classification of a database (*Preview*)

You can now set a classification profile on a database rather than a schema so that all tables and views within the database are
automatically classified for sensitive data.

For more information, see [Set a classification profile on a database](/user-guide/classify-auto#label-classify-auto-set-profile).

## Determine which databases and schemas are monitored by automatic sensitive data classification (*Preview*)

You can now call a system function to determine which tables and views are being automatically classified by sensitive data classification.
This function, SYSTEM$SHOW\_SENSITIVE\_DATA\_MONITORED\_ENTITIES, returns the databases and schemas that are associated with a classification
profile, which indicates that objects within the databases and schemas are being automatically classified at the interval specified by the
profile.

For more information, see [Determine which databases are being classified](/user-guide/classify-intro#label-classify-auto-determine-objects).
