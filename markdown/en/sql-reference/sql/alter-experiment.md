# ALTER EXPERIMENT

Modifies the properties of an existing [experiment](/developer-guide/snowflake-ml/experiments).

See also:
:   [CREATE EXPERIMENT](/sql-reference/sql/create-experiment) , [SHOW EXPERIMENTS](/sql-reference/sql/show-experiments), [DROP EXPERIMENT](/sql-reference/sql/drop-experiment) , [SHOW RUNS IN EXPERIMENT](/sql-reference/sql/show-runs-in-experiment) , [SHOW RUN … IN EXPERIMENT](/sql-reference/sql/show-run-in-experiment)

## Syntax

Copy code

```
ALTER EXPERIMENT <experiment_name> ADD RUN <run_name>

ALTER EXPERIMENT <experiment_name> COMMIT RUN <run_name>

ALTER EXPERIMENT <experiment_name> DROP RUN <run_name>
```

## Parameters

`experiment_name`
:   Specifies the identifier for the experiment to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ADD RUN run_name`
:   Adds a new run with the identifier `run_name`; must be unique for the runs in experiment `experiment_name`.

    For information on how to manually conduct an experiment run in SQL, see [Start an experiment run](/developer-guide/snowflake-ml/experiments#label-ml-experiments-run).

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`COMMIT RUN run_name`
:   Completes the run with the identifier `run_name` for experiment `experiment_name`. Committed runs can’t be altered.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

    For information on how to retrieve the results and artifacts of an experiment run, see [Complete a run](/developer-guide/snowflake-ml/experiments#label-ml-experiments-complete).

`DROP RUN run_name`
:   Deletes the run with the identifier `run_name`.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY | Experiment |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example creates a new run named `run_1` in the experiment `my_experiment`:

Copy code

```
ALTER EXPERIMENT my_experiment ADD RUN run_1;
```

The following example completes and records the run named `run_1` in the experiment `my_experiment`:

Copy code

```
ALTER EXPERIMENT my_experiment COMMIT RUN run_1;
```
