# Canceling the execution of a SQL statement

To cancel the execution of a statement, send a `POST` request to the cancel endpoint. See
[POST /api/v2/statements/{statementHandle}/cancel](/developer-guide/sql-api/reference#label-sql-api-reference-post-statements-cancel) for details.

Copy code

```
POST /api/v2/statements/{statementHandle}/cancel
```

The following flow chart illustrates the steps that you take to cancel a request.

> ![Flow chart for cancelling the execution of a statement](/static/images/sql-api-flow-chart-cancel.png)
