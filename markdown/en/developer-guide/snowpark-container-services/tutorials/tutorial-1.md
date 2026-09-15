# Tutorial 1: Create a Snowpark Container Services Service

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

## Introduction

After completing the [common setup](/developer-guide/snowpark-container-services/tutorials/common-setup), you are ready to create a service. In this tutorial, you create a
service (named `echo_service`) that simply echoes back text that you provide as input. For example, if the input string is
“Hello World,” the service returns “I said, Hello World.”

There are two parts to this tutorial:

**Part 1: Create and test a service.** You download code provided for this tutorial and follow step-by-step instructions:

1. Download the service code for this tutorial.
2. Build a Docker image for Snowpark Container Services, and upload the image to a repository in your account.
3. Create a service by providing the service specification file and the compute pool in which to run the service.
4. Create a service function to communicate with the service.
5. Use the service. You send echo requests to the service and verify the response.

**Part 2: Understand the service**. This section provides an overview of the service code and highlights how different
components collaborate.

## 1: Download the service code

Code (a Python application) is provided to create the Echo service.

1. Download [SnowparkContainerServices-Tutorials.zip](/static/samples/spcs/SnowparkContainerServices-Tutorials.zip).
2. Unzip the content, which includes one directory for each tutorial. The `Tutorial-1` directory has the following files:
   - `Dockerfile`
   - `echo_service.py`
   - `templates/basic_ui.html`

## 2: Build an image and upload

Build an image for the linux/amd64 platform that Snowpark Container Services supports, and then upload the image to the image
repository in your account (see [Common Setup](/developer-guide/snowpark-container-services/tutorials/common-setup)).

You will need information about the repository (the repository URL and the registry hostname) before you can build and upload the image. For more information, see
[Registry and Repositories](/developer-guide/snowpark-container-services/working-with-registry-repository).

**Get information about the repository**

1. To get the repository URL, execute the [SHOW IMAGE REPOSITORIES](/sql-reference/sql/show-image-repositories) SQL command.

   Copy code

   ```
   SHOW IMAGE REPOSITORIES;
   ```

   - The `repository_url` column in the output provides the URL. An example is shown:

     ```
     <orgname>-<acctname>.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository
     ```
   - The host name in the repository URL is the registry host name. An example is shown:

     ```
     <orgname>-<acctname>.registry.snowflakecomputing.com
     ```

**Build image and upload it to the repository**

1. Open a terminal window, and change to the directory containing the files you unzipped.
2. To build a Docker image, execute the following `docker build` command using the Docker CLI.
   Note the command specifies current working directory (`.`)
   as the `PATH` for files to use for building the image.

   Copy code

   ```
   docker build --rm --platform linux/amd64 -t <repository_url>/<image_name> .
   ```

   - For `image_name`, use `my_echo_service_image:latest`.

   **Example**

   Copy code

   ```
   docker build --rm --platform linux/amd64 -t myorg-myacct.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_echo_service_image:latest .
   ```
