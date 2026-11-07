# Trust Center organization-level configuration procedures

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

## Overview

The following stored procedures are used to configure scanner and scanner package settings at the organization level. Scanners can be provided by Snowflake or by [third-party security partners](/user-guide/trust-center/trust-center-extensions).

### Usage notes and requirements

- These procedures require the SNOWFLAKE.TRUST\_CENTER\_ADMIN application role.
- These procedures also require access to [premium views](/user-guide/organization-accounts-premium-views), which are associated with Enterprise Edition or higher.

### Scanner configuration precedence

Scanner configuration settings can be applied as a default on the scanner or package, at the account level, or at the organization level. Scanner settings are applied according to
the following order of precedence, where 1 is the lowest precedence, and 6 is the highest precedence. The setting set at the highest level of precedence is applied.

1. Default package setting (lowest precedence).
2. Default scanner setting.
3. Organization-level package setting (these procedures).
4. Organization-level scanner setting (these procedures).
5. Account-level package setting.
6. Account-level scanner settings (highest precedence).

### Discovering the scanner ID, scanner package ID, and provider ID

To discover the ID of a scanner, scanner package, or provider, run the following SQL command:

Copy code

```
SELECT 'SNOWFLAKE' AS provider_id, scanner_package_id, id AS scanner_id FROM SNOWFLAKE.TRUST_CENTER.SCANNERS;
```

## SET\_ORG\_PACKAGE\_CONFIGURATION

Schema:
:   SNOWFLAKE.TRUST\_CENTER

Configures the schedule and notification settings for a scanner package at the organization level.

### Syntax

Copy code

```
SNOWFLAKE.TRUST_CENTER.SET_ORG_PACKAGE_CONFIGURATION(
  <provider_id>,
  <scanner_package_id>,
  <enabled>,
  <schedule>,
  <notification>
);
```

### Arguments

