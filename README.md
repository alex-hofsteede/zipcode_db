Zipcode DB
=========

A small-ish (860k) SQLite database of US ZIP codes and their associated city and state. For inclusion in mobile apps, or wherever a quick zip lookup needs to be made with minimal latency.

To look up a city and state for a zipcode, it can be queried like so:

    SELECT zipcodes.zip, cities.name, states.name FROM zipcodes 
    INNER JOIN cities on zipcodes.city_id = cities.id
    INNER JOIN states on zipcodes.state_id = states.id
    WHERE zipcodes.zip = 94401;

Zipcodes are stored as integers, so leading zeroes are not returned (e.g. `2238|Cambridge|MA`)

The data was seeded using the csv file from http://www.unitedstateszipcodes.org/zip-code-database and comes with 2 scripts:  
`populate_zips.py` Creates the zipcodes.sqlite database from the CSV file.  
`check_zips.py` Checks the codes in the database against the USPS zipcode API
