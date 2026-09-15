# Dependency management policy for the Python Connector

The Snowflake Connector for Python depends on third party libraries, all of which are essential for communicating with the
Snowflake database. Although we intend to make dependency management easy and reliable, each library can introduce changes that
might result in unexpected behavior in the Snowflake Connector for Python or cause conflicts with other libraries.

This topic covers the following information:

- The policy for determining how the dependent library versions are selected as requirements for the Snowflake Connector for
  Python.
- The process for handling incidents that might occur as a result of changes in the dependent libraries.

## Policy for determining dependency requirements

The Snowflake Connector for Python sets dependency requirements according to the following rules:

- If the Snowflake Connector for Python directly refers to a package, the name of that package is included in the list of
  dependencies.
- For each dependent library, the requirements specify both the lower bound and upper bound versions of the library.

  - The lower bound version (the minimum version) is the earliest version used to verify that the library worked.
  - The upper bound version (the first version that is not supported) is the next major version.

    If a minor version introduces a change that breaks compatibility, the upper bound version will be set to that minor version.

  This provides a stable environment in which the connector can be tested with specific versions of the dependent libraries.

Note

These rules are based on the assumption that all packages, including the Snowflake Connector for Python, follow the
semantic versioning guidelines. According to these guidelines, a minor or patch version of a library
should not introduce any API changes.

For more information, see the [semantic versioning guidelines](https://semver.org/)..

## Handling incidents resulting from changes to dependent libraries

Although the dependency management policy is designed to minimize the effects of changes made in dependent libraries, incidents
can occur under unexpected conditions. This section discusses how each case is handled.

### Case 1. A dependent library introduces a change in API or behavior

If an incident occurs because a new version of a dependent library introduced a change to their API (and/or behavior), we will
release a new version of the Snowflake Connector for Python that excludes the new version of the dependent library from the range
of supported versions. We will make this change at the earliest opportunity. (Snowflake will make a best effort to address the
issue in the next release.)

For example, suppose that the requirements file specifies this range of versions for the dependent library `package1`:

Copy code

```
package1>=1.0,<2.0
```

In theory, the API should not change in any versions released within this range. However, if a change in version 1.3 breaks
compatibility, the upper bound version will be changed to exclude version 1.3 and later versions:

Copy code

```
package1>=1.0,<1.3
```

This change is intended to be a temporary solution to the problem. Once the issue has been resolved, we will change the upper
bound version back to the next major version of the library.

### Case 2. A dependent library introduces a new version greater than the upper bound

In this case, after we verify that the Snowflake Connector for Python works with the new version of the library, we’ll include the
new version in the range of supported versions for the next release of the Snowflake Connector for Python. For example, suppose
that the requirements file specifies this range of versions for the dependent library `package1`:

Copy code

```
package1>=1.0,<2.0
```

If `package1` version 2.0 is released, the new version cannot be used with the Snowflake Connector for Python because the
version is out of the range of required versions. We have automated tests that detect this case.

Note that if there are critical reasons for supporting this new version of the library (for example, if the new version includes a
security patch), we’ll make a best effort to release the updated Snowflake Connector for Python in the next release after the
incident is reported.
