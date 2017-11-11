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
- cd /vagrant
- git clone https://github.com/cristianacmc/Log-Analysis.git
- cd Log-Analysis
- Bring the virtual machine online (with *vagrant up*) and then log into it with *vagrant ssh*.
- load the data: *psql -d news -f newsdata.sql*
- Connect to the database : psql news
- create the views listed in *Required code*
- Exit psql
- run python reporting.py

After that you need to load the data into your local database:
- cd into the vagrant directory *psql -d news -f newsdata.sql*

## Addictional Code

For this project I created 3 views to solve the querie **3**:

- View 1:
	create view access as select date(time) as tdate, count(*) as views from log GROUP BY date(time) ORDER BY date(time);

- View 2:
	create view lerrors as select date(time) as edate, count(*) as errors from log where status like '%4%' group by time::date order by date(time);

- View 3:
    create view percent as select lerrors.edate, cast(errors * 100 as double precision) / views as p from access, lerrors where access.tdate = lerrors.edate;

FYI: **You do not need to create these views in the psql console because it is already implemented in the script**

## Possible Errors

If the commands above give an error message such as:
- psql: FATAL: database "news" does not exist
- psql: could not connect to server: Connection refused

This means the database server is not running or is not set up correctly. If you have an older version of the VM configuration you need to download the virtual machine configuration into a new directory and start it from there.


