import json
import os
import math


# =====================================================================
# CONFIGURATION 
# =====================================================================

ITINER_E_FILE = "itiner_e_land_routes_only.ndjson"
OUTPUT_FILE = "bracara_augusta_to_aquae_flaviae.json"

# Provide a list of the Itiner-e road segments that make up your route in order
# Starting with the road segment that touches your starting point/caput viae-
TARGET_IDS = [
    27205, 27203, 27204,
]

# Set the starting point of the route/caput viae
# It doesn't have to be the exact start of the first itiner-e road segment
# Any coordinate in the vicinity will work. Just use the Pleiades coordinates for your caput viae.
START_LAT = -8.421360
START_LON = 41.550146

# not exactly neccessary; will not affect later calculations but naming it is good practice.
ROUTE_ASSET_NAME = "Bracara Augusta to Aquae Flaviae Route" 

# =====================================================================
START_COORD = (START_LON, START_LAT)

if not os.path.exists(ITINER_E_FILE):
    print(f"'{ITINER_E_FILE}' not found.")
    exit()

target_set = set(TARGET_IDS)
raw_features = {}


with open(ITINER_E_FILE, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        try:
            feature = json.loads(line)
            raw_id = feature.get("id")
            if raw_id is not None and int(raw_id) in target_set:
                raw_features[int(raw_id)] = feature
        except (json.JSONDecodeError, ValueError):
            continue


def get_gap(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

processed_features = []
master_route_points = []

# Stitch road segments together in the correct orientation starting from your start point.
for idx, seg_id in enumerate(TARGET_IDS, 1):
    if seg_id not in raw_features:
        print(f"Road Segment {seg_id} was missing from dataset.")
        continue
        
    feature = raw_features[seg_id]
    coords = list(feature["geometry"]["coordinates"])
    is_reversed = False
    
    if len(master_route_points) == 0:
        d_start = get_gap(START_COORD, coords[0])
        d_end = get_gap(START_COORD, coords[-1])
       
        if d_end < d_start:
            coords = coords[::-1]
            is_reversed = True
        master_route_points.extend(coords)
        
    else:
        last_master_pt = master_route_points[-1]
        d_normal = get_gap(last_master_pt, coords[0])
        d_flipped = get_gap(last_master_pt, coords[-1])
        
        if d_normal <= d_flipped:
            master_route_points.extend(coords[1:])
        else:
            coords = coords[::-1]
            master_route_points.extend(coords[1:])
            is_reversed = True
            
    feature["geometry"]["coordinates"] = coords
    feature["properties"]["direction_corrected"] = True
    feature["properties"]["original_digitization_was_backwards"] = is_reversed
    
    status = "REVERSED" if is_reversed else "NORMAL"
    print(f"  [{idx:02d}/{len(TARGET_IDS)}] Segment {seg_id:<6} -> {status}")
    processed_features.append(feature)

output_payload = {
    "route_name": ROUTE_ASSET_NAME,
    "total_segments": len(processed_features),
    "ordered_ids": TARGET_IDS,
    "unified_master_track": master_route_points, 
    "features": processed_features                 
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output_payload, f, indent=4, ensure_ascii=False)

print(f"\nSUCCESS! Full road exported to '{OUTPUT_FILE}'")