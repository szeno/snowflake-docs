# Jul 15, 2026: Named key pair management for users

You can now use SQL to register, rotate, modify, and remove named [key pairs](/user-guide/key-pair-auth) for a user.
Each key pair has its own name and supports an optional role restriction and expiration time.

Named key pairs improve on the legacy approach of setting the `RSA_PUBLIC_KEY` and `RSA_PUBLIC_KEY_2` user
properties, which Snowflake continues to support.

For more information, see the following topics:

- [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth)
- [ALTER USER … ADD KEY PAIR](/sql-reference/sql/alter-user-add-key-pair)
- [ALTER USER … MODIFY KEY PAIR](/sql-reference/sql/alter-user-modify-key-pair)
- [ALTER USER … ROTATE KEY PAIR](/sql-reference/sql/alter-user-rotate-key-pair)
- [ALTER USER … REMOVE KEY PAIR](/sql-reference/sql/alter-user-remove-key-pair)
- [SHOW USER KEY PAIRS](/sql-reference/sql/show-user-key-pairs)
