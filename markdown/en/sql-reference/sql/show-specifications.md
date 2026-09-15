# SHOW SPECIFICATIONS

Lists the app specifications that have been defined for an app.

See also:
:   [DESCRIBE SPECIFICATION](/sql-reference/sql/desc-specification), [ALTER APPLICATION SET SPECIFICATION](/sql-reference/sql/alter-application-set-app-spec)

## Syntax

Copy code

```
SHOW [ { APPROVED | DECLINED | PENDING } ] SPECIFICATIONS [ IN APPLICATION <app_name> ];
```

## Parameters

`APPROVED | DECLINED | PENDING`
:   Narrows the output to app specifications with one of these statuses.

`IN APPLICATION app_name`
:   Specifies the name of the app whose app specification you want to view.

## Usage notes

- Consumers must provide the name of an app using the IN APPLICATION clause.
- An app can run this command without specifying the
  IN APPLICATION clause.

## Output

The command output provides information about the properties of an app specification in the following
columns:

| Column | Description |
| --- | --- |
| `name` | Name of the app specification. |
| `requested_on` | Timestamp when the app specification was requested. |
| `type` | Type of app specification. Supported values are: `EXTERNAL_ACCESS`, `SECURITY_INTEGRATION`, `LISTING`, `CONNECTION`, and `SETTING`. |
| `sequence_number` | ID for a version of an app specification. This value is incremented each time a provider changes the [app specification definition](/developer-guide/native-apps/requesting-app-specs#label-native-apps-app-spec-definition). |
| `status` | Specifies the current status of the app specification. Possible values are:   - APPROVED: The consumer approved the app specification. - PENDING: The app specification is waiting for the consumer to approve or   decline. - DECLINED: The consumer declined the app specification. |
| `status_updated_on` | Timestamp of the last status change. |
| `label` | Name of the app specification that is displayed to the consumer in Snowsight. |
| `description` | Description of the app specification that is displayed to the consumer in Snowsight. This is the provider-supplied explanation of why the app requires this permission. |
| `system_description` | For `SETTING` specifications: Snowflake’s description of the behavior associated with the setting. Not present for other specification types. |
| `definition` | Values that are part of the [app specification definition](/developer-guide/native-apps/requesting-app-specs#label-native-apps-app-spec-definition). The values of this column depend on the type of app specification. |

Expand

Show lessSee more

## Examples

Show all specifications that you have privileges to view:

Copy code

```
SHOW SPECIFICATIONS;
```
