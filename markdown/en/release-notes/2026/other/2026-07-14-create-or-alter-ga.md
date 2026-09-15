# Jul 14, 2026: CREATE OR ALTER is generally available for 24 object types

[CREATE OR ALTER](/sql-reference/sql/create-or-alter) is now generally available for 24 object
types. CREATE OR ALTER creates an object if it doesn’t exist, or modifies an existing object to
match the statement definition. It’s especially useful in declarative deployment workflows and
CI/CD pipelines where the same script must be safe to re-run.

For more information, see [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).
