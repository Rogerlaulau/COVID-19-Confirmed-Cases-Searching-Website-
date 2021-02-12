import traceback
from include.Logger import logging, get_logger
import os
import sys
log = get_logger(__name__)

import configparser
config = configparser.ConfigParser()

conf_file = 'my_config.conf'

if not os.path.isfile(conf_file):
    raise ValueError(f'CONFIG FILE NOT FOUND: {conf_file}')
config.read(conf_file)

threads = config['service']['threads']
port = config['service'].getint('port')
cleanup_interval = config['service']['cleanup_interval']
channel_timeout = config['service']['channel_timeout']



from flask import Flask, request, make_response, jsonify, render_template, send_file, url_for
from functools import wraps
from time import sleep
from flask_cors import CORS
import json
import time
from HKAddressParser.components.core import Address
from HKAddressParser.components.util import Similarity
from math import sin, cos, sqrt, atan2, radians
from os import path
import folium
import pandas as pd
from waitress import serve

import threading
import requests
import csv

# creates a Flask application, named app
app = Flask(__name__)
CORS(app)   # withhout this, error "No 'Access-Control-Allow-Origin'" will block access from webpage


mydate = ""
mydict = {}
ls_interval_x, ls_interval_y = [], []


#this is a  HTTP Basic Authentication that is used for each endpoint
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == "noentry" and auth.password == "noentry":
            return f(*args, **kwargs)
        return make_response('Could not verify\nYou have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated

@app.route("/")
def status():
    log.info("/")
    return render_template("index.html")

@app.route("/status")
def home():
    log.info("/status")
    return "<h1>status: ok</h1>"

@app.route("/search/<location>", methods=["GET"])
@auth_required
def search(location):

    global mydict
    log.info(f"/search/{location}")
    print(location)
    result = {}
    origin = get_lat_long(location)
    
    nearby_locations = nearest_locations(origin)
    print(f'nearby_locations: {nearby_locations}')
    print(f'origin:{origin}')
    result["locations"] = get_distance_for_list(origin, nearby_locations)

    return jsonify(result)

@app.route("/map/<location>", methods=["GET"])
def geo(location):
    log.info(f"/map/{location}")

    if location == "" or location is None or location == "null":
        return '<h1>NOT FOUND</h1><p>Please return to <a href="http://www.rogerlau.ml">HOME</a> page to search a location first</p>'
    else:
        origin = get_lat_long(location)
        nearby_locations = nearest_locations(origin)
        mymap = folium.Map(
            location=[float(origin[1]),float(origin[2])],
            tiles='cartodbpositron',
            zoom_start=16,
            control_scale = True,
            zoom_control = True
        )

        for loc in nearby_locations:
            folium.Marker(location=[float(loc[1]), float(loc[2])], popup=loc[0], icon=folium.Icon(color='red', prefix='fa fa-circle-o')).add_to(mymap)
        folium.Marker([float(origin[1]),float(origin[2])], popup='You are here').add_to(mymap)
        print("genMap - done")
        
        return(mymap.get_root().render())

    

@app.route("/map/all", methods=["GET"])
def geoAll():
    log.info(f"/map/all")
    global mydate 
    if not path.exists(f"templates/{mydate}_whole_map.html"):
        log.error(f"templates/{mydate}_whole_map.html NOT exist, it is being generated")
        generate_whole_map()
    return render_template(f"{mydate}_whole_map.html")

@app.route("/comment", methods=["GET"])
def comment():
    log.info(f"/comment")
    return render_template("comment.html")

@app.route("/comment/submit", methods=["POST"])
def comment_submit():
    log.info(f"/comment/submit")
    data = request.form
    name, mail, subject = "", "", ""
    name = data["name"]
    mail = data["mail"]
    subject = data["subject"]

    t = time.localtime()
    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", t)
    print(current_time)

    # should replaced with Database in order not to have transaction conflict
    f = open("comment.txt", "a+")
    f.write(f"{current_time}:{name}:{mail}:{subject}\n")
    f.close() 

    return '<h1>Thank You.</h1><h2>I have received your feedback.</h2><p>Go to <a href="http://www.rogerlau.ml">HOME</a> page</p>'

@app.route("/receiver", methods=["POST"])
def receiver():
    print("/receiver")
    data = request.json
    print(data)

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    # lat1 = radians(22.317894943558315)
    # lon1 = radians(114.16941842867648)
    # lat2 = radians(22.30905239183873)
    # lon2 = radians(114.1746070329752)
    # dlon = lon2 - lon1
    # dlat = lat2 - lat1
    if type(lat1) is str:
        lat1 = float(lat1)
    if type(lon1) is str:
        lon1 = float(lon1)
    if type(lat2) is str:
        lat2 = float(lat2)
    if type(lon2) is str:
        lon2 = float(lon2)

    dlon = radians(lon2) - radians(lon1)
    dlat = radians(lat2) - radians(lat1)

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    #print(f"Result: {distance} km")
    #return f"{int(round(distance, 2)*1000)} 米/metres"
    return int(round(distance, 2)*1000)

def get_distance_for_list(origin, ls_locations):
    for i, loc in enumerate(ls_locations):
        distance = calculate_distance(origin[1], origin[2], loc[1], loc[2])
        if len(ls_locations[i]) >=4:
            ls_locations[i][3] = distance
        else:ls_locations[i].append(distance)
    return ls_locations

def get_lat_long(location_name):
    log.info(f"[get_lat_long] - {location_name}")

    if location_name is not None or location_name != "":
        try:  
            address = Address(location_name) 
            result = address.ParseAddress()
            latitude = result['geo']['Latitude']
            longitude = result['geo']['Longitude']
        except Exception as e:
            print(e)
            location_name = "NOT FOUND"
            latitude, longitude = "22.29554257683054", "114.1723419520053" # default Tsim Sha Tsui

    return [location_name, latitude, longitude]


def block_identifier(target):
    # to identify which grid the location (latitude and longitude) belongs to
    # param - target: [loc_name, latitude, longitude]
    # return - col, row of block
    global ls_interval_x
    global ls_interval_y

    pre_x_ele = -1
    pre_y_ele = -1

    latitude = float(target[1])
    longitude = float(target[2])

    for col, x in enumerate(ls_interval_x):
        if latitude > pre_x_ele and latitude <= x:
            for row, y in enumerate(ls_interval_y):
                if longitude > pre_y_ele and longitude <= y:
                    return col, row
                pre_y_ele = y
        pre_x_ele = x
    return None, None # by default None if not found

def nearest_blocks(col, row, depth=1):
    # determine which blocks are regarded as nearest given a block
    min_col = col-depth
    max_col = col+depth
    min_row = row-depth
    max_row = row+depth
    nearest_blocks_ls = []

    for i in range(min_col, max_col+1):
        for j in range(min_row, max_row+1):
            nearest_blocks_ls.append(f"{i}-{j}")
    return nearest_blocks_ls

def nearest_locations(myloc, depth=1):
    # state the nearest locations
    # param - myloc: e.g. ["mylocation", 84, 222]
    #       - depth: the searching area
    # return- nearest_locations_ls: e.g. [['華景大廈', '22.31792', '114.18964'], ['何文田邨靜文樓', '22.31497', '114.18242']]
    nearest_locations_ls = []

    if myloc is None or len(myloc) != 3:
        return nearest_locations_ls

    mycol, myrow = block_identifier(myloc)
    if mycol is None or myrow is None:
        return nearest_locations_ls
    else:
        for block in nearest_blocks(mycol, myrow, depth):
            if block in mydict:
                nearest_locations_ls.extend(mydict[block])
    return nearest_locations_ls



def physical2latlong():
    log.info(f'physical2latlong - START')
    global mydate
    building_list = []

    with open(f"{mydate}_building_list_chi.csv", 'r') as file:
        reader = csv.reader(file, delimiter = ',')
        for row in reader:
            building_list.append(row[1].replace('(非住宅)', ''))

    GCS_ls = [["Location","Latitude","Longitude"]]
    # get the geographical coordinate system (latitude, longitude)
    for i, building in enumerate(building_list): 
        log.info(f"{i}: {building}")
        if i != 0:
            try:
                address = Address(building)
                result = address.ParseAddress()
                GCS_ls.append([building, result['geo']['Latitude'], result['geo']['Longitude']])
                sleep(0.2)
            except Exception as e:
                log.error(f"physical2latlong - Except: {i} - {building}")
                log.error(e)

    # save to file
    with open(f'{mydate}_GCS.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(GCS_ls)

    log.warning(f'{mydate}_GCS.csv saved')
    log.info(f'physical2latlong - END')


def preprocessing_mapping():
    global mydate
    global mydict
    mydict.clear()
    define_memory_dict()

    with open(f'{mydate}_GCS.csv', newline='') as f:
        reader = csv.reader(f)
        GCS_ls = list(reader)

    for element in GCS_ls[1:]:
        col, row = block_identifier(element)
        if col is None or row is None:
            log.error(f"Location - {element} out of scope")
            continue
        else:
            my_key = str(col)+"-"+str(row)
            if my_key in mydict:
                #mydict[my_key].append(element[0])
                mydict[my_key].append(element)
            else:
                log.warning(f"no such key {my_key}")
    #print(mydict)


def update_building_list():
    log.info(f"update_building_list - START")
    global mydate
    while True:
        t = time.localtime()
        current_time = time.strftime("%H", t)
        #log.error(f'current_time in hour: {current_time}')
        if (not path.exists(f"{mydate}_building_list_chi.csv") and(current_time!="00" and current_time!="01")) or current_time == "02":
            # update at 2am
            log.info("==============================")
            log.info("Time to update the data source")
            url = 'https://www.chp.gov.hk/files/misc/building_list_chi.csv'
            r = requests.get(url, allow_redirects=True)

            mydate = time.strftime("%Y-%m-%d", t)
            open(mydate+"_building_list_chi.csv", 'wb').write(r.content)

            physical2latlong()
            preprocessing_mapping()
            log.info(f"=========== {mydate+'_building_list_chi.csv'} Done Updating =============")
            time.sleep(3000) # to avoid get duplicate file
        time.sleep(1000)

# def update_building_list():
#     global mydate
#     physical2latlong()
#     preprocessing_mapping()
#     print(f'=========== {mydate+"_building_list_chi.csv"} Done Updating =============')


def define_memory_dict():
    log.info('define_memory_dict - START')
    global mydict
    # I define the length of Hong Kong is 43km and width is 63km
    x_min, y_min = 22.175381, 113.826690
    x_max, y_max = 22.564129, 114.442054

    interval_num_x = 83 # the number of slots that split the length
    interval_num_y = 123

    # interval_num_x = 10 # the number of slots that split the length
    # interval_num_y = 20


    for i in range(1, interval_num_x+1):
        ls_interval_x.append(((x_max - x_min)/interval_num_x)*i+x_min)

    for j in range(1, interval_num_y+1):
        ls_interval_y.append(((y_max - y_min)/interval_num_y)*j+y_min)

    # initialize mydict
    for i, x in enumerate(ls_interval_x):
        for j, y in enumerate(ls_interval_y):
            mydict[str(i)+"-"+str(j)] = []
    log.info('define_memory_dict - END')

def generate_whole_map():
    log.warning(f'generate_whole_map - START')
    global mydate

    df = pd.read_csv(f"{mydate}_GCS.csv")

    df["Latitude"] = pd.DataFrame(df["Latitude"].tolist(), index=df.index)
    df["Longitude"] = pd.DataFrame(df["Longitude"].tolist(), index=df.index)

    wholemap = folium.Map(
        location=[22.392601796955326, 114.15393760079547],
        tiles='cartodbpositron',
        zoom_start=11,
        control_scale = True,
        zoom_control = True
    )

    #tiles='cartodbpositron', 'CartoDB dark_matter', 'OpenStreetMap', “Stamen” (Terrain, Toner, and Watercolor)(i.e. 'Stamen Terrain')
    df.apply(lambda row:folium.Marker(location=[row["Latitude"], row["Longitude"]], popup=row["Location"], icon=folium.Icon(color='red', prefix='fa fa-circle-o')).add_to(wholemap), axis=1)  #tooltip="newcase", 
    wholemap.save(f"templates/{mydate}_whole_map.html")

    log.info(f"templates/{mydate}_whole_map.html is saved")
    log.warning(f'generate_whole_map - END')


if __name__ == "__main__":
    mydict = {}
    t = time.localtime()
    mydate = time.strftime("%Y-%m-%d", t)

    #define_memory_dict()

    x = threading.Thread(target=update_building_list)
    log.warning("running thread")
    x.start()
    sleep(5)
    #physical2latlong()
    preprocessing_mapping()
    generate_whole_map()


    #app.run(host="0.0.0.0", port=4000, debug=True)
    serve(app, host="0.0.0.0", port=port, threads=threads, cleanup_interval=cleanup_interval, channel_timeout=channel_timeout)

