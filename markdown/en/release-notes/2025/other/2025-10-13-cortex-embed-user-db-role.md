# Oct 13, 2025: CORTEX\_EMBED\_USER database role (*General availability*)

Snowflake has added a CORTEX\_EMBED\_USER database role in the SNOWFLAKE database to better manage access to Cortex
embedding functions. Embedding functions, which convert text to a vector of numbers that represent the meaning of the
text, include AI\_EMBED, EMBED\_TEXT\_768, and EMBED\_TEXT\_1024. This new role allows you to grant users access to embedding
functions without granting them access to other Cortex features. The pre-existing CORTEX\_USER role continues to provide
access to Cortex features including embedding functions.

For more information about this role, see [SNOWFLAKE.CORTEX\_EMBED\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-embed-user).
