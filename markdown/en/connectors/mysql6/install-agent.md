# Setting up the Snowflake Connector for MySQL Agent container

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for MySQL.
We’re now focused on a next-generation solution that will offer a significantly
improved experience; therefore, moving this connector to the general availability
status is currently not on our product roadmap.
You may continue to use this connector as preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/about) and
includes better performance, customizability, and enhanced deployment options.

This topic describes the procedure to set up the Snowflake Connector for MySQL agent container.
A database connector agent is a containerized application that runs inside your infrastructure,
connecting directly to your databases and to Snowflake.

The process of configuring the Snowflake Connector for MySQL agent includes the following tasks:

1. [Review prerequisites and choose an orchestration system](#review-prerequisites-and-choose-an-orchestration-system)
2. [Configure and run the agent](#configure-and-run-the-agent)
3. [Optionally] [Configure orchestration using Kubernetes](#configure-orchestration-using-kubernetes)
4. [Monitor the agent](#monitor-the-agent)

## Review prerequisites and choose an orchestration system

Review and complete all prerequisites and proceed to [Configure and run the agent](#configure-and-run-the-agent).

### Choose a container orchestration system

The agent is packaged as a standard Docker container image, and can be run on any orchestration system
that supports the standard.
This can be a stand-alone [Docker](https://www.docker.com/) instance, [Kubernetes](https://kubernetes.io/),
[RedHat OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift),
a cloud-managed solution, such as [AWS Fargate](https://aws.amazon.com/fargate/), and others. Your organization will often have a preferred, existing system for you to use.

Pay attention to the agent configuration section of this document, because different orchestration systems come with
different constraints. Your system, or specific setup, may not permit you to mount writable volumes
(as is required with the agent’s primary configuration option).

Later examples will focus on Kubernetes as the most popular orchestration system.
The approach will often be similar in other systems, and you will need to adjust the examples for your setup.

### Confirm required system resources

- The agent is a memory-intensive application, and requires a minimum 6GB of RAM to operate correctly.
- The optimal number of CPUs is 4. Fewer CPUs can decrease performance. More CPUs will not improve performance.

### Set up connectivity

The agent needs to connect to every source database that you intend to read data from.
Configure your network and firewalls, so that direct connections are possible, and MySQL’s classic client port is reachable.
Typically that’s port `3306`.
For more information see [MySQL’s Port Reference Tables](https://dev.mysql.com/doc/mysql-port-reference/en/mysql-port-reference-tables.html).

If your source databases reside in isolated networks, and connecting from a single agent won’t be possible,
you will need to install additional instances of the connector’s native application, each one with its own agent.
This feature is currently in private preview. Please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to request access.

The agent also connects directly to your Snowflake deployment. For information on which hostnames need to be available
see [Allowing Host names](/user-guide/hostname-allowlist).

If any of the agent’s connections pass through a proxy, you will need to pass additional configuration to the agent.
See [Review optional configuration environment variables](#label-agent-optional-envs-mysql6).

## Configure and run the agent

Configuring and running the agent is composed of the following steps:

1. [Download the MariaDB JDBC driver](#download-the-mariadb-jdbc-driver)
2. [[Optional] Obtain and prepare SSL certificates for source databases](#optional-obtain-and-prepare-ssl-certificates-for-source-databases)
3. [Prepare agent configuration](#prepare-agent-configuration) files or environment variables for the agent and start the agent
4. [Review optional configuration environment variables](#review-optional-configuration-environment-variables)
5. [Set up PrivateLink connectivity](#set-up-privatelink-connectivity) where required

### Download the MariaDB JDBC driver

The agent uses this driver to connect to, and interact with MySQL databases.
Despite it nominally being a driver for MariaDB, they’re compatible.

Due to licensing limitations, the JDBC driver cannot be distributed together with the agent, and you’ll have to provide it.
Download the [MariaDB JDBC Connector 3.4.1](https://repo1.maven.org/maven2/org/mariadb/jdbc/mariadb-java-client/3.4.1/mariadb-java-client-3.4.1.jar) and
save it in a directory from which you can mount it to the agent’s container.

### [Optional] Obtain and prepare SSL certificates for source databases

When the agent connects to source databases via SSL, it requires their certificates to validate the connections. These certificates must be available in the Java Truststore inside the agent’s container, under the path `/opt/java/openjdk/lib/security/cacerts`.

The simplest way to supply certificates to the agent is to add them to the host machine’s existing `cacerts` file, and then mount that file to the running container.

Copy code

```
openssl x509 -outform der -in ca-root.pem -out ca-root.der
keytool -import -alias server-root \
    -keystore $JAVA_HOME/jre/lib/security/cacerrts -file ca-root.der
```

### Prepare agent configuration

The agent can be configured via container-mounted JSON files, or environment variables, or a mix of both.
The access keys required to connect to Snowflake can be mounted from the host’s file system, supplied as container secrets,
or as environment variables.

The following sections describe different configuration options, from the most straightforward, to the most comprehensive.
Choose an approach based on the specifics of your infrastructure.

JSONEnvironment variables

The simplest way to configure the agent is to mount two JSON files into the container at runtime:

- `snowflake.json` contains configuration for the agent to connect to your Snowflake account.
  :   Download this file at the end of the connector’s setup process via the wizard available in Snowsight.
- `datasources.json` contains the list of source databases for the agent to connect to.
  :   You will need to prepare this file yourself.

Right after downloading, `snowflake.json` includes a temporary private key for the Snowflake service account that represents the agent. When starting the agent for the first time, the agent will automatically replace that temporary key with a new, permanent set of keys, and output them to the path `/home/agent/.ssh/` inside the container. Both `snowflake.json` and the path under `/home/agent/.ssh/` must be mounted as writable for the agent to start.

Alternatively, you can provide your own private key for the agent’s service account.
See [Review optional configuration environment variables](#label-agent-optional-envs-mysql6) for the required environment variables to pass.

Caution

If the agent finds an existing private key, either as a mounted file or as
an environment variable, it will ignore any temporary key that might still be
present in `snowflake.json`.

Prepare the `datasources.json` file by using the following template:

Copy code

```
{
    "<data_source_name_1>": {
        "url": "jdbc:mariadb://<host>:<port>/[?<key1>=<value1>[&<key2>=<value2>]]",
        "username": "<mysql_db_username>",
        "password": "<mysql_db_password>"
    },
    "<data_source_name_2>": {
        "url": "jdbc:mariadb://<host>:<port>/[?<key1>=<value1>[&<key2>=<value2>]]",
        "username": "<mysql_db_username>",
        "password": "<mysql_db_password>"
    }
}
```

When creating the file:

- You have to add at least one data source with a URL, otherwise the agent will not start.
- You can add as many data sources, as you need, as long as the agent can connect directly to all of them.
- The names you enter become the identifiers that you will need later to call the connector’s native app and enable replication. They must be unique for each data source.
- The names of data sources can contain only letters and numbers. All lowercase letters are automatically uppercased by the agent.

Once you have both JSON files in place, the JAR file with JDBC drivers, and a directory to output the new set of keys, you can run the container:

Copy code

```
docker run -d \
   --restart unless-stopped \
   --name database-connector-agent \
   --volume </path/to/ssh/keys/directory>:/home/agent/.ssh \
   --volume </path/to/mariadb/jdbc/jar>:/home/agent/libs/mariadb-jdbc-driver \
   --volume </path/to/snowflake/json/file>:/home/agent/snowflake.json \
   --volume </path/to/datasources/json/file>:/home/agent/datasources.json \
   -m 6g \
   snowflakedb/database-connector-agent:latest
```

Configuration options passed through `snowflake.json` and `datasources.json` can be supplied through environment variables.

Important

Environment variables take precedence over settings supplied through either of the JSON files.

The environment variable names follow the same structure as the paths in both JSON files.
Nested keys must be separated with underscores `_`, every variable must be prefixed with `SNOWFLAKE_`, and array entries prefixed with integer indexes.

Copy code

```
docker run \
  -e SNOWFLAKE_USERNAME="MYSQL_AGENT_USER" \
  -e SNOWFLAKE_APPLICATION_NAME="SNOWFLAKE_CONNECTOR_FOR_MYSQL" \
  -e SNOWFLAKE_ALLOWLIST_0_HOST="example_account.us-west-2.aws.snowflakecomputing.com" \
  -e SNOWFLAKE_ALLOWLIST_0_PORT=443 \
  -e SNOWFLAKE_ALLOWLIST_0_TYPE="SNOWFLAKE_DEPLOYMENT" \
  ...
```

Is equivalent to:

Copy code

```
{
  "userName": "MYSQL_AGENT_USER",
  "applicationName": "SNOWFLAKE_CONNECTOR_FOR_MYSQL",
  "allowlist": [
  {
    "host": "example_account.us-west-2.aws.snowflakecomputing.com",
    "port": 443,
    "type": "SNOWFLAKE_DEPLOYMENT"
  }
  ]
}
```

You don’t need to copy all the entries of the `allowList` or `allowlistPrivatelink` arrays. Instead, find the `allowList` entry with the `type` of `SNOWFLAKE_DEPLOYMENT` and use this URL to set the variable `SNOWFLAKE_ENFORCEDURL`, as in:

Copy code

```
docker run \
  -e SNOWFLAKE_USERNAME="CONNECTOR_MYSQL_AGENT" \
  -e SNOWFLAKE_APPLICATION_NAME="CONNECTOR_MYSQL_INSTANCE" \
  -e SNOWFLAKE_ENFORCEDURL="example_account.us-west-2.aws.snowflakecomputing.com:443" \
  ...
```

Data sources follow a similar structure and are prefixed with `SNOWFLAKE_DATASOURCES_`.

For example:

Copy code

```
docker run \
  -e SNOWFLAKE_DATASOURCES_MYSQLDS1_URL="jdbc:mariadb://example.internal:3306/" \
  -e SNOWFLAKE_DATASOURCES_MYSQLDS1_USERNAME="example_user" \
  -e SNOWFLAKE_DATASOURCES_MYSQLDS1_PASSWORD="example_password" \
  ...
```

Is equivalent to:

Copy code

```
{
    "MYSQLDS1": {
        "url": "jdbc:mariadb://example.internal:3306/",
        "username": "example_user",
        "password": "example_password"
    }
}
```

### Review optional configuration environment variables

The agent supports the following, optional settings, available by setting additional environment variables on the container:

`SNOWFLAKE_PRIVATEKEYPATH`
:   Specifies the absolute path to the file with the agent user’s private key. This is used when mounting your own private key to the container, usually via an orchestration system’s secret.

`SNOWFLAKE_PRIVATEKEYPASSWORD`
:   Specifies the password for agent user’s the private key. If you let the agent generate the keys, this password will be set on the private key. If you reuse existing keys, this password will be used to access the existing private key.

`SNOWFLAKE_PRIVATEKEY`
:   Specifies the content of the agent user’s private key. This can be set, when mounting the private key as a file in the container is not an option.

`SNOWFLAKE_ENFORCEDURL`
:   Specifies the URL to connect to Snowflake, overriding the agent’s own discovery mechanism. This is primarily used to connect to PrivateLink deployments.

`JAVA_OPTS`
:   Specifies additional Java settings or properties that will be passed to the agent’s process.

    The most commonly used are:

    - The `-Xmx` option to set the maximum Java heap size. Snowflake recommends setting this value to the amount of memory available to the container, minus 1GB.

      For example, if the container has 6GB of RAM available, set the following:

      Copy code

      ```
      JAVA_OPTS=-Xmx5g
      ```
    - When the connection from agent to Snowflake requires a proxy, set the following:

      Copy code

      ```
      JAVA_OPTS=-Dhttp.useProxy=true -Dhttp.proxyHost=<proxy-host> -Dhttp.proxyPort=<proxy-port>
      ```
    - To bypass the proxy for some hosts or IP addresses, for instance, source databases, set the additional `http.nonProxyHosts` property. Use a pipe symbol (`|`) to separate multiple host names. Use an asterisk (`*`) as a wildcard character.

      Copy code

      ```
      JAVA_OPTS=-Dhttp.useProxy=true -Dhttp.proxyHost=<proxy-host> -Dhttp.proxyPort=<proxy-port>
        -Dhttp.nonProxyHosts='*.example.com%localhost%myorganization-myaccount.snowflakecomputing.com|192.168.91.*'
      ```
    - To pass credentials for the proxy, set the `http.proxyUser` and `http.proxyPassword` system properties.

      Copy code

      ```
      JAVA_OPTS=-Dhttp.useProxy=true -Dhttp.proxyHost=<proxy-host> -Dhttp.proxyPort=<proxy-port>
        -Dhttp.proxyUser=<proxy-user> -Dhttp.proxyPassword=<proxy-pass>
      ```

### Set up PrivateLink connectivity

If you’re connecting to a PrivateLink deployment, you must provide the URL for the agent to
connect to explicitly by setting the `SNOWFLAKE_ENFORCEDURL` environment variable.

To determine the PrivateLink URL of your account, you can either:

- Open the `snowflake.json` file that you obtained during the configuration process. Find the array named `allowlistPrivatelink`, and then the entry with the `type` of `SNOWFLAKE_DEPLOYMENT`.
- Use the [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) function.

### Understanding Snowflake access keys

The agent authenticates with Snowflake as a service account,
created by the connector’s setup wizard in Snowsight, using a set of access keys.
The setup wizard creates temporary access keys, and adds the *private* key
to the `snowflake.json` file in a field named `temporaryPrivateKey`.

During its initial startup, the agent replaces these temporary keys by:

1. Generating a new set of access keys, and storing them under `/home/agent/.ssh`
   as `database-connector-agent-app-private-key.p8` and `database-connector-agent-app-public-key.pub` inside the container.
   This directory should be mounted as an external, writable volume to the container,
   so that the keys persist when the container shuts down.
2. Altering its service account to use the new keys.
3. Removing the `temporaryPrivateKey` field from the `snowflake.json` file.

After the initial key replacement, the agent never rotates access keys.

You can use the keys generated by the agent.
Or you can create your own set, alter the service account,
and provide the private key to the agent.

The agent’s private key discovery order is:

1. Any key passed using the `SNOWFLAKE_PRIVATEKEY` environment variable. If this value is found, the connector will ignore the temporary key from `snowflake.json`.
2. Keys found on mounted volumes in `/home/agent/.ssh/database-connector-agent-app-private-key.p8`.
   If this file is found, the connector will ignore the temporary key from `snowflake.json`.
3. The value of the `temporaryPrivateKey` field from the `snowflake.json` file.

## Configure orchestration using Kubernetes

Note

While this section concentrates on Kubernetes, the connector can be launched in any container orchestration system.
The configuration syntaxes are often similar. For details, refer to your system’s documentation.

When using Kubernetes, mounting writable volumes is typically not an option.
As a result, the agent will not be able to automatically replace the keys for its Snowflake user account.
You will have to create a set of keys manually, alter the user, and then provide the private key to the container running the agent,
typically as a mounted secret. For details on setting key-pairs for Snowflake users see [Configuring key-pair authentication](/user-guide/key-pair-auth#label-configuring-key-pair-authentication).

We recommend that you store the secrets in a secure store, such as HashiCorp Vault.
These stores usually have existing integrations with Kubernetes, for instance,
[Vault offers a specialized operator](https://developer.hashicorp.com/vault/tutorials/kubernetes/vault-secrets-operator).
The integration details will be specific to your container orchestration system and secure store. Refer to their respective documentation for details.

Kubernetes normally runs in multi-node clusters, with no way to mount files from the host machines.
To supply the agent’s container with the configuration JSON files,
you can create a [Kubernetes ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) storing all three of the files.

The following shows a basic example for configuring the agent in Kubernetes.

1. Create a ConfigMap that will store the JDBC driver and `snowflake.json`:

   Copy code

   ```
   kubectl create configmap database-connector-config \
     --from-file=jdbc-driver.jar=</path/to/mariadb/jdbc/jar> \
     --from-file=snowflake.json=</path/to/snowflake/json/file>
   ```

   Tip

   The JDBC driver JAR is around 650KB in size, as of this writing, and well under the ConfigMap’s limit of 1MB imposed by Kubernetes. If you prefer not to put this much data into a ConfigMap, a common pattern is to build a custom Docker image, based on the agent’s official one, with the addition of the JDBC JAR.
2. Create a secret that will store the content of the agent user’s private key and `datasources.json`:

   Copy code

   ```
   kubectl create secret generic database-connector-secrets \
     --from-file=private-key=</path/to/private/key/file> \
     --from-file=datasources.json=</path/to/datasources.json>
   ```
3. Configure the agent’s Pod, mounting the configuration files and private key as volumes:

   Copy code

   ```
   apiVersion: v1
   kind: Pod
   metadata:
     name: database-connector-agent
   spec:
     restartPolicy: Always
     containers:
    - name: database-connector-agent
      image: snowflakedb/database-connector-agent:latest
      resources:
        requests:
          memory: "6Gi"
        limits:
          memory: "8Gi"
      volumeMounts:
        - name: config
          mountPath: /home/agent/libs/jdbc-driver.jar
          subPath: jdbc-driver.jar
        - name: config
          mountPath: /home/agent/snowflake.json
          subPath: snowflake.json
        - name: secrets
          mountPath: /home/agent/datasources.json
          subPath: datasources.json
        - name: secrets
          mountPath: /etc/private-key/private-key
          subPath: private-key
      env:
        - name: MYSQL_DATASOURCE_DRIVERPATH
          value: /home/agent/libs/jdbc-driver.jar
        - name: SNOWFLAKE_PRIVATEKEYPATH
          value: /etc/private-key/private-key
     volumes:
    - name: config
      configMap:
        name: database-connector-config
    - name: secrets
      secret:
       secretName: database-connector-secrets
   ```
4. Save the Pod’s configuration as a YAML file, for instance, `database-connector.yaml` and start:

   Copy code

   ```
   kubectl apply -f database-connector.yaml
   ```

## Monitor the agent

The agent’s container outputs logs to `stdout` which can be accessed using Docker.
For example, if your container’s name is `database-connector-agent`, then the command to view logs would be:

Copy code

```
docker container logs database-connector-agent
```

These logs are also streamed into Snowflake. See [Monitor](monitor) for information about how to access these.

### Accessing the health check endpoint

The agent exposes a HTTP endpoint with health information. You can use this endpoint when running the agent in an
orchestration system to determine when the agent has fully launched and whether it is healthy.
The endpoint is available under port `8080` and path `/actuator/health`.

To use the endpoint as a liveness probe in Kubernetes, add the following to your Pod configuration:

Copy code

```
apiVersion: v1
kind: Pod
spec:
  containers:
  - ...
    livenessProbe:
      httpGet:
        path: /actuator/health
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 10
```

## Next steps

After completing these procedures, follow the steps in [Configuring replication for the Snowflake Connector for MySQL](/connectors/mysql6/configure-replication).
