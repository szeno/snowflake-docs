# SHOW APPLICATIONS command: Changes to the LABEL column output

The output of the [SHOW APPLICATIONS](/sql-reference/sql/show-applications) command behaves as follows:

Before the change:
:   The value of the LABEL column for the APPLICATION object is `NONE` if no label is specified.

After the change:
:   The value of the LABEL column for the APPLICATION object will be empty if no label is specified.

Ref: n/a
