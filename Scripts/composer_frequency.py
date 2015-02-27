#import modules
from __future__ import division
from sys import argv
import re
from collections import Counter
from sets import Set
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import MySQLdb

#create xml collection of "docs" (i.e., programs in NYPhil's definition)
tree = ET.parse('../Programs/complete.xml')
root = tree.getroot()
concerts = root.findall('doc')

#convert season listing (e.g., 1842-43) to a single leading year (1842)
def simplify_date(hyphenated_season):
    simple_season = re.sub(r'(\d{4})-\d{2}',r'\1',hyphenated_season)
    return simple_season

#get the composer's last name only from the worksComposerTitle elements
def get_name(work):
    composer_name = re.sub(r'(.*?)(,| \[).*',r'\1',work)
    composer_name = re.sub(r"(.*)'(.*)",r"\1\\'\2",composer_name)
    return composer_name

#gather info from XML file
all_seasons = []
composers = []
current_season = '1842'
total_works = 0

for c in concerts:
    season = simplify_date(c.find('season').text)
    
    if season != current_season:
        counted_composers = list(Counter(composers).items())
        all_seasons.append([current_season, total_works, counted_composers])
        current_season = season
        total_works = 0
        composers = []
        continue
    else:
        for work in c.findall('.//worksComposerTitle'):
            composer = get_name(work.text)
            if not re.match(r'Intermission',composer):
                composers.append(composer)
                total_works += 1
            else:
                pass
            
#open mysql connection
db = MySQLdb.connect(host="localhost",user="root",db="ny_phil")
c = db.cursor()
c.execute("DROP TABLE IF EXISTS Composers")
c.execute("DROP TABLE IF EXISTS Years")
c.execute("DROP TABLE IF EXISTS Works")
c.execute("CREATE TABLE Composers(name VARCHAR(40))")
c.execute("CREATE TABLE Years(year INT, total_works INT)")
c.execute("CREATE TABLE Works(year INT, number_works INT, composer VARCHAR(40))")

#put data into mysql
composers_set = Set([])
set_years = Set([])
years = {}

for s in all_seasons:
    if int(s[0]) not in set_years:
        set_years.add(int(s[0]))
        years[s[0]] = int(s[1])
    else:
        years[s[0]] += int(s[1])
    for x in s[2]:
        composers_set.add(x[0])

for x in composers_set:
    c.execute("INSERT INTO Composers VALUE('%s')"%x)

for key, value in years.iteritems():
    c.execute("INSERT INTO Years VALUES(%d,%d)"%(int(key),value))
    
for s in all_seasons:
    for x in s[2]:
        c.execute("INSERT INTO Works VALUES(%d,%d,'%s')"%(int(s[0]),x[1],x[0]))
        
#query and plot
query = """SELECT Years.year,(Works.number_works/Years.total_works*100) AS percent, Works.composer FROM Works
JOIN Years ON Works.year=Years.year
WHERE Works.composer='%s'"""

#composer_list = ['Beethoven','Mozart','Wagner','Tchaikovsky','Strauss','Brahms','Mendelssohn','Bach','Berlioz','Dvorak','Gershwin']
composer_list = argv[1:]

for n in composer_list:
    dates = []
    fixed = []
    
    c.execute(query%n)
    result = c.fetchall()

    for r in result:
        dates.append(r[0])
        if r[1]:
            fixed.append(r[1])
        else:
            fixed.append(0)        
        
    plt.plot(dates,fixed,label=n)

plt.legend()
plt.show()
db.close()