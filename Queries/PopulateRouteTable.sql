declare @fc as geography
select @fc=placemark from ftcollinsplaceboundary
--populate temp table with full cartisian join between census blocks and destinations
select cb.ID CensusBlockID, d.id DestinationID, 
		geom.EnvelopeCenter().STDistance(geography::STGeomFromText('POINT(' + cast(d.longitude as varchar) + ' ' +  cast(d.latitude as varchar) + ')', 4326)) as DistanceToDestination
into #DistanceBetweenCensusBlocksAndSchools
from censusblock cb inner join destination d on 1=1
WHERE geom.STIntersects(@fc)=1 and d.destinationTypeID = 3			--3 is middle schools

--populate Route with shortest routes between each census block and the nearest elementary school
insert into Route (OriginID, DestinationID, Distance)
select o.ID as OriginID, d.DestinationID as DestinationID, D.DistanceToDestination as Distance
from #DistanceBetweenCensusBlocksAndSchools D join 
	(select censusblockid, min(distancetodestination) mindist
	from #DistanceBetweenCensusBlocksAndSchools
	group by censusblockid) mins
	on d.censusblockid = mins.censusblockid and d.DistanceToDestination = mins.mindist
	join origin o on o.censusblockid = d.censusblockid