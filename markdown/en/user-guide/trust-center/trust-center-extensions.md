# Using Trust Center extensions

To integrate solutions with the Trust Center, security partners can use the
[Snowflake Native App Framework](/developer-guide/native-apps/native-apps-about) to create applications that
provide one or more additional scanner packages. These applications are called *Trust Center extensions*.

You can create Trust Center extensions to tailor security, privacy, governance, and compliance solutions to better
fit your requirements, and then share the extensions in your organization. You can also create extensions that can
be used more broadly and list them to specific Snowflake accounts or on the [Snowflake Marketplace](https://other-docs.snowflake.com/collaboration/collaboration-marketplace-about). For more information,
see [Develop a Trust Center extension](#label-trust-center-extensions-developing).

Users can discover, install, and manage third-party extensions that contain scanner packages. For more information,
see [Install Trust Center extensions](#label-trust-center-extensions-installing).

## Access control requirements

To create and manage Trust Center extensions, a user with the
[ACCOUNTADMIN role](/user-guide/security-access-control-overview#label-access-control-overview-roles-system) must grant
the following privileges to your role:

- SNOWFLAKE.TRUST\_CENTER\_ADMIN [application role](/developer-guide/native-apps/creating-setup-script#label-native-apps-app-roles-about)
- CREATE APPLICATION PACKAGE
- CREATE APPLICATION

## Develop a Trust Center extension

You can develop and deploy a Trust Center extension with scanner packages. You can version your Trust Center
extension by using [Native App versioning](/developer-guide/native-apps/update-app-overview). Extensions
also use the [Native App privilege model](/developer-guide/native-apps/requesting-about) to access any
data or metadata, such as tables within a customer account or Account Usage views.

### Prerequisites

Before you develop an extension with scanner packages, complete the following prerequisites:

- Understand how to develop a [Native App](/developer-guide/native-apps/native-apps-about).
- Understand how to create and use Snowflake [stored procedures](/developer-guide/extensibility).
- Create or identify a Snowflake account that can act as an extension provider account. Every Native App
  requires a provider account.

### Create a scanner package manifest and scanners

To create a scanner package manifest and scanners, complete the following steps:

1. [Create an extension manifest file](#label-trust-center-extensibility-model-create-scanner-package-manifest).
2. [Create scanners](#label-trust-center-extensions-create-scanners).
3. [Create an extension](#label-trust-center-extensions-create-extension).
4. [Grant privileges](#label-trust-center-extensions-grant-privileges).
5. [Register the extension](#label-trust-center-view-extensions-register).
6. [Test the extension](#label-trust-center-view-extensions-test).

#### Create an extension manifest file

Create a manifest file that contains information and metadata about the various scanner packages and scanners:

1. Create a manifest file.

   The manifest file has the following requirements:

   - The name of the manifest file must be `tc_extension_manifest.yml`.
   - The `tc_extension_manifest.yml` file must exist at the root of the directory structure
     on the named stage where the Native App `manifest.yml` file resides.

   The manifest file lists the scanner package properties and all of the scanners that are included in the scanner package.

   Use the following definition for the manifest file:

   Copy code

   ```
   manifest_version: '2.0'
   scanner_packages:
   - id: ''
     name: ''
     short_description: ''
     description: ''
     scanners:
    - id: ''
      name: ''
      short_description: ''
      description: ''
      type: 'VULNERABILITY'
      callback:
        schema: ''
        name: ''
        version: ''
   ```

   The manifest file has the following properties:

   | Property | Description | Maximum number of characters |
   | --- | --- | --- |
   | `manifest_version` | Currently, only `2.0` is valid. | Not applicable |
   | `scanner_packages.id` | A unique identifier for the scanner package, which the provider must maintain for the scanner package’s lifetime. Only ASCII alphanumeric and underscore characters are supported. All of the configurations that the customer applies to a scanner package are persisted in Trust Center using this ID. | 25 |
   | `scanner_packages.name` | The name of the scanner package. | 30 |
   | `scanner_packages.short_description` | The short description of the scanner package. | 150 |
   | `scanner_packages.description` | The description of the scanner package. | 700 |
   | `scanner_packages.scanners.id` | A unique identifier for the scanner, which the provider must maintain for the scanner’s lifetime. Only ASCII alphanumeric and underscore characters are supported. All of the configurations that customers apply to a scanner are persisted in Trust Center using this ID. | 25 |
   | `scanner_packages.scanners.name` | The name of the scanner. | 30 |
   | `scanner_packages.scanners.short_description` | The short description of the scanner. | 150 |
   | `scanner_packages.scanners.description` | The long description of the scanner. | 1,500 |
   | `scanner_packages.scanners.type` | The type of the scanner. Currently, only `VULNERABILITY` is supported. | — |
   | `scanner_packages.scanners.callback` | The callback section for the scanner. Every scanner must have a `callback` section that specifies its `schema`, `name`, and `version`. | Not applicable |
   | `scanner_packages.scanners.callback.schema` | The schema for the stored procedure. The schema must exist in the `setup_script.sql` file. For more information about this file, see [Create an extension](#label-trust-center-extensions-create-extension). | Not applicable |
   | `scanner_packages.scanners.callback.name` | The name of the stored procedure. The following requirements apply to the stored procedure:  - Currently, it must be named `scan`. - The stored procedure name that is defined here must exist in the `setup_script.sql` file under the schema   that is specified in `callback.schema`. | Not applicable |
   | `scanner_packages.scanners.callback.version` | The version of the stored procedure. Currently, only `1.0` is supported. | Not applicable |

   Expand

   Show lessSee more

The following example shows the contents of a manifest file:

Copy code

```
manifest_version: '2.0'
scanner_packages:
  - id: 'se_extension'
    name: 'Security Extension'
    short_description: 'Enhances security features and capabilities.'
    description: 'This extension provides additional security features and capabilities to the platform.'
    scanners:
      - id: 'es_check'
        name: 'NA event sharing check'
        short_description: 'Checks for NA event sharing configurations.'
        description: 'This scanner checks for event sharing configurations in the North America region.'
        type: 'VULNERABILITY'
        callback:
          schema: 'security_essentials_na_consumer_es_check'
          name: 'scan'
          version: '1.0'
      - id: 'se_mfa'
        name: 'MFA Required for Users'
        short_description: 'Ensures that MFA is required for all users.'
        description: 'This scanner checks that Multi-Factor Authentication (MFA) is enforced for all users in the system.'
        type: 'VULNERABILITY'
        callback:
          schema: 'security_essentials_mfa_required_for_users_check'
          name: 'scan'
          version: '1.0'
      - id: 'se_client'
        name: 'Client Security'
        short_description: 'Ensures that client security best practices are followed.'
        description: 'This scanner checks that client security best practices are enforced for all clients in the system.'
        type: 'VULNERABILITY'
        callback:
          schema: 'security_essentials_client_security'
          name: 'scan'
          version: '1.0'
      - id: 'cis_1_4'
        name: 'Extension CIS 1_4'
        short_description: 'Checks for compliance with CIS Benchmark 1.4.'
        description: 'This scanner checks for compliance with the CIS Benchmark 1.4, ensuring that security best practices are followed.'
        type: 'VULNERABILITY'
        callback:
          schema: 'security_essentials_cis1_4'
          name: 'scan'
          version: '1.0'
      - id: 'cis_3_1'
        name: 'Extension CIS 3_1'
        short_description: 'Checks for compliance with CIS Benchmark 3.1.'
        description: 'This scanner checks for compliance with the CIS Benchmark 3.1, ensuring that security best practices are followed.'
        type: 'VULNERABILITY'
        callback:
          schema: 'security_essentials_cis3_1'
          name: 'scan'
          version: '1.0'
```

#### Create scanners

Create a [versioned schema](/developer-guide/native-apps/versioned-schema) and a stored procedure
that implements the scanner logic.

If the scanner package contains multiple scanners, then complete these steps for each scanner,
using a different versioned schema for each scanner:

1. Create a versioned schema to host the scanner logic.

   The name of the schema must be the same as the schema specified for the scanner in the
   [extension manifest file](#label-trust-center-extensibility-model-create-scanner-package-manifest).

   For example, the following SQL statement creates a versioned schema that is named
   `security_essentials_mfa_required_for_users`:

   Copy code

   ```
   CREATE OR ALTER VERSIONED SCHEMA security_essentials_mfa_required_for_users;
   ```
2. Create a stored procedure that implements the scanner logic.

   The following example creates a stored procedure named `scan` in the `security_essentials_mfa_required_for_users`
   schema:

   Copy code

   ```
   CREATE OR REPLACE PROCEDURE security_essentials_mfa_required_for_users.scan(
    run_id VARCHAR)
     RETURNS TABLE(
    risk_id VARCHAR,
    risk_name VARCHAR,
    total_at_risk_count NUMBER,
    scanner_type VARCHAR,
    risk_description VARCHAR,
    suggested_action VARCHAR,
    impact VARCHAR,
    severity VARCHAR,
    at_risk_entities ARRAY
     )
     LANGUAGE SQL
     AS
     $$
    -- Scanning logic --
     $$;
   ```

   Verify that the stored procedure returns exactly one row for each severity and risk ID combination.

   The returned table must have the following columns:

   | Column | Type | Description |
   | --- | --- | --- |
   | `risk_id` | VARCHAR | The identifier for the risk. |
   | `risk_name` | VARCHAR | The name of the risk. |
   | `total_at_risk_count` | NUMBER | Total number of entities at risk for a scanner. For scenarios where the scanner doesn’t detect any violations, the value is `0`. The maximum number of at-risk entities is 1,000, and the maximum combined size of all values in an [array](/sql-reference/data-types-semistructured#label-data-type-array) is 128 MB. |
   | `scanner_type` | VARCHAR | Currently, only the `VULNERABILITY` scanner type is supported. |
   | `risk_description` | VARCHAR | The description of the risk. |
   | `suggested_action` | VARCHAR | Suggested action for remediation. |
   | `impact` | VARCHAR | Possible consequences of not addressing the risk. |
   | `severity` | VARCHAR | The severity level of the risk. The possible values are LOW, MEDIUM, HIGH, and CRITICAL. |
   | `at_risk_entities` | ARRAY of OBJECT values | The OBJECT values in the array have the following structure:  ``` [   {  "entity_id": <id>,  "entity_name": "<name>",  "entity_object_type": "<type>",  "entity_detail": {    ..., -- custom data  }   },   ... ] ```  The OBJECT values contain the following key-value pairs:  - `entity_id` - An optional field that corresponds to the ID of the entity at risk. - `entity_name` - A required field that corresponds to the name of the entity at risk. - `entity_object_type` - A required field that corresponds to the type of the entity at risk.   For example: `APPLICATION`, `TASK`, `NETWORK_POLICY`, `SECURITY_INTEGRATION`, `ROLE`,   `PROCEDURE`, `QUERY`, `DRIVER`, `PARAMETER`, `TABLE`, `STAGE`, `DATA_MASKING_POLICY`,   or `ROW_ACCESS_POLICY`. - `entity_detail` - Custom data that describes the entity. The maximum size of an array is 128 MB.  For scenarios where the scanner doesn’t detect any violations, the value is an empty list. |

   Expand

   Show lessSee more

#### Create an extension

An *extension* bundles scanner packages in a Native App, makes them accessible to the Trust Center, and
configures the privileges to allow the Trust Center to invoke the required stored procedures.

To create an extension, complete the following steps:

1. Create a `setup_script.sql` file for the extension by following the instructions in
   [Create the setup script](/developer-guide/native-apps/creating-setup-script).

   In the `setup_script.sql` file, create an application role that will provide Snowflake with the privileges to use the schema and procedure that have the scanner logic. For example, you can create an application role named `trust_center_integration_role`.

   Then, grant the required privileges on
   [the versioned schema and stored procedure](#label-trust-center-extensions-create-scanners) to
   that application role.

   The following example shows how to create the application role `trust_center_integration_role`, and then
   grant the required privileges:

   Copy code

   ```
   CREATE APPLICATION ROLE IF NOT EXISTS trust_center_integration_role;

   GRANT USAGE ON SCHEMA security_essentials_mfa_required_for_users
     TO APPLICATION ROLE trust_center_integration_role;

   GRANT USAGE ON PROCEDURE security_essentials_mfa_required_for_users.scan(VARCHAR)
     TO APPLICATION ROLE trust_center_integration_role;
   ```

   The privileges are required for every scanner in the package.
2. Create a `manifest.yml` file for the extension by following the instructions in
   [Create the manifest file for an app](/developer-guide/native-apps/manifest-overview).

   The following example shows the contents of a `manifest.yml` file for a Trust Center extension:

   Copy code

   ```
   manifest_version: 1
   artifacts:
     setup_script: setup_script.sql
     readme: README.md
   privileges:
     - IMPORTED PRIVILEGES ON SNOWFLAKE DB:
    description: "Required access to SNOWFLAKE.ACCOUNT_USAGE views to scan for vulnerabilities"
   ```
3. Create an application package for the extension by following the instructions in
   [Create and manage an application package](/developer-guide/native-apps/creating-app-package).
4. Register a version of the application package by following the instructions in
   [Register a version](/developer-guide/native-apps/release-channels#label-native-apps-relchan-register).

   To confirm that the application package has registered versions, you can run the [SHOW VERSIONS IN APPLICATION PACKAGE](/sql-reference/sql/show-versions).
5. Create an application that is based on a registered version by following the instructions in
   [Create an app from a version or patch](/developer-guide/native-apps/installing-testing-application#label-native-apps-application-creating-version).

   To confirm that the application object was created, you can run the [SHOW APPLICATIONS](/sql-reference/sql/show-applications).

#### Grant privileges

After you install the extension, grant the required privileges by completing the following steps:

1. Grant the privileges requested by the extension by following the instructions in [Manage access requests using Snowsight](https://other-docs.snowflake.com/en/native-apps/consumer-granting-privs#manage-access-requests-using-snowsight).
2. To grant the `trust_center_integration_role` application role in the namespace of the extension to the SNOWFLAKE
   application, run the [GRANT APPLICATION ROLE](/sql-reference/sql/grant-application-role) command:

   Copy code

   ```
   GRANT APPLICATION ROLE <extension_name>.trust_center_integration_role
     TO APPLICATION snowflake;
   ```
3. To grant the application role in the namespace of the extension to the SNOWFLAKE
   application, run the [GRANT APPLICATION ROLE](/sql-reference/sql/grant-application-role) command:

   Copy code

   ```
   GRANT APPLICATION ROLE <extension_name>.<role_name>
     TO APPLICATION snowflake;
   ```

   For example, to grant the `tc_extension.trust_center_integration_role` application role ([that you created earlier](#label-trust-center-extensions-create-extension)) to the SNOWFLAKE application,
   run the following command:

   Copy code

   ```
   GRANT APPLICATION ROLE tc_extension.trust_center_integration_role
     TO APPLICATION snowflake;
   ```

#### Register the extension

You can register or deregister an extension by calling the following stored procedures:

- [SNOWFLAKE.TRUST\_CENTER.REGISTER\_EXTENSION](/sql-reference/stored-procedures/register_extension)
- [SNOWFLAKE.TRUST\_CENTER.DEREGISTER\_EXTENSION](/sql-reference/stored-procedures/deregister_extension)

To register an extension with the Trust Center, complete the following steps:

1. Switch to a role with the SNOWFLAKE.TRUST\_CENTER\_ADMIN application role granted to it.
2. Call the [SNOWFLAKE.TRUST\_CENTER.REGISTER\_EXTENSION](/sql-reference/stored-procedures/register_extension)
   stored procedure.

   To view details about the extension, you can run the [SHOW APPLICATIONS](/sql-reference/sql/show-applications) command. The
   application package or listing identifier is in the `source` column.

   For example, to register an extension named `tc_extension` that was installed from the application package named `my_tc_package`,
   call the stored procedure:

   Copy code

   ```
   CALL SNOWFLAKE.TRUST_CENTER.REGISTER_EXTENSION(
     'APPLICATION PACKAGE',
     'my_tc_package',
     'tc_extension');
   ```

   You can display information about your registered extensions by querying the
   [EXTENSIONS view](/sql-reference/trust_center/extensions).

   Note

   To deregister an extension, call the
   [SNOWFLAKE.TRUST\_CENTER.DEREGISTER\_EXTENSION](/sql-reference/stored-procedures/deregister_extension)
   stored procedure.
3. Confirm that the scanner package provided by the extension is now in the list of Trust Center scanner packages by
   following the instructions in [View available scanner packages](/user-guide/trust-center/using-the-trust-center#label-trust-center-view-scanner-packages).

#### Test the extension

After granting the privileges and enabling the scanner package, test the extension and examine the results generated
by the scanner by querying the SNOWFLAKE.TRUST\_CENTER.FINDINGS view. If a scanner run has failed, you can check
the `ERROR_CODE` and `ERROR_MESSAGE` to debug the scanner failure.

You can also monitor telemetry data for Trust Center extensions by using the views in the
[DATA\_SHARING\_USAGE schema](/sql-reference/data-sharing-usage). For example, you can find the number of installed
instances of the extension by querying the [APPLICATION\_STATE view](/sql-reference/data-sharing-usage/application-state-view), and you can
monitor consumer usage of an extension by querying the [LISTING\_ACCESS\_HISTORY view](/sql-reference/data-sharing-usage/listing-access-history).

## Install Trust Center extensions

You can discover, install, and manage third-party extensions that contain scanner packages.

### Install and manage third-party scanner packages

To install and manage a third-party scanner package, complete the following steps:

1. [Discover and install extensions](#label-trust-center-extensions-discover-and-install).
2. [Manage the new scanner packages](#label-trust-center-extensions-manage).

#### Discover and install extensions

You can discover and install a public Trust Center extension that was published to the [Snowflake Marketplace](https://other-docs.snowflake.com/collaboration/collaboration-marketplace-about) or a private one that was shared with you by using private listings. Trust Center extensions can contain one or more scanner packages.

To discover and install a public extension, follow these steps:

1. [Sign in to Snowsight](/user-guide/connecting#label-sign-in-using-snowsight).
2. Switch to a role that has been granted the SNOWFLAKE.TRUST\_CENTER\_ADMIN application role.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Manage scanners** tab.
5. To view a list of public extensions that are available to your account, select **Extensions**.
6. Select the public extension that you want to install.

   The Snowflake Marketplace page for the extension opens.
7. To access the listing, select **Get**.
8. Optional: For **Application name**, enter a name.
9. To install the extension, select **Get**.

   Consumer registration of public extensions with the Trust Center happens automatically.

To discover and install a private extension, follow these steps:

1. [Sign in to Snowsight](/user-guide/connecting#label-sign-in-using-snowsight).
2. Switch to a role that has been granted the SNOWFLAKE.TRUST\_CENTER\_ADMIN application role.
3. Install the private extension, using [these instructions](/developer-guide/native-apps/ui-consumer-installing#label-nativeapps-consumer-listings-install).
4. Grant the TRUST\_CENTER\_INTEGRATION\_ROLE to the Snowflake application.
5. Register the private extension with the Trust Center, as described in [Register the extension](#label-trust-center-view-extensions-register).

Note

A consumer must register private extensions with the Trust Center after installing them. The Trust Center does not generate notifications or
send email after a private extension is installed.

When the installation of a public extension is complete, a Snowsight notification appears, and an email is sent to the email address
associated with your account.

For more information about installing Native Apps, see [Use and manage Snowflake Native Apps as a consumer](/developer-guide/native-apps/ui-consumer-about).

#### Manage the new scanner packages

Installing a Trust Center extension adds one or more scanner packages to the Trust Center. To view the newly installed scanner
packages, complete the following steps:

1. [Sign in to Snowsight](/user-guide/connecting#label-sign-in-using-snowsight).
2. Switch to a role that has been granted the SNOWFLAKE.TRUST\_CENTER\_ADMIN application role.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Manage scanners** tab.

   In the list of scanner packages, the following information is displayed for each new scanner package:

   - **NAME** - The name of the new scanner package.
   - **SOURCE** - The name of the extension that you installed.
   - **SCANNERS** - The number of enabled and disabled scanners in the scanner package.
   - **STATUS** - The status of the scanner package. By default, newly installed scanner packages are disabled.
5. To enable a new scanner package, complete the following steps:

   1. In the list of scanner packages, select the scanner package.
   2. On the scanner package page, select **Enable package**.
   3. To grant the privileges required by the new scanner package, select **Grant**.
   4. Select **Enable**.

   Repeat these steps for each new scanner package that you want to enable.

You can manage the new scanner package in the same way that you manage other scanner packages in the Trust Center. For
example, you can schedule or disable the new scanner package. For more information, see
[Manage scanner packages](/user-guide/trust-center/using-the-trust-center#label-trust-center-managing-scanners).

You can manage the scanners in the new scanner package in the same way that you manage other scanners. For example,
you can enable, disable, or schedule a scanner. For more information, see [Manage scanners](/user-guide/trust-center/using-the-trust-center#label-trust-center-managing-individual-scanners).

You can also monitor and manage the Native App associated with the extension directly. For more information, see
[Manage apps](/developer-guide/native-apps/ui-consumer-managing-applications).

You can view the findings generated by the scanner packages that are installed with the extension by querying the
SNOWFLAKE.TRUST\_CENTER.FINDINGS view. For example, the following query returns the findings for
the scanner packages that are installed with an extension that has a `extension_id` of `4486988721`:

Copy code

```
SELECT * FROM snowflake.trust_center.findings WHERE extension_id = 4486988721;
```

To find the identifiers for registered extensions, query the [EXTENSIONS view](/sql-reference/trust_center/extensions).

For more information about Trust Center findings, see [Trust Center findings](/user-guide/trust-center/overview#label-trust-center-findings)
and [View security risks](/user-guide/trust-center/using-the-trust-center#label-trust-center-view-security-risks).

### Troubleshooting extension installation and registration

If a query on the SNOWFLAKE.TRUST\_CENTER.FINDINGS view returns `FAILED` in the
`COMPLETION_STATUS` column, then scanner execution has failed. One possible reason for scanner
failure is that the extension wasn’t granted the required privileges. Ensure that the extension was
granted the privileges that are described in [Grant privileges](#label-trust-center-extensions-grant-privileges).

After you grant the required privileges, run the scanner package again to generate new findings.
If a query on the SNOWFLAKE.TRUST\_CENTER.FINDINGS view still returns `FAILED` in the
`COMPLETION_STATUS` column, then contact Snowflake Support.
