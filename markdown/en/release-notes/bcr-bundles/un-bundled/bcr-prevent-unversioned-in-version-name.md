# Snowflake Native App Framework Cannot use “UNVERSIONED” as the prefix of a version label

Beginning with the **7.40** release, applications installed from staged files will use the string “UNVERSIONED” as the version name.
This means that providers will not be able to create a version name using “UNVERSIONED” as a prefix.

Before the change:
:   Providers can begin a version name with “UNVERSIONED” as a prefix.

After the change:
:   Providers can no longer begin a version name with “UNVERSIONED” as a prefix.

    Attempts to use “UNVERSIONED” in the version name will result in an error.

Ref: n/a
