# Troubleshooting Snowflake Data Clean Rooms

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

This page is a general troubleshooting guide when using clean rooms. If you are using the API, be sure to read the reference documentation for any procedures that you call, as well as the use case guidelines, to see if your issue is covered there.

## Installation issues

- See the [installation troubleshooting section](/user-guide/cleanrooms/v1/enable-clean-rooms-ui#label-dcr-troubleshooting-installation).
- Confirm that you have [updated your network policy](/user-guide/cleanrooms/admin-tasks#label-cleanrooms-configure-network-policy) to allow the UI to access your data.

## Analysis and template issues

Error:
:   `Failure during expansion of shared view <CLEAN ROOM VIEW NAME> as view owner: Insufficient permission to resolve external/iceberg table <TABLE_NAME> shared by application SAMOOHA_CLEANROOM_APP_<CLEAN ROOM ID>`

Cause:
:   You are trying to access external or Iceberg tables, but External and Iceberg tables are not enabled in both the provider’s and consumer’s accounts.

Solution:
:   Ensure that both provider and consumer accounts have [enabled external and Iceberg tables](/user-guide/cleanrooms/register-data#label-cleanrooms-external-iceberg-tables).

---

Error:
:   `SQL compilation error: Failure during expansion of shared view '<CLEAN ROOM VIEW NAME>' as view owner: Object '<some object name>' does not exist or not authorized.`

Cause:
:   Clean room grants no longer exist on the dataset that you are trying to access. Most likely this is because the source object has been renamed or replaced.

Solution:
:   - If the table was renamed, change the name back to what is linked in the clean room. You might need to re-register the object as well.
    - If the table was recreated, register the object again in the clean room.

---

Error:
:   Query returns zero results and you think that’s wrong.

Possible causes and solutions:
:   - Confirm that neither side has a masking policy on the data that could prevent it from being joined or shown.
    - Confirm that the join columns are formatted the same way.
    - Confirm that you are not falling below any fixed threshold settings. The audience overlap has a default threshold of five, meaning that
      fewer than five rows will be omitted from the results. Ask the provider what the threshold is, and confirm whether you have any overlaps
      greater than that number; temporarily modify the overlap specifications to guarantee large segment groups to see whether you get
      results then.

---

Error:
:   `Uncaught exception of type 'STATEMENT_ERROR' ... SQL compilation error: invalid URL prefix found ...`

Cause:
:   The template uses a string value, rather than identifier, for a column or table name. This happens when the template doesn’t properly
    convert string variables into identifiers by using either the `sqlsafe` filter or the `IDENTIFIER` function.

    For example, passing in `p.col1` to `my_column` to the template `SELECT {{ my_column }} ...` resolves to
    `SELECT "p.col1" ...`. “p.col1” is a string, not a valid identifier (and `p.` is interpreted as a URL prefix).

Solution:
:   Apply either the IDENTIFIER function (preferred) or the `sqlsafe` filter to the variable:

    - `SELECT IDENTIFIER({{ my_column }}) ...` *(Preferred)*
    - `SELECT {{ my_column | sqlsafe }} ...`

---

Error:
:   `FAILURE: Unauthorized columns: column_name`

Cause:
:   Your query uses a column of collaborator data that is not part of the collaborator’s usage policy in the clean room. For example, you are
    trying to SELECT a column of collaborator data that is not in their column policy.

Solution:
:   Use a column that your collaborator has approved for projection, joining, or activation in your query. Inspect the template for policy
    filters by calling `consumer.view_template_definition`, then see which columns the provider allows you to project or join by calling
    `consumer.view_provider_join_policy` or `consumer.view_provider_column_policy`. Finally either update your query to pass in an
    approved column, or ask your collaborator to adjust their usage policy to include the column that you want to use.

---

Error:
:   `**FAILURE**: Invalid aliases: P.{column name}'` or `**FAILURE**: Invalid aliases: C.{column name}'`

Cause:
:   You are using uppercase `P` or `C` table aliases to scope a column name. You must use lowercase `p` or `c` aliases when scoping a column name. (The template itself can use either uppercase or lowercase when *declaring* the alias.)

Solution:
:   Always use a lowercase alias when scoping a column.

    > **Example:**

    Copy code

    ```
    -- Always scope the column name with a lowercase alias.
    -- The casing of the alias declared for the table doesn't matter.

    -- These will fail.
    SELECT P.hashed_email FROM mydb.mysch.t1 AS P;
    SELECT P.hashed_email FROM mydb.mysch.t1 AS p;

    -- These will succeed.
    SELECT p.hashed_email FROM mydb.mysch.t1 AS P;
    SELECT p.hashed_email FROM mydb.mysch.t1 AS p;
    ```

---

Error:
:   `**FAILURE**: Invalid aliases: {database name}.{schema name}.{column name}`

Cause:
:   You must always reference columns using the `p` or `c` alias declared for a table. Columns can’t reference a table by its full path.

    **Invalid:** `SELECT hashed_email FROM mydb.mysch.t1;`

Solution:
:   Use the `p` or `c` (lowercase!) table alias when referencing a column:

    **Valid:** `SELECT p.hashed_email FROM mydb.mysch.t1 AS p;`

## Cross-cloud issues

Error:
:   `Analysis Execution Failure: 'SnowparkSQLException' due to Database Listing Conflict` in a single-account testing clean room

Cause:
:   Cross-Cloud Auto-Fulfillment is not supported with single-account testing clean rooms.

Solution:
:   Disable cross-cloud auto-fulfillment in this clean rooms account by calling `library.disable_laf_on_account` during testing, or don’t
    try to make cross-cloud procedure calls in this clean room.

## Cloud data connector issues

If you are having problems with an external data connector for AWS, Azure, or Google Cloud Storage, see [Snowflake Data Clean Rooms: Troubleshooting external data connectors](/user-guide/cleanrooms/external-data-troubleshoot).

## Request log issues

Error:
:   `**Failure**: Request logs unable to be mounted. Try again.`

Cause:
:   Mounting request logs succeeded for internal clean room, then fails for external clean room in same account. Internal clean rooms have fewer requirements than external clean rooms. Your installation met the requirements for using internal clean rooms, but not for external clean rooms.

Solution:
:   Confirm that your email was validated by clean rooms, and that you fulfill all the [clean rooms account requirements](/user-guide/cleanrooms/installing-dcr#label-cleanroom-account-requirements).

## Data access issues

### General guidelines about data access issues

You can get an error message that reports the inability to access a data source during several points in the usage flow:

**If the error occurred during the registration process:**

- You misspelled the table name or path, if using the API.
- If this is an external or Iceberg table, confirm that you have fulfilled the [requirements and procedure](/user-guide/cleanrooms/register-data#label-cleanrooms-external-iceberg-tables) for registering an external or Iceberg table.
- Confirm that your current role has the REFERENCE\_USAGE privilege on the object being registered.

**If the error occurred during the linking process:**

- In the API, you might be using the wrong role.
- The object might not have been registered. In the API if you try to link an object that isn’t registered, you will see an error. In the UI, you should see only objects that have been registered as available for linking.
- Confirm that SAMOOHA\_APP\_ROLE has USAGE and SELECT privileges on your object.
- The table might have been moved, renamed, or had its permissions (or any Snowflake policy permissions) changed since registration. When this happens, you might also see the error *SQL access control error: Insufficient privileges to operate on table…*

**If the error occurred after data was successfully registered and linked:**

If using the API, confirm that you spelled the fully qualified table name correctly.

### Data access errors

Error:
:   *Object ‘<some\_object\_name>’ does not exist or not authorized*

Cause:
:   The source table might have been moved, renamed, or had its permissions (or permissions on a policy or ancestor object that it depends on) changed.

Solution:
:   Try re-registering and re-linking the object in your account, or move the object back to the old location, or revert any additional permissions added.

---

Error:
:   *Insufficient permission to resolve external/iceberg table*

Cause:
:   If an external or Iceberg table is involved in your query, then the table was not registered properly.

Solution:
:   See [Enabling external and Apache Iceberg™ tables](/user-guide/cleanrooms/register-data#label-cleanrooms-external-iceberg-tables) to ensure that you fulfill the requirements and procedures to use these table types. You can sometimes resolve this by explicitly granting SELECT on the table to SAMOOHA\_BY\_SNOWFLAKE.

---

Error:
:   *not approved:unauthorized columns used* error as a result of run analysis

Cause:
:   You are joining or projecting a collaborator’s column against the collaborator’s join or column policy.

Solution:
:   View the join and column policies set by your collaborator by calling `consumer.view_provider_column_policy` and `consumer.view_provider_join_policy`.

    Copy code

    ```
    CALL samooha_by_snowflake_local_db.consumer.view_provider_join_policy($cleanroom_name);
    CALL samooha_by_snowflake_local_db.consumer.view_provider_column_policy($cleanroom_name);
    ```

    You might have also exhausted your privacy budget:

    Copy code

    ```
    CALL samooha_by_snowflake_local_db.consumer.view_remaining_privacy_budget($cleanroom_name);
    ```

---

Error:
:   When the consumer calls any procedure that takes a clean room name and gets
    `Application 'SAMOOHA_CLEANROOM_APP<some name>' does not exist or not authorized.`

Cause:
:   If the clean room name is reported as *SAMOOHA\_CLEANROOM\_APP<cleanroom name>* rather than *SAMOOHA\_CLEANROOM\_APP*<cleanroom name>\_,
    (missing the underscore after `SAMOOHA_CLEANROOM_APP`), the *provider* did not install the clean rooms environment in the correct way
    in their account.

Solution:
:   Tell the provider that they should install the clean rooms environment in their account by following the instructions here:
    [Installing the Snowflake Data Clean Rooms environment](/user-guide/cleanrooms/installing-dcr). After that, the provider can re-create and share the clean room.

## External and Iceberg table issues

Error:
:   `Failure during expansion of shared view <CLEAN ROOM VIEW NAME> as view owner: Insufficient permission to resolve external/iceberg table <TABLE_NAME> shared by application SAMOOHA_CLEANROOM_APP_<CLEAN ROOM ID>`

Cause:
:   External or Iceberg tables are not enabled in both the provider and consumer accounts.

Solution:
:   Ensure that both provider and consumer accounts have [enabled external and Iceberg tables](/user-guide/cleanrooms/register-data#label-cleanrooms-external-iceberg-tables).

---

Error:
:   Consumer gets *Invalid restricted feature ‘external\_data’* when linking in an external or Iceberg table.

Cause:
:   The provider has not yet enabled external and Iceberg tables.

Solution:
:   The provider must complete the process of [enabling external and Iceberg tables for their account](/user-guide/cleanrooms/register-data#label-cleanrooms-external-iceberg-tables). If they are doing this in code, the provider must check the security scan results and, if successful, must update the default release version.

---

Error:
:   *Insufficient permission to resolve external/iceberg table* error when running an analysis involving an external or Iceberg table.

Cause:
:   The table was probably not registered properly by both the provider and consumer.

Solution:
:   [Read the external and Iceberg table registration information](/user-guide/cleanrooms/register-data#label-cleanrooms-external-iceberg-tables) and be sure to follow all instructions on both the provider and consumer side.
