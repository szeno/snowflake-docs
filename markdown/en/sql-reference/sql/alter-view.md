# ALTER VIEW

Modifies the properties for an existing view. Currently the only supported operations are:

- Renaming a view.
- Converting to (or reverting from) a secure view.
- Adding, overwriting, removing a comment for a view.

Note that you cannot use this command to change the definition for a view. To change the view definition, you must drop the view and
then recreate it.

See also:
:   [CREATE VIEW](/sql-reference/sql/create-view) , [DROP VIEW](/sql-reference/sql/drop-view) , [SHOW VIEWS](/sql-reference/sql/show-views) , [DESCRIBE VIEW](/sql-reference/sql/desc-view)

## Syntax

Copy code

```
ALTER VIEW [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER VIEW [ IF EXISTS ] <name> SET
  [ SECURE ]
  [ CHANGE_TRACKING =  { TRUE | FALSE } ]
  [ CONTACT <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ]
  [ COMMENT = '<string_literal>' ]

ALTER VIEW [ IF EXISTS ] <name> UNSET
  [ SECURE ]
  [ CONTACT <purpose> ]
  [ COMMENT = '<string_literal>' ]
  [ DCM PROJECT ]

ALTER VIEW <name> dataMetricFunctionAction

ALTER VIEW [ IF EXISTS ] <name> dataGovnPolicyTagAction
```

Where:

