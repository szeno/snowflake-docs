# Installing the Snowflake Data Clean Rooms environment

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Before you begin

- If the Snowflake Data Clean Room environment is not installed for your account, follow the installation instructions on this page.
- If the clean rooms environment is installed for your account, and you want access to it, ask an administrator to provide you appropriate privileges to conduct clean room operations in your account.

## Supported regions

Snowflake Data Clean Rooms are available for Snowflake accounts in the following cloud regions:

| Cloud platform | Supported regions |
| --- | --- |
| Amazon Web Services (AWS) | - South America (Sao Paulo) - US East (N. Virginia) - US East (Ohio) - US West (Oregon) - Canada (Central) - Europe (London) - EU (Ireland) - EU (Frankfurt) - EU (Paris) - EU (Stockholm) - EU (Zurich) - Africa (Cape Town) - Asia Pacific (Mumbai) - Asia Pacific (Singapore) - Asia Pacific (Tokyo) - Asia Pacific (Osaka) - Asia Pacific (Seoul) - Asia Pacific (Jakarta) - Asia Pacific (Sydney) - Asia Pacific (Bangkok) - Asia Pacific (Kuala Lumpur) - Asia Pacific (Auckland) |
| Microsoft Azure | - Central US (Iowa) - East US (Virginia) - East US 2 (Virginia) - Mexico Central (Querétaro) - South Central US (Texas) - West US 2 (Washington) - Canada Central (Toronto) - North Europe (Ireland) - Sweden Central (Gävle) - Switzerland North (Zurich) - UAE North (Dubai) - UK South (London) - West Europe (Netherlands) - Central India (Pune) - Southeast Asia (Singapore) - Japan East (Tokyo) - Korea Central (Seoul) - Australia East (New South Wales) |
| Google Cloud (GCP) | - US Central1 (Iowa) - US East4 (N. Virginia) - Middle East Central2 (Dammam) - Europe West (Frankfurt) - Europe West2 (London) - Europe West4 (Netherlands) - Australia Southeast1 (Melbourne) |

Expand

Show lessSee more

## Requirements to install Snowflake Data Clean Rooms

### Account, installer, and user requirements

When you install the clean rooms environment, you install it for all potential users in the Snowflake account. However, access to the clean
rooms environment must be granted to users explicitly by a clean rooms administrator.

Here are the requirements to install Snowflake Data Clean Rooms in your Snowflake account:

- **The account must be the required** [Snowflake Edition](/user-guide/intro-editions):

  - **To create collaborations and be an owner**, you must have Standard Edition or higher.
  - **To join a collaboration as an analysis runner**, you must have Standard Edition or higher.
  - **To join a collaboration as a data provider or activate data to another collaborator**, you must have Enterprise Edition or higher.
- **The installer must fulfill** [these role and user requirements](#label-cleanroom-web-app-prereq-installer).
- **Reader accounts are not supported,** because reader accounts do not allow the data sharing required to install and run the clean rooms
  application.
- **You must accept data sharing terms.** If you have not accepted the
  [Snowflake Customer-Controlled Data Sharing Functionality Terms](https://www.snowflake.com/legal/data-sharing-terms/), contact
  [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support). Snowflake Data Clean Rooms use [listings](/collaboration/collaboration-listings-about), which are part
  of the Snowflake Service and subject to your Service terms with Snowflake, including the Snowflake Customer-Controlled Data Sharing
  Functionality Terms and
  [Snowflake Acceptable Use Policy](https://www.snowflake.com/legal/acceptable-use-policy/).
- **You must unset any unsupported account-level parameters.** See the [list of unsupported account-level settings](#label-dcr-unsupported-parameters).

If you do not meet all these requirements and need to upgrade, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

### Unsupported account-level parameters

Snowflake Data Clean Rooms does not support certain account-level parameter values. The following table shows the required values for these parameters:

| Parameter name | Required value | Notes |
| --- | --- | --- |
| DEFAULT\_DDL\_COLLATION | *No values supported, must be null* | [Account-level collation](/sql-reference/collation) is not supported. |
| QUOTED\_IDENTIFIERS\_IGNORE\_CASE | `false` |  |

Expand

Show lessSee more

To check a parameter in your account, run the following SQL command, substituting the parameter name for `<parameter_name>`:

Copy code

```
SHOW PARAMETERS LIKE '<parameter_name>' IN ACCOUNT;
```

For example:

Copy code

```
SHOW PARAMETERS LIKE 'DEFAULT_DDL_COLLATION' IN ACCOUNT;
```

### Role and user requirements

Here are the role requirements for the person installing the clean rooms environment:

- You must have an ACCOUNTADMIN role in a Snowflake account to install the clean rooms environment in that account.
- The user with the ACCOUNTADMIN role must have a valid first name, last name, and verified email defined for their user object. To check,
  run [DESCRIBE USER](/sql-reference/sql/desc-user).

## Install the Snowflake Data Clean Rooms environment

Follow these steps to install the clean rooms environment in your Snowflake account.

You must always install the native app (Step 1), but after that you can enable the clean rooms API for code usage (Step 2).

### 1. Install the native application

Install the native application from the marketplace:

> 1. Set your current role to ACCOUNTADMIN
> 2. Install the [Snowflake Data Clean Rooms application](https://app.snowflake.com/marketplace/listing/GZSTZTP0KKO/snowflake-snowflake-data-clean-rooms)
>    from the Snowflake Marketplace
> 3. Select **Open** and accept the default options.

Installation takes several minutes. When done, proceed to step 2.

### 2. Install the clean rooms API

The clean rooms API is required to use clean rooms either through the UI or the API.

Here are the steps to install the clean rooms API in your Snowflake account:

1. After installing the native application, launch it in Snowflake. In the navigation menu, select **Catalog** » **Apps** »
   **Snowflake Data Clean Rooms**. Click the **Open in Worksheet** button at the top right corner.
   This opens a worksheet with SQL commands.
2. Run the SQL commands to install the clean rooms API, with the following notes:

   - If you renamed the native application during installation, you will need to modify the script as indicated in the script comments.
   - If you want to review the full installation script before running it, uncomment the `DRY_RUN=TRUE` script line and run all commands
     up to and including that line to see the script contents. Note that you should **not run the installation script** exposed by that
     command manually, as it might result in an incomplete installation.
   - Note that installation takes several minutes.
3. Confirm that you can access the API:

   Copy code

   ```
   USE ROLE SAMOOHA_APP_ROLE;
   USE WAREHOUSE app_wh;
   CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.LIBRARY.CHECK_MOUNT_STATUS();
   ```

   If this returns FALSE, confirm you are using SAMOOHA\_APP\_ROLE, and if so, retry running the mount script command using the ACCOUNTADMIN role.

## Next steps

After you have installed the clean room environment on your account successfully, you can proceed with the following:

- [Add developers.](/user-guide/cleanrooms/manage-access) Grant access to roles in your Snowflake account, so they can access the clean room environments based on specific privileges.
- [Enable Cross-Cloud Auto-Fulfillment.](/user-guide/cleanrooms/laf) By default, clean rooms can be shared only with participants in the same underlying cloud region. To enable collaborations with collaborators in different cloud regions, you must enable Cross-Cloud Auto-Fulfillment for your account.
- [Enable automatic clean room version updates.](/user-guide/cleanrooms/admin-tasks#label-dcr-updating-cleanrooms-environment) Enable the clean rooms API environment to
  be updated automatically whenever Snowflake releases a new version. You can also install updates manually, but we recommend enabling
  automatic updates.
