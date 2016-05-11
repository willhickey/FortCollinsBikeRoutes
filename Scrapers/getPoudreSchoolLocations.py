import re
import urllib2
import time

url = 'https://www.psdschools.org/school-resources/school-locator'
req  = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0'});
html = urllib2.urlopen(req).read()
#print html
#schoolData.push({position:new google.maps.LatLng(40.589363,-105.124610),url:"/school/poudre-community-academy-pca",name:"Poudre Community Academy (PCA)",type:["High Schools"],content:"",code:"PCA",});

schools = re.findall('schoolData.push\(\{(.*?)\}\);', html, re.S)
for school in schools:
    #print '->'+school+'<-'
    #->position:new google.maps.LatLng(0.000000,0.000000),url:"/school/fullana-learning-center",name:"Fullana Learning Center",type:["Early Childhood Programs"],content:"",code:"FUL",<-
    location = re.search('LatLng\((.*?),(.*?)\)', school)
    lat = location.group(1)
    lon = location.group(2)
    
    url = re.search('url:"(.*?)"', school).group(1)
    name = re.search('name:"(.*?)"', school).group(1)
    if name == 'Lab School for Creative Learning':          #403 error. skip this one
        continue
    type = re.search('type:\["(.*?)"\]', school).group(1)
    
    #print lat, lon, url, name, type
    #print type
    url = 'https://www.psdschools.org' + url
    #print url
    req  = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0'});
    html = urllib2.urlopen(req).read()
    #print html
    address = re.search('<span itemprop="streetAddress">(.*?)</span>', html).group(1)
    city = re.search('<span class="locality" itemprop="addressLocality">(.*?)</span>', html).group(1)
    #print address, city
    DestinationTypeID = 0
    if type == 'Elementary Schools':
        DestinationTypeID = 2
    if type == 'Middle Schools':
        DestinationTypeID = 3
    if type == 'High Schools':
        DestinationTypeID = 4

    print '--', lat, lon, url, name, type, address, city, DestinationTypeID
    name = re.sub("'", "''", name)      #escape ' for the SQL
    sql = "INSERT INTO Destination (Name, DestinationTypeID, Address, City, State, Latitude, Longitude) VALUES ('" + name + "', " + str(DestinationTypeID) + ", '" + address + "', '" + city + "', 'CO', " + lat + ", " + lon + ")"
    print sql
    time.sleep(5)