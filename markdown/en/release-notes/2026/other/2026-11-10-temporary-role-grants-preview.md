# Nov 10, 2026: Temporary role grants to users (*Preview*)

You can now grant an account role to a user temporarily. When you run [GRANT ROLE](/sql-reference/sql/grant-role) to grant a role to a user, use
the `FOR INTERVAL` clause to specify how long the grant lasts, or the `UNTIL` clause to specify when it expires. When the grant expires,
the user automatically loses access through that grant, so you don’t need to revoke it yourself.

Copy code

```
GRANT ROLE oncall TO USER alice FOR INTERVAL '24 HOURS';
```

To set the expiration of an existing grant to exactly the value you specify, use the `RESET EXPIRATION` clause. The output of
[SHOW GRANTS](/sql-reference/sql/show-grants) and the [GRANTS\_TO\_USERS view](/sql-reference/account-usage/grants_to_users) include an
`expires_on` column that shows when each grant expires.

For more information, see [GRANT ROLE](/sql-reference/sql/grant-role).
