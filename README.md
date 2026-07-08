# Milestone Location Calculator

If you ever encounter a Roman milestone **(for which the caput viae and mile number is known)**, divorced from its original context, or published under a legacy place name that is no longer identifiable, this calculator will help you estimate where it originally stood.

In order to use this calculator, you MUST know 


**a) the (Roman) mile number of your milestone,**

**b) the caput viae of the road your milestone served**

**c) the Itiner-e ID's of the route segments making up that road**

**d) the total length of the road in (Roman) miles**

# How it works

I made this because while working on my thesis I encountered a cluster of milestones reused in a medieval bridge in Aquae Flaviae; 6 of which, tantalisingly, records both the caput viae of the road and the mile number. I thought this was definitely enough information for us to have a rough estimate of where they originally stood, so I made this calculator.


### The Problem

One major design hurdle I encountered while making this calculator was the **coastline paradox**. 

The more detailed a road asset is, the "longer" it becomes due to all the kinks and bends. If we simply convert Roman miles to kms and attempt to plot the milestone at the Xth km of the very detailed Itiner-e based route asset, we would be very far off. 

For example, according to the Itinerarium Antonini Augusti, the road between Bracara Augusta and Aquae Flaviae is **80 Roman miles** long (20+26+16+18=80) 

But the total length of all Itiner-e road segments making up that road is **almost 124 Roman miles (183.36 km)!** 

This means if we simply convert our milestone's mile number into Roman miles, and try to plot it on the road, we will be very far off. Using this method, **a milestone marking the 80th mile, i.e. the final mile of the road that should be at the gates of Aquae Flaviae, would be plotted to a location almost 65 km away from Aquae Flaviae**


### The Solution

Therefore, to sidestep this paradox, my calculator uses **percentage**, instead of a raw conversion from Roman miles to kilometers. 

**For a milestone on the Xth mile of a road Y miles long:**


**FIRST**: It divides X by Y, and finds that for a road Y miles long, X miles would be Z percent of its total length.


**THEN**: It looks at the unified route asset (based on Itiner-e data), grabs its total length in kilometers, and multiplies the total length of the route asset by Z percent.


**FINALLY**: It "crawls" along the route asset and finds the (Z percent x total length) km mark of the road, and prints the coordinates of that location.




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

**itiner-e.org/route-segment/27204**

The final number is the route segment's itiner-e ID. They are not always 5 digits long so if yours isn't dont be alarmed.

Try to track your road from start to finish on the Itiner-e Project and copy the ID of each segment as you go along.

Remember to paste all ID's in order into the file

     ```
     TARGET_IDS = [
     123456, 123457, 123458, 
     ]


### Configuring and Running the Script
After this, the first script can stitch all the route segments together for you. 

Remember to set up the configuration block properly before running the script
Specifically, change the name of the OUTPUT_FILE to match your road. 
Currently the name of the OUTPUT_FILE is set to that of a demo file ("bracara_augusta_to_aquae_flaviae_demo.json")



## mile_based_location.py
Using the output of the first script, you can calculate a coordinate for any mile number on that road.

Remember to set up the configuration block properly before running the script.

Set the INPUT_FILE to the name of your OUTPUT_FILE from route_extraction.py

Set the total length of your road in Roman miles. **Importantly**, you do not need the absolute total length of the "entire road". If you know your milestone definitely lies between the caput viae and city B, you just need the length of the road between the caput viae and city B for this calculator to work. 

Set the mile number of your milestone.

Then run the script.


The approximate coordinate of your milestone based on its mile number and caput viae will be printed in your terminal.

### Finding the total length of your road in Roman miles
This can take a bit more work, but we rely on it to make an accurate calculation. 

https://omnesviae.org/tabula is a very good online tool based on the Peutinger tablet. However, please be careful. Do not rely on their route-planning function to find your route-- it will find you the shortest route between point A and point B but not necessarily the route you are looking for. I would advise going segment by segment and tallying the miles up along the way. 


If your route is not in the Peutinger tablet, try the Itinerarium Antonini Augusti; unfortunately there isn't a similar online tool for consulting it. 



## How to Run the Scripts

<details>
<summary><b>Click here for step-by-step instructions on how to run these scripts using the Terminal / Command Line</b></summary>

### Step 1: Downloading the scripts
1) Click the green button Code to open a dropdown menu. From there, click the button download zip
2) Find your downloaded file milestone_location_calculator_based_on_caput_viae_and_mile_number-main.zip and move it to your desktop
3) **Open the file milestone_location_calculator_based_on_caput_viae_and_mile_number-main.zip**, this should unzip it and create a new folder named milestone_location_calculator_based_on_caput_viae_and_mile_number-main on your desktop
4) Now everything is set up!

### Step 2: Downloading the Itiner-e Data
1) Go to the Itiner-e Project's About page https://itiner-e.org/about
2) Click Download Latest Export
3) Drag the file you downloaded from your downloads folder into the milestone_location_calculator_based_on_caput_viae_and_mile_number-main folder.
### Step 3: Configure route_extraction.py and mile_based_location.py
1) Open route_extraction.py, edit the Configuration block on the very top so that

    ```bash
    ITINER_E_FILE = "name_of_your_download.ndjson"


    OUTPUT_FILE = "name_of_your_road.json"
    
    TARGET_IDS = [your itiner road segment id 1, your itinere road segment id 2, your itinere road segment id 3]


3) Open mile_based_location.py, edit the Configuration block at the very top so that

    ```bash
    INPUT_FILE = "name_of_your_road.json"


    TOTAL_ROUTE_ROMAN_MILES = total length of the route in Roman miles


    TARGET_ROMAN_MILES = mile number of your milestone      


### Step 4: Open your Terminal / Command Line
Depending on your operating system, open your computer's command line interface:
* **Windows:** Press the **Windows Key**, type `cmd` (or `Command Prompt`), and press **Enter**.
* **Mac:** Press **Cmd + Spacebar**, type `Terminal`, and press **Enter**.
* **Linux:** Press **Ctrl + Alt + T**.


### Step 5: Navigate to your project folder
You need to point the terminal to the folder where you have saved the script and ndjson file. 

Type `cd ` followed by **a space**, and then type your folder's path. See tip for how to find your folder's path!

> **Tip:** To avoid typing out long paths manually, type `cd ` (with **a space** after it), and then **drag and drop the folder** from your desktop directly into the terminal window. It will automatically fill in the path for you! Then press **Enter**.

### Step 6: Run route_extraction.py
Once your terminal is inside the correct directory, Type one of the following commands and press **Enter** to run route_extraction.py


* **Windows:**
  ```bash
  python route_extraction.py
  
* **Mac and Linux**
  ```bash
  python3 route_extraction.py


If everything goes well you should see a message "SUCCESS! Full road exported to '{OUTPUT_FILE}'"

If your computer tells you to install python, you can do so here. https://www.python.org/downloads/

### Step 7: Run mile_based_location.py
Type one of the following commands and press **Enter** to run mile_based_location.py

* **Windows:**
  ```bash
  python mile_based_location.py

  
* **Mac and Linux**
  ```bash
  python3 mile_based_location.py


If everything goes well you should the coordinates of your milestones in the terminal in a message formatted like so

e.g.
 29 Roman miles accounts for: 36.25% of the total route.
Latitude:  41.665171
Longitude: -8.157625


</details>
---



## Personal Tangent
BTW

If you are interested in my thesis project (which did not end up relying on these calculations, but it was a fun detour), see https://maximinusthraxdatabaseui.streamlit.app/
