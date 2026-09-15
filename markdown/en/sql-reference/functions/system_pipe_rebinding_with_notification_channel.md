Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$PIPE\_REBINDING\_WITH\_NOTIFICATION\_CHANNEL

Retries the notification channel binding process when a replicated pipe has not been successfully bound to a notification channel during replication time. Binding can be unsuccessful for one of the following reasons:

- The cloud messaging is not correctly set up in the secondary deployment during replication. For example, a notification integration with the same name is not created manually, or SNS policy is not set to allow subscription, etc.
- There is a cloud provider error when Snowpipe tries to bind the pipe to the notification channel.
- The pipe and its source stage are in different replication groups, and the stage is not replicated when the pipe is replicated.

You can also retry the notification binding by refreshing the replication group or database. However, if the primary account is down, or a failover has already completed, the only option is to call this system function.

For more information, see [Snowpipe](/user-guide/data-load-snowpipe-intro) and [Stage, pipe, and load history replication](/user-guide/account-replication-stages-pipes-load-history).

## Syntax

Copy code

```
SYSTEM$PIPE_REBINDING_WITH_NOTIFICATION_CHANNEL( '<pipe_name>' )
```

## Arguments

`'pipe_name'`
:   The name of the pipe that needs to go through the rebind notification process.

## Access control requirements

- Only the pipe owner (that is, the role with the OWNERSHIP privilege on the pipe) or a role with the OPERATE privilege on the pipe can call this SQL
  function.

  Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Usage notes

- `pipe_name` is a string so it must be enclosed in single quotes:
  - Note that the entire name must be enclosed in single quotes, including the database and schema (if the name is fully qualified), that is, `'db.schema.pipe_name'`.
  - If the pipe name is case-sensitive or includes any special characters or spaces, double quotes are required to process the case/characters. The double quotes must be enclosed within the single quotes, that is, `'"pipe_name"'`.

## Examples

Retries the notification channel binding process for `mypipe`:

Copy code

```
SELECT SYSTEM$PIPE_REBINDING_WITH_NOTIFICATION_CHANNEL('mydb.myschema.mypipe');
```
