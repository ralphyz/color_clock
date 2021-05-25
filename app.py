from flask import Flask, render_template, request, redirect, url_for
import sys, json, time, datetime
from datetime import datetime

import RPi.GPIO as GPIO

app = Flask(__name__)

# Global variables
config_file = 'config.json'
web_file = 'web.json'
red_start = 'red_start'
green_start = 'green_start'
yellow_start = 'yellow_start'
next_led = 'next'
override = 'override'
override_time = 'override_start'
active = 'active'

mode = 'mode'
yellow_mode = 'yellow_mode'
green_notice = 'green_notice'

# Colors
red = 'red'
green = 'green'
yellow = 'yellow'
gray = 'gray'
led = 'led'
delimiter = ':'
index = "web_index"

def_green_start = '07:45'
def_red_start = '20:45'
def_yellow_start = '07:40'

data = {}

#--------------------------------------------------------------------------------
#
#  name: create_time_config
#  desc: get the default times for the lights. and write the config
#
#--------------------------------------------------------------------------------
def create_time_config():
    global data

    data = {
        red_start: def_red_start,
        green_start: def_green_start,
        yellow_start: def_yellow_start,
        next_led: '',
        override: '',
        override_time: '',
        active: ''
    }

    with open(config_file, 'w') as outfile:
        json.dump(data, outfile)

#--------------------------------------------------------------------------------
#
#  name: write_time_config
#  desc: write the config file for the lights.
#
#--------------------------------------------------------------------------------
def write_time_config():
    global data

    with open(web_file, 'w') as f:
        json.dump(data, f)

#--------------------------------------------------------------------------------
#
#  name: read_light_config
#  desc: read the configuration file
#
#--------------------------------------------------------------------------------
def read_light_config():
    global data

    try:
        with open(config_file, 'r') as f:
            data = json.load(f)
    except:
        create_time_config()

    if data.get(red_start) is None:
        data[red_start] = def_red_start

    if data.get(green_start) is None:
        data[green_start] = def_green_start

    if data.get(override_time) is None:
        data[override_time] = ''
        data[override] = ''
    elif data.get(override) is None:
        data[override_time] = ''
        data[override] = ''

    if data.get(yellow_mode) is None:
        data[yellow_mode] = False
    print(data[yellow_mode])

    if data.get(active) is None:
        data[active] = green

    try:
        g_h, g_m = data[green_start].split(delimiter)
        y_h, y_m = data[yellow_start].split(delimiter)
        r_h, r_m = data[red_start].split(delimiter)
    except:
        create_time_config

    # make sure good values were sent
    if int(g_h) < 0 and int(g_h) > 24 and int(g_m) < 0 and int(g_m) > 59 and int(r_h) < 0 and int(r_h) > 24 and int(r_m) < 0 and int(r_m) > 59:
        create_time_config

 
#--------------------------------------------------------------------------------
#
#  name: web_index
#  desc: the default page when / is called in the URL
#
#--------------------------------------------------------------------------------
@app.route('/')
def web_index():
    global data
    read_light_config()

    light = data[active]

    if data[override]:
        light = data[override]

    lights = {
        red:red if light == red else gray,
        green: green if light == green else gray,
        yellow: yellow if light == yellow else gray,
        override:True if data[override] else False
    }

    y_h, y_m = data[yellow_start].split(":")
    g_h, g_m = data[green_start].split(":")

    if int(g_m) > int(y_m):
        y_m = int(g_m) - int(y_m)
    else:
        y_m = (int(g_m) - int(y_m)) * -1
        
    times = {
        red:data[red_start],
        green:data[green_start],
        green_notice:y_m,
        yellow: data[yellow_start],
        mode: int(data[yellow_mode])
    }

    return render_template('main.html', title=light, light=lights, time=times, clock=time.strftime("%H:%M:%S"))

