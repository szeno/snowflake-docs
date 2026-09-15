# Snowpark Migration Accelerator: Known Issues

- There are some scenarios that are not properly supported in order to resolve symbols for assessment reports and mappings.
- Partial support for Companions, Case Classes, Generic classes with multiple type parameters.
- Lack of support of Generic Functions, Lambdas with multiple parameters.
- Partial support for Equivalence of types, currently all primitive types are fully supported, but user types that involve inheritance don’t.
- There is a minor issue at the migrated code, related with formatting (pretty-printing) of the scala code. Some newlines or indentations are not preserved exactly as the original code.
- Lack of support of migration for Embedded Sql queries.
- Partial support of Spark symbols libraries. See documentation for detail of what is currently supported.
- There might be issues when using third party libraries, due to having not supported elements (described below).
