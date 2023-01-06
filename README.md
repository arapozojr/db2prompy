# db2prompy
> Simple command line interpreter application for Db2

Db2 Command line interpreter in Python that opens a connection with a Db2 database (setting its own "Application Name" for Db2), and allows to execute SQL files, roll back or commit transactions.

Good if you want to run some tests for Db2 workload manager.

## Running in Docker

Clone this repo:

```shell
git clone https://github.com/arapozojr/db2prompy.git
cd db2prompy/
```

Create .env file with connection parameters:

```shell
cat << EOF > .env
DB_HOST=...
DB_PORT=...
DB_NAME=...
DB_USER=...
EOF
```

Create a sample SQL file in [sqls/](sqls/) directory

```shell
cat << EOF > sqls/hello.sql
SELECT 'HELLO WORLD' FROM SYSIBM.SYSDUMMY1
EOF
```

Build Docker image:

```shell
docker build -t db2prompy .
```

Run it:

```shell
docker run --rm -it -v "$PWD/sqls:/app/sqls:ro" --env-file .env db2prompy
```