3. Upload the image to the repository in your Snowflake account.

   1. For Docker to upload an image on your behalf to your repository,
      first [authenticate Docker with the registry](/developer-guide/snowpark-container-services/working-with-registry-repository#label-registry-and-repository-authentication).

      1. We recommend using [Snowflake CLI](/developer-guide/snowflake-cli/index)
         to authenticate your local Docker instance with the image
         registry for your Snowflake account. Make sure that you configured Snowflake CLI to connect to Snowflake. For more information,
         see [Configuring Snowflake CLI and connecting to Snowflake](/developer-guide/snowflake-cli/connecting/connect).
      2. To authenticate, execute the following Snowflake CLI command:

         Copy code

         ```
         snow spcs image-registry login
         ```
   2. To upload the image, execute the following command:

      Copy code

      ```
      docker push <repository_url>/<image_name>
      ```

      **Example**

      Copy code

      ```
      docker push myorg-myacct.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_echo_service_image:latest
      ```

## 3: Create a service

In this section you create a service.

To create a service, you need the following items:

- A [compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool). Snowflake runs your service in the specified compute pool. You created a compute pool named `tutorial_compute_pool` as part of the common setup.
- A [service specification](/developer-guide/snowpark-container-services/specification-reference). This specification provides Snowflake with the information
  needed to configure and run your service. For more information, see [Snowpark Container Services: Working with services](/developer-guide/snowpark-container-services/working-with-services). In this tutorial, you provide the specification inline, in CREATE SERVICE command. You can also save the specification to a file in your Snowflake stage and provide file information in the CREATE SERVICE command as shown in Tutorial 2.

The following sections explain how to create a service by using SQL or Snowsight. Use one of the methods to create a service.

Note

You can create a service by using SQL or Snowsight. However, you can’t perform the preceding step, by uploading an image to image repository, cannot be done using Snowsight.

### Create a service by using SQL

1. Verify that the compute pool is ready and that you are in the right context to create the service.

   1. Previously you set the context in the [Common Setup](/developer-guide/snowpark-container-services/tutorials/common-setup#label-snowpark-containers-common-setup-create-objects) step. To ensure you are in the right context for the SQL statements in this step, execute the following:

   Copy code

   ```
   USE ROLE test_role;
   USE DATABASE tutorial_db;
   USE SCHEMA data_schema;
   USE WAREHOUSE tutorial_warehouse;
   ```

   1. To ensure the compute pool you created in the [common setup](/developer-guide/snowpark-container-services/tutorials/common-setup#label-snowpark-containers-common-setup-create-objects) is ready, execute `DESCRIBE COMPUTE POOL`, and verify that the `state` is `ACTIVE` or `IDLE`. If the `state` is `STARTING`, you need to wait until the `state` changes to either `ACTIVE` or `IDLE`.

   Copy code

   ```
   DESCRIBE COMPUTE POOL tutorial_compute_pool;
   ```
2. To create the service, execute the following command using `test_role`:

   Copy code

   ```
   CREATE SERVICE echo_service
     IN COMPUTE POOL tutorial_compute_pool
     FROM SPECIFICATION $$
    spec:
      containers:
      - name: echo
        image: /tutorial_db/data_schema/tutorial_repository/my_echo_service_image:latest
        env:
          SERVER_PORT: 8000
          CHARACTER_NAME: Bob
        readinessProbe:
          port: 8000
          path: /healthcheck
      endpoints:
      - name: echoendpoint
        port: 8000
        public: true
      $$
   MIN_INSTANCES=1
   MAX_INSTANCES=1;
   ```

   Note

   If a service with that name already exists, use the DROP SERVICE command to delete the previously created service, and then
   create this service.
3. Execute the following SQL commands to get detailed information about the service you just created. For more information, see
   [Snowpark Container Services: Working with services](/developer-guide/snowpark-container-services/working-with-services).

   - To list services in your account, execute the SHOW SERVICES command:

     Copy code

     ```
     SHOW SERVICES;
     ```
   - To get information about your service including the service status, execute the [DESCRIBE SERVICE](/sql-reference/sql/desc-service) command.

     Copy code

     ```
     DESC SERVICE echo_service;
     ```

     Verify the `status` column shows the service status as RUNNING; if the status is PENDING, it indicates the service is still starting. To investigate why the service is not RUNNING, execute the [SHOW SERVICE CONTAINERS IN SERVICE](/sql-reference/sql/show-service-containers-in-service) command and review the `status` of individual containers:

     Copy code

     ```
     SHOW SERVICE CONTAINERS IN SERVICE echo_service;
     ```

### Create a service by using Snowsight

[Sign in to Snowflake](/user-guide/connecting) and complete the following steps to create a service:

1. In the navigation menu, select **Monitoring** » **Services & jobs**.
2. Under **Create new**, select **Create new service**.
3. On the **Create service** page, provide the following information:

   - **Service details**:

     - In the top-right corner, from the role selector menu, select `test_role`.
     - Specify the **Service details**:
       - Service name: `echo_service`
       - Compute pool: `tutorial_compute_pool`
       - Location to store: `tutorial_db.data_schema`
       - Select **Next**.
   - **Service specification**: You can get this information from the service specification in the preceding section.

     - On the **Containers** tab, specify the following information:

       - Name: `echo`
       - Image: `TUTORIAL_REPOSITORY.my_echo_service_image:latest`
     - On the **Endpoints** tab, specify the following information:

       - Name: `echoendpoint`
       - Network port: `8080`
       - Protocol: `HTTP`
       - Select the **Allow public access** checkbox.
     - Select **Next**.
4. To create the service, select **Create**.

   Snowflake creates the service and displays the service details.

Note

The SQL version of creating the service in the preceding section includes an environment variable (`SERVER_PORT`) that changes the network port the code listens on to 8000. The Snowsight version of the tutorial doesn’t provide this override. Therefore, we specify the network port as 8080, which is the default in the code.

> To use Snowsight and use some of the service specification’s advanced features, you can provide a YAML version of the service specification in the UI.

## 4: Use the service

First, setup the context for the SQL statements in this section, execute the following:

Copy code

```
USE ROLE test_role;
USE DATABASE tutorial_db;
USE SCHEMA data_schema;
USE WAREHOUSE tutorial_warehouse;
```

Now you can communicate with the Echo service. As explained in [Using a service](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating), you can use the service in the following ways:

- From a SQL query by using a service function
- From outside Snowflake, which is called *network ingress*

In the following sections you use these methods to communicate with the Echo service.

### Communicate with your service by using a service function

A service function is one of the methods available to communicate with your service. A service function is a user-defined
function (UDF) that you associate with the service endpoint. When the service function is executed, it sends a request to the
service endpoint, and hen receives a response.

To create a service function, execute the following command:

Copy code

```
CREATE FUNCTION my_echo_udf (InputText varchar)
  RETURNS varchar
  SERVICE=echo_service
  ENDPOINT=echoendpoint
  AS '/echo';
```

In the query:

- The SERVICE property associates the UDF with the `echo_service` service.
- The ENDPOINT property associates the UDF with the `echoendpoint` endpoint within the service.
- AS ‘/echo’ specifies the HTTP path to the Echo server. You can find this path in the service code: `echo_service.py`.

You can invoke the service function in a query.
The example service function, `my_echo_udf`, can take either a single string or a list of strings as input.

#### Example 1.1: Pass a single string

- To call the `my_echo_udf` service function, execute the following
  SELECT statement, passing one input string (`'hello'`):

  Copy code

  ```
  SELECT my_echo_udf('hello!');
  ```

  Snowflake sends a POST request to the service endpoint (`echoendpoint`). Upon receiving the request, the service echos the input string in the response:

  ```
  +--------------------------+
  | **MY_ECHO_UDF('HELLO!')**|
  |------------------------- |
  | Bob said hello!          |
  +--------------------------+
  ```

If service is created by using Snowsight, the following response is returned:

> ```
> +--------------------------+
> | **MY_ECHO_UDF('HELLO!')**|
> |------------------------- |
> | I said hello!            |
> +--------------------------+
> ```

#### Example 1.2: Pass a list of strings

When you pass a list of strings to the service function, Snowflake batches these input strings, and then sends a series of POST
requests to the service. After the service processes all the strings, Snowflake combines the results, and then returns them.

The following example passes a table column as input to the service function.

1. Create a table with multiple strings:

   Copy code

   ```
   CREATE TABLE messages (message_text VARCHAR)
     AS (SELECT * FROM (VALUES ('Thank you'), ('Hello'), ('Hello World')));
   ```
2. Verify that the table was created:

   Copy code

   ```
   SELECT * FROM messages;
   ```
3. To call the service function, execute the following SELECT statement, passing table rows as input:

   Copy code

   ```
   SELECT my_echo_udf(message_text) FROM messages;
   ```

   Output:

   ```
   +---------------------------+
   | MY_ECHO_UDF(MESSAGE_TEXT) |
   |---------------------------|
   | Bob said Thank you        |
   | Bob said Hello            |
   | Bob said Hello World      |
   +---------------------------+
   ```

### Communicate with your service by using a web browser

The service exposes the endpoint publicly. For details, see the inline specification provided in the CREATE SERVICE command. Therefore, you can sign in to a web UI that the service exposes to the internet, and then send requests to the service from a web browser.

1. Find the URL of the public endpoint that the service exposes:

   Copy code

   ```
   SHOW ENDPOINTS IN SERVICE echo_service;
   ```

   The `ingress_url` column in the response provides the URL.

   **Example**

   ```
   p6bye-myorg-myacct.snowflakecomputing.app
   ```
2. Append `/ui` to the endpoint URL, and then paste it in the web browser. This causes the service to execute the `ui()` function (see `echo_service.py`).

   The first time you access the endpoint URL, you are asked to sign in to Snowflake. For this test, use the same user that you used to create the service to ensure that the user has the necessary privileges.

   ![Web form to communicate with echo service.](/static/images/spcs/Snowpark-Containers-T1-web-ui-10.png)
3. In the **Input** box, enter string “Hello”, and then press **Return** (**Enter**).

   ![Web form showing response from the Echo service.](/static/images/spcs/Snowpark-Containers-T1-web-ui-20.png)

Note

You can access the public endpoint programmatically. For more information, see [Tutorial 8: Access the public endpoint programmatically](/developer-guide/snowpark-container-services/tutorials/advanced/tutorial-8-access-public-endpoint-programmatically).

## 5: Clean up

If you don’t plan to continue with [Tutorial 2](/developer-guide/snowpark-container-services/tutorials/tutorial-2) or [Tutorial 4](/developer-guide/snowpark-container-services/tutorials/advanced/tutorial-4), you should remove billable
resources you created. For more information, see Step 5 in [Tutorial 4](/developer-guide/snowpark-container-services/tutorials/advanced/tutorial-4).

## 6: Reviewing the service code

This section covers the following topics:

- [Examining the tutorial 1 code](#label-snowpark-containers-tutorial-1-step-6a): Review the code files that implement the Echo service.
- [Understanding the service function](#label-snowpark-containers-tutorial-1-step-6b): This section explains how the service function in this tutorial is linked
  with the service.
- [Building and testing an image locally](#label-snowpark-containers-tutorial-1-step-6c). The section provides an explanation of how you can locally test the
  Docker image before uploading it to a repository in your Snowflake account.

### Examining the tutorial 1 code

The zip file you downloaded in Step 1 includes the following files:

- `Dockerfile`
- `echo_service.py`
- `templates/basic_ui.html`

You also use service specification when creating the service. The following section explains how these code components work together to create the service.

#### echo\_service.py file

This Python file contains the code that implements a minimal HTTP server that returns (echoes back) input text. The code
primarily performs two tasks: handling echo requests from Snowflake service functions, and providing a web user interface (UI)
for submitting echo requests.

Copy code

```
from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
import logging
import os
import sys

SERVICE_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = os.getenv('SERVER_PORT', 8080)
CHARACTER_NAME = os.getenv('CHARACTER_NAME', 'I')

def get_logger(logger_name):
  logger = logging.getLogger(logger_name)
  logger.setLevel(logging.DEBUG)
  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.DEBUG)
  handler.setFormatter(
    logging.Formatter(
      '%(name)s [%(asctime)s] [%(levelname)s] %(message)s'))
  logger.addHandler(handler)
  return logger

logger = get_logger('echo-service')

app = Flask(__name__)

@app.get("/healthcheck")
def readiness_probe():
  return "I'm ready!"

@app.post("/echo")
def echo():
  '''
  Main handler for input data sent by Snowflake.
  '''
  message = request.json
  logger.debug(f'Received request: {message}')

  if message is None or not message['data']:
    logger.info('Received empty message')
    return {}

  # input format:
  #   {"data": [
  #     [row_index, column_1_value, column_2_value, ...],
  #     ...
  #   ]}
  input_rows = message['data']
  logger.info(f'Received {len(input_rows)} rows')

  # output format:
  #   {"data": [
  #     [row_index, column_1_value, column_2_value, ...}],
  #     ...
  #   ]}
  output_rows = [[row[0], get_echo_response(row[1])] for row in input_rows]
  logger.info(f'Produced {len(output_rows)} rows')

  response = make_response({"data": output_rows})
  response.headers['Content-type'] = 'application/json'
  logger.debug(f'Sending response: {response.json}')
  return response

@app.route("/ui", methods=["GET", "POST"])
def ui():
  '''
  Main handler for providing a web UI.
  '''
  if request.method == "POST":
    # getting input in HTML form
    input_text = request.form.get("input")
    # display input and output
    return render_template("basic_ui.html",
      echo_input=input_text,
      echo_reponse=get_echo_response(input_text))
  return render_template("basic_ui.html")

def get_echo_response(input):
  return f'{CHARACTER_NAME} said {input}'

if __name__ == '__main__':
  app.run(host=SERVICE_HOST, port=SERVER_PORT)
```

In the code:

- The `echo` function enables a Snowflake service function to communicate with the service. This function specifies the
  `@app.post()` decoration as shown:

  Copy code

  ```
  @app.post("/echo")
  def echo():
  ```

  When the echo server receives your HTTP POST request with the `/echo` path, the server routes the request to this
  function. The function executes and echoes back the strings from the request body in the response.

  To support communication from a Snowflake service function, this server implements the external functions. That is, the
  server implementation follows a certain input/output data format in order to serve a SQL function, and this is the same
  [input/output data format](/sql-reference/external-functions-data-format) used by
  [External Functions](/sql-reference/external-functions).
- The `ui` function section of the code displays a web form and handles echo requests submitted from the web form. This
  function uses the `@app.route()` decorator to specify that requests for `/ui` are handled by this function:

  Copy code

  ```
  @app.route("/ui", methods=["GET", "POST"])
  def ui():
  ```

  The Echo service exposes the `echoendpoint` endpoint publicly (see service specification), enabling communication with
  the service over the web. When you load the URL of the public endpoint with /ui appended in your browser, the browser sends
  an HTTP GET request for this path, and the server routes the request to this function. The function executes and returns a
  simple HTML form for the user to enter a string in.

  After the user enters a string and submits the form, the browser sends an HTTP post request for this path, and the server
  routes the request to this same function. The function executes and returns an HTTP response containing the original string.
- The `readiness_probe` function uses the `@app.get()` decorator to specify that requests for `/healthcheck`
  are handled by this function:

  Copy code

  ```
  @app.get("/healthcheck")
  def readiness_probe():
  ```

  This function enables Snowflake to check the readiness of the service. When the container starts, Snowflake wants to confirm
  that the application is working and that the service is ready to serve the requests. Snowflake sends an HTTP GET request with
  this path (as a health probe, readiness probe) to ensure that only healthy containers serve traffic. The function can do
  whatever you want.
- The `get_logger` function helps set up logging.

#### Dockerfile

This file contains all the commands to build an image using Docker.

Copy code

```
ARG BASE_IMAGE=python:3.10-slim-buster
FROM $BASE_IMAGE
COPY echo_service.py ./
COPY templates/ ./templates/
RUN pip install --upgrade pip && \\
pip install flask
CMD ["python", "echo_service.py"]
```

The Dockerfile contains instructions to install the Flask library in the Docker container. The code in `echo_service.py`
relies on the Flask library to handle HTTP requests.

#### /template/basic\_ui.html

The Echo service exposes the `echoendpoint` endpoint publicly (see service specification), enabling communication with the
service over the web. When you load the public endpoint URL with `/ui` appended in your browser, the Echo service displays
this form. You can enter a string in the form and submit the form, and the service returns the string in an HTTP response.

Copy code

```
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Welcome to echo service!</title>
  </head>
  <body>
    <h1>Welcome to echo service!</h1>
    <form action="{{ url_for("ui") }}" method="post">
      <label for="input">Input:<label><br />
      <input type="text" id="input" name="input"><br />
    </form>
    <h2>Input:</h2>
    {{ echo_input }}
    <h2>Output:</h2>
    {{ echo_reponse }}
  </body>
</html>
```

#### Service specification

Snowflake uses information you provide in this specification to configure and run your service.

Copy code

```
spec:
  containers:
  - name: echo
    image: /tutorial_db/data_schema/tutorial_repository/my_echo_service_image:latest
    env:
      SERVER_PORT: 8000
      CHARACTER_NAME: Bob
    readinessProbe:
      port: 8000
      path: /healthcheck
  endpoints:
  - name: echoendpoint
    port: 8000
    public: true
```

In the service specification:

- The `containers.image` specifies the image for Snowflake to start a container.
- The optional `endpoints` field specifies the endpoint the service exposes.

  - The `name` specifies a user-friendly name for the TCP network port the container is listening on. You use this
    user-friendly endpoint name to send requests to the corresponding port. Note that the `env.SERVER_PORT` controls this
    port number.
  - The endpoint is also configured as `public`. This allows traffic to this endpoint from the public web.
- The optional `containers.env` field is added to illustrate how you might override environment variables that Snowflake
  passes to all processes in your container. For example, the service code (`echo_service.py`) reads the environment
  variables with default values as shown:

  Copy code

  ```
  CHARACTER_NAME = os.getenv('CHARACTER_NAME', 'I')
  SERVER_PORT = os.getenv('SERVER_PORT', 8080)
  ```

  It works as follows:

  - When the Echo service receives an HTTP POST request with a string (e.g., “Hello”) in the request body, the service returns
    “I said Hello” by default. The code uses the `CHARACTER_NAME` environment variable to determine the word before
    “said.” By default, `CHARACTER_NAME` is set to “I.”

    You can overwrite the CHARACTER\_NAME default value in the service specification. For example, if you set the value to “Bob,”
    the Echo service returns a “Bob said Hello” response.
  - Similarly, the service specification overrides the port (SERVER\_PORT) that the service listens on to 8000, overriding the
    default port 8080.
- The `readinessProbe` field identifies the `port` and `path` that Snowflake can use to send an HTTP GET
  request to the readiness probe to verify that the service is ready to handle traffic.

  The service code (`echo_python.py`) implements the readiness probe as follows:

  Copy code

  ```
  @app.get("/healthcheck")
  def readiness_probe():
  ```

  Therefore, the specification file includes the `container.readinessProbe` field accordingly.

For more information about service specifications, see [Service specification reference](/developer-guide/snowpark-container-services/specification-reference).

### Understanding the service function

A service function is one of the methods of communicating with your service (see
[Using a service](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating)). A service function is a user-defined function (UDF) that you associate
with a service endpoint. When the service function is executed, it sends a request to the associated service endpoint and
receives a response.

You create the following service function by executing the CREATE FUNCTION command with the following parameters:

Copy code

```
CREATE FUNCTION my_echo_udf (InputText VARCHAR)
  RETURNS VARCHAR
  SERVICE=echo_service
  ENDPOINT=echoendpoint
  AS '/echo';
```

Note the following:

- The `my_echo_udf` function takes a string as input and returns a string.
- The SERVICE property identifies the service (`echo_service`), and the ENDPOINT property identifies the user-friendly
  endpoint name (`echoendpoint`).
- The AS ‘/echo’ specifies the path for the service. In `echo_service.py`, the `@app.post` decorator associates this
  path with the `echo` function.

This function connects with the specific ENDPOINT of the specified SERVICE. When you invoke this function, Snowflake sends a
request to the `/echo` path inside the service container.

### Building and testing an image locally

You can test the Docker image locally before uploading it to a repository in your Snowflake account. In local testing, your
container runs standalone (it is not a service that Snowflake runs).

To test the Tutorial 1 Docker image:

1. To create a Docker image, in the Docker CLI, execute the following command:

   Copy code

   ```
   docker build --rm -t my_service:local .
   ```
2. To launch your code, execute the following command:

   Copy code

   ```
   docker run --rm -p 8080:8080 my_service:local
   ```
3. Send an echo request to the service using one of the following methods:

   - **Using the cURL command:**

     In another terminal window, using cURL, send the following POST request to port 8080:

     Copy code

     ```
     curl -X POST http://localhost:8080/echo \
       -H "Content-Type: application/json" \
       -d '{"data":[[0, "Hello friend"], [1, "Hello World"]]}'
     ```

     Note that the request body includes two strings. This cURL command sends a POST request to port 8080 on which the service
     is listening. The 0 in the data is the index of the input string in the list. The Echo service echoes the input strings
     in response as shown:

     ```
     {"data":[[0,"I said Hello Friend"],[1,"I said Hello World"]]}
     ```
   - **Using a web browser:**

     1. In your browser, on the same computer, open `http://localhost:8080/ui`.

        This sends a GET request to port 8080, which the service is listening on. The service executes the `ui()`
        function, which renders a HTML form as shown:

        ![Web form to communicate with echo service.](/static/images/spcs/Snowpark-Containers-T1-web-ui-10.png)
     2. Enter the string “Hello” in the **Input** box, and press **Return**.

        ![Web form showing response from the Echo service.](/static/images/spcs/Snowpark-Containers-T1-web-ui-20.png)

## What’s next?

You can now test the [Tutorial 2](/developer-guide/snowpark-container-services/tutorials/tutorial-2) that executes a job.
