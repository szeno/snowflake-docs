# <classification\_profile\_name>!SET\_SNOWFLAKE\_SEMANTIC\_CATEGORIES

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Configures the classification profile to limit which types of data (semantic categories) to classify as sensitive. Snowflake
classifies data only if it belongs to the subset of [native semantic categories](/user-guide/classify-native) that you
specify using this method.

## Syntax

Copy code

```
<classification_profile_name>!SET_SNOWFLAKE_SEMANTIC_CATEGORIES( <array> )
```

## Arguments

`array`
:   An [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) value that specifies a list of Snowflake [native semantic categories](/user-guide/classify-native)
    (types of data) and optional locales to use for classification. Snowflake identifies data as sensitive only if the data is classified as
    belonging to the specified categories (and locales, if provided).

    The array can contain objects with the following keys:

    - `category` — Required string that specifies a native semantic category.
    - `country_codes` — Optional array that specifies two-letter country codes. Snowflake identifies data as belonging to a category
      only if a semantic subcategory exists for the specified locales.

      To determine if a semantic subcategory exists for a locale and obtain the two-letter code for a country, see
      [Native semantic categories of sensitive data classification](/user-guide/classify-native).

## Returns

Returns a successful status message or an error message.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Instance role | Object | Notes |
| --- | --- | --- |
| `classification_profile`!PRIVACY\_USER | The classification profile instance. | The account role that calls this method must be granted this instance role on the classification profile. The role used to create the instance is automatically granted this instance role. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
return value of this method. Instead, call each method in a separate SQL statement.

## Examples

Configure a classification profile so that data is classified only if it belongs to the NAME and NATIONAL\_IDENTIFIER semantic categories:

Copy code

```
CALL my_classification_profile!SET_SNOWFLAKE_SEMANTIC_CATEGORIES(
  [
    {'category': 'NAME'},
    {'category': 'NATIONAL_IDENTIFIER'}
  ]);
```

Configure a classification profile so that data is classified only if Snowflake identifies it as a tax identifier in Italy (IT) or France (FR):

Copy code

```
CALL my_classification_profile!SET_SNOWFLAKE_SEMANTIC_CATEGORIES(
  [
    {
      'category': 'TAX_IDENTIFIER',
      'country_codes': ['IT', 'FR']
    }
  ]);
```

Combine global semantic categories with country-specific categories:

Copy code

```
CALL my_classification_profile!SET_SNOWFLAKE_SEMANTIC_CATEGORIES(
  [
    {'category': 'NAME'},
    {
      'category': 'PASSPORT',
      'country_codes': ['US']
    }
  ]);
```
