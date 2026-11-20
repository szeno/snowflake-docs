# Build a Node.js app

Snowflake App Runtime runs Node.js apps on Node.js 22. Start from the Next.js
template, or bring the framework and stack you already use, such as Express,
Fastify, or your own Next.js app.

## Start from the Next.js template

The template comes configured for App Runtime, with Snowflake data
access through the
[Node.js SDK](/developer-guide/snowflake-app-runtime/nodejs-sdk). Create an app
from it in any of these ways:

- **Snowsight Workspaces** (Public Preview): select **+ Add new** »
  **Next.js App**.
- **Cortex Code**: describe the app with the
  [`snowflake-apps`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-snowflake-apps)
  skill.

For each step through deploy, see
[Get started with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/getting-started).

## Bring your own framework

Any Node.js app runs on App Runtime if it can be installed and built with
commands and serves HTTP on the address App Runtime gives it. You need the
[Snowflake CLI](/developer-guide/snowflake-cli/installation) with a
[connection](/developer-guide/snowflake-cli/connecting/configure-connections),
and Node.js 22 or later on your machine.

1. From the project directory, generate an
   [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml) manifest:

   Copy code

   ```
   snow app setup
   ```
2. Add the commands that install, build, and run the app. The build runs only
   the commands you declare. See the examples for
   [Next.js](#label-snowflake-app-runtime-build-nodejs-app-nextjs) and
   [other frameworks](#label-snowflake-app-runtime-build-nodejs-app-other).
3. Have the server listen on the `PORT` and `HOSTNAME` that App Runtime sets.
   See [Listen address](/developer-guide/snowflake-app-runtime/runtime-environment#label-runtime-environment-listen-address).
4. Deploy the app, then open it:

   Copy code

   ```
   snow app deploy
   snow app open
   ```

### Next.js

In `next.config.*`, set `output: "standalone"`. App Runtime runs the standalone
server that Next.js builds, and that server already reads `PORT` and
`HOSTNAME`. Add these commands to `app.yml`:

Copy code

```
install:
  commands:
    - [npm, ci]
build:
  commands:
    - [npm, run, build]
    - [cp, -r, .next/static, .next/standalone/.next/static]
    - [cp, -r, public, .next/standalone/public]
    - [rm, -rf, node_modules]
run:
  command: [node, .next/standalone/server.js]
```

The standalone output doesn’t include static assets, so the `cp` commands copy
them in. Without them, static files return 404 after deploy. Omit the `public`
line if the project has no `public/` directory. The `rm` command keeps the root
`node_modules` out of the deployed app, because the standalone output has its
own.

To preview the app in [Snowsight Workspaces](/developer-guide/snowflake-app-runtime/workspaces),
keep the `dev` script in `package.json` that runs `next dev`.

### Express and other frameworks

For Express, Fastify, or another Node.js server, install dependencies and run
the entry point. Add a `build` command only if the app has a build step.

This Express app deploys as is. Create three files in an empty directory:

`package.json`:

Copy code

```
{
  "name": "hello-express",
  "private": true,
  "dependencies": { "express": "^4.21.2" }
}
```

`server.js` listens on the `PORT` and `HOSTNAME` that App Runtime sets:

Copy code

```
const express = require("express");

const app = express();
app.get("/", (req, res) => res.send("Hello from Express on Snowflake App Runtime"));

const port = Number(process.env.PORT ?? 8080);
const hostname = process.env.HOSTNAME ?? "0.0.0.0";
app.listen(port, hostname);
```

`app.yml`:

Copy code

```
version: 2
name: HELLO_EXPRESS
database: SNOWFLAKE_APPS
schema: PUBLIC
query_warehouse: SNOWFLAKE_APPS_QUERY_WH

ignore:
  - node_modules

install:
  commands:
    - [npm, ci]
run:
  command: [node, server.js]
```

`npm ci` needs a `package-lock.json`, so run `npm install` once before you
deploy. Then deploy and open the app:

Copy code

```
npm install
snow app deploy
snow app open
```

Replace `database`, `schema`, and `query_warehouse` with your own, or run
`snow app setup` to fill them in from your account’s defaults.

## Query Snowflake

Install the [Node.js SDK](/developer-guide/snowflake-app-runtime/nodejs-sdk)
and call it from server code: server components, route handlers, and server
actions.

Copy code

```
npm install @snowflake/sar-sdk
```

For owner’s and caller’s rights queries, see
[Query Snowflake from a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/query-snowflake).

## Run locally

Run `npm run dev`. On your machine, the SDK uses the default connection in your
Snowflake CLI configuration, and caller’s rights queries run as that
connection’s user.

## Next steps

- Deploy more than one way from one project:
  [Deploy targets for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/deploy-targets).
- Run an app on serverless compute:
  [Serverless compute for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/serverless).
- Share the app with other roles:
  [Share a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/access-control).
