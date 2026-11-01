# Oct 30, 2026: CREATE OR ALTER SECRET, DCM Projects DEFINE SECRET, and environment variables (*Preview*)

With this Public Preview release, you can use `DEFINE SECRET` in DCM Projects definition files to declaratively manage secrets. You can also declare environment variables and secrets in the DCM project manifest to supply values that stay out of your definition files, repository, and deployment artifacts. DCM Projects masks secret values in `PLAN` and `DEPLOY` changesets, deployment history artifacts, and logs. You can supply the values in Workspaces, from Snowflake CLI, or from SQL.

You can also use `CREATE OR ALTER SECRET` to create a secret if it doesn’t exist, or to alter an existing secret to match the definition in the statement.

For more information, see [Secret](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-object-type-secret), [Environment variables and secrets](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-env-vars-and-secrets), and [CREATE OR ALTER SECRET](/sql-reference/sql/create-secret#label-create-or-alter-secret-syntax).
