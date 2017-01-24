# README

## Task description

Please go through the described scenario and write 2 scripts, one in Windows Batch and one in Unix BASH implementing a fix to the issue below. For the development of the scripts you have 24h and are allowed to use Google and any other material as long as the work submitted was written by you.

#### Disclaimer: I wrote Batch version in Python, why? It's 2017...

### Use Case: 

* A database upgrade requires the execution of numbered scripts stored in a folder. E.g. 045.createtable.sql

* There may be holes in the numbering and there isn't always a . after the number.

* The database upgrade works by looking up the current version in the database. It then compares this number to the scripts.

* If the version number from the db matches the highest number from the script then nothing is executed.

* If the number from the db is lower than the highest number from the scripts, then all scripts that contain a higher number than the db will be executed against the database.

* In addition the database version table is updated after the install with the latest number.


## How to use it?

You'll need to create a new database with sample tables.
I've prepared a `db_seed.sql` that will do this for you.

Just run

```sh
mysql -u root -p < sql/db_seed.sql
```

It will create a new user **karol** with password **test123** it will also create a new database called **testdb** and create 2 tables.

From that point `db_upgrade.sh` script should work out-of-the-box.

### Example

```sh
→ mysql -u root < sql/db_seed.sql
→ mysql -u karol -ptest123 testdb < sql/01.add_new_user.sql
→ ./upgrade_db.sh
You need to be a root to run this script!
→ sudo ./upgrade_db.sh
Password:
Migration already in schema 01.add_new_user.sql
Adding migration: 05edit_old_user.sql
Adding migration: 06_add_10_new_users.sql
Adding migration: 10-remove_user_with_id-4.sql
Adding migration: 153-remove_user_with-id-5.sql
```

### Windows
Please change your MySQL path in line **15** and **39** (python script) - In my case I've used MySQL 5.6.