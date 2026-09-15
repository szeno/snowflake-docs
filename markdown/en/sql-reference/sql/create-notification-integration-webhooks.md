# CREATE NOTIFICATION INTEGRATION (webhooks)

Creates a new notification integration or replaces an existing integration for a
[webhook](/user-guide/notifications/webhook-notifications).

See also:
:   [ALTER NOTIFICATION INTEGRATION (webhooks)](/sql-reference/sql/alter-notification-integration-webhooks) , [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) ,
    [SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name>
  TYPE = WEBHOOK
  ENABLED = { TRUE | FALSE }
  WEBHOOK_URL = '<url>'
  [ WEBHOOK_SECRET = <secret_name> ]
  [ WEBHOOK_BODY_TEMPLATE = '<template_for_http_request_body>' ]
  [ WEBHOOK_HEADERS = ( '<header_1>'='<value_1>' [ , '<header_N>'='<value_N>', ... ] ) ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (i.e. name) for the integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ENABLED = { TRUE | FALSE }`
:   Specifies whether to initiate operation of the integration or suspend it.

    - `TRUE` enables the integration.
    - `FALSE` disables the integration for maintenance. Any integration between Snowflake and a third-party service fails to
      work.

    The value is case-insensitive.

    The default is `TRUE`.

`TYPE = WEBHOOK`
:   Specifies that this is a notification integration for a webhook.

`WEBHOOK_URL = 'url'`
:   Specifies the URL for the webhook. The URL must use the `https://` protocol.

    You can only specify the following URLs:

    - URLs for Slack webhooks. These URLs must start with `https://hooks.slack.com/services/`.
    - URLs for Microsoft Teams webhooks. These URLs must use the following general format:

      - Up until November 30, 2025, Microsoft Teams supports URLs in the following format:

        Copy code

        ```
        https://<hostname>.<region>.logic.azure.com:443/workflows/<secret>
        ```
      - [From November 30, 2025 onward](https://learn.microsoft.com/en-us/troubleshoot/power-platform/power-automate/flow-run-issues/triggers-troubleshoot?tabs=new-designer#changes-to-http-or-teams-webhook-trigger-flows),
        Microsoft Teams supports URLs in the following format:

        Copy code

        ```
        https://default<hostname>.environment.api.powerplatform.com/powerautomate/automations/direct/workflows/<secret>/triggers/manual/paths/invoke
        ```

      Note

      You must omit the port number (`:443`) from the URL in the WEBHOOK\_URL parameter.
      For information about the Microsoft API data format, see <https://adaptivecards.io/>.
    - URLs for PagerDuty webhooks. This URL must be `https://events.pagerduty.com/v2/enqueue`.
    - URLs for Jira automation webhooks. These URLs must start with `https://api-private.atlassian.com/automation/webhooks/jira/`.
    - URLs for ServiceNow webhooks. These URLs use the host of your ServiceNow instance and have the following general format:

      Copy code

      ```
      https://<instance>.service-now.com/<path>
      ```

    If the URL includes a secret and you [created a secret object for that secret](/user-guide/notifications/webhook-notifications#label-notifications-webhook-secret),
    replace that secret in the URL with SNOWFLAKE\_WEBHOOK\_SECRET. For example, if you
    [created a secret object for the secret in a Slack webhook URL](/user-guide/notifications/webhook-notifications#label-notifications-webhook-secret-slack), set
    WEBHOOK\_URL to:

    Copy code

    ```
    WEBHOOK_URL='https://hooks.slack.com/services/SNOWFLAKE_WEBHOOK_SECRET'
    ```

    For Jira and ServiceNow webhooks, the secret isn’t part of the URL. You pass the secret in an HTTP header instead (using
    the WEBHOOK\_HEADERS parameter). For details, see
    [Sending webhook notifications](/user-guide/notifications/webhook-notifications).

## Optional parameters

`WEBHOOK_SECRET = secret_name`
:   Specifies the [secret to use with this integration](/user-guide/notifications/webhook-notifications#label-notifications-webhook-secret).

    If you are using the SNOWFLAKE\_WEBHOOK\_SECRET placeholder in WEBHOOK\_URL, WEBHOOK\_BODY\_TEMPLATE, or WEBHOOK\_HEADERS, the
    placeholder is replaced by this secret when you send a notification.

    If the database and schema containing the secret object will not be active when you send a notification,
    [qualify the secret name with the schema name or the database and schema names](/sql-reference/name-resolution). For
    example:

    Copy code

    ```
    WEBHOOK_SECRET = my_secrets_db.my_secrets_schema.my_slack_webhook_secret
    ```

    You must have the USAGE privilege on the secret (and the database and schema that contain it) to specify this parameter.

    Default: No value

`WEBHOOK_BODY_TEMPLATE = 'template_for_http_request_body'`
:   Specifies a template for the body of the HTTP request to send for the notification.

    If the webhook requires a specific format for the body of the HTTP request (for example, a specific JSON format), set this to
    a string that specifies the format. In this string:

    - If the message needs to include a secret and you
      [created a secret object for that secret](/user-guide/notifications/webhook-notifications#label-notifications-webhook-secret), use the SNOWFLAKE\_WEBHOOK\_SECRET
      placeholder where the secret should appear in the message.
    - Use the SNOWFLAKE\_WEBHOOK\_MESSAGE placeholder where the notification message needs to be included.

    For example:

    Copy code

    ```
    WEBHOOK_BODY_TEMPLATE='{
      "routing_key": "SNOWFLAKE_WEBHOOK_SECRET",
      "event_action": "trigger",
      "payload":
        {
          "summary": "SNOWFLAKE_WEBHOOK_MESSAGE",
          "source": "Snowflake monitoring",
          "severity": "INFO",
        }
      }'
    ```

    If you set WEBHOOK\_BODY\_TEMPLATE, you must also set WEBHOOK\_HEADERS to include the `Content-Type` header with the type
    of your message. For example, if you set WEBHOOK\_BODY\_TEMPLATE to a template in JSON format, set WEBHOOK\_HEADERS to include
    the header `Content-Type: application/json`:

    Copy code

    ```
    WEBHOOK_HEADERS=('Content-Type'='application/json')
    ```

    Default: No value

`WEBHOOK_HEADERS = ( 'header'='value' [ , 'header'='value', ... ] )`
:   Specifies a list of HTTP headers and values to include in the HTTP request for the webhook.

    If an HTTP header must include a secret (for example, the `Authorization` header) and you
    [created a secret object for that secret](/user-guide/notifications/webhook-notifications#label-notifications-webhook-secret), use the SNOWFLAKE\_WEBHOOK\_SECRET
    placeholder in the header value. For example:

    Copy code

    ```
    WEBHOOK_HEADERS=('Authorization'='Basic SNOWFLAKE_WEBHOOK_SECRET')
    ```

    Default: No value

`COMMENT = 'string_literal'`
:   String (literal) that specifies a comment for the integration.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTEGRATION | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |
| USAGE | Secret | If you set the WEBHOOK\_SECRET property to a secret object, you must have the USAGE privilege on that secret and on the database and schema containing that secret. |
| CREATE NOTIFICATION INTEGRATION | Account | Grants the ability to create notification integrations. This privilege does not grant the ability to create other types of integrations. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

See [Creating a webhook notification integration](/user-guide/notifications/webhook-notifications#label-notifications-webhook-integration).
