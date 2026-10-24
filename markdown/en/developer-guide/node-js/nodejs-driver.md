# Node.js Driver

Node.js 4.0 Alpha 1 Private Preview - Universal Core

A version of the Snowflake Node.js Driver built on the Universal Core is available in private preview.
Preview participants can obtain the `snowflake-sdk` alpha release from
[npm](https://www.npmjs.com/package/snowflake-sdk/v/4.0.0-alpha.1).
This release requires Node.js 22 or later.

Use this driver only if you are participating in the private preview, subject to
[Snowflake’s Preview Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/).
It may be unstable and is not ready for use with production data. Use it only for internal evaluation;
do not use it to process personal data or other data subject to compliance or legal requirements.

The documentation below describes the existing Node.js driver. Its requirements and supported
functionality might differ from the preview.

Note

This driver currently does not support GCP regional endpoints. Please ensure that any workloads using through this driver do not require support for regional endpoints on GCP. If you have questions about this, please contact Snowflake Support.

Written in pure JavaScript, the Node.js driver provides a native asynchronous Node.js interface to Snowflake.

For more information about Node.js, see [nodejs.org](https://nodejs.org).

The driver supports the versions of Node.js supported by the Node.js Foundation. The driver supports the following Node.js versions:

- v20
- v22
- v24

See the [driver release timeline](https://nodejs.org/en/about/previous-releases) for more information.

The typical workflow for using the driver is:

1. Establish a connection with Snowflake.
2. Execute statements, e.g. queries and DDL/DML commands.
3. Consume the results.
4. Terminate the connection.

Important

To upload and download files from a Snowflake stage, you must use the following minimum versions of the driver:

- Version 1.6.2 to upload files (using the [PUT](/sql-reference/sql/put) command)
- Version 1.6.6 to download files (using the [GET](/sql-reference/sql/get) command)

**Next topics:**

- [Installing the Node.js Driver](/developer-guide/node-js/nodejs-driver-install)
- [Managing connections](/developer-guide/node-js/nodejs-driver-connect)
- [Authenticating connections](/developer-guide/node-js/nodejs-driver-authenticate)
- [Executing statements](/developer-guide/node-js/nodejs-driver-execute)
- [Consuming results](/developer-guide/node-js/nodejs-driver-consume)
- [Configuring log levels and files](/developer-guide/node-js/nodejs-driver-logs)
- [Node.js options reference](/developer-guide/node-js/nodejs-driver-options)
