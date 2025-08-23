# Kaspersky Security Center database tables parser | KSC DBMS | ALTS
The script is intended for parsing of resulting files (all_tables_sizes)
### Demo
[![UI-demo.gif](https://i.postimg.cc/3Ng44jY1/UI-demo.gif)](https://postimg.cc/QKdxvTBK)

## Fast start
### How to launch application
1) load the project, put all the files in a single directory;
2) install Python 3.13 or higher (if absent);
3) open the administration console (CMD), enter the commands:

> pip install -r requirements.txt

> cd [The path to the catalog where Source.zip files]

Console version:
> Python main.py

User interface version:
> Python gui.py

### The data is presented as follows:
<details>
  <summary>Click to open</summary>
  
- DB Type
- Updates
- DB Name
- Creator
- Creation date

- Current Volume
- Maximal Volume

- [Table] Tables in size (MB)
- [Table] Events stored in the database

- Events count
</details>

### Pars the resulting files from the following DBMS:
- Microsoft SQL (MSSQL)
- PostgreSQL
- MariaDB
- MySQL

## How to get result.xml files
### The resulting files are unloading information from the Kaspersky Security Center database
### To obtain files you need::
- Download .sql-files [all_tables_sizes](https://media.kaspersky.com/utilities/CorporateUtilities/all_tables_sizes.zip) for creating request to DBMS 
- Through the utility [klsql2](https://support.kaspersky.com/ksc/15.1/151343?page=help)


### An example of a request for a KSC database (MSSQL) via KLSQL2:
> cd "C:\Program Files (x86)\Kaspersky Lab\Kaspersky Security Center"

> > .\klsql2 -i all_tables_sizes_mssqlsrv.sql -o result.xml