> Copy code
>
> ```
> dataMetricFunctionAction ::=
>
>     SET DATA_METRIC_SCHEDULE = {
>         '<num> MINUTE'
>       | 'USING CRON <expr> <time_zone>'
>       | 'TRIGGER_ON_CHANGES'
>     }
>
>   | UNSET DATA_METRIC_SCHEDULE
>
>   | ADD DATA METRIC FUNCTION <metric_name>
>       ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] )
>       [ WITHIN GROUP ( <group_col1> [ , <group_col2> ... ] )
>         [ GROUP LIMIT <integer> ] ]
>       [ FILTER ( <predicate> ) ]
>       [ EXPECTATION <expectation_name> ( <expression> )
>         [, <expectation_name> ( <expression> ) [ , ... ] ] ]
>       [ EXECUTE AS ROLE <role_name> ]
>       [ ANOMALY_DETECTION = { TRUE | FALSE } ]
>       [ SENSITIVITY = { 'LOW' | 'MEDIUM' | 'HIGH' } ]
>       [ , <metric_name_2> ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] ) ]
>         [ WITHIN GROUP ( <group_col1> [ , <group_col2> ... ] )
>           [ GROUP LIMIT <integer> ] ]
>         [ FILTER ( <predicate> ) ]
>         [ EXPECTATION <expectation_name> ( <expression> )
>           [, <expectation_name> ( <expression> ) [ , ... ] ] ]
>         [ EXECUTE AS ROLE <role_name> ]
>         [ ANOMALY_DETECTION = { TRUE | FALSE } ]
>         [ SENSITIVITY = { 'LOW' | 'MEDIUM' | 'HIGH' } ]
>
>   | DROP DATA METRIC FUNCTION <metric_name>
>       ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] )
>       [ , <metric_name_2> ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] ) ]
>
>   | MODIFY DATA METRIC FUNCTION <metric_name>
>       ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] )
>         { SUSPEND | RESUME }
>       [ , <metric_name_2> ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] )
>         { SUSPEND | RESUME } ]
>
>   | MODIFY DATA METRIC FUNCTION <metric_name>
>       ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] )
>       { ADD | MODIFY } EXPECTATION <expectation_name> ( <expression> )
>           [, <expectation_name> ( <expression> ) [ , ... ] ]
>
>   | MODIFY DATA METRIC FUNCTION <metric_name>
>       ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] )
>       DROP EXPECTATION <expectation_name> [ , <expectation_name> [ , ... ] ]
>
>   | MODIFY DATA METRIC FUNCTION <metric_name>
>       ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] )
>       FILTER ( [ <predicate> ] )
>       [ , <metric_name_2> ON ( <col_name> [ , ... ] [ , TABLE <table_name>( <col_name> [ , ... ] ) ] )
>         FILTER ( [ <predicate> ] ) ]
>
>   | MODIFY DATA METRIC FUNCTION <metric_name>
>       SET <list_of_properties>
> ```
>
> Copy code
>
> ```
> dataGovnPolicyTagAction ::=
>   {
>       SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]
>     | UNSET TAG <tag_name> [ , <tag_name> ... ]
>   }
>   |
>   {
>       ADD ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , ... ] )
>     | DROP ROW ACCESS POLICY <policy_name>
>     | DROP ROW ACCESS POLICY <policy_name> ,
>         ADD ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , ... ] )
>     | DROP ALL ROW ACCESS POLICIES
>   }
>   |
>   {
>       SET AGGREGATION POLICY <policy_name>
>         [ ENTITY KEY ( <col_name> [, ... ] ) ]
>         [ FORCE ]
>     | UNSET AGGREGATION POLICY
>   }
>   |
>   {
>       SET JOIN POLICY <policy_name>
>         [ FORCE ]
>     | UNSET JOIN POLICY
>   }
>   |
>   ADD [ COLUMN ] [ IF NOT EXISTS ] <col_name> <col_type>
>     [ [ WITH ] MASKING POLICY <policy_name>
>           [ USING ( <col1_name> , <cond_col_1> , ... ) ] ]
>     [ [ WITH ] PROJECTION POLICY <policy_name> ]
>     [ [ WITH ] TAG ( <tag_name> = '<tag_value>'
>           [ , <tag_name> = '<tag_value>' , ... ] ) ]
>   |
>   {
>     { ALTER | MODIFY } [ COLUMN ] <col1_name>
>         SET MASKING POLICY <policy_name>
>           [ USING ( <col1_name> , <cond_col_1> , ... ) ] [ FORCE ]
>       | UNSET MASKING POLICY
>   }
>   |
>   {
>     { ALTER | MODIFY } [ COLUMN ] <col1_name>
>         SET PROJECTION POLICY <policy_name>
>           [ FORCE ]
>       | UNSET PROJECTION POLICY
>   }
>   |
>   { ALTER | MODIFY } [ COLUMN ] <col1_name> SET TAG
>       <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]
>       , [ COLUMN ] <col2_name> SET TAG
>           <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]
>   |
>   { ALTER | MODIFY } [ COLUMN ] <col1_name> UNSET TAG <tag_name> [ , <tag_name> ... ]
>                    , [ COLUMN ] <col2_name> UNSET TAG <tag_name> [ , <tag_name> ... ]
> ```

## Parameters

`name`
:   Specifies the identifier for the view to alter. If the identifier contains spaces or special characters, the entire string must be enclosed
    in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`RENAME TO new_name`
:   Specifies the new identifier for the view; must be unique for the schema.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When an object is renamed, other objects that reference it must be updated with the new name.

