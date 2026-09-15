# Oracle - Wrapped objects

Input code can contain wrapped objects depending on the extraction tool used to produce it. Encrypted code will be exported as a “nonsense” group of characters which are preceded with the “wrapped” word. We call these blocks wrapped objects, they may run in Oracle but won’t be transformed.

This wrapped code can cause **low conversion rates** in the tool because for now, the migrator tries to recognize those blocks and comment out the entire object. This code is considered not supported and will affect the conversion rate negatively.

The following objects can appear wrapped:

- Functions
- Procedures
- Packages
- Package bodies
- Types
- Type bodies

This is how the source code may look like (sometimes with thousands of lines of code):

Copy code

```
CREATE OR REPLACE PACKAGE BOOKS_ADMIN.PKG_2 wrapped
a000000
b2
abcd
abcd
abcd
abcd
abcd
abcd
abcd
abcd
abcd
abcd
abcd
abcd
abcd
abcd
abcd
9
78 ba
ob/kXtqN74HGC6XDBIra6MlzY6Awg5m49TOf9b9c56Wf0HgJuHQrjwb1mYHHywjS/l6mf3Qq
5OYQspR6c+ZxVUzWIZSscYTm1uRwz/bR/6nKqhfqnFDKDvNnp2tgdQvIa+HIuDO4dAlLwlxp
lgxH+pYJWqEuDFbXPsyxoIvAgcctyaamw2YsCg==

/
```

And this is how the output should look:

Copy code

```
----** SSC-OOS - OUT OF SCOPE CODE UNIT. Wrapped PACKAGE IS OUT OF TRANSLATION SCOPE. **
--CREATE OR REPLACE PACKAGE BOOKS_ADMIN.PKG_2 wrapped
--a000000
--b2
--abcd
--abcd
--abcd
--abcd
--abcd
--abcd
--abcd
--abcd
--abcd
--abcd
--abcd
--abcd
--abcd
--abcd
--abcd
--9
--78 ba
--ob/kXtqN74HGC6XDBIra6MlzY6Awg5m49TOf9b9c56Wf0HgJuHQrjwb1mYHHywjS/l6mf3Qq
--5OYQspR6c+ZxVUzWIZSscYTm1uRwz/bR/6nKqhfqnFDKDvNnp2tgdQvIa+HIuDO4dAlLwlxp
--lgxH+pYJWqEuDFbXPsyxoIvAgcctyaamw2YsCg==

/
```

The objects recognized as wrapped, are being counted in the assessment reports. Find a total wrapped objects count in the second page of the Assessment.docx report:

[![](/static/images/migrations/sc-assets/Screenshot2024-02-07at2.37.49PM.png)](/static/images/migrations/sc-assets/Screenshot2024-02-07at2.37.49PM.png)

Also, you can find counts for each specific wrapped object that was recognized in the corresponding statement section:

[![](/static/images/migrations/sc-assets/Screenshot2024-02-07at2.15.45PM.png)](/static/images/migrations/sc-assets/Screenshot2024-02-07at2.15.45PM.png)

As a user of the tool you may want to:

- Decrypt and extract the objects again from your database.
- Remove these objects from your source code.
- No actions. Objects should be assessed and commented out, but the conversion rate may drop.
