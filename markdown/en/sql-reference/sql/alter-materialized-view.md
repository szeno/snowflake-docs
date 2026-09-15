# ALTER MATERIALIZED VIEW

[Enterprise Edition Feature](/user-guide/intro-editions)

Materialized views require Enterprise Edition. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Alters a materialized view in the current/specified schema. Supported actions include:

- Renaming the materialized view.
- Suspending and resuming use and maintenance of the materialized view.
- Clustering the materialized view.
- Suspending and resuming reclustering of the materialized view.
- Dropping clustering of the materialized view.

For more details, see [Working with Materialized Views](/user-guide/views-materialized).

See also:
:   [CREATE MATERIALIZED VIEW](/sql-reference/sql/create-materialized-view) , [DROP MATERIALIZED VIEW](/sql-reference/sql/drop-materialized-view) , [SHOW MATERIALIZED VIEWS](/sql-reference/sql/show-materialized-views) , [DESCRIBE MATERIALIZED VIEW](/sql-reference/sql/desc-materialized-view)

## Syntax

Copy code

```
ALTER MATERIALIZED VIEW <name>
  {
  RENAME TO <new_name>                     |
  CLUSTER BY ( <expr1> [, <expr2> ... ] )  |
  DROP CLUSTERING KEY                      |
  SUSPEND RECLUSTER                        |
  RESUME RECLUSTER                         |
  SUSPEND                                  |
  RESUME                                   |
  SET {
    [ SECURE ]
    [ CONTACT <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ]
    [ COMMENT = '<comment>' ]
    }                                      |
  UNSET {
    SECURE
    CONTACT <purpose>                                 |
    COMMENT
    }
  }

ALTER MATERIALIZED VIEW
  SET DATA_METRIC_SCHEDULE = {
      '<num> MINUTE'
    | 'USING CRON <expr> <time_zone>'
  }

ALTER MATERIALIZED VIEW UNSET DATA_METRIC_SCHEDULE
```

## Parameters

`name`
:   Specifies the identifier of the materialized view to alter.

`RENAME TO new_name`
:   This option allows you to rename a materialized view.

    The new identifier must be unique for the schema in which the view is created.
    The new identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier string
    is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.
    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    Note that renaming a materialized view does not update references to that view. For example, if
    you create a view named `V1` on top of a materialized view, and then you rename
    the materialized view, the definition of view `V1` becomes out of date.

