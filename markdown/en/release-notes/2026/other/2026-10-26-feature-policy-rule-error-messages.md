# Oct 26, 2026: Custom error messages for feature policy rules

With this release, a feature policy rule can include an `error_message` that explains why a statement was
blocked. When the rule blocks a statement, Snowflake adds the message to the error that the user sees, so you
can tell users what’s allowed instead.

Copy code

```
CREATE FEATURE POLICY require_permanent_tables
  AS $$
    blocked_creation_rules:
      - object_type: TABLE
        block_when: "$IS_TEMPORARY OR $IS_TRANSIENT"
        error_message: "Temporary and transient tables aren't allowed. Create a permanent table."
  $$;
```

For more information, see [Custom error messages](/user-guide/feature-policies#label-feature-policy-rules-error-message).
