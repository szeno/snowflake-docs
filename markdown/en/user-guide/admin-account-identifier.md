# Account identifiers

An account identifier uniquely identifies a Snowflake account within your [organization](/user-guide/organizations), as well as
throughout the global network of Snowflake-supported [cloud platforms](/user-guide/intro-cloud-platforms) and
[cloud regions](/user-guide/intro-regions).

The preferred account identifier consists of the *name* of the account prefixed by its organization; for example, `myorg-account123`. You
can also use the Snowflake-assigned *locator* as the account identifier; however, the use of this legacy format is *not recommended*.

## Requirements for account identifiers

> Important
>
> To prevent DNS resolution failures, an account identifier should meet all the following requirements:
>
> - Must be unique within an organization, regardless of which Snowflake region the account is in.
> - Must start with an alphabetic character and can’t contain spaces or special characters *except for* underscores (`_`).
> - Shouldn’t end with `_`.
> - If the account name includes `_`, features that don’t accept account names with `_`, such as Okta SSO or SCIM, can reference a version
>   of the account identifier that substitutes a hyphen (`-`) for each `_` character.
> - The account identifier string length, including the organization name, account name, and `-` characters, shouldn’t exceed 63 characters.
> - Names should comply with the “Letter, Digit, Hyphen” (LDH) rule defined in [RFC 952](https://datatracker.ietf.org/doc/html/rfc952).

## Where are account identifiers used?

Account identifiers are required in Snowflake wherever you need to specify the account you are using, including:

- URLs for accessing any of the Snowflake web interfaces.
- Snowflake CLI, SnowSQL, and other clients (such as connectors and drivers) for connecting to Snowflake.
- Third-party applications and services that comprise the Snowflake ecosystem.
- Security features for protecting Snowflake internal operations and communication/interaction with external systems.
- Global features such as [Secure Data Sharing](/user-guide/data-sharing-intro) and [Replication and Failover/Failback](/user-guide/replication-intro).

For example, the URL for an account uses the following format:

`account_identifier.snowflakecomputing.com`

If your organization uses the [Client Redirect](/user-guide/client-redirect) feature, the name of a
[connection object](/user-guide/client-redirect#label-intro-to-client-redirect) can be used in place of the account name in the account identifier
to connect to a Snowflake account using a Snowflake client. For more information, see [Using a connection URL](/user-guide/client-redirect#label-using-a-connection-url).

For more information about using account identifiers and connections to connect to a Snowflake account, see
[Connecting to your accounts](/user-guide/organizations-connect).

## Format 1 (preferred): Account name in your organization

An [organization](/user-guide/organizations) is a Snowflake object that links the accounts owned by your business
entity. [Organization administrators](/user-guide/organization-administrators) view, create, and manage all of your
accounts across different cloud platforms and regions.

Account names must be unique within your organization, and can be changed, which allows more flexibility and leads to shorter and more
intuitive account names. You specify an account name when you create a new account
(see [Creating an account](/user-guide/organizations-manage-accounts-create)). To change a name
for an existing account, see [Renaming an account](/user-guide/organizations-manage-accounts-rename).

While an account name uniquely identifies an account within your organization, it is *not* a unique identifier of an account
across Snowflake organizations.

Account names with underscores also have a dashed version of the URL for features that don’t accept URLs with underscores, such as
Okta SSO/SCIM.

The next sections explain the format to use and how to find your account identifier:

- [Finding the organization and account name for an account](#label-account-name-find)
- [Understanding the format to use for the identifier](#label-account-name-using)
- [Organization and account names](#label-organization-and-account-name)

### Finding the organization and account name for an account

To find the organization and account name for an account, you can use Snowsight or SQL.

Snowsight:
:   1. Open the account selector and review the list of accounts that you previously signed in to.

       > ![Screenshot of the account selector open and listing multiple accounts. The account selector is labeled with the name of the currently-selected account.](/static/images/snowsight/snowsight-gs-account-details.png)
    2. Select **View account details**.

       The **Account Details** dialog displays information about the account, including the account identifier and the account URL.

    The following table lists some examples of getting the different forms of the account identifier:

    | Use case | Instructions |
    | --- | --- |
    | Get the [data sharing account identifier](#label-account-name-data-sharing) (for example, if a provider wants to share a private listing with you). | Copy the value in the **Data Sharing Account Identifier** field. |
    | Get the Snowflake account URL for configuring a third-party tool (such as Tableau or PowerBI) to connect to Snowflake. | Copy the value in the **Account/Server URL** field.  See [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config). |
    | Set up a configuration file for a client (such as [Snowflake CLI](/developer-guide/snowflake-cli/index) or [SnowSQL](/user-guide/snowsql)). | Select the **Config File** tab.  See [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config). |
    | Configure a driver (such as the [ODBC](/developer-guide/odbc/odbc) or [JDBC](/developer-guide/jdbc/jdbc) driver) or library. | Select the **Connectors/Drivers** tab.  See [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config). |

    Expand

    Show lessSee more

SQL:
:   In the [Account Details](#label-account-name-find-snowsight) dialog in Snowsight, you can select the
    **SQL Commands** tab to find and copy the SQL statement that returns the account identifier.

    If you want to construct the account identifier yourself:

    - To retrieve the organization of the current account, call the [CURRENT\_ORGANIZATION\_NAME](/sql-reference/functions/current_organization_name) function.
    - To retrieve the name of the current account, call the [CURRENT\_ACCOUNT\_NAME](/sql-reference/functions/current_account_name) function.

    For details on the format to use for the identifier, see [Understanding the format to use for the identifier](#label-account-name-using).

    For example, to get the account identifier for configuring a client, driver, or library to connect to Snowflake, run:

    Copy code

    ```
    SELECT CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME();
    ```

### Understanding the format to use for the identifier

The account identifier for an account in your organization takes one of the following forms, depending on where and how you use
the identifier:

- [Specifying the account name when connecting to Snowflake](#label-account-name-using-connecting)
- [Specifying the fully qualified account name in a SQL statement](#label-account-name-using-sql-statement)
- [Providing your data sharing account identifier](#label-account-name-data-sharing)

#### Specifying the account name when connecting to Snowflake

The following table lists some of the commonly used forms of the account identifier, based on the use case:

| Use cases | Format to use |
| --- | --- |
| Using a URL to [sign in to Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in). | `orgname-account_name.snowflakecomputing.com` |
| Specifying the Snowflake account URL when configuring a third-party tool (such as Tableau or PowerBI) to [connect to Snowflake](/user-guide/gen-conn-config). | `orgname-account_name.snowflakecomputing.com` |
| Specifying the Snowflake account when configuring a client, driver, or library to [connect to Snowflake](/user-guide/gen-conn-config):   - Specifying the account in a configuration file for a client (such as   [Snowflake CLI](/developer-guide/snowflake-cli/index) or [SnowSQL](/user-guide/snowsql)) to   [connect to Snowflake](/user-guide/gen-conn-config). - Specifying the account when configuring a driver (such as the [ODBC](/developer-guide/odbc/odbc) or   [JDBC](/developer-guide/jdbc/jdbc) driver) or library to   [connect to Snowflake](/user-guide/gen-conn-config). | `orgname-account_name` |

Expand

Show lessSee more

Where:

- `orgname` is the [name of your Snowflake organization](#label-account-name-find).
- `account_name` is the [unique name of your account within your organization](#label-account-name-find).

To get the account identifier in the correct format for clients, drivers, libraries, and third-party applications, you can use
Snowsight. For more information, see [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).

Note

For scenarios/features where underscores in an account name are not supported, use hyphens instead of underscores.

For example, in a [configuration file for Snowflake CLI](/developer-guide/snowflake-cli/connecting/configure-cli), if your
organization is `myorganization` and your account is `myaccount`, set `account` to:

Copy code

```
[connections]
[connections.myconnection]
account = "myorganization-myaccount"
```

#### Specifying the fully qualified account name in a SQL statement

In a SQL statement, when specifying the fully qualified account name, use a period between the
[organization name and account name](#label-account-name-find):

> `orgname.account_name`

#### Providing your data sharing account identifier

When a [provider](https://other-docs.snowflake.com/en/collaboration/collaboration-listings-about) plans to share a [private listing](https://other-docs.snowflake.com/en/collaboration/collaboration-listings-about) with you, the provider will ask you for your account identifier. This is
referred to as the *data sharing account identifier*.

Specify your account identifier in the following format, using a period between the
[organization name and account name](#label-account-name-find):

> `orgname.account_name`

### Organization and account names

#### Organization name

For users who sign up for a Snowflake account using the self-service option, an organization is automatically created with a
system-generated name when the account is created. For entities who work directly with Snowflake personnel to set up accounts,
Snowflake can assign the organization a custom name. This custom name must be unique across all other organizations in Snowflake.
The name must start with a letter and can only contain letters (lowercase and uppercase) and numbers. The name can’t contain underscores
or other delimiters.

If you want to change the name of an organization, for example to change a system-generated name to a more user-friendly one,
contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

As a best practice, review and change your organization name, if needed, before using the name in any account identifiers. Renaming
the organization name in the future will result in changing all the URLs for your Snowflake accounts to match the new name.

To view the name of your organization, see [Viewing the name of your organization and its accounts](/user-guide/organizations#label-viewing-organization-name).

#### Account name

Each account name must be unique within your organization. You specify an account name when you create the account (see [Creating an account](/user-guide/organizations-manage-accounts-create)).

While an account name uniquely identifies an account within your organization, it is *not* a unique identifier of an account across
Snowflake organizations. To uniquely identify an account in Snowflake, you must prepend your organization name to the account name. For
example:

`orgname-account_name`

Consistent with SQL standards for identifiers, account names can include underscores as separators between words, such as `MARKETING_TEST_ACCOUNT`.

URLs that include underscores can sometimes cause issues for certain features, such as Okta SSO/SCIM. For this reason, Snowflake also
supports a version of the account name that substitutes the hyphen character (`-`) in place of the underscore character. For example
both of the following URLs are supported:

> URL with underscores: `https://acme-marketing_test_account.snowflakecomputing.com`
>
> URL with dashes: `https://acme-marketing-test-account.snowflakecomputing.com`

#### Existing accounts

If you have any accounts that existed before the Organizations feature was enabled, the [Format 2: Account locator in a region](#label-account-locator) is used as the
account name.

In addition, if you have existing accounts with the same name in different regions, the cloud and region names are appended to the
account name in the new URL format.

For example, if your organization name is `ACME`, and there are two accounts named `TEST`, one in the AWS `us-east-2` region
and the other in the Azure `west-us-2` region, the new URLs will use the following structure:

- First account:

  Original URL:
  :   `https://test.us-east-2.aws.snowflakecomputing.com`

  New URL:
  :   `https://acme-test_aws_us_east_2.snowflakecomputing.com`
- Second account:

  Original URL:
  :   `https://test.west-us-2.azure.snowflakecomputing.com`

  New URL:
  :   `https://acme-test_azure_west_us_2.snowflakecomputing.com`

These account names can be changed as long as the new names are unique. For instructions on how to change an account name, see [Renaming an account](/user-guide/organizations-manage-accounts-rename).

## Format 2: Account locator in a region

An account locator is an identifier assigned by Snowflake when the account is created:

- If the account is created by a Snowflake representative, you may be able to request a specific value for the locator, such as a
  company name, acronym, or other recognizable string.
- If the account is created through self-service or an automated/background process, the locator is a random string of unique characters
  and numbers, such as `xy12345`).

The locator for an account can’t be changed once the account is created.

Note

Account locators continue to be supported for identifying accounts in Snowflake, but this is no longer the preferred method. The
preferred method for identifying accounts is now the account name within your organization (as described earlier in this topic).

The next sections explain the format to use:

- [Using an account locator as an identifier](#label-account-locator-identifier)
- [Finding the region and locator for an account](#label-account-locator-identifier-find)
- [Finding the account locator format for a VPS account](#label-account-identifier-for-vps)
- [Non-VPS account locator formats by cloud platform and region](#label-account-identifiers-locator)

### Using an account locator as an identifier

Each Snowflake account is hosted on a [cloud platform](/user-guide/intro-cloud-platforms) in a geographical
[region](/user-guide/intro-regions).

The region determines where the data in the account is stored and where the compute resources used by the account are provisioned.

When using an account locator to identify an account, the locator by itself is not always sufficient to identify the account. Depending
on the region and cloud platform for the account, *additional* segments may be required, in the form of:

`account_locator.cloud_region_id` *or*

`account_locator.cloud_region_id.cloud` *or*

`account_locator.gov_compliance.cloud_region_id.cloud`

Where:

- `cloud_region_id` is the identifier for the cloud region (dictated by the cloud platform).
- `cloud` is the identifier for the cloud platform (`aws`, `azure`, or `gcp`).
- `compliance` is for SnowGov regions only and specifies the level of U.S. government compliance supported by the region
  (`fhplus` or `dod`).

For example, if your account locator is `xy12345`:

- If the account is located in the AWS US West (Oregon) region, no additional segments are required and the URL would be
  `xy12345.snowflakecomputing.com`.
- If the account is located in the AWS US East (Ohio) region, additional segments are required and the URL would be
  `xy12345.us-east-2.aws.snowflakecomputing.com`.

For a complete list of regions and locator formats, see [Non-VPS Account Locator Formats by Cloud Platform and Region](#non-vps-account-locator-formats-by-cloud-platform-and-region) (in this topic).

Note

If your Snowflake Edition is [VPS](/user-guide/intro-editions#label-snowflake-editions-vps), the account locator uses a different format. See
[Finding the account locator format for a VPS account](#label-account-identifier-for-vps) (in this topic).

### Finding the region and locator for an account

To find the region and locator for an account, you can use Snowsight or SQL.

Snowsight:
:   1. Open the account selector and review the list of accounts that you previously signed in to.

       > ![Screenshot of the account selector open and listing multiple accounts. The account selector is labeled with the name of the currently-selected account.](/static/images/snowsight/snowsight-gs-account-details.png)
    2. Select **View account details**.

       The **Account Details** dialog displays information about the account, including the account identifier and the account URL.

    You can copy the full account locator from the **Full Account Locator** field.

SQL:
:   If you can connect to your Snowflake account, call the following context functions to identify the region and account locator
    for the Snowflake account you are connected to:

    - Call [CURRENT\_REGION](/sql-reference/functions/current_region) to retrieve the region in which your account is located.
    - Call [CURRENT\_ACCOUNT](/sql-reference/functions/current_account) to retrieve the account locator.

If you are unable to connect to Snowflake, contact the Snowflake administrator for your account to retrieve this information.

### Finding the account locator format for a VPS account

If your Snowflake Edition is [VPS](/user-guide/intro-editions#label-snowflake-editions-vps), the account locator format uses different
naming conventions than the accounts for other Snowflake Editions. This results in a different structure for the hostnames and URLs used to
access VPS accounts.

For details, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) or your Snowflake representative.

As an alternative, you can use the preferred format of `organization_name-account_name` as your account identifier. This
format works for accounts that use the VPS edition. For details, see [Format 1 (preferred): Account name in your organization](#label-account-name) (in this topic).

### Non-VPS account locator formats by cloud platform and region

The following table lists the account locator formats across all the supported non-VPS regions, including whether the account locator
for a given region requires additional segments:

If your account locator is `xy12345`:

| Cloud Platform / Region | Account Identifier | Notes |
| --- | --- | --- |
| **Amazon Web Services (AWS)** |  |  |
| US West (Oregon) | `xy12345` | No additional segments required. |
| US West (Commercial Gov - Oregon) | `xy12345.us-west-2-gov.aws` |  |
| US Gov West 1 (FedRAMP High Plus) | `xy12345.fhplus.us-gov-west-1.aws` | Additional `fhplus` segment required after the account locator. |
| US Gov West 1 (DoD) | `xy12345.dod.us-gov-west-1.aws` | Additional `dod` segment required after the account locator. |
| US East (Ohio) | `xy12345.us-east-2.aws` |  |
| US East (N. Virginia) | `xy12345.us-east-1` | Cloud region ID is the only additional segment required. |
| US East (Commercial Gov - N. Virginia) | `xy12345.us-east-1-gov.aws` |  |
| US Gov East 1 (FedRAMP High Plus) | `xy12345.fhplus.us-gov-east-1.aws` | Additional `fhplus` segment required after the account locator. |
| Canada (Central) | `xy12345.ca-central-1.aws` |  |
| South America (Sao Paulo) | `xy12345.sa-east-1.aws` |  |
| Africa (Cape Town) | `xy12345.af-south-1.aws` |  |
| EU (Ireland) | `xy12345.eu-west-1` | Cloud region ID is the only additional segment required. |
| Europe (London) | `xy12345.eu-west-2.aws` |  |
| EU (Paris) | `xy12345.eu-west-3.aws` |  |
| EU (Frankfurt) | `xy12345.eu-central-1` | Cloud region ID is the only additional segment required. |
| EU (Zurich) | `xy12345.eu-central-2.aws` |  |
| EU (Stockholm) | `xy12345.eu-north-1.aws` |  |
| Middle East (UAE) | `xy12345.me-central-1.aws` |  |
| Asia Pacific (Tokyo) | `xy12345.ap-northeast-1.aws` |  |
| Asia Pacific (Osaka) | `xy12345.ap-northeast-3.aws` |  |
| Asia Pacific (Seoul) | `xy12345.ap-northeast-2.aws` |  |
| Asia Pacific (Mumbai) | `xy12345.ap-south-1.aws` |  |
| Asia Pacific (Singapore) | `xy12345.ap-southeast-1` | Cloud region ID is the only additional segment required. |
| Asia Pacific (Sydney) | `xy12345.ap-southeast-2` | Cloud region ID is the only additional segment required. |
| Asia Pacific (Jakarta) | `xy12345.ap-southeast-3.aws` |  |
| Asia Pacific (Malaysia) | `xy12345.ap-southeast-5.aws` |  |
| Asia Pacific (New Zealand) | `xy12345.ap-southeast-6.aws` |  |
| Asia Pacific (Thailand) | `xy12345.ap-southeast-7.aws` |  |
| China (Ningxia) | `xy12345.cn-northwest-1.aws` | This region utilizes the `snowflakecomputing.cn` domain instead of the `snowflakecomputing.com` domain utilized by the other regions. |
| **Google Cloud Platform (GCP)** |  |  |
| US Central1 (Iowa) | `xy12345.us-central1.gcp` |  |
| US East4 (N. Virginia) | `xy12345.us-east4.gcp` |  |
| Europe West2 (London) | `xy12345.europe-west2.gcp` |  |
| Europe West3 (Frankfurt) | `xy12345.europe-west3.gcp` |  |
| Europe West4 (Netherlands) | `xy12345.europe-west4.gcp` |  |
| Middle East Central2 (Dammam) | `xy12345.me-central2.gcp` |  |
| Australia Southeast 2 (Melbourne) | `xy12345.australia-southeast2.gcp` |  |
| **Microsoft Azure** |  | Snowflake added hyphens to the Azure region IDs for consistency with AWS and GCP. |
| West US 2 (Washington) | `xy12345.west-us-2.azure` |  |
| Central US (Iowa) | `xy12345.central-us.azure` |  |
| South Central US (Texas) | `xy12345.south-central-us.azure` |  |
| East US (Virginia) | `xy12345.east-us.azure` |  |
| East US 2 (Virginia) | `xy12345.east-us-2.azure` |  |
| US Gov Virginia (FedRAMP High Plus) | `xy12345.fhplus.us-gov-virginia.azure` |  |
| US Gov Virginia | `xy12345.us-gov-virginia.azure` |  |
| Canada Central (Toronto) | `xy12345.canada-central.azure` |  |
| Mexico Central (Mexico City) | `xy12345.mexicocentral.azure` |  |
| UK South (London) | `xy12345.uk-south.azure` |  |
| North Europe (Ireland) | `xy12345.north-europe.azure` |  |
| Sweden Central (Gävle) | `xy12345.sweden-central.azure` |  |
| West Europe (Netherlands) | `xy12345.west-europe.azure` |  |
| Switzerland North (Zurich) | `xy12345.switzerland-north.azure` |  |
| UAE North (Dubai) | `xy12345.uae-north.azure` |  |
| Central India (Pune) | `xy12345.central-india.azure` |  |
| Japan East (Tokyo) | `xy12345.japan-east.azure` |  |
| Korea Central (Seoul) | `xy12345.korea-central.azure` |  |
| Southeast Asia (Singapore) | `xy12345.southeast-asia.azure` |  |
| Australia East (New South Wales) | `xy12345.australia-east.azure` |  |

Expand

Show lessSee more

## Account identifiers for private connectivity

If private connectivity to the Snowflake service is enabled for your account and you wish to use the feature to connect to Snowflake,
run the [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) function to determine the private connectivity URL to use.
You can use either the account name or account locator in the URL to connect to the Snowflake web interface.

If you want to connect to Snowsight using private connectivity, use the following instructions in the
[Signing in to Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).

## Account identifiers for replication and failover

The preferred method of identifying an account in replication and failover related SQL commands uses the organization name and account name
as the account identifier. If you decide to use the legacy account locator instead, it may need to contain additional segments in order to
uniquely identify the account. See the table below for reference:

> | Account Identifier | Location of the Remote Account |
> | --- | --- |
> | `organization_name.account_name` | Preferred account identifier that can be used regardless of the region or region group of the account that stores the primary database. |
> | `account_locator` | Same region but a different account from the account that stores the primary database. |
> | `snowflake_region.account_locator` | Same region group but a different region from the account that stores the primary database. |
> | `region_group.snowflake_region.account_locator` | Different [region group](/user-guide/admin-account-identifier#label-region-groups) from the account that stores the primary database. |
>
> Expand
>
> Show lessSee more

The values for `snowflake_region` and `region_group` can be found in the output of [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts).

## Snowflake region IDs and region groups

A Snowflake Region is a distinct region (deployed within an AWS, Azure, or GCP cloud region) that is isolated from other Snowflake
Regions. A Snowflake Region can be either multi-tenant (containing accounts for multiple organizations) or single-tenant
(aka Virtual Private Snowflake for a single organization).

Each Snowflake Region has a unique identifier and belongs to a region group, which enables global features such as data sharing and
replication.

### Region IDs

Because each cloud platform utilizes different conventions and formats for naming their regions, Snowflake assigns a canonical ID to
each Snowflake Region that uniquely identifies it across all the cloud platforms and their regions.

If the Organizations feature is enabled, specifying the Snowflake Region ID as part of an account identifier is required when you create
a new account, as well as when you configure replication and failover.

The following table displays the complete list of Snowflake Region IDs:

| Cloud Region | Cloud Region ID | Snowflake Region ID | Notes |
| --- | --- | --- | --- |
| **Amazon Web Services (AWS)** |  |  |  |
| US West (Oregon) | `us-west-2` | `aws_us_west_2` |  |
| US West (Commercial Gov - Oregon) | `us-west-2` | `aws_us_gov_west_2` | Available only for accounts on Business Critical (or higher); located in US West 2, not [AWS GovCloud (US)](https://aws.amazon.com/govcloud-us/). |
| US Gov West 1 (FedRAMP High Plus) | `us-gov-west-1` | `aws_us_gov_west_1_fhplus` | Available only for accounts on Business Critical (or higher); located in [AWS GovCloud (US)](https://aws.amazon.com/govcloud-us/). |
| US Gov West 1 (DoD) | `us-gov-west-1` | `aws_us_gov_west_1_dod` | Available only for accounts on Business Critical (or higher); located in [AWS GovCloud (US)](https://aws.amazon.com/govcloud-us/). |
| US East (Ohio) | `us-east-2` | `aws_us_east_2` |  |
| US East (N. Virginia) | `us-east-1` | `aws_us_east_1` |  |
| US East (Commercial Gov - N. Virginia) | `us-east-1` | `aws_us_gov_east_1` | Available only for accounts on Business Critical (or higher); located in US East 1, not [AWS GovCloud (US)](https://aws.amazon.com/govcloud-us/). |
| US Gov East 1 (FedRAMP High Plus) | `us-gov-east-1` | `aws_us_gov_east_1_fhplus` | Available only for accounts on Business Critical (or higher); located in [AWS GovCloud (US)](https://aws.amazon.com/govcloud-us/). |
| Canada (Central) | `ca-central-1` | `aws_ca_central_1` |  |
| South America (Sao Paulo) | `sa-east-1` | `aws_sa_east_1` |  |
| Africa (Cape Town) | `af-south-1` | `aws_af_south_1` |  |
| EU (Ireland) | `eu-west-1` | `aws_eu_west_1` |  |
| Europe (London) | `eu-west-2` | `aws_eu_west_2` |  |
| EU (Paris) | `eu-west-3` | `aws_eu_west_3` |  |
| EU (Frankfurt) | `eu-central-1` | `aws_eu_central_1` |  |
| EU (Zurich) | `eu-central-2` | `aws_eu_central_2` |  |
| EU (Stockholm) | `eu-north-1` | `aws_eu_north_1` |  |
| Middle East (UAE) | `me-central-1` | `aws-me-central-1` |  |
| Asia Pacific (Tokyo) | `ap-northeast-1` | `aws_ap_northeast_1` |  |
| Asia Pacific (Osaka) | `ap-northeast-3` | `aws_ap_northeast_3` |  |
| Asia Pacific (Seoul) | `ap-northeast-2` | `aws_ap_northeast_2` |  |
| Asia Pacific (Mumbai) | `ap-south-1` | `aws_ap_south_1` |  |
| Asia Pacific (Singapore) | `ap-southeast-1` | `aws_ap_southeast_1` |  |
| Asia Pacific (Sydney) | `ap-southeast-2` | `aws_ap_southeast_2` |  |
| Asia Pacific (Jakarta) | `ap-southeast-3` | `aws_ap_southeast_3` |  |
| Asia Pacific (Malaysia) | `ap-southeast-5` | `aws_ap_southeast_5` |  |
| Asia Pacific (New Zealand) | `ap-southeast-6` | `aws_ap_southeast_6` |  |
| Asia Pacific (Thailand) | `ap-southeast-7` | `aws_ap_southeast_7` |  |
| China (Ningxia) | `cn-northwest-1` | `aws_cn_northwest_1` | Utilizes a different domain name (`snowflakecomputing.cn`) and is operated by Digital China Cloud Technology Limited (DCC), an authorized operating partner of Snowflake. |
| **Google Cloud Platform (GCP)** |  |  |  |
| US Central1 (Iowa) | `us-central1` | `gcp_us_central1` |  |
| US East4 (N. Virginia) | `us-east4` | `gcp_us_east4` |  |
| Europe West2 (London) | `europe-west2` | `gcp_europe_west2` |  |
| Europe West3 (Frankfurt) | `europe-west3` | `gcp_europe_west3` |  |
| Europe West4 (Netherlands) | `europe-west4` | `gcp_europe_west4` |  |
| Middle East Central2 (Dammam) | `me-central2` | `gcp_me_central2` |  |
| Australia Southeast 2 (Melbourne) | `australia-southeast2` | `gcp-australia-southeast2` |  |
| **Microsoft Azure** |  |  |  |
| West US 2 (Washington) | `westus2` | `azure_westus2` |  |
| Central US (Iowa) | `centralus` | `azure_centralus` |  |
| South Central US (Texas) | `southcentralus` | `azure_southcentralus` |  |
| East US (Virginia) | `eastus` | `azure_eastus` |  |
| East US 2 (Virginia) | `eastus2` | `azure_eastus2` |  |
| US Gov Virginia (FedRAMP High Plus) | `usgovvirginia` | `azure_usgovvirginia_fhplus` | Available only for accounts on Business Critical (or higher); located in [Microsoft Azure Government](https://docs.microsoft.com/en-us/azure/azure-government/). |
| US Gov Virginia | `usgovvirginia` | `azure_usgovvirginia` | Available only for accounts on Business Critical (or higher); located in [Microsoft Azure Government](https://docs.microsoft.com/en-us/azure/azure-government/). |
| Canada Central (Toronto) | `canadacentral` | `azure_canadacentral` |  |
| Mexico Central (Mexico City) | `mexicocentral` | `azure_mexicocentral` |  |
| UK South (London) | `uk-south` | `azure_uksouth` |  |
| North Europe (Ireland) | `northeurope` | `azure_northeurope` |  |
| Sweden Central (Gävle) | `swedencentral` | `azure_swedencentral` |  |
| West Europe (Netherlands) | `westeurope` | `azure_westeurope` |  |
| Switzerland North (Zurich) | `switzerlandnorth` | `azure_switzerlandnorth` |  |
| UAE North (Dubai) | `uaenorth` | `azure_uaenorth` |  |
| Central India (Pune) | `centralindia` | `azure_centralindia` |  |
| Japan East (Tokyo) | `japaneast` | `azure_japaneast` |  |
| Korea Central (Seoul) | `koreacentral` | `azure_koreacentral` |  |
| Southeast Asia (Singapore) | `southeastasia` | `azure_southeastasia` |  |
| Australia East (New South Wales) | `australiaeast` | `azure_australiaeast` |  |

Expand

Show lessSee more

### Region groups

A region group is a group of Snowflake Regions that offer similar security controls, isolation, and compliance. The region group to which
a Snowflake Region belongs differs depending on the region:

- All Snowflake multi-tenant commercial regions (across all the supported cloud platforms) are in the same shared/general `PUBLIC`
  group.
- Each Snowflake multi-tenant government region is in a separate group specific to the region.
- Each single-tenant Virtual Private Snowflake (VPS) is in a separate region group specific to the VPS. If your organization has more than
  one VPS, you can have one VPS per region group or multiple VPSs can share the same region group.

Specifying the region group as part of an account identifier is required when you want to create
accounts in different region groups. If you have questions about the region group of your account, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
