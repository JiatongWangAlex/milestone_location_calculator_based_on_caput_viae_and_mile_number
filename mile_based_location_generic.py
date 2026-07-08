import json
import os
import math


# =====================================================================
# CONFIGURATION 
# =====================================================================

INPUT_FILE = "bracara_augusta_to_aquae_flaviae.json"  
TOTAL_ROUTE_ROMAN_MILES = 80       
TARGET_ROMAN_MILES = 29             


def calculate_haversine_km(lon1, lat1, lon2, lat2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


if not os.path.exists(INPUT_FILE):
    print(f"Could not find '{INPUT_FILE}'")
    exit()

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    route_data = json.load(f)

master_track = route_data.get("unified_master_track", [])

if not master_track:
    print(f" '{INPUT_FILE}' is empty.")
    exit()

# This does not convert Roman miles to km.
# It converts the percentage to km's along the route, 
# however detailed the Itiner-e route asset is, however long the road is purported to be in km's. 
total_network_km = 0.0
step_distances = []

for i in range(len(master_track) - 1):
    p1 = master_track[i]
    p2 = master_track[i+1]
    dist = calculate_haversine_km(p1[0], p1[1], p2[0], p2[1])
    total_network_km += dist
    step_distances.append(dist)


if TARGET_ROMAN_MILES > TOTAL_ROUTE_ROMAN_MILES or TARGET_ROMAN_MILES < 0:
    print(f"Mile ({TARGET_ROMAN_MILES}) is out of bounds for a {TOTAL_ROUTE_ROMAN_MILES} mile-long route.")
    exit()

target_percentage = TARGET_ROMAN_MILES / TOTAL_ROUTE_ROMAN_MILES
target_distance_km = total_network_km * target_percentage

print(f" {TARGET_ROMAN_MILES} Roman miles accounts for: {target_percentage * 100:.2f}% of the total route.")

accumulated_km = 0.0
target_coordinate = None

for i in range(len(master_track) - 1):
    step_km = step_distances[i]
    
    if accumulated_km + step_km >= target_distance_km:
        p_current = master_track[i]
        p_next = master_track[i+1]
        
        needed_km = target_distance_km - accumulated_km
        t = needed_km / step_km  
        
        target_lon = p_current[0] + t * (p_next[0] - p_current[0])
        target_lat = p_current[1] + t * (p_next[1] - p_current[1])
        target_coordinate = (target_lon, target_lat)
        break
        
    accumulated_km += step_km


if target_coordinate:
    print(f"Latitude:  {target_coordinate[1]:.6f}")
    print(f"Longitude: {target_coordinate[0]:.6f}")
else:
    print("Can't find a coordinate for your milestone")
print("="*60)