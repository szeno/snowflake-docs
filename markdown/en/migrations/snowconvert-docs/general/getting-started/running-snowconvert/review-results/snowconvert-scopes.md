# SnowConvert AI - Scopes

## Scope definitions

### Submitted Scope

Every single file in the input path is considered the *Submitted Scope.* However, there can be files with unrecognized extensions or unsupported encodings that will not be processed by SnowConvert AI. Even though the assessment documents provide the list of excluded files, their content is not parsed (recognized).

For more information about unrecognized extensions and unsupported encodings, see the [Validation section](../validation/README).

### Assessment Scope

The portion of the Submitted Scope that is seen as valid by SnowConvert AI is considered the *Assessment Scope, that is* all files with recognized extensions and supported encodings. SnowConvert AI will try to parse every single file in this scope in order to be able to provide assessment information.

### Conversion Scope

There can be elements within the Assessment Scope that are not part of the conversion scope. SnowConvert AI classifies specific top-level code units as out-of-scope for multiple reasons, such as:

- they are not relevant in Snowflake
- there is no comparable code unit in Snowflake
- the code unit definition is not readable (ex: encrypted)
- the code unit definition is in a not supported programming language (ex: java)

Lines of code of code units out of the conversion scope will not be used to calculate conversion rates, but they will be used to provide some information in the assessment documents. For example, a Database Link object in Oracle is considered out of scope, however, references made to this object are still counted and reported in the [Object References Report](reports/object-references-report).

The following is the list of Code Units per language considered out of the conversion scope.

#### Teradata out-of-conversion scope code units

- Triggers
- Grants
- Functions or procedures with unsupported language

#### Oracle out-of-conversion scope code units

- Triggers
- Grants
- DB Links
- Wrapped Objects
- Functions or procedures with unsupported languages

#### Transact SQL out-of-conversion scope code units

- Triggers
- Grants

#### Redshift out-of-conversion scope code units

- Grants
