# Snowflake Native App Framework Changes to the version output for the SHOW APPLICATIONS and DESC APPLICATION commands

For applications [created using staged files](/developer-guide/native-apps/installing-testing-application#label-native-apps-application-creating-stage),
the output of the [SHOW APPLICATIONS](/sql-reference/sql/show-applications) and
[DESCRIBE APPLICATION](/sql-reference/sql/desc-application) will change as follows:

Before the change:
:   The value of the `version` column of the [SHOW APPLICATIONS](/sql-reference/sql/show-applications) command
    is `dev_stage`.

    The value of the `version` row of the [DESCRIBE APPLICATION](/sql-reference/sql/desc-application) command
    is `dev_stage`.

After the change:
:   The value of the `version` column of the [SHOW APPLICATIONS](/sql-reference/sql/show-applications) command
    will be `UNVERSIONED`.

    The value of the `version` row of the [DESCRIBE APPLICATION](/sql-reference/sql/desc-application) command
    is `UNVERSIONED`.

Ref: n/a
