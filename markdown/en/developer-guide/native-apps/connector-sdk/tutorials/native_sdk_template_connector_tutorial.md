Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

# Tutorial: Snowflake Native SDK for Connectors Java connector template

## Introduction

Welcome to our tutorial on using a connector template utilizing Snowflake Native SDK for Connectors. This guide will help you setup a simple Connector Native Application.

In this tutorial you will learn how to:

- Deploy a Connector Native Application
- Configure a template connector to ingest data
- Customize a template connector to your own needs

The template contains various helpful comments in the code to make it easier for you to find specific files that need to be modified.
Look for the comments with the following keywords, they will guide you and help implement your own connector:

- `TODO`
- `TODO: HINT`
- `TODO: IMPLEMENT ME`

Before you begin this tutorial, you should prepare yourself by reviewing the following recommended content:

- [Snowflake Native SDK for Connectors](/developer-guide/native-apps/connector-sdk/about-connector-sdk)
- [Tutorial: Snowflake Native SDK for Connectors example Java connector](/developer-guide/native-apps/connector-sdk/tutorials/native_sdk_example_connector_tutorial)

### Prerequisites

Before getting started please make sure that you meet the following requirements:

- Access to a Snowflake account with an `ACCOUNTADMIN` role
- Review [Snowflake Native SDK for Connectors](/developer-guide/native-apps/connector-sdk/about-connector-sdk) and keep it open while following this tutorial
- Review [Tutorial: Snowflake Native SDK for Connectors example Java connector](/developer-guide/native-apps/connector-sdk/tutorials/native_sdk_example_connector_tutorial)
  - That tutorial uses an example connector based on this template and it can be referenced to check
    out example implementations of various components.

## Prepare your local environment

Before proceeding you need to make sure all necessary software is installed on your machine and
clone the connector template.

### Java installation

Snowflake Native SDK for Connectors requires Java LTS (Long-Term Support) version 11 or higher. If
the minimum required version of Java is not installed on your machine, you must install either
Oracle Java or OpenJDK.

#### Oracle Java

