"""
Imports zipcodes from a CSV file names zipcodes.csv into a normalized zipcodes DB in sqlite called zipcodes.sqlite
"""

import sqlite3, csv, sys

con = sqlite3.connect('zipcodes.sqlite', isolation_level=None)
cur = con.cursor()

cur.executescript("""
    DROP TABLE IF EXISTS cities;
    DROP TABLE IF EXISTS states;
    DROP TABLE IF EXISTS zipcodes;
    CREATE TABLE cities (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE states (id INTEGER PRIMARY KEY, name CHAR(3));
    CREATE TABLE zipcodes (zip INTEGER PRIMARY KEY, city_id INTEGER, state_id INTEGER);

    INSERT INTO "states" VALUES(1,'AA');
    INSERT INTO "states" VALUES(2,'AE');
    INSERT INTO "states" VALUES(3,'AK');
    INSERT INTO "states" VALUES(4,'AL');
    INSERT INTO "states" VALUES(5,'AP');
    INSERT INTO "states" VALUES(6,'AR');
    INSERT INTO "states" VALUES(7,'AS');
    INSERT INTO "states" VALUES(8,'AZ');
    INSERT INTO "states" VALUES(9,'CA');
    INSERT INTO "states" VALUES(10,'CO');
    INSERT INTO "states" VALUES(11,'CT');
    INSERT INTO "states" VALUES(12,'DC');
    INSERT INTO "states" VALUES(13,'DE');
    INSERT INTO "states" VALUES(14,'FL');
    INSERT INTO "states" VALUES(15,'FM');
    INSERT INTO "states" VALUES(16,'GA');
    INSERT INTO "states" VALUES(17,'GU');
    INSERT INTO "states" VALUES(18,'HI');
    INSERT INTO "states" VALUES(19,'IA');
    INSERT INTO "states" VALUES(20,'ID');
    INSERT INTO "states" VALUES(21,'IL');
    INSERT INTO "states" VALUES(22,'IN');
    INSERT INTO "states" VALUES(23,'KS');
    INSERT INTO "states" VALUES(24,'KY');
    INSERT INTO "states" VALUES(25,'LA');
    INSERT INTO "states" VALUES(26,'MA');
    INSERT INTO "states" VALUES(27,'MD');
    INSERT INTO "states" VALUES(28,'ME');
    INSERT INTO "states" VALUES(29,'MH');
    INSERT INTO "states" VALUES(30,'MI');
    INSERT INTO "states" VALUES(31,'MN');
    INSERT INTO "states" VALUES(32,'MO');
    INSERT INTO "states" VALUES(33,'MP');
    INSERT INTO "states" VALUES(34,'MS');
    INSERT INTO "states" VALUES(35,'MT');
    INSERT INTO "states" VALUES(36,'NC');
    INSERT INTO "states" VALUES(37,'ND');
    INSERT INTO "states" VALUES(38,'NE');
    INSERT INTO "states" VALUES(39,'NH');
    INSERT INTO "states" VALUES(40,'NJ');
    INSERT INTO "states" VALUES(41,'NM');
    INSERT INTO "states" VALUES(42,'NV');
    INSERT INTO "states" VALUES(43,'NY');
    INSERT INTO "states" VALUES(44,'OH');
    INSERT INTO "states" VALUES(45,'OK');
    INSERT INTO "states" VALUES(46,'OR');
    INSERT INTO "states" VALUES(47,'PA');
    INSERT INTO "states" VALUES(48,'PR');
    INSERT INTO "states" VALUES(49,'PW');
    INSERT INTO "states" VALUES(50,'RI');
    INSERT INTO "states" VALUES(51,'SC');
    INSERT INTO "states" VALUES(52,'SD');
    INSERT INTO "states" VALUES(53,'TN');
    INSERT INTO "states" VALUES(54,'TX');
    INSERT INTO "states" VALUES(55,'UT');
    INSERT INTO "states" VALUES(56,'VA');
    INSERT INTO "states" VALUES(57,'VI');
    INSERT INTO "states" VALUES(58,'VT');
    INSERT INTO "states" VALUES(59,'WA');
    INSERT INTO "states" VALUES(60,'WI');
    INSERT INTO "states" VALUES(61,'WV');
    INSERT INTO "states" VALUES(62,'WY');
    """);

with open('zipcodes.csv','r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        if row['zip'] and row['decommissioned'] == "0" and len(row['primary_city']) != 0 and len(row['zip']) != 0:
            cur.execute("SELECT id FROM states WHERE name = '%s'" % row['state'])
            state_id = cur.fetchone()[0]
            cur.execute("SELECT id FROM cities WHERE name = '%s'" % row['primary_city'])
            result = cur.fetchone()
            if result:
                city_id = result[0]
            else:
               cur.execute("INSERT INTO cities (name) VALUES ('%s')" % row['primary_city'])
               city_id = cur.lastrowid
            cur.execute("INSERT INTO zipcodes (zip, city_id, state_id) VALUES (%s, %s, %s)" % (int(row['zip']), city_id, state_id))
            sys.stdout.write(".")
            sys.stdout.flush()
