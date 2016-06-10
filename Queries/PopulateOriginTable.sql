declare @fc as geography
select @fc=placemark from ftcollinsplaceboundary


--INSERT Census blocks that are part of the city of Ft Collins.
INSERT INTO Origin
select ID as CenusBlockID, geom.EnvelopeCenter().Lat as Latitude, geom.EnvelopeCenter().Long as Longitude
from censusblock cb 		
WHERE geom.STIntersects(@fc)=1 