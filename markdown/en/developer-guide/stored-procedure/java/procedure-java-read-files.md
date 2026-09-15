# Reading files with a Java stored procedure

You can read the contents of a file with handler code. The file must be on a Snowflake stage that’s available to your handler.
For example, you might want to read a file to process unstructured data in the handler.

To read the contents of staged files, your handler can call methods in either the `SnowflakeFile` class or the `InputStream`
class. You might do this if you need to access the file dynamically during compute. For more information, see
[Reading a dynamically-specified file with](#label-reading-file-snowflakefile-java) or [Reading a dynamically-specified file with](#label-reading-file-inputstream-java) in this topic.

`SnowflakeFile` provides features not available with `InputStream`, as described in the following table.

| Class | Input | Notes |
| --- | --- | --- |
| `SnowflakeFile` | URL formats:   - Scoped URL to reduce the risk of file injection attacks when the function’s caller is not also its owner. - File URL or string path for files that the procedure owner has access to.   The file must be located in a named internal stage or an external stage. | Easily access additional file attributes, such as file size. |
| `InputStream` | URL formats:   - Scoped URL to reduce the risk of file injection attacks when the function’s caller is not also its owner.   The file must be located in a named internal stage or an external stage. |  |

Expand

Show lessSee more

## Reading a dynamically-specified file with `SnowflakeFile`

Code in the following example has a handler function `execute` that takes a `String` and returns a `String`
with the file’s contents. At run time, Snowflake initializes the handler’s `fileName` variable from the incoming file path in the
procedure’s `input` variable. The handler code uses a `SnowflakeFile` instance to read the file.

Copy code

```
CREATE OR REPLACE PROCEDURE file_reader_java_proc_snowflakefile(input VARCHAR)
RETURNS VARCHAR
LANGUAGE JAVA
RUNTIME_VERSION = 11
HANDLER = 'FileReader.execute'
PACKAGES=('com.snowflake:snowpark:latest')
AS $$
import java.io.InputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import com.snowflake.snowpark_java.types.SnowflakeFile;
import com.snowflake.snowpark_java.Session;

class FileReader {
  public String execute(Session session, String fileName) throws IOException {
    InputStream input = SnowflakeFile.newInstance(fileName).getInputStream();
    return new String(input.readAllBytes(), StandardCharsets.UTF_8);
  }
}
$$;
```

Code in the following CALL example creates a scoped file URL that points to the file. This is an encoded URL that permits temporary
access to a staged file without granting privileges to the stage itself.

Copy code

```
CALL file_reader_java_proc_snowflakefile(BUILD_SCOPED_FILE_URL('@sales_data_stage', '/car_sales.json'));
```

Note

For an owner’s rights stored procedure, the procedure’s owner must have access to any files that are not scoped URLs. For caller’s rights
procedures, the caller must have access to any files that are not scoped URLs. In either case, you can read the staged file by having the
handler code call the `SnowflakeFile.newInstance` method with a `boolean` value for a new `requireScopedUrl` parameter.

The following example uses `SnowflakeFile.newInstance` while specifying that a scoped URL is not required.

Copy code

```
String filename = "@my_stage/filename.txt";
SnowflakeFile sfFile = SnowflakeFile.newInstance(filename, false);
```

## Reading a dynamically-specified file with `InputStream`

Code in the following example has a handler function `execute` that takes an `InputStream` and returns a `String`
with the file’s contents. At run time, Snowflake initializes the handler’s `stream` variable from the incoming file path in the
procedure’s `input` argument. The handler code uses the `InputStream` to read the file.

Copy code

```
CREATE OR REPLACE PROCEDURE file_reader_java_proc_input(input VARCHAR)
RETURNS VARCHAR
LANGUAGE JAVA
RUNTIME_VERSION = 11
HANDLER = 'FileReader.execute'
PACKAGES=('com.snowflake:snowpark:latest')
AS $$
import java.io.InputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import com.snowflake.snowpark.Session;

class FileReader {
  public String execute(Session session, InputStream stream) throws IOException {
    String contents = new String(stream.readAllBytes(), StandardCharsets.UTF_8);
    return contents;
  }
}
$$;
```

Code in the following CALL example creates a scoped file URL that points to the file. This is an encoded URL that permits temporary
access to a staged file without granting privileges to the stage itself.

Copy code

```
CALL file_reader_java_proc_input(BUILD_SCOPED_FILE_URL('@sales_data_stage', '/car_sales.json'));
```
