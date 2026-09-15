# May 14, 2025: Data Governance release notes

## Automatic propagation of user-defined tags (*General availability*)

You can now configure an object tag so it is automatically propagated from a source object to target objects, which streamlines tag
management across objects and ensures that data protection policies associated with tags get consistently applied to target objects.

Tags can be configured to propagate in the following scenarios:

- When a target object depends on a source object (for example, a view based on a tagged table). Tags propagated to target objects that
  depend on a source object are continuously updated as the tags change on the source object.
- When data moves from a source object to another object (for example, using an INSERT statement that uses a query to update a table with
  data from another table).

For more information, see [Automatic tag propagation with user-defined tags](/user-guide/object-tagging/propagation).
