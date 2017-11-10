#! /usr/bin/env python
import psycopg2

DBNAME = "news"


''' 1. What are the most popular three articles of all time? '''


def most_article():

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select articles.title, count(log.path) as views from articles, log \
        where log.path like '%'||articles.slug group by articles.title \
        order by views desc limit 3")
    rows = c.fetchall()

    print("***The most popular three articles of all time***")
    for row in rows:
        print("\" %s \" - %s views" % (row[0], row[1]))
    print(" \n ")

    db.close()

'''2. Who are the most popular article authors of all time? '''


def most_authors():

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select authors.name, count(log.path) as views from authors, log, \
        articles where log.path like '%'||articles.slug and articles.author = \
        authors.id group by authors.name order by views desc")
    rows = c.fetchall()

    print("***The most popular article authors of all time***")
    for row in rows:
        print("%s - %s views" % (row[0], row[1]))
    print(" \n ")

    db.close()


'''3. On which days did more than 1% of requests lead to errors? '''


def percent_errors():

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    c.execute("create view access as select date(time) as tdate, count(*) as views \
        from log GROUP BY date(time) ORDER BY date(time)")
    c.execute("create view lerrors as select date(time) as edate, count(*) as errors from \
        log where status like '%4%' group by time::date order by date(time)")
    c.execute("create view percent as select lerrors.edate, cast(errors * 100 \
        as double precision) / views as p from access, lerrors \
        where access.tdate = lerrors.edate")
    c.execute("select * from percent where p > 1 ")
    rows = c.fetchall()

    print("***Days with more than 1% requests errors***")
    for row in rows:
        print("%s - %s%% errors" % (row[0].strftime('%B %d, %Y'), round(row[1], 2)))
    print(" \n ")

    db.close()


if __name__ == "__main__":
    most_article()
    most_authors()
    percent_errors()
