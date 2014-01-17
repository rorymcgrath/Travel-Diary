import csv
import math


# Procedure that takes as input a csv file, and stores the NUMERICAL data as a list, 
# where each element of the list is a list itself that corresponds to a row in the file,
# and each element of that list corresponds to an entry in that row. Any non-numerical elements
# in any row in the csv file are skipped over.

def parseCSV(filePath, data):
    with open(filePath, 'rU') as csvfile:
        for row in csv.reader(csvfile, dialect = csv.excel_tab):
            entry = row[0].split(',')
            tList = []
            for element in entry:
                try:
                    tList.append(float(element))    
                except:
                    pass
            data.append(tList)


# Function that uses the haversine formula to calculate the 'great-circle' distance in meters
# between two points whose latitutde and longitude are known

def calDistance(point1, point2):

    earthRadius = 6371000 
    dLat = math.radians(point1[0]-point2[0])
    dLon = math.radians(point1[1]-point2[1])    
    lat1 = math.radians(point1[0])
    lat2 = math.radians(point2[0])
    
    a = (math.sin(dLat/2) ** 2) + ((math.sin(dLon/2) ** 2) * math.cos(lat1) * math.cos(lat2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = earthRadius * c 
    
    return d


# Function that takes as input the GPS location of a point and a list of points, where each element of the 
# list is a tuple containing the latitutde and longitude for that point. The function outputs the maximum 
# distance, in meters, from that point to any point in the list of points

def calDistanceToPoint(point, points):
    maxDistance = 0
    for i in range(0, len(points)):
        dist = calDistance(point, points[i])
        if dist > maxDistance:
            maxDistance = dist
    return maxDistance
    

# Procedure that takes as input the list containing GPS data, called gpsTraces, and two empty lists, 
# called trips and activities. 
#
# Each element of trips is a tuple and corresponds to a particular trip. The elements of the tuple are the 
# indices of the corresponding GPS data points in gpsTraces for where the trip began and ended, respectively.
# Similarly, each element of activities is a tuple and corresponds to a particular activity. The elements 
# of the tuple are the indices of the corresponding GPS data point in gpsTraces for where the activity began 
# and ended, respectively.
# 
# An activity is defined as a set of GPS points over a minimum duration of minDuration milliseconds that fall within 
# a circle of radius maxRadius meters. The minimum interval between successive activites must be at least 
# minInterval milliseconds, for them to be recorded as separate activities.

def inferTripActivity(gpsTraces, trips, activities, minDuration, maxRadius, minInterval):
    
    i = 0
    while i < len(gpsTraces) - 1:
        
        # Create a collection of successive points that lie within a circle of radius maxRadius meters
        j = i + 1
        points = [gpsTraces[i][2:4]]  
        while j < len(gpsTraces) and calDistanceToPoint(gpsTraces[j][2:4], points) < maxRadius:
            points.append(gpsTraces[j][2:4])
            j += 1
        
        # Check if the duration over which these points were collected exceeds minDuration milliseconds
        if gpsTraces[j-1][1] - gpsTraces[i][1] > minDuration:
            
            # Check if the activity is separated in time from previous activity by at least minInterval milliseconds
            if len(activities) > 0 and gpsTraces[i][1] - gpsTraces[activities[-1][-1]][1] < minInterval:
                activities[-1][-1] = j-1
            else:
                activities.append([i, j-1])
            i = j - 1
        else:
            i += 1

    numActivities = len(activities)
    if numActivities != 0:
        
        # Check if the GPS log begins with a trip
        if activities[0][0] != 0:
            trips.append([0, activities[0][0]])
        
        # Interpolate trips from activities
        if numActivities > 1:
            for i in range(0, numActivities - 1):            
                trips.append([activities[i][-1], activities[i+1][0]])
        
        # Check if the GPS log ends with a trip
        if activities[-1][-1] < len(gpsTraces)-1:
            trips.append([activities[-1][-1], len(gpsTraces)-1])
    else:
        trips.append([0, len(gpsTraces)-1])
        

# The input file is a csv containing the GPS data and ground truth. The file should contain eleven columns.  
# The first nine columns denote the phone number of the test phone (a 9-digit number with no brackets and hyphens),
# timestamp (in epoch time, recorded in milliseconds), latitude, longitude, GPS accuracy (in feet), battry status
# (in percentage), sampling rate (in seconds), accelermoeter reading, and the activity as inferred by the Google
# API, respectively. The values for each of these fields will be generated by the tracking app installed on the 
# test phone in the appropriate units, and you shouldn't have to change anything.
#
# The tenth and eleventh columns will have to be filled manually at the end of each day, and will reflect the 
# ground truth that will be used to train our inference algorithms.
# 
# The tenth column can take on two string values: (1) Trip, if the individual at the time was making a trip; 
# or (2) Activity, if the individual at the time was engaging in an activity.
#
# The eleventh column is a string as well. If the person was making a trip, then it denotes the mode, which can
# take the following values: Walk, Bike, Drive, Transit (Transit Agency). The variable Transit Agency can,
# for now, take the following values: AC Transit, MUNI, BART, Emery Go-Round, Dumbarton Express, Caltrain.
# As and when you encounter an agency not included in the list, be sure to add it to the protocol.
#
# If the person was engaging in an activity, then it denotes the location and/or purpose. For now, we're leaving
# it to the individual's discretion to fill this field however they deem appropriate. However, at some stage we'll 
# want to come up with a list of clearly defined activity purposes, if we wish to infer the same (which we do!).
#
# Finally, the rows in the file should be ordered in terms of increasing time. This will have to be done manually.

filePath = '/Users/biogeme/Desktop/Vij/Academics/Post-Doc/Travel-Diary/Data/Samsung_Google_Vij_010314.csv'
gpsTraces = []
parseCSV(filePath, gpsTraces)

trips, activities = [], []
minDuration, maxRadius, minInterval = 180000, 50, 60000
inferTripActivity(gpsTraces, trips, activities, minDuration, maxRadius, minInterval)
print trips, activities