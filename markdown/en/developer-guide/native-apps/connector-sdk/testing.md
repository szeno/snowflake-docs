# Testing native connectors

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

Native SDK for connectors uses tests on 3 different levels:

- unit tests
- integration tests
- application tests

These unit tests are not different from unit tests for any other application. Parts of the system are mocked up to easily manipulate their returned values.
The `connectors-native-sdk-test` library, which as a library bundled with the SDK provides useful `InMemory` mockups of some classes responsible for communication with Snowflake.
It enables the developer to write and run unit tests on the local environment without a need to use any Snowflake connection.

Integration tests require a connection to Snowflake and run queries against Snowflake objects. However, the used database objects are stand-alone in these kinds of tests.
Keep in mind some Snowflake features may be unavailable in the context of Native Apps.

Application tests are tests that run on a native app deployed into Snowflake.
These kinds of tests are quite time-consuming and might be costly, so the recommendation is to test only some main scenarios this way.

Overall, the recommendation is to test as many cases as possible using unit tests and minimize the number of integration and application tests to the most critical paths.

## Testing library

As mentioned above the Native SDK has a `connectors-native-sdk-test` library, which provides various features useful in tests. The main features are:

- custom assertions
- in-memory implementations
- test builders

### Assertions

Assertions provided in the library are based on the [AssertJ fluent assertions](https://assertj.github.io/doc/).
All the assertions provided have a fabrication method implemented inside the `NativeSdkAssertions` class, furthermore,
this class inherits all of the original AssertJ fabrication methods, so only one import is needed to use both custom and base assertions.

The list of provided assertions:

- `TestConfigAssert`
- `IngestionProcessAssert`
- `IngestionRunAssert`
- `ConnectorResponseAssert`
- `FullConnectorStatusAssert`
- `ResourceIngestionDefinitionAssert`
- `ResponseMapAssert`
- `TestStateAssert`
- `TaskAssert`
- `TaskPropertiesAssert`
- `VariantAssert`

### Mockups

The mockups used inside the library are using an in-memory map under the hood to mock up the data stored inside database table.
They can be used like in the example below:

Copy code

```
var customResourceRepository = new InMemoryDefaultResourceIngestionDefinitionRepository();
var key = "test_key";

var resource = createResource(key);
customResourceRepository.save(resource);

var result = customResourceRepository.fetch(key);
```

Copy code

```
var table = new InMemoryDefaultKeyValueTable();
var repository = new DefaultConfigurationRepository(table);
var connectorService = new DefaultConnectorConfigurationService(repository);
```

List of provided in memory objects:

- `InMemoryResourceIngestionDefinitionRepository`
- `InMemoryIngestionProcessRepository`
- `InMemoryAppendOnlyKeyValueTable`
- `InMemoryDefaultKeyValueTable`
- `InMemoryReadOnlyKeyValueTable`
- `InMemoryConnectorErrorHelper`
- `InMemoryTaskRef`
- `InMemoryTaskRepository`

List of provided in memory task reactor objects:

- `InMemoryCommandsQueueRepository`
- `InMemoryConfigRepository`
- `InMemoryWorkSelector`
- `InMemoryExpiredWorkSelector`
- `InMemoryWorkItemQueue`
- `InMemoryInstanceRegistryRepository`
- `InMemoryWorkerQueue`
- `InMemoryWorkerQueueManager`
- `InMemoryWorkerRegistry`
- `InMemoryWorkerStatusRepository`
- `InMemoryWorkerCombinedView`
- `InMemoryConfiguredTaskReactorExistenceVerifier`
- `InMemoryNotConfiguredTaskReactorExistenceVerifier`
- `InMemoryTaskReactorInstanceComponentProvider`

### Test builders

Test builders are helper objects similar to the `Builders` used when customizing SDK components.
However, they expose all of the internal services to override.
For more information on using `Builders` check customization documentation.

Copy code

```
new ConfigureConnectorHandlerTestBuilder()
                .withErrorHelper(mock(ConnectorErrorHelper.class))
                .withInputValidator(mock(ConfigureConnectorInputValidator.class))
                .withCallback(mock(ConfigureConnectorCallback.class))
                .withConfigurationService(mock(ConnectorConfigurationService.class))
                .withStatusService(mock(ConnectorStatusService.class))
                .build();
```
