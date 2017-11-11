#! /usr/bin/env python
import psycopg2

DBNAME = "news"


''' 1. What are the most popular three articles of all time? '''


def most_article():
    """ This function uses the tables article and log
    to return the most accessed articles """

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        SELECT articles.title, count(log.path) AS VIEWs
        FROM articles, log
        WHERE log.path LIKE '%'||articles.slug
        GROUP BY articles.title
        ORDER BY VIEWs DESC LIMIT 3
        """)
    rows = c.fetchall()

    print("***The most popular three articles of all time***")
    for row in rows:
        print("\" %s \" - %s views" % (row[0], row[1]))
    print(" \n ")

    db.close()


'''2. Who are the most popular article authors of all time? '''


def most_authors():
    """ This function uses the tables article, authors and log
    to return the most accessed article authors based on article VIEWs"""

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        SELECT authors.name, count(log.path) AS views
        FROM authors, log, articles
        WHERE log.path LIKE '%'||articles.slug
        AND articles.author = authors.id
        GROUP BY authors.name
        ORDER BY views DESC;
        """)
    rows = c.fetchall()

    print("***The most popular article authors of all time***")
    for row in rows:
        print("%s - %s views" % (row[0], row[1]))
    print(" \n ")

    db.close()


'''3. On which days did more than 1% of requests lead to errors? '''


def percent_errors():
    """ It retuns the day with more than 1% requests errors """

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    c.execute("""
        CREATE VIEW access AS SELECT date(time) AS tdate,
        count(*) AS views
        FROM log
        GROUP BY date(time)
        ORDER BY date(time);
        """)
    c.execute("""
        CREATE VIEW lerrors AS SELECT date(time) AS edate,
        count(*) AS errors
        FROM log
        WHERE status LIKE '%4%'
        GROUP BY time::date
        ORDER BY date(time);
        """)
    c.execute("""
        CREATE VIEW percent as
        SELECT lerrors.edate,
        cast(errors * 100 AS double precision) / views AS p
        FROM access, lerrors
        WHERE access.tdate = lerrors.edate;
        """)

    c.execute("SELECT * FROM percent WHERE p > 1 ")
    rows = c.fetchall()

    print("***Days with more than 1% requests errors***")
    for row in rows:
        print("%s - %s%% errors" % (row[0].strftime('%B %d, %Y'),
              round(row[1], 2)))
    print(" \n ")

    db.close()


if __name__ == "__main__":
    """ Call the three functions and show the results """

    most_article()
    most_authors()
    percent_errors()
