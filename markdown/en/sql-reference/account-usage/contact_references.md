Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage)

# CONTACT\_REFERENCES view

This Account Usage view can be used to identify the associations between [contacts](/user-guide/contacts-using) and the objects to
which they have been added.

Contact lineage is not included in this view. For example, if a contact is associated with a schema, the view does not have records for
associations between the contact and all the tables in the schema even though the tables inherit the association from the schema.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| CONTACT\_DATABASE | VARCHAR | Name of the database in which the contact exists. |
| CONTACT\_SCHEMA | VARCHAR | Name of schema in which the contact exists. |
| CONTACT\_ID | NUMBER | Internal/system-generated identifier for the contact. |
| CONTACT\_NAME | VARCHAR | Name of a contact. |
| CONTACT\_PURPOSE | VARCHAR | Purpose that was specified when the contact was associated with the object. |
| OBJECT\_DATABASE | VARCHAR | Name of the database that contains the referenced object. If the object is not a database or schema object, the value is empty. |
| OBJECT\_SCHEMA | VARCHAR | Name of the schema that contains the referenced object. If the referenced object is not a schema object (for example, a warehouse), the value is empty. |
| OBJECT\_ID | NUMBER | Internal/system-generated identifier of the referenced object. |
| OBJECT\_NAME | VARCHAR | Name of the referenced object. |
| OBJECT\_DELETED | TIMESTAMP\_LTZ | Date and time when the referenced object was dropped or when its parent object was dropped. |
| OBJECT\_DOMAIN | VARCHAR | Type of the referenced object. |

Expand

Show lessSee more

## Usage notes

- Latency for the view is 2 hours.
