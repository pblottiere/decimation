#!/bin/sh

# var
DATABASE="test_decimation"

# clean
rm -f *_pipe.json

# get data
if [ ! -f 292-5040_2015_2-5-6.laz ]
then
	wget http://depot.ville.montreal.qc.ca/geomatique/lidar_aerien/2015/292-5040_2015_2-5-6.laz
fi

if [ ! -f 292-5041_2015_2-5-6.laz ]
then
	wget http://depot.ville.montreal.qc.ca/geomatique/lidar_aerien/2015/292-5041_2015_2-5-6.laz
fi

if [ ! -f 293-5040_2015_2-5-6.laz ]
then
	wget http://depot.ville.montreal.qc.ca/geomatique/lidar_aerien/2015/293-5040_2015_2-5-6.laz
fi

if [ ! -f 293-5041_2015_2-5-6.laz ]
then
	wget http://depot.ville.montreal.qc.ca/geomatique/lidar_aerien/2015/293-5041_2015_2-5-6.laz
fi

# prepare database
dropdb $DATABASE
createdb $DATABASE

psql -d $DATABASE -f schema.sql

# fill database
for f in *.laz
do
	# build pipe
	FILENAME=$(echo $f | cut -f 2 -d '/')
	FILENAME_BASE=$(echo $FILENAME | cut -f 1 -d '.')
	PIPE_NAME="$FILENAME_BASE""_pipe.json"

	cp pipe.json.tpl $PIPE_NAME

	sed -i -e "s@LAZFILE@$FILENAME@g" $PIPE_NAME

	pdal pipeline -i $PIPE_NAME
done
