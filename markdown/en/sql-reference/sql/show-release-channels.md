# SHOW RELEASE CHANNELS

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Lists the
[release channels](/developer-guide/native-apps/release-channels) for
an application package or listing.

## Syntax

Copy code

```
SHOW RELEASE CHANNELS IN APPLICATION PACKAGE <application_package_name>

SHOW RELEASE CHANNELS IN LISTING <listing_name>
```

## Parameters

`application_package_name`
:   Specifies the identifier of the application package.

`listing_name`
:   Specifies the identifier of the listing.

## Output

The command output displays release channel properties and metadata in the following columns:

**Output for application packages**

| Column | Description |
| --- | --- |
| `name` | The type of the release channel. The following values are possible: `QA`, `ALPHA`, and `DEFAULT`. |
| `description` | A description of the release channel. |
| `versions` | The versions defined in the release channel. |
| `default_version_name` | The name of the version specified in the default release directive of the release channel. |
| `default_patch_number` | The patch number in the default release directive of the release channel. |
| `targets` | The target accounts added to the release channel. This only applies to the nondefault channels.  You cannot add target accounts to the default channel. However, you can add targets to the custom release directives of the default release channel. |
| `created_on` | The timestamp when the release channel was created. |
| `updated_on` | The timestamp when the release channel was last updated. |

Expand

Show lessSee more

**Output for listings**

| Column | Description |
| --- | --- |
| `name` | The type of the release channel. The following values are possible: `QA`, `ALPHA`, and `DEFAULT`. |
| `version` | The version of the app included in the listing. |
| `patch` | The patch number of the app included in the listing. |
| `description` | A description of the release channel. |
| `created_on` | The timestamp when the release channel was created. |
| `updated_on` | The timestamp when the release channel was last updated. |

Expand

Show lessSee more