`CLUSTER BY expr#`
:   This command clusters the materialized view. Clustering
    re-orders the rows in the materialized view to increase performance for queries
    that filter based on the clustering key expressions.

    The `expr#` specifies an expression on which to cluster the materialized view.
    Typically, each expression is the name of a column in the materialized view.

    For more information about clustering materialized views, see:
    [Materialized Views and Clustering](/user-guide/views-materialized#label-clustering-base-table-and-materialized-view).
    For more information about clustering in general, see:
    [What is Data Clustering?](/user-guide/tables-clustering-micropartitions#label-data-clustering).

`DROP CLUSTERING KEY`
:   This command drops the clustering of the materialized view.

`SUSPEND RECLUSTER`
:   The `SUSPEND RECLUSTER` option suspends re-clustering of the materialized
    view. For more information about clustering materialized views,
    see [Materialized Views and Clustering](/user-guide/views-materialized#label-clustering-base-table-and-materialized-view).

`RESUME RECLUSTER`
:   The `RESUME RECLUSTER` option resumes reclustering of the materialized
    view.

`SUSPEND`
:   The `SUSPEND` option suspends the maintenance (updates) and use of the
    materialized view. While the view is suspended, updates to the base table are
    not propagated to the materialized view. The materialized view itself is
    also inaccessible; if you attempt to use it, you get an error message
    similar to:

    ```
    Failure during expansion of view 'MV1':
      SQL compilation error: Materialized View MV1 is invalid.
      Invalidation reason: Marked Materialized View as invalid manually.
    ```

    If you suspend a clustered materialized view, suspending the view implicitly
    suspends reclustering of that view.

`RESUME`
:   The `RESUME` option allows you to resume using the materialized view.
    It also resumes maintenance of the materialized view.
    If the view is clustered, it also implicitly resumes reclustering of that view.

`SET ...`
:   Specifies the property to set for the materialized view:

    `SECURE`
    :   This option turns the view into a secure view. For more information about secure views, see
        [Working with Secure Views](/user-guide/views-secure).

    `CONTACT purpose = contact [ , purpose = contact ... ]`
    :   Associate the existing object with one or more [contacts](/user-guide/contacts-using). For a list of valid purposes, see [Associate a contact with an object](/user-guide/contacts-using#label-contacts-associate).

        You cannot set the CONTACT property with other properties in the same statement.

    `COMMENT = 'string_literal'`
    :   This option sets a comment for the materialized view. The comment has no effect on the behavior of the view,
        but can provide useful information to people who use or maintain the view.

    `DATA_METRIC_SCHEDULE ...`
    :   Specifies the schedule to run the data metric function periodically.

        `'num MINUTE'`
        :   Specifies an interval (in minutes) of wait time inserted between runs of the data metric function. Accepts positive integers only.

            Also supports `num M` syntax.

            For data metric functions, use one of the following values: `5`, `15`, `30`, `60`, `720`, or `1440`.

        `'USING CRON expr time_zone'`
        :   Specifies a cron expression and time zone for periodically running the data metric function. Supports a subset of standard cron
            utility syntax.

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
                not scheduled to run in January (3 months after the October run).

            Note

            - The cron expression currently evaluates against the specified time zone only. Altering the [TIMEZONE](/sql-reference/parameters#label-timezone) parameter value
              for the account (or setting the value at the user or session level) does not change the time zone for the data metric
              function.
            - The cron expression defines all valid run times for the data metric function. Snowflake attempts to run a data metric
              function based on this schedule; however, any valid run time is skipped if a previous run has not completed before the next valid
              run time starts.
            - When both a specific day of month and day of week are included in the cron expression, then the data metric function is scheduled
              on days satisfying either the day of month or day of week. For example,
              `DATA_METRIC_SCHEDULE = 'USING CRON 0 0 10-20 * TUE,THU UTC'` schedules a data metric function at 0AM on any 10th to 20th
              day of the month and also on any Tuesday or Thursday outside of those dates.
            - The shortest granularity of time in cron is minutes.

`UNSET ...`
:   Specifies the property to unset for the materialized view:

    - `SECURE`
    - `TAG tag_name [ , tag_name ... ]`
    - `CONTACT purpose`
    - `COMMENT`
    - `DATA_METRIC_SCHEDULE`

    You cannot unset the CONTACT property with other properties in the same statement.

## Usage notes

- Use the [ALTER VIEW](/sql-reference/sql/alter-view) command to set/unset a masking policy, row access policy, or tag on/from a materialized view.
- You can use data metric functions (DMFs) with materialized views as follows:

  - To set the [DATA\_METRIC\_SCHEDULE](/sql-reference/parameters#label-data-metric-schedule) parameter on the materialized view, use the ALTER MATERIALIZED VIEW command. For more
    information, see [Adjust the schedule for DMFs](/user-guide/data-quality-working#label-data-quality-schedule).
  - To add a DMF to a column or drop a DMF from a column in a materialized view, use the [ALTER VIEW](/sql-reference/sql/alter-view) command.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Rename a materialized view:

> Copy code
>
> ```
> ALTER MATERIALIZED VIEW table1_MV RENAME TO my_mv;
> ```

Cluster a materialized view:

> Copy code
>
> ```
> ALTER MATERIALIZED VIEW my_mv CLUSTER BY(i);
> ```

Suspend clustering of a materialized view, but not use of the view:

> Copy code
>
> ```
> ALTER MATERIALIZED VIEW my_mv SUSPEND RECLUSTER;
> ```

Resume clustering of a materialized view:

> Copy code
>
> ```
> ALTER MATERIALIZED VIEW my_mv RESUME RECLUSTER;
> ```

Suspend all use and automatic maintenance of the specified materialized view:

> Copy code
>
> ```
> ALTER MATERIALIZED VIEW my_mv SUSPEND;
> ```

Resume all use and automatic maintenance of the specified materialized view:

> Copy code
>
> ```
> ALTER MATERIALIZED VIEW my_mv RESUME;
> ```

Stop clustering a materialized view:

> Copy code
>
> ```
> ALTER MATERIALIZED VIEW my_mv DROP CLUSTERING KEY;
> ```

Modify the view to be a secure view:

> Copy code
>
> ```
> ALTER MATERIALIZED VIEW mv1 SET SECURE;
> ```

Add or replace the comment for a materialized view:

> Copy code
>
> ```
> ALTER MATERIALIZED VIEW mv1 SET COMMENT = 'Sample view';
> ```
