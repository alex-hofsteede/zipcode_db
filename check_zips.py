import sqlite3, urllib2, lxml.html, re

con = sqlite3.connect('zipcodes-new.sqlite',isolation_level = None)
cur = con.cursor()

def check_zips():
    for row in cur.execute("SELECT zipcodes.zip, cities.name as city, states.name as state FROM zipcodes INNER JOIN cities ON zipcodes.city_id = cities.id INNER JOIN states on zipcodes.state_id = states.id WHERE valid IS NULL"):
        result = lxml.html.fromstring(urllib2.urlopen("https://tools.usps.com/go/ZipLookupResultsAction!input.action?resultMode=2&companyName=&address1=&address2=&city=&state=Select&urbanCode=&postalCode=%s&zip=" % str(row[0]).zfill(5)).read())
        result = result.xpath('//p[@class="std-address"]')
        if len(result) == 0:
            print "invalid zip: %s" % row[0]
        else:
            usps_result = result[0].text_content()
            if re.match("%s %s" % (row[1],row[2]), usps_result, re.I):
                con.cursor().execute("UPDATE zipcodes set valid = 1 where zip = %s" % row[0])
            else:
                con.cursor().execute("UPDATE zipcodes set valid = 0 where zip = %s" % row[0])
                print "city and state didnt match: %s != %s" % (row, usps_result)
    con.close()

if __name__ == '__main__':
    check_zips()
