# DESCRIBE SPECIFICATION

Describes the details about an [app specification](/developer-guide/native-apps/requesting-app-specs).

## Syntax

Copy code

```
{ DESCRIBE | DESC }  SPECIFICATION <name> [ IN APPLICATION <app_name> ];
```

## Parameters

`IN APPLICATION app_name`
:   Specifies the name of the app whose app specification you want to view.

## Usage notes

- Consumers must provide the name of an app using the IN APPLICATION clause.
- An app can run this command without specifying the
  IN APPLICATION clause.

## Output

This command displays the following output:

| Column | Description |
| --- | --- |
| `sequenceNumber` | ID for a version of an app specification. This value is incremented each time a provider changes the [app specification definition](/developer-guide/native-apps/requesting-app-specs#label-native-apps-app-spec-definition). |
| `property` | The name of the property of the app specification. |
| `value` | The value of the property. |

Expand

Show lessSee more
