# Milestone Location Calculator
Two python scripts, one to stitch together a series of Itiner-e road segments into one .json asset, another to calculate the location of any milestone on that road given its mile number. 

In order to use this calculator, you MUST know a) the (Roman) mile number of your milestone, b) the caput viae of the road your milestone served c) the Itiner-e ID's of the route segments making up that road, d) the total length of the road in (Roman) miles


## route_extraction.py
First, we need to make the unified route asset.


### Download the Itiner-e data

The Itiner-e project is the "most detailed open digital dataset of roads in the entire Roman Empire". It documents tens of thousands of route segments. This calculator relies on data from Itiner-e. You must download the itiner-e nightly ndjson file (and place it in the same folder).

Go to https://itiner-e.org/about and click Download Latest Export.

Please remember to change ITINER_E_FILE = to reflect the actual name of the file you downloaded. 

### Identifying the relevant Itiner-e route segments
 To make the unified route asset, you will need to copy the itiner-e ID's of the route segments making up the road your milestone served, and put them into a comma separated list in order (starting from the route segment touching your caput viae). Go to the Itiner-e Project site and browse the roads. 
 
https://itiner-e.org/


#### Using the Itiner-e site
On the Itiner-e site, if you click on any route segment and click on the details tab to the left of your screen,
you will see more information on the route. One of the fields in the details tab is url/uri

An itiner-e url/uri looks like this 
itiner-e.org/route-segment/27204 

The final number is the route segment's itiner-e ID. They are not always 5 digits long so if yours isn't dont be alarmed.

Try to track your road from start to finish on the Itiner-e Project and copy the ID of each segment as you go along.

### Configuring and Running the Script
After this, the first script can stitch all the route segments together for you. 

Remember to set up the configuration block properly before running the script
Specifically, change the name of the OUTPUT_FILE to match your road. 
Currently the name of the OUTPUT_FILE is set to that of a demo file ("bracara_augusta_to_aquae_flaviae_demo.json")



## mile_based_location.py
Using the output of the first script, you can calculate a coordinate for any mile number on that road.

Remember to set up the configuration block properly before running the script.

Set the INPUT_FILE to the name of your OUTPUT_FILE from route_extraction.py

Set the total length of your road in Roman miles. Importantly, you do not need the absolute total length of the "entire road". If you know your milestone definitely lies between the caput viae and city B, you just need the length of the road between the caput viae and city B for this calculator to work. 

Set the mile number of your milestone.

Then run the script.


The approximate coordinate of your milestone based on its mile number and caput viae will be printed in your terminal.

### Finding the total length of your road in Roman miles
This can take a bit more work, but we rely on it to make an accurate calculation. 

https://omnesviae.org/tabula is a very good online tool based on the Peutinger tablet. However, please be careful. Do not rely on their route-planning function to find your route-- it will find you the shortest route between point A and point B but not necessarily the route you are looking for. I would advise going segment by segment and tallying the miles up along the way. 


If your route is not in the Peutinger tablet, try the Itinerarium Antonini Augusti; unfortunately there isn't a similar online tool for consulting it. 

## Why did I make this?

I made this because there was a cluster of milestones reused in a medieval bridge in Aquae Flaviae; 6 of which, tantalisingly, records both the caput viae of the road and the mile number. I thought this was definitely enough information for us to have a rough estimate of where they originally stood, so I made this calculator.


One major design hurdle I encountered while making this calculator was the coastline paradox. The more detailed a road asset is, the "longer" it becomes due to all the kinks and bends. If we simply convert Roman miles to kms and attempt to plot the milestone at the Xth km of the very detailed Itiner-e based route asset, we would be at the mercy of the coastline paradox. 

Therefore, to sidestep this entirely, the calculator uses percentage, not a raw conversion from Roman miles to km. 


FIRST: It calculates the Xth mile of a road Y miles long is Zth percent of the road


THEN: it looks at the unified route asset, grabs its total length in KM, and multiplies the total length of the route asset by Z percent.


FINALLY: it "crawls" along the route asset and finds the (Z percent x total length) km mark and prints that coordinate


If you ever encounter a Roman milestone (for which the caput viae and mile number is known),  divorced from its original context, or published under a legacy place name that is no longer identifiable, this calculator will help you estimate where it originally stood. 

If you are interested in my thesis project (which did not end up relying on these calculations, but it was a fun detour), see https://maximinusthraxdatabaseui.streamlit.app/
