# Nov 19, 2026: Code Bundles (*General availability*)

Code Bundles are now generally available and are no longer in [Preview](/release-notes/preview-features). Code Bundles let you package
non-SQL code, like Python, Java, or Scala, and run it on Snowflake warehouses or compute pools with a single `EXECUTE CODE BUNDLE` command,
without building containers or wrapping logic in stored procedures. You can create, run, schedule, and monitor Code Bundles from SQL,
tasks, Snowsight, the REST API, the Python API, and the Snowflake CLI, including Spark jobs and ML Jobs. For more information, see
[Snowflake Code Bundles](/developer-guide/code-bundles/code-bundles).

`DEFINE CODE BUNDLE` and [project assets](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-project-assets) in
DCM Projects are also generally available. You can declare Code Bundles and their source files in DCM Projects definition files and manage the
bundle lifecycle across environments. For more information, see
[Code Bundle](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-object-type-code-bundle) and
[DEFINE CODE BUNDLE](/sql-reference/sql/create-code-bundle#label-define-code-bundle-syntax).
