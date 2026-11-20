Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$VALIDATE\_CONSUMER\_ACCOUNT

Checks whether an account exists and is not a trial account, so that a listing provider can confirm the account is
valid before adding it to a listing as a listing consumer. The account is identified by its organization name and
account alias.

The function returns only a validity flag. It does not return any other account information.

## Syntax

Copy code

```
SYSTEM$VALIDATE_CONSUMER_ACCOUNT( '<org_name>.<account_alias>' )
```

## Arguments

`org_name.account_alias`
:   The name of the account to validate, in `ORG.ALIAS` format, for example `ORG1.ACCT1`. The name is matched
    case-insensitively.

## Returns

Returns a `VARCHAR` value that contains a JSON object with a single property, `is_valid`:

- `true` if the account exists and is not a trial account.
- `false` if the account does not exist, or if it is a trial account. A trial account is an account whose type is
  `TRIAL`, or an account that belongs to a trial organization.

## Access control requirements

The caller can’t be a trial account. If a trial account calls this function, Snowflake returns the same error that it
returns for an unknown function.

Other than the trial-account restriction, no privileges are required to call this function.

## Examples

Validate an account:

Copy code

```
SELECT SYSTEM$VALIDATE_CONSUMER_ACCOUNT('ORG1.ACCT1');
```

Example output:

Copy code

```
{
  "is_valid" : true
}
```