#--------------------------------------------------------------------------------
#
#  name: change_web_led
#  desc: a LED light was selected by the user
#
#--------------------------------------------------------------------------------
@app.route("/led", methods=["GET"])
def change_web_led():
    global data

    # make sure we have the latest
    read_light_config()

    new_led = request.args.get(led)
    print(new_led)
    data[override] = new_led
    data[override_time] = datetime.now().strftime('%H:%M')
    
    # writing the config will trigger the watchdog to update the LED
    write_time_config()
    time.sleep(0.2)
    return redirect(url_for(index))

#--------------------------------------------------------------------------------
#
#  name: normal
#  desc: remove override
#
#--------------------------------------------------------------------------------
@app.route("/normal", methods=["GET", "POST"])
def normal():
    global data

    data[override] = ""

    # writing the config will trigger the watchdog to update the LED
    write_time_config()

    return redirect(url_for(index))

#--------------------------------------------------------------------------------
#
#  name: schedule
#  desc: change the led schedule
#
#--------------------------------------------------------------------------------
@app.route("/schedule", methods=["POST"])
def schedule():
    global data


    # get the expected parameters
    if request.method == 'POST':
        new_green = request.form[green]
        new_red = request.form[red]
        new_yellow = request.form[yellow]
        new_mode = request.form[mode]

    # make sure good values were sent
    if not new_green or not new_red or not new_yellow or not new_mode:
        return redirect(url_for(index))

    # make sure good values were sent
    try:
        new_mode = int(new_mode)
    except:
        return redirect(url_for(index))

    # make sure good values were sent
    if new_mode != 0 and new_mode != 1:
        return redirect(url_for(index))

    # make sure good values were sent
    try:
        g_h, g_m = new_green.split(delimiter)
        r_h, r_m = new_red.split(delimiter)
    except:
        return redirect(url_for(index))

    # make sure good values were sent
    if int(g_h) < 0 and int(g_h) > 24 and int(g_m) < 0 and int(g_m) > 59 and int(r_h) < 0 and int(r_h) > 24 and int(r_m) < 0 and int(r_m) > 59:
        return redirect(url_for(index))

    # make sure good values were sent
    if new_green == new_red or new_green ==  new_yellow or new_red == new_yellow:
        return redirect(url_for(index))

    # make sure good values were sent
    if new_mode == 0:
        try:
            new_yellow = int(new_yellow)
        except:
            return redirect(url_for(index))

        if (new_yellow % 5) != 0:
            return redirect(url_for(index))

        if new_yellow < 0 or new_yellow > 60:
            return redirect(url_for(index))

        y_h, y_m = map(int, new_green.split(delimiter))

        y_m -= new_yellow

        if y_m < 0:
            y_h -= 1
            y_m += 60

        if y_h < 0:
            y_h += 24

        if y_m < 10:
            y_m = '0%d' % y_m
        else:
            y_m = '%d' % y_m

        if y_h < 10:
            y_h = '0%d' % y_h
        else:
            y_h = '%d' % y_h

        data[yellow_start] = '%s:%s' % (y_h, y_m)

        data[yellow_mode] = 0

    else:
        try:
            y_h, y_m = new_yellow.split(delimiter)
        except:
            return redirect(url_for(index))

        # make sure good values were sent
        if int(y_h) < 0 and int(y_h) > 24 and int(y_m) < 0 and int(y_m) > 59:
            return redirect(url_for(index))

        data[yellow_mode] = 1
        data[yellow_start] = new_yellow

    # new schedule passed all the checks: set the environment, write it, then redirect the web page
    data[green_start] = new_green
    data[red_start] = new_red
    data[override] = ''
    data[override_time] = ''

    # writing the config will trigger the watchdog to update the LED
    write_time_config()

    return redirect(url_for(index))


#--------------------------------------------------------------------------------
#
#  name: __main__
#  desc: the default function when the script is run
#
#--------------------------------------------------------------------------------
if __name__ == '__main__':
    src_path = "."
    time.sleep(5)

    app.run(debug=True, host='0.0.0.0', port=80)
