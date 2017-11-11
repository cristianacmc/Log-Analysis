# Logs Analysis


## Overview

The purpose of this project is to build a reporting tool to analyse data from the database in order to answer questions about the site's user activity.

The report needs to anwer the following questions:

- What are the most popular three articles of all time?
- Who are the most popular article authors of all time?
- On which days did more than 1% of requests lead to errors?

## Getting Started

In order to run this project, you need to follow these steps:

- Install virtual machine [VM](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and [Vagrant](https://www.vagrantup.com/)
- Download the file [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and unzip into the vagrant directory
- `cd /vagrant`
- `git clone` https://github.com/cristianacmc/Log-Analysis.git
- `cd Log-Analysis`
- Bring the virtual machine online (with `vagrant up`) and then log into it with `vagrant ssh`.
- load the data: `psql -d news -f newsdata.sql`
- Connect to the database : `psql news`
- Exit psql
- run `python reporting.py`

## Additional Code

For this project I created 3 views to solve the querie **3**:

- View 1:
```sql
	CREATE VIEW access AS
	SELECT date(time) AS tdate, count(*) AS views
	FROM log
	GROUP BY date(time)
        ORDER BY date(time);
```

- View 2:
```sql
	CREATE VIEW lerrors AS
	SELECT date(time) as edate, count(*) AS errors
	FROM log
	WHERE status like '%4%'
	GROUP BY time::date
	ORDER BY date(time);
```

- View 3:
```sql
    CREATE VIEW percent AS
    SELECT lerrors.edate, cast(errors * 100 as double precision) / views AS p
    FROM access, lerrors
    WHERE access.tdate = lerrors.edate;
```

FYI: **You do not need to create these views in the psql console because it is already implemented in the script**

## Possible Errors

If the commands above give an error message such as:
- psql: FATAL: database "news" does not exist
- psql: could not connect to server: Connection refused

This means the database server is not running or is not set up correctly. If you have an older version of the VM configuration you need to download the virtual machine configuration into a new directory and start it from there.


