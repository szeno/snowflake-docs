# Oct 27, 2026: Carry over comments, tags, and privileges with COPY = ( … )

The `COPY = ( ... )` parameter for CREATE OR REPLACE statements names the kinds of metadata to carry over from the object
being replaced onto its replacement, so you don’t need to restate it.

- `COPY = ( COMMENTS )` retains the object comment and the column comments of the replaced object. Previously, a
  CREATE OR REPLACE statement dropped any comment that the statement didn’t restate.
- `COPY = ( TAGS )` and `COPY = ( GRANTS )` request the same carry-over as the existing COPY TAGS and COPY GRANTS
  parameters.

You can name several kinds in one parameter, for example `COPY = ( COMMENTS, TAGS, GRANTS )`, and you can combine the
parameter with the COPY GRANTS and COPY TAGS parameters in the same statement.

For more information, see the [COPY = ( … )](/sql-reference/sql/create-table#label-create-table-copy-property) parameter.
