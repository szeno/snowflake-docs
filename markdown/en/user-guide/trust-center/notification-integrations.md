# Programmatic notifications for Trust Center findings

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Trust Center [scanners](/user-guide/trust-center/overview#label-trust-center-scanners) run in customer accounts to surface security violations or detect potential threats as findings.
The findings appear automatically in Snowsight. A Trust Center administrator can also [configure notifications](/user-guide/trust-center/notifications-trust-center) so that users
with verified email addresses receive notifications about findings as email messages.

This preview introduces support for additional notifications such as webhooks (PagerDuty, Slack, Microsoft Teams) and queues (Amazon SNS, Azure Event Grid, Google Pub/Sub) for Trust Center findings. The notifications are triggered by a
specific event, such as generation of a finding. Using notification integrations with
the Trust Center provides the option to receive notifications independent from Snowsight, through a customer-configured
PagerDuty service, SNS topic, or other endpoint.

For more information, see [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration).

## Configure notification integrations for Trust Center findings

To configure notification integrations for the Trust Center, perform the following steps:

1. [Create a notification integration](#label-trust-center-webhook-create)
2. [Grant access to the notification integration](#label-trust-center-webhook-grant-access)
3. [Configure notification settings for scanners](#label-trust-center-webhook-configure-scanner)
4. [Run the scanner](#label-trust-center-webhook-run-scanner)
5. [Interpret the notification payload](#label-trust-center-webhook-notification-payload)
6. [Troubleshoot notification issues](#label-trust-center-webhook-debug)

### Create a notification integration

To enable the Trust Center to send notifications to a third-party system, run the CREATE NOTIFICATION INTEGRATION command.

Note

Only outbound notification integrations are supported.

For more information, see [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration).

The following examples show how to create notification integrations:

**AWS SNS**

Copy code

```
CREATE NOTIFICATION INTEGRATION test_aws_int
  ENABLED = TRUE
  DIRECTION = OUTBOUND
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = AWS_SNS
  AWS_SNS_TOPIC_ARN = 'arn:aws:sns:us-east-2:1234567890:sns-topic-name'
  AWS_SNS_ROLE_ARN = 'arn:aws:iam::1234567890:role/sns-access-role';
```

**PagerDuty webhook**

The following example creates a webhook that relies on a secret.

Note

Trust Center populates `SNOWFLAKE_WEBHOOK_MESSAGE` with the notification output in JSON format. Configure your notification integration to handle this appropriately.

Copy code

```
CREATE OR REPLACE SECRET test_db.test_schema.integration_key
  TYPE = GENERIC_STRING
  SECRET_STRING = '1234567890abcdef1234567890abcdef';

CREATE OR REPLACE NOTIFICATION INTEGRATION test_pagerduty_int
  TYPE = WEBHOOK
  ENABLED = TRUE
  WEBHOOK_URL = 'https://events.pagerduty.com/v2/enqueue'
  WEBHOOK_SECRET = test_db.test_schema.integration_key
  WEBHOOK_BODY_TEMPLATE = '{
    "routing_key": "SNOWFLAKE_WEBHOOK_SECRET",
    "event_action": "trigger",
    "payload": {
        "summary": "Snowflake Trust Center Scanner Finding",
        "source": "Snowflake",
        "severity": "critical",
        "custom_details": SNOWFLAKE_WEBHOOK_MESSAGE
    }
  }'
  WEBHOOK_HEADERS = ('Content-Type'='application/json');
```

### Grant access to the integration

To enable the Trust Center to use an integration to send notifications, grant the USAGE privilege on the notification integration to the SNOWFLAKE application. For example:

Copy code

```
GRANT USAGE ON INTEGRATION test_pagerduty_int TO APPLICATION snowflake;
```

If the integration relies on a secret, such as a PagerDuty webhook integration key, grant the following
additional privileges to the SNOWFLAKE application:

- READ privilege on the secret
- USAGE privilege on the database containing the secret
- USAGE privilege on the schema containing the secret

For example:

Copy code

```
GRANT READ ON SECRET test_db.test_schema.integration_key TO APPLICATION snowflake;
GRANT USAGE ON DATABASE test_db TO APPLICATION snowflake;
GRANT USAGE ON SCHEMA test_db.test_schema TO APPLICATION snowflake;
```

### Configure notification settings for a scanner

You must define for each scanner or scanner package the findings that trigger a webhook notification. A `NOTIFICATION_INTEGRATION` configuration contains
this definition. To set a `NOTIFICATION_INTEGRATION` configuration for a scanner or a scanner package, use the SET\_CONFIGURATION() stored procedure.
The configuration value is a string that contains an array of JSON objects. Each object specifies the following:

| Key | Description |
| --- | --- |
| `INTEGRATION_NAME` | Name of the notification integration to use. |
| `SEVERITY_THRESHOLD` | Minimum severity level of a finding that triggers a notification. Valid values are `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL`. Notifications are sent only for findings at or above this severity level. |
| `INCLUDE_AT_RISK_ENTITIES_AND_FINDING_METADATA` | Optional. When set to `TRUE`, the notification includes entity details such as user names and IP addresses. Defaults to `FALSE`. Enable this parameter only if you accept sending sensitive account information outside your Snowflake account. |

Expand

Show lessSee more

The following example sets a notification configuration for all scanners in the `CIS_BENCHMARKS` scanner package:

Copy code

```
CALL SNOWFLAKE.TRUST_CENTER.SET_CONFIGURATION(
  'NOTIFICATION_INTEGRATION',
  ARRAY_CONSTRUCT(
    OBJECT_CONSTRUCT(
      'SEVERITY_THRESHOLD', 'HIGH',
      'INTEGRATION_NAME', 'TEST_PAGERDUTY_INT',
      'INCLUDE_AT_RISK_ENTITIES_AND_FINDING_METADATA', 'TRUE'
    )
  )::VARCHAR,
  'CIS_BENCHMARKS'
);
```

The following example sets a notification configuration for a specific scanner (`CIS_BENCHMARKS_CIS1_1`) within a scanner package:

Copy code

```
CALL SNOWFLAKE.TRUST_CENTER.SET_CONFIGURATION(
  'NOTIFICATION_INTEGRATION',
  ARRAY_CONSTRUCT(
    OBJECT_CONSTRUCT(
      'SEVERITY_THRESHOLD', 'HIGH',
      'INTEGRATION_NAME', 'TEST_PAGERDUTY_INT'
    )
  )::VARCHAR,
  'CIS_BENCHMARKS',
  'CIS_BENCHMARKS_CIS1_1'
);
```

You can configure multiple notification integrations for the same scanner or scanner package. The following example
configures the `CIS_BENCHMARKS` scanner package so that the Azure Event Grid integration receives notifications for `CRITICAL`
findings, the PagerDuty integration receives notifications for `HIGH` or `CRITICAL` findings, and the AWS SNS
integration receives notifications for findings of any severity level:

Copy code

```
CALL SNOWFLAKE.TRUST_CENTER.SET_CONFIGURATION(
  'NOTIFICATION_INTEGRATION',
  ARRAY_CONSTRUCT(
    OBJECT_CONSTRUCT(
      'SEVERITY_THRESHOLD', 'CRITICAL',
      'INTEGRATION_NAME', 'TEST_AZURE_EVENT_GRID_INT',
      'INCLUDE_AT_RISK_ENTITIES_AND_FINDING_METADATA', 'TRUE'
    ),
    OBJECT_CONSTRUCT(
      'SEVERITY_THRESHOLD', 'HIGH',
      'INTEGRATION_NAME', 'TEST_PAGERDUTY_INT'
    ),
    OBJECT_CONSTRUCT(
      'SEVERITY_THRESHOLD', 'LOW',
      'INTEGRATION_NAME', 'TEST_AWS_INT'
    )
  )::VARCHAR,
  'CIS_BENCHMARKS'
);
```

To remove the notification configuration for a scanner, call the UNSET\_CONFIGURATION stored procedure:

Copy code

```
CALL SNOWFLAKE.TRUST_CENTER.UNSET_CONFIGURATION(
  'NOTIFICATION_INTEGRATION',
  'CIS_BENCHMARKS',
  'CIS_BENCHMARKS_CIS1_6'
);
```

### Run the scanner

Trust Center supports [schedule-based scanners](/user-guide/trust-center/overview#label-trust-center-scanners-schedule-based) and [event-driven scanners](/user-guide/trust-center/overview#label-trust-center-scanners-event-driven). After setting the configuration, you can run a scanner on demand or wait for the scanner
to either run on its schedule or be triggered by an event.

Note

- An event-driven scanner does not send a notification if it detects no findings.
- Notification integration notifications are sent for a scanner finding only when the severity threshold is met or exceeded.

To manually trigger a scanner, use one of the following methods:

- **Snowsight**: Navigate to **Trust Center** > **Manage Scanners**, select the three-dot menu for the scanner, and then select **Run Scanner**.

  For more information, see [Run a scanner package on demand](/user-guide/trust-center/using-the-trust-center#label-trust-center-start-scanner-package-on-demand).
- **SQL**: Call the `EXECUTE_SCANNER` stored procedure. For example:

  Copy code

  ```
  CALL SNOWFLAKE.TRUST_CENTER.EXECUTE_SCANNER('CIS_BENCHMARKS', 'CIS_BENCHMARKS_CIS3_1');
  ```

### Interpret the notification output

When a Trust Center scanner runs and produces findings that meet the configured severity threshold, the notification message
contains a JSON object similar to the following:

Copy code

```
{
  "scanner_name": "<scanner_name>",
  "scanner_package_name": "<scanner_package_name>",
  "scanner_package_short_description": "<scanner_package_descr>",
  "scanner_short_description": "<scanner_descr>",
  "scanner_finish_time_unix_timestamp_ms": "<scanner_finish_time>",
  "scanner_finish_time_formatted": "<scanner_finish_time_as_date>",
  "findings": [
    {
      "event_id": "<event_id>",
      "finding_identifier": "<finding_identifier>",
      "finding_severity": "<finding_severity>",
      "at_risk_entities": [
        {
          "entity_detail": {},
          "entity_id": "<entity_id>",
          "entity_name": "<entity_name>",
          "entity_object_type": "<entity_object_type>"
        }
      ],
      "total_at_risk_count": "<total_at_risk_count>",
      "metadata": {},
      "note": "The list of at-risk entities has been truncated"
    }
  ]
}
```

Note

The above is an example. The actual payload differs based on the notification integration configured. The `at_risk_entities` and `metadata` fields are included in the notification message only when `INCLUDE_AT_RISK_ENTITIES_AND_FINDING_METADATA` is enabled.

The JSON object contains the following key-value pairs:

| Key | Description |
| --- | --- |
| `scanner_name` | Name of the scanner that produced the findings. |
| `scanner_package_name` | Name of the scanner package containing the scanner. |
| `scanner_package_short_description` | Short description of the scanner package. |
| `scanner_short_description` | Short description of the scanner. |
| `scanner_finish_time_unix_timestamp_ms` | Unix timestamp (in milliseconds) when the scanner finished running. |
| `scanner_finish_time_formatted` | Human-readable formatted date and time when the scanner finished running. |
| `findings` | Array of finding objects. Each finding object contains the following fields. |

Expand

Show lessSee more

| Finding field | Description |
| --- | --- |
| `event_id` | Unique identifier for the event. |
| `finding_identifier` | Identifier for the finding. Can be used for deduplication. |
| `finding_severity` | Severity level of the finding. |
| `at_risk_entities` | Array of at-risk entity objects. Each entity contains `entity_detail`, `entity_id`, `entity_name`, and `entity_object_type`. This field might be excluded or truncated. |
| `total_at_risk_count` | Total number of at-risk entities. This field might be excluded. |
| `metadata` | Additional metadata. The structure depends on the scanner. This field might be excluded. |
| `note` | A note indicating whether the list of at-risk entities has been truncated. This field is present only when truncation occurs to meet the size limit constraints. If truncated, you can retrieve the full list of at-risk entities by querying the Trust Center findings. |

Expand

Show lessSee more

### Troubleshoot notification issues

If notifications are not being delivered as expected, you can query the following to examine the notification sending flow.

To check notifications sent through the notification platform:

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.NOTIFICATION_HISTORY());
```

To check scanner notifications sent through Trust Center:

Copy code

```
SELECT * FROM SNOWFLAKE.TRUST_CENTER.NOTIFICATION_HISTORY ORDER BY SENT_ON DESC;
```
