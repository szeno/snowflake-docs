# Working with entities

Entities organize feature views by subject matter so that users can more easily find the feature views they need.
For example, a feature store for a video streaming service might define entities for users and movies. Each feature view in the feature store
is tagged as related to movies or to users, or to both, and you can retrieve a list of feature views related to these entities.

In addition to helping to organize feature views, entities store the names of the key columns you can use to join the
extracted features back to the original data.

## Creating an entity

To create a new entity and register it in a feature store, use the feature store’s `register_entity` method. Here,
`fs` is the feature store instance (see [Creating or connecting to a feature store](/developer-guide/snowflake-ml/feature-store/create)).

Copy code

```
from snowflake.ml.feature_store import Entity

entity = Entity(
    name="MY_ENTITY",
    join_keys=["UNIQUE_ID"],
    desc="my entity"
)
fs.register_entity(entity)
```

## Listing entities

To see the registered entities in your feature store, use the feature store’s `list_entities` method, which
returns a Snowpark DataFrame. (`fs` is the feature store instance; see [Creating or connecting to a feature store](/developer-guide/snowflake-ml/feature-store/create).)

Copy code

```
fs.list_entities().show()
```

## Retrieving an entity

You can retrieve a registered entity using the feature store’s `get_entity` method; for example, to obtain its join keys.

Copy code

```
entity = fs.get_entity(name="MY_ENTITY")
print(entity.join_keys)
```

## Modifying an entity

You can update an entity’s description using the feature store’s `update_entity` method:

Copy code

```
fs.update_entity(
    name="MY_ENTITY",
    desc="NEW DESCRIPTION"
)
```

Other aspects of the entity, such as its join keys, are immutable. To change these, create a new entity.

## Deleting an entity

You can delete an entity using the feature store’s `delete_entity` method.

Copy code

```
fs.delete_entity(name="MY_ENTITY")
```

Entities that are referenced by any feature view cannot be deleted.

## Known limitations

- Entities are implemented as tags and are subject to the limit of [10,000 tags per account](/sql-reference/sql/create-tag#label-create-tag-usage-notes)
  and [50 unique tags per object](/user-guide/object-tagging/introduction#label-object-tagging-quota).
