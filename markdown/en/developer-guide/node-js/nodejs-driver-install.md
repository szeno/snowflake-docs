# Installing the Node.js Driver

This topic describes how to install the Node.js driver using `npm`, the default package manager for the Node.js JavaScript runtime
environment.

## Prerequisites

- Node.js must already be installed in the environment where you wish to install the driver.
- You need to be able to run the `node` and `npm` commands.
- Depending on your environment, you may need `sudo` privileges.

For a list of the operating systems supported by Snowflake clients, see [Operating system support](/release-notes/requirements#label-client-operating-system-support).

## Installing the driver

The Node.js driver (`snowflake-sdk`) is available directly from `npm`.

To install the driver, open a terminal window and type the following command:

> Copy code
>
> ```
> npm install snowflake-sdk
> ```

The command downloads and installs the Snowflake Node.js driver. The driver should now appear in your `node_modules` directory and
you should be able to use the driver using `require('snowflake-sdk')`.
