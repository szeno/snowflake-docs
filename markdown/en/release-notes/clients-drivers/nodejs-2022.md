# Node.js Driver release notes for 2022

This article contains the release notes for the Node.js Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Node.js Driver updates.

See [Node.js Driver](/developer-guide/node-js/nodejs-driver) for documentation.

## Version 1.6.17 (December 14, 2022)

### New Features

- Fixed an issue where supplying an incorrect password could cause an infinite loop when attempting to log into a
  connection pool.
- Added the `arrayBindingThreshold` connection parameter for array binding, which directs the Node.js Driver
  to write an array to a file and upload it to the server when the number of binds exceeds the threshold.

## Version 1.6.16 (November 18, 2022)

### New Features

- Added a `noProxy` configuration parameter to support bypassing the proxy server when needed.
- Updated the moment library to version 2.29.4.

## Version 1.6.15 (October 28, 2022)

### New Features

- Removed the requirement to provide the original SQL query in addition to the requestId when resubmitting requests.
- Updated mocha to version 10.1.0.

## Version 1.6.14 (September 21, 2022)

### New Features

- Added support for array binding.

## Version 1.6.13 (August 23, 2022)

### Updates

- Added the ability to resubmit SQL statements with a request ID.

## Version 1.6.12 (June 25, 2022)

### Updates

- Added the `readme.md` file to the npm project description.
- Set the default timeout for HTTP requests to 360 seconds.

### Bug Fixes

- Fixed an issue regarding inaccurate encryption material IDs for numbers exceeding the maximum safe integer.

## Version 1.6.11 (June 23, 2022)

### Bug Fixes

- Fixed an issue for proxy connection not working.

## Version 1.6.10 (May 25, 2022)

### Bug Fixes

- Fixed an issue where the application configuration parameter was not being recognized.
- Fixed an issue where the PUT command did not overwrite data when the OVERWRITE argument was set to TRUE.
- Fixed an issue where the OKTA authenticator threw an error when the closing slash (“/”) was missing; now
  it authenticates whether or not the slash in provided.
- Fixed an issue where the OKTA authenticator failed to authenticate accounts that included a region in the
  connection string.

## Version 1.6.8 (Mar 17, 2022)

### Bug Fixes

- Updated “npm test” to run all unit tests.
- Added a confirmation message when a connection is authenticated.
- Updated `agent-base` and `https-proxy-agent` to latest version.

## Version 1.6.7 (Feb 16, 2022)

### Bug Fixes

- Updated the required version of the `follow-redirect` package to 1.14.18.
- Updated the version of the mocha test framework to 9.2.0.
