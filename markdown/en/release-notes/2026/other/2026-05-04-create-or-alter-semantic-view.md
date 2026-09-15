# May 04, 2026: CREATE OR ALTER SEMANTIC VIEW support (*Preview*)

You can now use [CREATE OR ALTER SEMANTIC VIEW](/sql-reference/sql/create-semantic-view#label-create-or-alter-semantic-view-syntax) to create a
[semantic view](/user-guide/views-semantic/overview) if it doesn’t exist, or alter an existing semantic view to match
the definition in the statement. This provides a declarative way to manage semantic view definitions that’s safe to re-run without
having to replace the view and re-grant privileges.

CREATE OR ALTER SEMANTIC VIEW supports modifying tables, relationships, facts, dimensions, metrics, comments, AI instructions,
and verified queries. Adding or changing tags isn’t supported. Existing tags are preserved.

For more information, see [Creating or altering a semantic view](/user-guide/views-semantic/sql#label-semantic-views-create-or-alter) and [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).