`provider_id`
:   The VARCHAR ID of the provider of the specified scanner package. [Learn how to get this value.](#label-trust-center-get-scanner-provider-ids)

`scanner_package_id`
:   The VARCHAR ID of the scanner package that contains the specified scanner. [Learn how to get this value.](#label-trust-center-get-scanner-provider-ids)

`enabled`
:   A BOOLEAN value that specifies whether this scanner package should be active. { TRUE | FALSE }

`schedule`
:   A VARCHAR CRON expression describing how often the scanner package should run. See the USING CRON syntax described for the SCHEDULE parameter in [CREATE TASK](/sql-reference/sql/create-task).

`notification`
:   A JSON-formatted string that specifies whom to notify when a scanner alert is tripped. The string must be in the following format:

    Copy code

    ```
    {
      "SEVERITY_THRESHOLD": "<severity>",
      "NOTIFY_ADMINS": <admins_bool>,
      "USERS": [<users_list>]
    }
    ```

    Field descriptions:

    - `severity` is one of the following values:

      - “CRITICAL”
      - “HIGH”
      - “MEDIUM”
      - “LOW”
    - `admins_bool` is TRUE or FALSE. If TRUE, notify the organization and account admins, and ignore the *USERS* list. If FALSE, do not
      notify any organization or account admins, but notify the *USERS* list.
    - `users_list` is an array of Snowflake user names for valid, active Snowflake users. Example: *[‘bob’,’alice’]*.

### Returns

Returns a VARCHAR success message if the procedure succeeds.

### Examples

This example runs all scanners in the package at midnight every day and notifies two users if a CRITICAL issue is encountered:

Copy code

```
SNOWFLAKE.TRUST_CENTER.SET_ORG_PACKAGE_CONFIGURATION(
  'provider_123',
  'package_ABC',
  TRUE,
  '0 0 * * *',
  '{
    "SEVERITY_THRESHOLD": "CRITICAL",
    "NOTIFY_ADMINS": FALSE,
    "USERS": ["BOB", "CAROL"]
   }'
);
```

## UNSET\_ORG\_PACKAGE\_CONFIGURATION

Schema:
:   SNOWFLAKE.TRUST\_CENTER

Removes the organization-level configuration for the specified scanner package. [See how this affects the configuration precedence.](#label-trust-center-scanner-config-precedence)

### Syntax

Copy code

```
SNOWFLAKE.TRUST_CENTER.UNSET_ORG_PACKAGE_CONFIGURATION(
  <provider_id>,
  <scanner_package_id>
);
```

### Arguments

`provider_id`
:   The VARCHAR ID of the provider of the specified scanner package. [Learn how to get this value.](#label-trust-center-get-scanner-provider-ids)

`scanner_package_id`
:   The VARCHAR ID of the scanner package to unset the configuration for. [Learn how to get this value.](#label-trust-center-get-scanner-provider-ids)

### Returns

Returns a VARCHAR success message if the procedure succeeds.

### Examples

Copy code

```
SNOWFLAKE.TRUST_CENTER.UNSET_ORG_PACKAGE_CONFIGURATION(
  'provider_123',
  'package_ABC'
);
```

## SET\_ORG\_SCANNER\_CONFIGURATION

Schema:
:   SNOWFLAKE.TRUST\_CENTER

Configures the schedule and notification settings for a single scanner at the organization level. [See how this affects the configuration precedence.](#label-trust-center-scanner-config-precedence)

### Syntax

Copy code

```
SNOWFLAKE.TRUST_CENTER.SET_ORG_SCANNER_CONFIGURATION(
  <provider_id>,
  <scanner_package_id>,
  <scanner_id>,
  <enabled>,
  <schedule>,
  <notification>
);
```

### Arguments

**Required:**

`provider_id`
:   The VARCHAR ID of the provider of the specified scanner package. [Learn how to get this value.](#label-trust-center-get-scanner-provider-ids)

`scanner_package_id`
:   The VARCHAR ID of the scanner package that contains the specified scanner. [Learn how to get this value.](#label-trust-center-get-scanner-provider-ids)

`scanner_id`
:   The VARCHAR ID of the scanner being configured. [Learn how to get this value.](#label-trust-center-get-scanner-provider-ids)

`enabled`
:   A BOOLEAN value that specifies whether this scanner package should be active. { TRUE | FALSE }

`schedule`
:   A VARCHAR CRON expression describing how often the scanner should run. See the USING CRON syntax described for the SCHEDULE parameter in [CREATE TASK](/sql-reference/sql/create-task).

`notification`
:   A JSON-formatted string that specifies whom to notify when a scanner alert is tripped. The string must be in the following format:

    Copy code

    ```
    {
      "SEVERITY_THRESHOLD": "<severity>",
      "NOTIFY_ADMINS": <admins_bool>,
      "USERS": [ <users_list> ]
    }
    ```

    Field descriptions:

    - `severity` is one of the following values:

      - ‘CRITICAL’
      - ‘HIGH’
      - ‘MEDIUM’
      - ‘LOW’
    - `admins_bool` is TRUE or FALSE. If TRUE, notify the organization and account admins, and ignore the *USERS* list. If FALSE, do not
      notify any organization or account admins, but notify the *USERS* list.
    - `users_list` is an array of Snowflake user names for valid, active Snowflake users. This is ignored if you have set NOTIFIY\_ADMINS to TRUE.
      Example: *[‘bob’,’alice’]*.

### Returns

Returns a VARCHAR success message if the procedure succeeds.

### Examples

This example runs the scanner daily at midnight and notifies the admins if a CRITICAL issue is encountered:

Copy code

```
SNOWFLAKE.TRUST_CENTER.SET_ORG_SCANNER_CONFIGURATION(
  'provider_123',
  'package_ABC',
  'scanner_XYZ',
  TRUE,
  '0 0 * * *',
  '{
    "SEVERITY_THRESHOLD": "CRITICAL",
    "NOTIFY_ADMINS": TRUE
   }'
);
```

## UNSET\_ORG\_SCANNER\_CONFIGURATION

Schema:
:   SNOWFLAKE.TRUST\_CENTER

Removes the organization-level configuration for the specified scanner. [See how this affects the configuration precedence.](#label-trust-center-scanner-config-precedence)

### Syntax

Copy code

```
SNOWFLAKE.TRUST_CENTER.UNSET_ORG_SCANNER_CONFIGURATION(
  <provider_id>,
  <scanner_package_id>,
  <scanner_id>
);
```

### Arguments

**Required:**

`provider_id`
:   The VARCHAR ID of the provider of the specified scanner package. [Learn how to get this value.](#label-trust-center-get-scanner-provider-ids)

`scanner_package_id`
:   The VARCHAR ID of the scanner package that contains the specified scanner. [Learn how to get this value.](#label-trust-center-get-scanner-provider-ids)

`scanner_id`
:   The VARCHAR ID of the scanner to remove the configuration for. [Learn how to get this value.](#label-trust-center-get-scanner-provider-ids)

### Returns

Returns a VARCHAR success message if the procedure succeeds.

### Examples

Copy code

```
SNOWFLAKE.TRUST_CENTER.UNSET_ORG_SCANNER_CONFIGURATION(
  'provider_123',
  'package_ABC',
  'scanner_XYZ'
);
```
