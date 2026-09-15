# Apr 2, 2026: Copy tags when running a CREATE OR REPLACE TABLE command (*General availability*)

With this release, the COPY TAGS parameter for the CREATE OR REPLACE TABLE command is generally available.

- When you use CREATE OR REPLACE TABLE … COPY TAGS without LIKE, CLONE, or a WITH TAG clause, tags from the replaced table
  and its columns are retained on the new table.
- When you use COPY TAGS with CREATE OR REPLACE TABLE … LIKE, CREATE OR REPLACE TABLE … CLONE, or together with
  a WITH TAG clause, Snowflake combines tags from the applicable sources. If both sources set the same tag, the value
  from the replaced table takes precedence.

For more information, see the COPY TAGS parameter and usage notes in [CREATE TABLE](/sql-reference/sql/create-table).
