Schema:
:   [DATA\_SHARING\_USAGE](/sql-reference/data-sharing-usage)

# APPLICATION\_STATE view

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This view in the DATA\_SHARING\_USAGE schema can be used to display information about apps installed
from a listing for all application packages in the current account.

If a listing was published using
[Cross-Cloud Auto-Fulfillment](/collaboration/provider-listings-auto-fulfillment),
this view displays information for installed apps across all regions.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| CONSUMER\_SNOWFLAKE\_REGION | VARCHAR | The Snowflake region of the consumer account where the app is installed. |
| CONSUMER\_ORGANIZATION\_NAME | VARCHAR | The organization name of the consumer account. |
| CONSUMER\_ACCOUNT\_LOCATOR | VARCHAR | The consumer account locator. |
| CONSUMER\_ACCOUNT\_NAME | VARCHAR | The consumer account name. |
| PROVIDER\_SNOWFLAKE\_REGION | VARCHAR | The Snowflake region of the provider account that created the application package. |
| PROVIDER\_ACCOUNT\_LOCATOR | VARCHAR | The provider account locator. |
| PROVIDER\_ACCOUNT\_NAME | VARCHAR | The provider account name. |
| PACKAGE\_NAME | VARCHAR | The current name for the application package in the provider’s account from which the app was installed. |
| APPLICATION\_NAME\_HASH | VARCHAR | The hash string of the name of the installed app instance in the consumer account. The consumer uses the [SYSTEM$GET\_HASH\_FOR\_APPLICATION](/sql-reference/functions/system_get_hash_for_application) function to calculate the hash value of the installed application. The consumer can then use this value when contacting the provider. |
| CREATED\_ON | DATETIME | The timestamp when the app instance was first installed. |
| CURRENT\_VERSION | VARCHAR | The current version of the app. |
| CURRENT\_PATCH | INT | The current patch level of the app. |
| CURRENT\_INSTALLED\_ON | DATETIME | The timestamp when the current version of the app was installed. |
| PREVIOUS\_VERSION\_STATE | VARCHAR | The state of the previous version. Possible values are COMPLETE and FINALIZING.   - `COMPLETE` indicates that upgrade is completed and that there are no active   queries being executed from the previous version, if it exists. - `FINALIZING` indicates that the instance has been upgraded from the previous version,   however one or more queries may be still be running that are using the previous version. |
| PREVIOUS\_VERSION | VARCHAR | The previous version of the app. |
| PREVIOUS\_PATCH | INT | The previous patch level of the app. |
| UPGRADE\_STATE | VARCHAR | The version upgrade state of the app. See [Application version upgrade states](#label-app-state-view-application-version-upgrade-states) for more information. |
| TARGET\_UPGRADE\_VERSION | VARCHAR | The target version of the app that is running or pending upgrade. |
| TARGET\_UPGRADE\_PATCH | INT | The version patch level of the app that is running or pending upgrade. |
| UPGRADE\_STARTED\_ON | DATETIME | The timestamp when the app upgrade started. |
| UPGRADE\_ATTEMPT | INT | The number of attempts to upgrade to the target version or patch. |
| UPGRADE\_ATTEMPTED\_ON | DATETIME | The timestamp when the most recent upgrade attempt was attempted. |
| UPGRADE\_FAILURE\_REASON | VARCHAR | A description of the failure if the previous app upgrade failed. |
| LISTING\_NAME | VARCHAR | The name of the listing on the data exchange from which the app was installed. |
| LISTING\_DISPLAY\_NAME | VARCHAR | The display name of the listing. |
| EXCHANGE\_NAME | VARCHAR | The data exchange name of the listing from which the app was installed. |
| LAST\_HEALTH\_STATUS | VARCHAR | The last reported health status of the app. Possible values are:   - OK - FAILED - PAUSED |
| LAST\_HEALTH\_STATUS\_UPDATED\_ON | VARCHAR | The timestamp when the health status was last reported. |
| ENABLED\_TELEMETRY\_EVENT\_DEFINITIONS | VARCHAR | A list of event definitions that the consumer has enabled. See [About event definitions](https://other-docs.snowflake.com/en/native-apps/consumer-enable-logging#about-event-sharing) for more information. |
| UPGRADE\_STATE\_UPDATED\_ON | TIMESTAMP\_LTZ | The timestamp when the app entered its current upgrade state. This value is automatically set by Snowflake. |
| DISABLEMENT\_REASONS | VARCHAR | An array containing the reasons why the Snowflake Native App was disabled. See [Reasons an app can become disabled](#label-app-state-view-disablement-reasons). |

Expand

Show lessSee more

## Reasons an app can become disabled

The following table lists the possible values for the DISABLEMENT\_REASONS column:

| Value | Status description | Is recoverable? |
| --- | --- | --- |
| MANUALLY\_DISABLED | The app is disabled by Snowflake | Yes. To re-enable the app, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support). |
| ACCOUNT\_INACTIVE | The account becomes inactive by being locked or suspended causing the app to be unavailable. In this state a consumer cannot execute any SQL queries in their account and the app cannot be upgraded. | Yes. The app is automatically re-enabled if the account lock or suspension is removed |
| PACKAGE\_VERSION\_IS\_MISSING | The application package version for the app was dropped by the provider. | Possibly. This can be caused by a temporary platform outage, in which case the app may recover automatically. Otherwise, the provider can work with Snowflake Support to attempt version recovery. Contact the application provider for more details. |
| CMK\_ACCESS\_DENIED | The consumer manages the encryption key themselves (ENCRYPT\_USE\_CMK\_KMS is enabled) and Snowflake doesn’t have access to this key. | Yes. To re-enable the app, ensure that the cloud provider configuration to retrieve the CMK is correct and that Snowflake has access to the key. |
| LISTING\_ACCESS\_REVOKED | The listing used to create the app is no longer available. Possible reasons for this status include:   - The provider deleted the listing - The provider manually removed access to the private listing from the consumer account | Possibly. Recoverability depends on the reason why access was revoked.  For example, if the listing was deleted it is not recoverable. If a consumer account was manually removed from the private listing, access to the listing and app can be restored. |
| LISTING\_TRIAL\_USAGE\_EXCEEDED | The application has exceeded the usage limit for a usage-based trial listing. | No |
| LISTING\_PAYMENT\_REQUIRED | The listing used to install the app is a paid listing and requires payment for further usage. | Yes. The consumer must correctly set up payment for the app. |
| LISTING\_TRIAL\_TIME\_EXCEEDED | The application exceeded the trial duration. | No |
| APPLICATION\_PACKAGE\_NOT\_AVAILABLE | The application package used to create the app no longer exists. The provider may have dropped the corresponding application package. | No |
| APPLICATION\_PACKAGE\_DISABLED | The application package used to create the app is disabled by the Snowflake. | Yes. The app is re-enabled, if Snowflake re-enables the application package. |
| APPLICATION\_SUSPENDED | The app resources for example, tasks, services, and compute pools, are suspended due to the app being disabled.  The suspended objects remain suspended until the app is re-enabled and there are no other reasons the app was disabled. | Yes |
| APPLICATION\_SUSPEND\_RESUME\_IN\_PROGRESS | The app resources, for example tasks, services, and compute pools, are currently resuming. | Yes |

Expand

Show lessSee more

## Application version upgrade states

The following are the possible values for the UPGRADE\_STATE column:

- `INSTALLING`: The application object is in the process of being created.
- `INSTALL_FAILED`: The creation of the application object failed. The application object
  remains in the `INSTALL_FAILED` state until it is dropped. See the `UPGRADE_FAILURE_REASON`
  column of the [DESCRIBE APPLICATION](/sql-reference/sql/desc-application) command for information about why the
  installation or upgrade failed.
- `COMPLETE`: The setup script successfully completed and the application object was created
  or upgraded.
- `QUEUED`: The application object is queued for upgrade.
- `UPGRADING`: The application object is in the process of being upgraded.
- `FAILED`: All upgrade attempts failed. The reason for the failure is listed in the
  `UPGRADE_FAILURE_REASON` column, if present. The instance remains in the `FAILED` state until
  a release directive is updated to point to a different version than the one that the upgrade was
  targeting, as defined in the `TARGET_UPGRADE_VERSION` column.
- `QUEUED_DELAYED`: The application object is queued for an upgrade that is scheduled for a future time.
- `QUEUED_RETRY`: The instance failed one or more upgrade attempts. The reason for the failure
  is indicated in `UPGRADE_FAILURE_REASON`: The instance is queued to perform another upgrade attempt.
- `DISABLED`: The application object and its upgrades were disabled. In this state the instance will be
  inaccessible for consumers, it will not be considered for upgrades and will not block application package
  version drop. The reason for the failure is listed in the `UPGRADE_FAILURE_REASON` column, if present.

## Usage notes

- There is no data retention for this view. If an app is uninstalled the information
  contained in this view is no longer available.