The latest LTS release of the JDK is free to download and use, at no cost,
under the Oracle NFTC. For download and installation instructions go to the [Oracle page](https://www.oracle.com/java/technologies/downloads/).

#### OpenJDK

OpenJDK is an open-source implementation of Java. For download and installation instructions go to
[openjdk.org](https://openjdk.org/install/) and [jdk.java.net](https://jdk.java.net/).

You may also use a 3rd party OpenJDK version, such as [Eclipse Temurin](https://adoptium.net/temurin/releases/)
or [Amazon Corretto](https://aws.amazon.com/corretto/).

### Snowflake CLI configuration

The [Snowflake CLI](/developer-guide/snowflake-cli/index) tool is
required to build, deploy and install the connector. If you do not have Snowflake CLI on your
machine - install it as per instructions available in [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation).

After the tool is installed - you need to configure a connection to Snowflake in your
[configuration file](/developer-guide/snowflake-cli/connecting/configure-cli#label-cli-config-locations).

If you do not have any connections configured - create a new one named `native_sdk_connection`. You
can find an example connection in the `deployment/snowflake.toml` file.

If you already have a connection configured and would like to use it with the connector - use its
name instead of `native_sdk_connection` whenever this connection is used in this tutorial.

### Template cloning

To clone the connector template use the following command:

```
snow init <project_dir> \
  --template-source https://github.com/snowflakedb/connectors-native-sdk \
  --template templates/connectors-native-sdk-template
```

In place of `<project_dir>` enter the name of the directory (it must not exist) in which the Java
project of your connector will be created.

After executing the command you will be asked to provide additional information for application instance
and stage name configuration. You may provide any names, as long as they are valid unquoted Snowflake
identifiers, or click enter to use the default values, which are shown in the square brackets.

An example command execution, providing custom application and stage names:

```
$ snow init my_connector \
    --template-source https://github.com/snowflakedb/connectors-native-sdk \
    --template templates/connectors-native-sdk-template

Name of the application instance which will be created in Snowflake [connectors-native-sdk-template]: MY_CONNECTOR
Name of the schema in which the connector files stage will be created [TEST_SCHEMA]:
Name of the stage used to store connector files in the application package [TEST_STAGE]: CUSTOM_STAGE_NAME
Initialized the new project in my_connector
```

## Connector build, deployment, and cleanup

The template can be deployed out of the box, even before any modification. The following sections will
show you how to build, deploy and install the connector.

### Build the connector

Building a connector created using Snowflake Native SDK for Connectors is a bit different from building a typical
Java application. There are some things which must be done besides just building the .jar archives
from the sources. Building the application consists of the following steps:

1. Copying custom internal components to the build directory
2. Copying SDK components to the build directory

#### Copy internal components

This step builds the connector .jar file and then copies it (along with the UI, manifest and setup
files) to the `sf_build` directory.

To run this step execute the command: `./gradlew copyInternalComponents`.

#### Copy SDK components

This step copies the SDK .jar file (added as a dependency to the connector Gradle module) to the
`sf_build` directory and extracts bundled .sql files from the .jar archive.

Those .sql files allow the customization of which provided objects will be created during the
application installation. For the first time users customization is not recommended, because omitting
objects may cause some features to fail if done incorrectly. The template connector application uses
the `all.sql` file, which creates all recommended SDK objects.

To run this step execute the command: `./gradlew copySdkComponents`.

### Deploy the connector

To deploy a Native App an application package needs to be created inside Snowflake. After that all
the files from the `sf_build` directory need to be uploaded to Snowflake.

Please note - for development purposes version creation is optional, an application instance can be
created directly from staged files. This approach allows you to see changes in most of the connector
files without recreating the version and application instance.

The following operations will be performed:

1. Create a new application package, if it does not already exist
2. Create a schema and file stage inside the package
3. Upload files from the `sf_build` directory to the stage (this step may take some time)

To deploy the connector execute the command: `snow app deploy --connection=native_sdk_connection`.

For more information about the `snow app deploy` command see [snow app deploy](/developer-guide/snowflake-cli/command-reference/native-apps-commands/deploy-app).

The created application package will now be visible in the `App packages` tab, in the
`Data products` category, in the Snowflake UI of your account.

### Install the connector

Installation of the application is the last step of the process. It creates an application from the
application package created previously.

To install the connector execute the command: `snow app run --connection=native_sdk_connection`.

For more information about the `snow app run` command see [snow app run](/developer-guide/snowflake-cli/command-reference/native-apps-commands/run-app).

The installed application will now be visible in the `Installed apps` tab, in the
`Data products` category, in the Snowflake UI of your account.

### Update connector files

If at any point you wish to modify any of the connector files - you can easily upload the modified
files into the application package stage. The upload command depends on which files were updated.

Before any of the update commands are run - you have to copy the new files of your connector to the
`sf_build` directory by running: `./gradlew copyInternalComponents`

#### UI .py files or connector .java files

Use the `snow app deploy --connection=native_sdk_connection` command, the current application
instance will use the new files without reinstallation.

#### setup.sql or manifest.yml files

Use the `snow app run --connection=native_sdk_connection` command, the current application
instance will be reinstalled after the new files are uploaded to stage.

### Cleanup

After the tutorial is completed, or if for any reason you want to remove the application and its
package, you can completely remove them from your account using the command:

`snow app teardown --connection=native_sdk_connection --cascade --force`

The `--cascade` option is needed to remove the destination database without transferring the ownership
to the account admin. In real connectors the database should not be removed to preserve the ingested
data, it should be either owned by the account admin or ownership should be transferred before
uninstallation.

**Please note - the connector will consume credits until it is paused or removed, even if no
ingestion was configured!**

## Prerequisites step

Right after installation the Connector is in its Wizard phase. This phase consists of a few steps
that guide the end user through all the necessary configurations.

The first step is the Prerequisites step. It is optional and might not be necessary for every connector.
Prerequisites are usually actions required from the user outside of the application, e.g. running
queries in the SQL worksheet, doing configuration on the source system side, etc.

Read more about prerequisites: [Prerequisites](/developer-guide/native-apps/connector-sdk/flow/prerequisites)

The contents of each prerequisite are retrieved directly from the `STATE.PREREQUISITES` table,
located inside the connector. They can be customized through the `setup.sql` script. However, keep
in mind that the `setup.sql` script is executed on every installation, upgrade and downgrade of the
application. The inserts must be idempotent, because of this it is recommended to use a merge query
as in the example below:

Copy code

```
MERGE INTO STATE.PREREQUISITES AS dest
USING (SELECT * FROM VALUES
           ('1',
            'Sample prerequisite',
            'Prerequisites can be used to notice the end user of the connector about external configurations. Read more in the SDK documentation below. This content can be modified inside `setup.sql` script',
            'https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/flow/prerequisites',
            NULL,
            NULL,
            1
           )
) AS src (id, title, description, documentation_url, learnmore_url, guide_url, position)
ON dest.id = src.id
WHEN NOT MATCHED THEN
    INSERT (id, title, description, documentation_url, learnmore_url, guide_url, position)
    VALUES (src.id, src.title, src.description, src.documentation_url, src.learnmore_url, src.guide_url, src.position);
```

## Connector configuration step

The next step of the Wizard Phase is the connector configuration step. During this step you can
configure database objects and permissions required by the connector. This step allows for the
following configuration properties to be specified:

- `warehouse`
- `operational_warehouse`
- `cortex_warehouse`
- `destination_database`
- `destination_schema`
- `global_schedule`
- `data_owner_role`
- `cortex_user_role`
- `agent_username`
- `agent_role`

If you need any other custom properties, they can be configured in one of the next steps of the Wizard
phase. For more information on each of the properties see: [Connector configuration](/developer-guide/native-apps/connector-sdk/flow/connector_configuration)

Additionally, the Streamlit component (`streamlit/wizard/connector_config.py`) provided in the
template shows how to trigger the [Native Apps Permission SDK](/developer-guide/native-apps/requesting-ui)
and requests privilege grants from the end-user. As long as the available properties satisfy the
needs of the connector then there is no need to overwrite any of the backend classes, although this
is still possible the same way as for the components in the further steps of the configuration.

For more information on internal procedures and Java objects see: [Connector configuration reference](/developer-guide/native-apps/connector-sdk/reference/connector_configuration_reference)

The provided Streamlit example allows for requesting account level privileges configured in the
`manifest.yml` file - `CREATE DATABASE` and `EXECUTE TASKS`. It also allows the user to specify
a warehouse reference through the Permission SDK popup.

In the template, the user is asked to only provide the `destination_database` and `destination_schema`.
However, a `TODO` comment in `streamlit/wizard/connector_configuration.py` contains commented
code that can be reused to display more input fields in the Streamlit UI.

Copy code

```
# TODO: Here you can add additional fields in connector configuration.
# For example:
st.subheader("Operational warehouse")
input_col, _ = st.columns([2, 1])
with input_col:
    st.text_input("", key="operational_warehouse", label_visibility="collapsed")
st.caption("Name of the operational warehouse to be used")
```

## Connection configuration step

The next step of the Wizard Phase is the connection configuration step. This step allows the end-user
to configure external connectivity parameters for the connector. This configuration may include
identifiers of objects like secrets, integrations, etc.

Because this information varies depending on the source system for the data ingested by the connector,
this is the first place where bigger customizations have to be made in the source code.

For more information on connection configuration see:

- [Connection configuration](/developer-guide/native-apps/connector-sdk/flow/connection_configuration)
- [Connection configuration reference](/developer-guide/native-apps/connector-sdk/reference/connection_configuration_reference)

Starting with the Streamlit UI side (`streamlit/wizard/connection_config.py`) you need to add text
inputs for all needed parameters. An example text input is implemented for you and if you search the
code in this file, you can find a `TODO` with commented code for a new field.

Copy code

```
# TODO: Additional configuration properties can be added to the UI like this:
st.subheader("Additional connection parameter")
input_col, _ = st.columns([2, 1])
with input_col:
    st.text_input("", key="additional_connection_property", label_visibility="collapsed")
st.caption("Some description of the additional property")
```

After the properties are added to the form, they need to be passed to the backend layer of the connector.
To do so, two additional places must be modified in the Streamlit files. The first one is the
`finish_config` function in the `streamlit/wizard/connection_config.py` file. The state of the
newly added text inputs must be read here. Additionally, it can be validated if needed, and then passed
to the `set_connection_configuration` function.

For example if `additional_connection_property` was added it would look like this after the edits:

Copy code

```
def finish_config():
try:
    # TODO: If some additional properties were specified they need to be passed to the set_connection_configuration function.
    # The properties can also be validated, for example, check whether they are not blank strings etc.
    response = set_connection_configuration(
        custom_connection_property=st.session_state["custom_connection_property"],
        additional_connection_property=st.session_state["additional_connection_property"],
    )

# rest of the method without changes
```

Then the `set_connection_configuration` function must be edited, it can be found in the
`streamlit/native_sdk_api/connection_config.py` file. This function is a proxy between Streamlit UI
and the underlying SQL procedure, which is an entry points to the backend of the connector.

Copy code

```
def set_connection_configuration(custom_connection_property: str, additional_connection_property: str):
    # TODO: this part of the code sends the config to the backend so all custom properties need to be added here
    config = {
        "custom_connection_property": escape_identifier(custom_connection_property),
        "additional_connection_property": escape_identifier(additional_connection_property),
    }

    return call_procedure(
        "PUBLIC.SET_CONNECTION_CONFIGURATION",
        [variant_argument(config)]
    )
```

After doing this, the new property is saved in the internal connector table, which contains the
configuration. However, this is not the end of the possible customizations. Some backend components
can be customized too, look for the following comments in the code to find them:

- `TODO: IMPLEMENT ME connection configuration validate`
- `TODO: IMPLEMENT ME connection callback`
- `TODO: IMPLEMENT ME test connection`

The validate part allows for any additional validation on the data received from the UI. It can also
transform the data, e.g. change the character case, trim the provided data, or check if objects with
provided names actually exist inside Snowflake.

Connection callback is a part that lets you perform any additional operation based on the config, e.g.
alter procedures that need to use external access integrations, using a solution described in
[External integration setup reference](/developer-guide/native-apps/connector-sdk/reference/setup_external_integration).

Test connection is the final component of the connection configuration, it checks whether the connection
can be established between the connector and the source system.

For more information on those internal components see:

- [Connection configuration](/developer-guide/native-apps/connector-sdk/flow/connection_configuration)
- [Connection configuration reference](/developer-guide/native-apps/connector-sdk/reference/connection_configuration_reference)

Example implementations might look like this:

Copy code

```
public class TemplateConfigurationInputValidator implements ConnectionConfigurationInputValidator {

    private static final String ERROR_CODE = "INVALID_CONNECTION_CONFIGURATION";

    @Override
    public ConnectorResponse validate(Variant config) {
      // TODO: IMPLEMENT ME connection configuration validate: If the connection configuration input
      // requires some additional validation this is the place to implement this logic.
      // See more in docs:
      // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/reference/connection_configuration_reference
      // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/flow/connection_configuration
      var integrationCheck = checkParameter(config, INTEGRATION_PARAM, false);
      if (!integrationCheck.isOk()) {
        return integrationCheck;
      }

      var secretCheck = checkParameter(config, SECRET_PARAM, true);
      if (!secretCheck.isOk()) {
        return ConnectorResponse.error(ERROR_CODE);
      }

      return ConnectorResponse.success();
    }
}
```

Copy code

```
public class TemplateConnectionConfigurationCallback implements ConnectionConfigurationCallback {

    private static final String[] EXTERNAL_SOURCE_PROCEDURE_SIGNATURES = {
        asVarchar(format("%s.%s()", PUBLIC_SCHEMA, TEST_CONNECTION_PROCEDURE)),
        asVarchar(format("%s.%s(VARIANT)", PUBLIC_SCHEMA, FINALIZE_CONNECTOR_CONFIGURATION_PROCEDURE)),
        asVarchar(format("%s.%s(NUMBER, STRING)", PUBLIC_SCHEMA, WORKER_PROCEDURE))
      };

    private final Session session;

    public TemplateConnectionConfigurationCallback(Session session) {
      this.session = session;
    }

    @Override
    public ConnectorResponse execute(Variant config) {
      // TODO: If you need to alter some procedures with external access you can use
      // configureProcedure method or implement a similar method on your own.
      // TODO: IMPLEMENT ME connection callback: Implement the custom logic of changes in application
      // to be done after connection configuration, like altering procedures with external access.
      // See more in docs:
      // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/reference/connection_configuration_reference
      // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/flow/connection_configuration
      var response = configureProceduresWithReferences();
      if (response.isNotOk()) {
         return response;
      }
      return ConnectorResponse.success();
    }

    private ConnectorResponse configureProceduresWithReferences() {
      return callProcedure(
        session,
        PUBLIC_SCHEMA,
        SETUP_EXTERNAL_INTEGRATION_WITH_NAMES_PROCEDURE,
        EXTERNAL_SOURCE_PROCEDURE_SIGNATURES);
    }
}
```

Copy code

```
public class TemplateConnectionValidator {

    private static final String ERROR_CODE = "TEST_CONNECTION_FAILED";

    public static Variant testConnection(Session session) {
      // TODO: IMPLEMENT ME test connection: Implement the custom logic of testing the connection to
      // the source system here. This usually requires connection to some webservice or other external
      // system. It is suggested to perform only the basic connectivity validation here.
      // If that's the case then this procedure must be altered in TemplateConnectionConfigurationCallback first.
      // See more in docs:
      // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/reference/connection_configuration_reference
      // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/flow/connection_configuration
      return test().toVariant();
    }

    private static ConnectorResponse test() {
      try {
        var response = SourceSystemHttpHelper.testEndpoint();

        if (isSuccessful(response.statusCode())) {
          return ConnectorResponse.success();
        } else {
          return ConnectorResponse.error(ERROR_CODE, "Connection to source system failed");
        }
      } catch (Exception exception) {
        return ConnectorResponse.error(ERROR_CODE, "Test connection failed");
      }
    }
}
```

## Finalize configuration step

The finalize connector configuration step is the final step of the Wizard Phase. This step has multiple
responsibilities:

1. Allows the user to specify any additional configuration needed by the connector
2. Creates the sink database, schema and additional tables and views for the ingested data if needed
3. Initializes internal components such as the scheduler and task reactor

For more information on configuration finalization see:

- [Finalize configuration](/developer-guide/native-apps/connector-sdk/flow/finalize_configuration)
- [Finalize configuration reference](/developer-guide/native-apps/connector-sdk/reference/finalize_configuration_reference)

For more information on task reactor and scheduling see:

- [Task reactor](/developer-guide/native-apps/connector-sdk/using/task_reactor)
- [Task reactor SQL reference](/developer-guide/native-apps/connector-sdk/reference/task_reactor_reference)
- [Ingestion scheduler](/developer-guide/native-apps/connector-sdk/using/scheduler)
- [Ingestion scheduler reference](/developer-guide/native-apps/connector-sdk/reference/scheduler_reference)

Similarly to the connection configuration step, customization can be started with the Streamlit UI.
The `streamlit/wizard/finalize_config.py` file contains a form with an example property. More
properties can be added according to the connector needs. To add another property look for a `TODO`
comment, that contains example code of adding a new property in the mentioned file.

Copy code

```
# TODO: Here you can add additional fields in finalize connector configuration.
# For example:
st.subheader("Some additional property")
input_col, _ = st.columns([2, 1])
with input_col:
    st.text_input("", key="some_additional_property", label_visibility="collapsed")
st.caption("Description of some new additional property")
```

After adding the text input for a new property it needs to be passed to the backend side. To do so,
modify the `finalize_configuration` function in the same file:

Copy code

```
def finalize_configuration():
    try:
        st.session_state["show_main_error"] = False
        # TODO: If some additional properties were introduced, they need to be passed to the finalize_connector_configuration function.
        response = finalize_connector_configuration(
            st.session_state.get("custom_property"),
            st.session_state.get("some_additional_property")
        )
```

Next, open the `streamlit/native_sdk_api/finalize_config.py` file and add the new property to the
following function:

Copy code

```
def finalize_connector_configuration(custom_property: str, some_additional_property: str):
    # TODO: If some custom properties were configured, then they need to be specified here and passed to the FINALIZE_CONNECTOR_CONFIGURATION procedure.
    config = {
        "custom_property": custom_property,
        "some_additional_property": some_additional_property,
    }
    return call_procedure(
        "PUBLIC.FINALIZE_CONNECTOR_CONFIGURATION",
        [variant_argument(config)]
    )
```

Again, similarly to the connection configuration step, this step also allows for the customization of
various backend components, they can be found using the following comments in the source code:

- `TODO: IMPLEMENT ME validate source`
- `TODO: IMPLEMENT ME finalize internal`

The validate source part is responsible for performing more sophisticated validations on the source
systems. If the previous test connection only checked that a connection can be established, then validate
source could check access to specific data in the system, e.g. extracting a single record of data.

Finalize internal is an internal procedure responsible for initializing task reactor and scheduler,
creating a sink database and any necessary nested objects. It can also be used to save the configuration
provided during the finalize step (this configuration is not saved by default).

More information on the internal components can be found in:

- [Finalize configuration](/developer-guide/native-apps/connector-sdk/flow/finalize_configuration)
- [Finalize configuration reference](/developer-guide/native-apps/connector-sdk/reference/finalize_configuration_reference)

Additionally, input can be validated using the `FinalizeConnectorInputValidator` interface and
providing it to the finalize handler - check the `TemplateFinalizeConnectorConfigurationCustomHandler` file.
More information on using builders can be found in: [Stored procedures and handlers customization](/developer-guide/native-apps/connector-sdk/using/sproc_and_handlers_customization).

Example implementation of the validate source might look like this:

Copy code

```
public class SourceSystemAccessValidator implements SourceValidator {

    @Override
    public ConnectorResponse validate(Variant variant) {
      // TODO: IMPLEMENT ME validate source: Implement the custom logic of validating the source
      // system. In some cases this can be the same validation that happened in
      // TemplateConnectionValidator.
      // However, it is suggested to perform more complex validations, like specific access rights to
      // some specific resources here.
      // See more in docs:
      // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/reference/finalize_configuration_reference
      // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/flow/finalize_configuration
      var finalizeProperties = Configuration.fromCustomConfig(variant);

      var httpResponse = SourceSystemHttpHelper.validateSource(finalizeProperties.get("custom_property"));
      return prepareConnectorResponse(httpResponse.statusCode());
    }

    private ConnectorResponse prepareConnectorResponse(int statusCode) {
      switch (statusCode) {
        case 200:
          return ConnectorResponse.success();
        case 401:
          return ConnectorResponse.error("Unauthorized error");
        case 404:
          return ConnectorResponse.error("Not found error");
        default:
          return ConnectorResponse.error("Unknown error");
      }
    }
}
```

## Create resources

After the Wizard Phase is completed, the connector is ready to start ingesting data. But first,
the resources must be implemented and configured. A resource is an abstraction describing a specific
set of data in the source system, e.g. a table, an endpoint, a file, etc.

Different source systems might need different information about a resource - for that reason a resource
definition needs to be customized according to the specific needs. To do so, go to the `streamlit/daily_use/data_sync_page.py`
file. There you can find a `TODO` comment about adding text inputs for resource parameters. The
resource parameters should allow for the identification and retrieval of data from the source system.
Those parameters can be then extracted during the ingestion.

Copy code

```
# TODO: specify all the properties needed to define a resource in the source system. A subset of those properties should allow for a identification of a single resource, be it a table, endpoint, repository or some other data storage abstraction
st.text_input(
    "Resource name",
    key="resource_name",
)
st.text_input(
    "Some resource parameter",
    key="some_resource_parameter"
)
```

Once all necessary properties are added to the form, they can be passed to the backend side.
First, the state of the text fields has to be extracted and passed to the API level `queue_resource`
method in the `streamlit/daily_use/data_sync_page.py` file:

Copy code

```
def queue_resource():
    # TODO: add additional properties here and pass them to create_resource function
    resource_name = st.session_state.get("resource_name")
    some_resource_parameter = st.session_state.get("some_resource_parameter")

    if not resource_name:
        st.error("Resource name cannot be empty")
        return

    result = create_resource(resource_name, some_resource_parameter)
    if result.is_ok():
        st.success("Resource created")
    else:
        st.error(result.get_message())
```

Then the `create_resource` function from the `streamlit/native_sdk_api/resource_management.py` file
needs to be updated:

Copy code

```
def create_resource(resource_name, some_resource_parameter):
    ingestion_config = [{
        "id": "ingestionConfig",
        "ingestionStrategy": "INCREMENTAL",
        # TODO: HINT: scheduleType and scheduleDefinition are currently not supported out of the box, due to globalSchedule being used. However, a custom implementation of the scheduler can use those fields. They need to be provided because they are mandatory in the resourceDefinition.
        "scheduleType": "INTERVAL",
        "scheduleDefinition": "60m"
    }]
    # TODO: HINT: resource_id should allow identification of a table, endpoint etc. in the source system. It should be unique.
    resource_id = {
        "resource_name": resource_name,
    }
    id = f"{resource_name}_{random_suffix()}"

    # TODO: if you specified some additional resource parameters then you need to put them inside resource metadata:
    resource_metadata = {
        "some_resource_parameter": some_resource_parameter
    }

    return call_procedure("PUBLIC.CREATE_RESOURCE",
                          [
                              varchar_argument(id),
                              variant_argument(resource_id),
                              variant_list_argument(ingestion_config),
                              varchar_argument(id),
                              "true",
                              variant_argument(resource_metadata)
                          ])
```

### Customizing CREATE\_RESOURCE() procedure logic

The `PUBLIC.CREATE_RESOURCE()` procedure allows the developer to customize its execution by implementing
custom logic that is plugged into several places of the main execution flow. The SDK allows the developer to:

1. Validate the resource before it’s created. The logic should be implemented in the
   `PUBLIC.CREATE_RESOURCE_VALIDATE()` procedure.
2. Perform custom operations before the resource is created. The logic should be implemented in the
   `PUBLIC.PRE_CREATE_RESOURCE()` procedure.
3. Perform custom operations after the resource is created. The logic should be implemented in the
   `PUBLIC.POST_CREATE_RESOURCE()` procedure.

More information about `PUBLIC.CREATE_RESOURCE()` procedure customization can be found here:

- [Create resource](/developer-guide/native-apps/connector-sdk/flow/ingestion-management/create_resource)
- [Create resource reference](/developer-guide/native-apps/connector-sdk/reference/create_resource_reference)

#### TemplateCreateResourceHandler.java

This class is a handler for the `PUBLIC.CREATE_RESOURCE()` procedure. Here, you can inject the Java
implementations of handlers for callback procedures mentioned before. By default the template provides
mocked Java implementations of callback handlers in order to get rid of calling SQL procedures, which
would extend the procedure execution time - Java implementations make the execution faster. These
mocked implementations do nothing apart from returning a success response. You can either provide the
custom implementation to the callback classes prepared by the template or create these callbacks
from scratch and inject them to the main procedure execution flow in the handler builder.

In order to implement the custom logic of callback methods that are called by default, look for the
following comments in the code:

- `TODO: IMPLEMENT ME create resource validate`
- `TODO: IMPLEMENT ME pre create resource callback`
- `TODO: IMPLEMENT ME post create resource callback`

## Ingestion

To perform ingestion of data you need to implement a class that will handle the connection with the
source system and retrieve data based on the resource configuration. Scheduler and Task Reactor modules
will take care of triggering and queueing of the ingestion tasks.

Ingestion logic is invoked from the `TemplateIngestion` class. Look for the `TODO: IMPLEMENT ME ingestion`
comment in the code and replace the random data generation with the data retrieval from the source system.
If you added custom properties to the resource definition, they can be fetched from the internal
connectors tables using the `ResourceIngestionDefinitionRepository` and properties available in the
`TemplateWorkItem`:

- `resourceIngestionDefinitionId`
- `ingestionConfigurationId`

Example of retrieving data from a webservice **might** look like this:

Copy code

```
public final class SourceSystemHttpHelper {

  private static final String DATA_URL = "https://source_system.com/data/%s";
  private static final SourceSystemHttpClient sourceSystemClient = new SourceSystemHttpClient();
  private static final ObjectMapper objectMapper = new ObjectMapper();

  private static List<Variant> fetchData(String resourceId) {
    var response = sourceSystemClient.get(String.format(url, resourceId));
    var body = response.body();

    try {
        return Arrays.stream(objectMapper.readValue(body, Map[].class))
              .map(Variant::new)
              .collect(Collectors.toList());
    } catch (JsonProcessingException e) {
      throw new RuntimeException("Cannot parse json", e);
    }
  }
}
```

Copy code

```
public class SourceSystemHttpClient {

  private static final Duration REQUEST_TIMEOUT = Duration.ofSeconds(15);

  private final HttpClient client;
  private final String secret;

  public SourceSystemHttpClient() {
    this.client = HttpClient.newHttpClient();
    this.secret =
        SnowflakeSecrets.newInstance()
            .getGenericSecretString(ConnectionConfiguration.TOKEN_NAME);
  }

  public HttpResponse<String> get(String url) {
    var request =
        HttpRequest.newBuilder()
            .uri(URI.create(url))
            .GET()
            .header("Authorization", format("Bearer %s", secret))
            .header("Content-Type", "application/json")
            .timeout(REQUEST_TIMEOUT)
            .build();

    try {
      return client.send(request, HttpResponse.BodyHandlers.ofString());
    } catch (IOException | InterruptedException ex) {
      throw new RuntimeException(format("HttpRequest failed: %s", ex.getMessage()), ex);
    }
  }
}
```

## Manage resources lifecycle

Once the logic of creating resources and the their ingestion is implemented, you can manage their
lifecycle by calling the following procedures:

1. `PUBLIC.ENABLE_RESOURCE()` enables a particular resource, meaning that it will be scheduled for ingestion
2. `PUBLIC.DISABLE_RESOURCE()` disables a particular resource, meaning that its ingestion scheduling will be stopped
3. `PUBLIC.UPDATE_RESOURCE()` allows you to update the ingestion configurations of a particular resource.
   It isn’t implemented in the Streamlit UI by default because sometimes it may be undesirable for the
   developer to allow the connector user to customize the ingestion configuration (revoke grants on
   this procedure to application role `ADMIN` in order to disallow its usage completely).

All these procedures have Java handlers and are extended with callbacks that allow you to customize
their execution. You can inject custom implementations of callbacks using the builders for these
handlers. By default the template provides mocked Java implementations of callback handlers.
These mocked implementations do nothing apart from returning a success response. You can either
provide the custom implementation to the callback classes prepared by the template or create these
callbacks from scratch and inject them to the main procedure execution flow in the handler builders.

### TemplateEnableResourceHandler.java

This class is a handler for the `PUBLIC.ENABLE_RESOURCE()` procedure, which can be extended with
the callbacks that are dedicated to:

1. Validate the resource before it’s enabled. Look for the `TODO: IMPLEMENT ME enable resource validate`
   comment in the code to provide the custom implementation.
2. Perform custom operations before the resource is enabled. Look for the `TODO: IMPLEMENT ME pre enable resource`
   comment in the code to provide the custom implementation.
3. Perform custom operations after the resource is enabled. Look for the `TODO: IMPLEMENT ME post enable resource`
   comment in the code to provide the custom implementation.

Learn more from the `PUBLIC.ENABLE_RESOURCE()` procedure detailed documentations:

- [Enable resource](/developer-guide/native-apps/connector-sdk/flow/ingestion-management/enable_resource)
- [Enable resource reference](/developer-guide/native-apps/connector-sdk/reference/enable_resource_reference)

### TemplateDisableResourceHandler.java

This class is a handler for the `PUBLIC.DISABLE_RESOURCE()` procedure, which can be extended with the callbacks that are
dedicated to:

1. Validate the resource before it’s disabled. Look for the `TODO: IMPLEMENT ME disable resource validate`
   comment in the code to provide the custom implementation.
2. Perform custom operations before the resource is disabled. Look for the `TODO: IMPLEMENT ME pre disable resource`
   comment in the code in order to provide the custom implementation.

Learn more from the `PUBLIC.DISABLE_RESOURCE()` procedure detailed documentations:

- [Disable resource](/developer-guide/native-apps/connector-sdk/flow/ingestion-management/disable_resource)
- [Disable resource reference](/developer-guide/native-apps/connector-sdk/reference/disable_resource_reference)

### TemplateUpdateResourceHandler.java

This class is a handler for the `PUBLIC.UPDATE_RESOURCE()` procedure, which can be extended with
the callbacks that are dedicated to:

1. Validate the resource before it’s updated. Look for the `TODO: IMPLEMENT ME update resource validate`
   comment in the code to provide the custom implementation.
2. Perform custom operations before the resource is updated. Look for the `TODO: IMPLEMENT ME pre update resource`
   comment in the code to provide the custom implementation.
3. Perform custom operations after the resource is updated. Look for the `TODO: IMPLEMENT ME post update resource`
   comment in the code to provide the custom implementation.

Learn more from the `PUBLIC.UPDATE_RESOURCE()` procedure detailed documentations:

- [Update resource](/developer-guide/native-apps/connector-sdk/flow/ingestion-management/update_resource)
- [Update resource reference](/developer-guide/native-apps/connector-sdk/reference/update_resource_reference)

## Settings

The template contains a settings tab that lets you view all the configuration made before.
However, if configuration properties were customized, then this view also needs some customizations.
Settings tab code can be found in the `streamlit/daily_use/settings_page.py` file.

To customize it, simply extract the values from the configuration for the keys that were added in
the respective configurations. For example, if earlier `additional_connection_property` was added
in the connection configuration step, then it could be added in the settings view like this:

Copy code

```
def connection_config_page():
    current_config = get_connection_configuration()

    # TODO: implement the display for all the custom properties defined in the connection configuration step
    custom_property = current_config.get("custom_connection_property", "")
    additional_connection_property = current_config.get("additional_connection_property", "")

    st.header("Connector configuration")
    st.caption("Here you can see the connector connection configuration saved during the connection configuration step "
               "of the Wizard. If some new property was introduced it has to be added here to display.")
    st.divider()

    st.text_input(
        "Custom connection property:",
        value=custom_property,
        disabled=True
    )
    st.text_input(
        "Additional connection property:",
        value=additional_connection_property,
        disabled=True
    )
    st.divider()
```