`SET ...`
:   Specifies the property to set for the view:

    `SECURE`
    :   Specifies a view as secure.

    `CHANGE_TRACKING = { TRUE | FALSE }`
    :   Specifies to enable or disable change tracking on the table.

        - `TRUE` enables change tracking on the view, and cascades the setting to all underlying tables.
        - `FALSE` disables change tracking on the view, and cascades the setting to all underlying tables.

    `CONTACT purpose = contact [ , purpose = contact ... ]`
    :   Associate the existing object with one or more [contacts](/user-guide/contacts-using). For a list of valid purposes, see [Associate a contact with an object](/user-guide/contacts-using#label-contacts-associate).

        You cannot set the CONTACT property with other properties in the same statement.

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the view.

    Note

    You must set each view property individually.

`UNSET ...`
:   Specifies the property to unset for the view, which resets it to the default:

    - `SECURE`
    - `CONTACT purpose`
    - `COMMENT`

    When resetting a property, specify only the name; specifying a value for the property will return an error.

    Note

    You must reset each view property individually.

`UNSET DCM PROJECT`

> Detaches the view from the [DCM project](/user-guide/dcm-projects/dcm-projects-overview) that currently manages it.
> The command removes the association between the view and the DCM project without dropping the view. See [Detach objects from a DCM project](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-detach-object) for more information.

## Data metric function actions (`dataMetricFunctionAction`)

`DATA_METRIC_SCHEDULE ...`
:   Specifies the schedule to run the data metric function periodically.

    `'num MINUTE'`
    :   Specifies an interval (in minutes) of wait time inserted between runs of the data metric function. Accepts positive integers only.

        Also supports `num M` syntax.

        For data metric functions, use one of the following values: `5`, `15`, `30`, `60`, `720`, or `1440`.

        If you want to suspend all DMFs associated with the object, set the parameter to an empty string.

        Default: `60 MINUTE`

    `'USING CRON expr time_zone'`
    :   Specifies a cron expression and time zone for periodically running the data metric function. Supports a subset of standard cron utility
        syntax.

        For a list of time zones, see the [list of tz database time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

        The cron expression consists of the following fields, and the periodic interval must be at least 5 minutes:

        Copy code

        ```
        # __________ minute (0-59)
        # | ________ hour (0-23)
        # | | ______ day of month (1-31, or L)
        # | | | ____ month (1-12, JAN-DEC)
        # | | | | _ day of week (0-6, SUN-SAT, or L)
        # | | | | |
        # | | | | |
          * * * * *
        ```

        The following special characters are supported:

        `*`
        :   Wildcard. Specifies any occurrence of the field.

        `L`
        :   Stands for “last”. When used in the day-of-week field, it allows you to specify constructs such as “the last Friday” (“5L”) of
            a given month. In the day-of-month field, it specifies the last day of the month.

        `/{n}`
        :   Indicates the *nth* instance of a given unit of time. Each quanta of time is computed independently. For example, if `4/3` is
            specified in the month field, then the data metric function is scheduled for April, July and October (i.e. every 3 months, starting
            with the 4th month of the year). The same schedule is maintained in subsequent years. That is, the data metric function is

            not scheduled to run in January (3 months after
            the October run).

        Note

        - The cron expression currently evaluates against the specified time zone only. Altering the [TIMEZONE](/sql-reference/parameters#label-timezone) parameter value
          for the account (or setting the value at the user or session level) does not change the time zone for the data metric
          function.
        - The cron expression defines all valid run times for the data metric function. Snowflake attempts to run a data metric
          function based on this schedule; however, any valid run time is skipped if a previous run has not completed before the next valid
          run time starts.
        - When both a specific day of month and day of week are included in the cron expression, then the data metric function is scheduled
          on days satisfying either the day of month or day of week. For example,
          `DATA_METRIC_SCHEDULE = 'USING CRON 0 0 10-20 * TUE,THU UTC'` schedules a data metric function at 0AM on any 10th to 20th day
          of the month and also on any Tuesday or Thursday outside of those dates.
        - The shortest granularity of time in cron is minutes.

          If a data metric function is resumed during the minute defined in its cron expression, the first scheduled run of the data metric
          function is the next occurrence of the instance of the cron expression. For example, if data metric function scheduled to run daily
          at midnight (`USING CRON 0 0 * * *`) is resumed at midnight plus 5 seconds (`00:00:05`), the first data metric function run
          is scheduled for the following midnight.

    `'TRIGGER_ON_CHANGES'`
    :   Specifies that the DMF runs when a [DML operation](/sql-reference/sql-dml) modifies the table, such as inserting a new row or
        deleting a row.

        You can specify `'TRIGGER_ON_CHANGES'` for the following objects:

        - Dynamic tables
        - External tables
        - Apache Iceberg™ tables
        - Regular tables
        - Temporary tables
        - Transient tables

        You cannot specify `'TRIGGER_ON_CHANGES'` for views.

        Changes to the table as a result of [reclustering](/user-guide/tables-auto-reclustering) do not trigger the DMF to run.

`UNSET DATA_METRIC_SCHEDULE`
:   Resets the schedule for DMFs associated with the object to the default of `60 MINUTE`.

    If you want to suspend DMFs associated with the object, run a `SET DATA_METRIC_SCHEDULE = ''` statement instead.

`{ ADD | DROP } DATA METRIC FUNCTION metric_name`
:   Identifier of the data metric function to add to the table or view or drop from the table or view.

    `ON ( col_name [ , ... ] [ , TABLE( table_name( col_name [ , ... ] ) ) ] )`
    :   The table or view columns on which to associate the data metric function. The data types of the columns must match the data types of
        the columns specified in the data metric function definition.

        If the data metric function accepts a second table as an argument, specify the fully qualified name of the table and its columns.

    `EXPECTATION expectation_name ( expression ) [, expectation_name ( expression ) [ , ... ] ]`
    :   Defines one or more [expectations](/user-guide/data-quality-expectations) for the association between the column and the DMF.

    `[ , metric_name_2 ON ( col_name [ , ... ] [ , TABLE( table_name( col_name [ , ... ] ) ) ] ) ]`
    :   Additional data metric functions to add to the table or view. Use a comma to separate each data metric function and its specified
        columns.

        If the data metric function accepts a second table as an argument, specify the fully qualified name of the table and its columns.

    `ANOMALY_DETECTION = { TRUE | FALSE }`

    > [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
    >
    > Available to all accounts that are Enterprise Edition (or higher).
    >
    > To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
    >
    > Specifies whether Snowflake uses the DMF to [automatically detect anomalies](/user-guide/data-quality-anomaly) in the table.
    >
    > Default: `FALSE`

    `SENSITIVITY = { LOW | MEDIUM | HIGH }`

    > [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
    >
    > Available to all accounts that are Enterprise Edition (or higher).
    >
    > To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
    >
    > Specifies the sensitivity of the anomaly-detecting algorithm. For more information, see [Adjust the sensitivity level of anomaly detection](/user-guide/data-quality-anomaly#label-data-quality-anomaly-sensitivity-level).
    >
    > Default: `'MEDIUM'`

    `EXECUTE AS ROLE role_name`
    :   Specifies which role the DMF runs with. The role must have the SELECT privilege on the table or view.

        For more information, see [Required privilege on the table or view](/user-guide/data-quality-access-control#label-data-quality-access-control-object-privilege).

`MODIFY DATA METRIC FUNCTION metric_name`
:   Identifier of the data metric function to modify.

    `ON ( col_name [ , ... ] [ , TABLE( table_name( col_name [ , ... ] ) ) ] )`
    :   Specifies the columns associated with the data metric function. If the data metric function accepts a second table as an argument,
        specify the fully qualified name of the table and its columns.

    `{ SUSPEND | RESUME }`
    :   Suspends or resumes the data metric function on the specified columns. When a data metric function is set for a table or view, the data
        metric function is automatically included in the schedule.

        - `SUSPEND` removes the data metric function from the schedule.
        - `RESUME` brings a suspended date metric function back into the schedule.

    `{ ADD | MODIFY } EXPECTATION expectation_name ( expression ) [, expectation_name ( expression ) [ , ... ] ]`
    :   Defines or modifies one or more [expectations](/user-guide/data-quality-expectations) for the association between the column and
        the DMF.

    `DROP EXPECTATION expectation_name [ , expectation_name [ , ... ] ]`
    :   Removes the specified expectations from the association between the column and the DMF.

    `FILTER ( [ predicate ] )`
    :   Sets, replaces, or clears the row filter on the association. Specify a Boolean expression to evaluate the DMF only on rows that
        satisfy the condition. Specify empty parentheses (`FILTER ()`) to remove the filter so the DMF evaluates all rows.

        You can’t combine `FILTER` with `SUSPEND`, `RESUME`, `EXPECTATION`, or `SET` in the same `MODIFY` statement. `FILTER` isn’t supported on
        associations that use `WITHIN GROUP`.

        For more information, see [Apply data quality checks to a subset of rows](/user-guide/data-quality-filter).

    `[ , metric_name_2 ON ( col_name [ , ... ] [ , TABLE(col_name [ , ... ] ) ] ) ]`
    :   Additional data metric functions to modify. Use a comma to separate each data metric function and its specified
        columns. If the data metric function accepts a second table as an argument, specify the fully qualified name of the table and its
        columns.

    `SET list_of_properties`
    :   Sets one or more properties of the association between the DMF and the object. You set more than one property by using a space-delimited list.

        `ANOMALY_DETECTION = { TRUE | FALSE }`

        > [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
        >
        > Available to all accounts that are Enterprise Edition (or higher).
        >
        > To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
        >
        > Controls whether Snowflake uses the DMF to [automatically detect anomalies](/user-guide/data-quality-anomaly) in the table.

        `SENSITIVITY = { 'LOW' | 'MEDIUM' | 'HIGH' }`

        > [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
        >
        > Available to all accounts that are Enterprise Edition (or higher).
        >
        > To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
        >
        > Sets the sensitivity of the anomaly-detecting algorithm. For more information, see [Adjust the sensitivity level of anomaly detection](/user-guide/data-quality-anomaly#label-data-quality-anomaly-sensitivity-level).

        `DATA_QUALITY_NOTIFICATION = { TRUE | FALSE }`

        > [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
        >
        > Available to all accounts that are Enterprise Edition (or higher).
        >
        > To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
        >
        > Controls whether notifications are sent when the value returned by the DMF is an expectation violation or an anomaly.
        >
        > Notifications are sent if the parameter is set to `TRUE` *and* notifications are turned on for the object’s database. Specify `FALSE` to turn off notifications for this object-DMF association even though notifications are sent for other associations in the database.
        >
        > For more information about configuring notifications, see [Sending notifications for data quality issues](/user-guide/data-quality-notifications).
        >
        > Default: `TRUE`

## Data Governance policy and tag actions (`dataGovnPolicyTagAction`)

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`policy_name`
:   Identifier for the policy; must be unique for your schema.

The following clauses apply to all table kinds that support row access policies, such as but not limited to tables, views, and event tables.
To simplify, the clauses just refer to “table.”

> `ADD ROW ACCESS POLICY policy_name ON (col_name [ , ... ])`
> :   Adds a row access policy to the table.
>
>     At least one column name must be specified. Additional columns can be specified with a comma separating each column name. Use this
>     expression to add a row access policy to both an event table and an external table.
>
> `DROP ROW ACCESS POLICY policy_name`
> :   Drops a row access policy from the table.
>
>     Use this clause to drop the policy from the table.
>
> `DROP ROW ACCESS POLICY policy_name, ADD ROW ACCESS POLICY policy_name ON ( col_name [ , ... ] )`
> :   Drops the row access policy that is set on the table and adds a row access policy to the same table in a single SQL statement.
>
> `DROP ALL ROW ACCESS POLICIES`
> :   Drops all [row access policy](/user-guide/security-row-using) associations from the table.
>
>     This expression is helpful when a row access policy is dropped from a schema before dropping the policy from an event table. Use this expression to drop row access policy associations from the table.
>
>     Suppose that a row access policy applied to the table when the backup was created, and the policy was later dropped. After you
>     restore the table from a [backup](/user-guide/backups), you can’t query it until you run an ALTER TABLE command with the
>     DROP ALL ROW ACCESS POLICIES clause.
>
> `SET AGGREGATION POLICY policy_name`
> :   `[ ENTITY KEY (col_name [ , ... ]) ] [ FORCE ]`
>     :   Assigns an [aggregation policy](/user-guide/aggregation-policies) to the table.
>
>         Use the optional ENTITY KEY parameter to define which columns uniquely identity an entity within the table. For more information, see
>         [Implementing entity-level privacy with aggregation policies](/user-guide/aggregation-policies-entity-privacy).
>
>         Use the optional FORCE parameter to atomically replace an existing aggregation policy with the new aggregation policy.
>
> `UNSET AGGREGATION POLICY`
> :   Detaches an aggregation policy from the table.
>
> `SET JOIN POLICY policy_name`
> :   `[ FORCE ]`
>     :   Assigns a [join policy](/user-guide/join-policies) to the table.
>
>         Use the optional FORCE parameter to atomically replace an existing join policy with the new join policy.
>
> `UNSET JOIN POLICY`
> :   Detaches a join policy from the table.

`{ ALTER | MODIFY } [ COLUMN ] ...`
:   `USING ( col_name , cond_col_1 ... )`
    :   Specifies the arguments to pass into the conditional masking policy SQL expression.

        The first column in the list specifies the column for the policy conditions to mask or tokenize the data and must match the
        column to which the masking policy is set.

        The additional columns specify the columns to evaluate to determine whether to mask or tokenize the data in each row of the query
        result when a query is made on the first column.

        If the USING clause is omitted, Snowflake treats the conditional masking policy as a normal
        [masking policy](/user-guide/security-column-intro).

    `FORCE`
    :   Replaces a masking or projection policy that is currently set on a column with a different policy in a single statement.

        Note that using the `FORCE` keyword with a masking policy requires the [data type](/sql-reference-data-types) of the policy
        in the ALTER TABLE statement (i.e. STRING) to match the data type of the masking policy currently set on the column (i.e. STRING).

        If a masking policy is not currently set on the column, specifying this keyword has no effect.

        For details, see: [Replace a masking policy on a column](/user-guide/security-column-intro#label-security-column-intro-replace-policy) or [Replace a projection policy](/user-guide/projection-policies#label-projection-policy-replace).

## Usage notes: General

- Moving a view to a managed access schema (using the ALTER VIEW … RENAME TO syntax) is prohibited unless the view owner (i.e.
  the role that has the OWNERSHIP privilege on the view) also owns the target schema.

- For masking policies:
  - The `USING` clause and the `FORCE` keyword are both optional; neither are required to set a masking policy on a column. The
    `USING` clause and the `FORCE` keyword can be used separately or together. For details, see:

    - [Apply a conditional masking policy on a column](/user-guide/security-column-intro#label-security-column-intro-apply-cond-cols)
    - [Replace a masking policy on a column](/user-guide/security-column-intro#label-security-column-intro-replace-policy)
  - A single masking policy that uses conditional columns can be applied to multiple tables provided that the column structure of the table
    matches the columns specified in the policy.
  - When modifying one or more table columns with a masking policy or the table itself with a row access policy, use the
    [POLICY\_CONTEXT](/sql-reference/functions/policy_context) function to simulate a query on the column(s) protected by a masking policy and the
    table protected by a row access policy.

- A single masking policy that uses conditional columns can be applied to multiple views provided that the column structure of the view
  matches the columns specified in the policy.

- For row access policies:
  - Snowflake supports adding and dropping row access policies in a single SQL statement.

    For example, to replace a row access policy that is already set on a table with a different policy, drop the row access policy first
    and then add the new row access policy.
  - For a given resource (i.e. table or view), to `ADD` or `DROP` a row access policy you must have either the
    [APPLY ROW ACCESS POLICY](/user-guide/security-row-intro#label-security-row-privileges) privilege on the schema, or the
    [OWNERSHIP](/user-guide/security-row-intro#label-security-row-privileges) privilege on the resource and the APPLY privilege on the row access policy resource.
  - A table or view can only be protected by one row access policy at a time. Adding a policy fails if the policy body refers to a table or
    view column that is protected by a row access policy or the column protected by a masking policy.

    Similarly, adding a masking policy to a table column fails if the masking policy body refers to a table that is protected by a row
    access policy or another masking policy.
  - Row access policies cannot be applied to system views or table functions.
  - Similar to other [DROP <object>](/sql-reference/sql/drop) operations, Snowflake returns an error if attempting to drop a row access policy from a
    resource that does not have a row access policy added to it.
  - If an object has both a row access policy and one or more masking policies, the row access policy is evaluated first.

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Usage notes: Data metric functions

Add a DMF to a table:
:   Prior to adding a data metric function to a table, you must:

    - Set the schedule for the data metric function to run. For details, see
      [DATA\_METRIC\_SCHEDULE](/sql-reference/parameters#label-data-metric-schedule).
    - Configure the event table to store the results of calling the data metric function. For details, see
      [View results of a data metric function](/user-guide/data-quality-results).
    - Ensure that the table is view is not granted to a share because you cannot set a data metric function on a shared table or view.

    Additionally:

    - When you specify a column, Snowflake uses the ordinal position. If you rename a column after adding a data metric function to the table
      or view, the association of the data metric function to the column remains valid.
    - Only one data metric function of its kind can be added to a column. For example, a NULL\_COUNT data metric function cannot be added to a
      single column twice.
    - If you drop a column after adding a data metric function that references the column, Snowflake cannot evaluate the data metric function.
    - Referencing a virtual column is not supported.

Schedule a DMF
:   It takes ten minutes for the schedule to become effective once the schedule is set.

    Similarly, it takes ten minutes once the DMF is unset for the scheduling changes to take effect. For more information, see
    [Adjust the schedule for DMFs](/user-guide/data-quality-working#label-data-quality-schedule).

## Examples

Rename view `view1` to `view2`:

Copy code

```
ALTER VIEW view1 RENAME TO view2;
```

Convert a view to a secure view:

Copy code

```
ALTER VIEW view1 SET SECURE;
```

Revert a secure view to a regular view:

Copy code

```
ALTER VIEW view1 UNSET SECURE;
```

Apply a Column-level Security masking policy to a view column:

Copy code

```
-- single column

ALTER VIEW user_info_v MODIFY COLUMN ssn_number SET MASKING POLICY ssn_mask_v;

-- multiple columns

ALTER VIEW user_info_v MODIFY
  COLUMN ssn_number SET MASKING POLICY ssn_mask_v,
  COLUMN dob SET MASKING POLICY dob_mask_v
  ;
```

Unset a Column-level Security masking policy from a view column:

Copy code

```
-- single column

ALTER VIEW user_info_v MODIFY COLUMN ssn_number UNSET MASKING POLICY;

-- multiple columns

ALTER VIEW user_info_v MODIFY
  COLUMN ssn_number UNSET MASKING POLICY,
  COLUMN dob UNSET MASKING POLICY
  ;
```

The following example adds a row access policy on a view. After setting policies, you can verify their
referenced objects by checking the [information schema](/user-guide/security-row-intro#label-security-row-policy-refs).

Copy code

```
ALTER VIEW v1
  ADD ROW ACCESS POLICY rap_v1 ON (empl_id);
```

The following example drops a row access policy from a view. Verify that the policies were dropped by querying the
[information schema](/user-guide/security-row-intro#label-security-row-policy-refs).

Copy code

```
ALTER VIEW v1
  DROP ROW ACCESS POLICY rap_v1;
```

The following example shows how to combine adding and dropping row access policies in a single SQL statement for a view. Verify the
results by checking the [information schema](/user-guide/security-row-intro#label-security-row-policy-refs).

Copy code

```
ALTER VIEW v1
  DROP ROW ACCESS POLICY rap_v1_version_1,
  ADD ROW ACCESS POLICY rap_v1_version_2 ON (empl_id);
```

The following example sets a [join policy](/user-guide/join-policies) on a view:

Copy code

```
ALTER VIEW join_view
  SET JOIN POLICY jp1;
```
