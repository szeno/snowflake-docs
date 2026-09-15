# Getting started with the Snowflake Native SDK for Connectors

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

The Snowflake Native SDK for Connectors is a library that provides universal components that can be used to build a Snowflake native app
that ingests the data from an external data source into Snowflake. The provided components define the recommended flow
of the connector application, allow customization, and provide building blocks for building ingestion logic.

The Snowflake Native SDK for Connectors is distributed as code to be pulled and built locally.
Below you can find some information to get you familiarized with the structure of the SDK, how to use it in your project,
how to deploy and install an application and how to use it during development.

## Project structure

The Snowflake Native SDK for Connectors consists of multiple parts, which will be described below.

- `connectors-native-sdk`

This directory contains the actual Snowflake Native SDK for Connectors source code and tests.
Because of the nature of the native app inside Snowflake, source code is not only Java code,
but also bundled SQL code with database object definitions.

The Java code is inside the `src/main` directory as for any regular Java library. Unit tests are located inside `src/test`.
Additionally, inside `src/` directory you can find `intTest` and `appTest` directories.
Those are respectively integration and application tests. Both of those test types require a connection to a Snowflake account.
The former ones test the SDK components using standalone database objects, while the latter deploy an actual application and run tests using it.

SQL source files are contained inside `src/main/resources` directory. They are included inside jar archive when building the Snowflake Native SDK for Connectors.
To use them they need to be extracted from the jar and put inside a build target directory that will be copied to Snowflake stage inside application package.

- `connectors-native-sdk-test`

This directory contains a helper library designed to enable easier unit testing of the Connector based on the Snowflake Native SDK for Connectors.
It provides mock implementations for some of the database objects,
specially designed test builders that allow overwriting parts of the code not available for customization and some custom assertions based on the [AssertJ library](https://assertj.github.io/doc/).

## SDK installation and usage

Currently, installation and usage of the Snowflake Native SDK for Connectors requires the developer to perform some manual actions.

The Snowflake Native SDK for Connectors library is available via Maven Central.

```
repositories {
    mavenCentral()
}

dependencies {
    compileOnly 'com.snowflake:connectors-native-sdk:2.0.0'
    testImplementation 'com.snowflake:connectors-native-sdk-test:2.0.0'
}
```

To access provided SQL files they need to be extracted to the target directory for the native app. To achieve this use the following gradle task definition (for now it has to be manually copied into the `build.gradle` file).

Copy code

```
String defaultBuildDir = './sf_build'
String defaultSrcDir = './app'
String libraryName = 'connectors-native-sdk'

project.tasks.register('copySdkComponents') {
    it.group = 'Snowflake'
    it.description = "Copies .sql files from ${sdkComponentsDirName} directory to the connector build file."
    doLast {
        copySdkComponents(libraryName, defaultBuildDir, sdkComponentsDirName)
    }
}

private void copySdkComponents(String libraryName, String defaultBuildDir, String sdkComponentsDirName) {
    TaskLogger.info("Starting 'copySdkComponents' task...")
    def targetDir = getCommandArgument('targetDir', {defaultBuildDir})

    try {
        project.copy {
            TaskLogger.info("Copying [${sdkComponentsDirName}] directory with .sql files to '${targetDir}'")
            from project.zipTree(project.configurations.compileClasspath.find {
                it.name.startsWith(libraryName)})
            into targetDir
            include "${sdkComponentsDirName}/**"
        }
    } catch (IllegalArgumentException e) {
        Utils.exitWithErrorLog("Unable to find [${libraryName}] in the compile classpath. Make sure that the library is " +
                "published to Maven local repository and the proper dependency is added to the build.gradle file.")
    }
    project.copy {
        TaskLogger.info("Copying [${libraryName}] jar file to [${targetDir}]")
        from configurations.runtimeClasspath.find {
            it.name.startsWith(libraryName)
        }
        into targetDir
        rename ("^.*${libraryName}.*\$", "${libraryName}.jar")
    }
    TaskLogger.success("Copying sdk components finished successfully.")
}
```

To then run this task:

Copy code

```
./gradlew copySdkComponents
```

The extracted SQL files can be then executed during the execution of the `setup.sql` for the Native App.

## Deployment and installation

The Snowflake Native SDK for Connectors is designed to be used with the Snowflake Native App Framework. This means that deployment and installation is happening the same way
as it does for any other native app. This means that first the Application Package needs to be created and all the files need to be uploaded into a stage,
recommendation is to create stage inside the Application Package. If the above example script was used then all the required files from
the Snowflake Native SDK for Connectors should be already present in the target build directory of the Connector.
This means that it’s up to the developer to make sure that the custom code of the Connector and any Streamlit files are also there.
For more information check [Create and manage an application package](/developer-guide/native-apps/creating-app-package).

Once the Application Package is created and files are uploaded to stage, then a `version` of the application can be created. This step is optional during development,
because Application Instance can be created directly from files in stage instead of using registered version.
For more information check [Install and test an app locally](/developer-guide/native-apps/installing-testing-application).

## Development

The Snowflake Native SDK for Connectors provides objects and procedures that handle common use cases for each Connector application.
This includes things like configuration, lifecycle, ingestion definition, and so on. To review the full list of features, see the SDK reference.
Some parts of the predefined features can be customized. For more information, check Stored procedures and handlers customization.

## Testing

As mentioned before, Connectors Native SDK contains different types of tests.
This includes unit tests, integration tests and so-called application tests.
The unit tests use features provided in the aforementioned `connectors-native-sdk-test`.
As for integration and application tests they require connection to Snowflake.
Connection details can be defined using the `.env/snowflake_credentials` file.
The application tests directory also contains an empty connector application in resources.
That application is deployed during the test suite execution.

Additional resources:

> - [Snowflake Native SDK for Connectors Java API Reference](/developer-guide/native-apps/connector-sdk/java.html)
> - [Snowflake Native SDK for Connectors Java API TEST Reference](/developer-guide/native-apps/connector-sdk/test.html)

For hands-on experience on using and implementing your own connector, try our tutorials:

> - [Tutorial: Snowflake Native SDK for Connectors example Java connector](/developer-guide/native-apps/connector-sdk/tutorials/native_sdk_example_connector_tutorial)
> - [Tutorial: Snowflake Native SDK for Connectors Java connector template](/developer-guide/native-apps/connector-sdk/tutorials/native_sdk_template_connector_tutorial)
