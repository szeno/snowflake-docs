# SnowConvert AI - PostgreSQL & Based Languages Conversion Settings

This topic applies to the following sources:

- PostgreSQL
- Amazon Redshift
- Greenplum
- Netezza

## Prepare Code Settings

[![Prepare Code Settings page](/static/images/migrations/sc-assets/Postgresql-Prepare-Code.png "image")](/static/images/migrations/sc-assets/Postgresql-Prepare-Code.png)

### **Description**

**Prepare my code:** Flag to indicate whether the input code should be processed before parsing and transformation. This can be useful to improve the parsing process. By default, it’s set to FALSE. When this flag is active, a new folder called `source_processed` will be generated and used for the migration.

Searches the input code for routine bodies using literals as definition delimiters. This is a non-standard PostgreSQL specific grammar that allows the user to define a procedure body using single quotes as delimiters. To facilitate SnowConvert AI transformation, the arrange step will transform these occurrences into standard procedure bodies, using `$$` as delimiters. Also, it will change dollar-quoted literals to regular single-quoted literals. All these changes will produce semantically equivalent code.

### **Example**

#### **Input**

Copy code

```
CREATE OR REPLACE PROCEDURE proc1 (x varchar default 'pigs')
LANGUAGE plpgsql
AS
'
begin
    --test
   insert into tabletest2 values (`Dianne''s pigs`);
   x = ''Diannes pigs'';
end;
';
```

#### **Output**

Copy code

```
CREATE OR REPLACE PROCEDURE proc1 (x varchar default 'pigs')
LANGUAGE plpgsql AS $$
begin
    --test
   insert into tabletest2 values ('Dianne''s pigs');
   x = 'Diannes pigs';
end;
 $$;
```
