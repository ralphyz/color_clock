from flask import Flask, render_template, request, redirect, url_for
import sys, json, time, datetime
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import RPi.GPIO as GPIO

app = Flask(__name__)

# Global variables
config_file = 'config.json'
red_start = 'red_start'
green_start = 'green_start'
yellow_start = 'yellow_start'
override = 'override'
saved = 'saved'
scheduled = 'scheduled'
led_status = 'led_status'
yellow_mode = 'yellow_mode'

# Colors
red = 'red'
green = 'green'
yellow = 'yellow'
gray = 'gray'
led = 'led'
delim = ':'
index = "web_index"

def_green_start = '07:45'
def_red_start = '20:45'

# GPIO Numbers
g_io = 17
r_io = 27
y_io = 22

green_notice = '00:05' # minutes
data = {}

#--------------------------------------------------------------------------------
#
#  name: Handler
#  desc: define the pattern for the config file
#
#--------------------------------------------------------------------------------
class Handler(PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        PatternMatchingEventHandler.__init__(self, patterns=[config_file], ignore_directories=True, case_sensitive=False)
    # Event is created, you can process it now
    def on_created(self, event):
        activate_light()

    # Event is modified, you can process it now
    def on_modified(self, event):
        activate_light()

#--------------------------------------------------------------------------------
#
#  name: calculate_scheduled_light
#  desc: determine which light should be active
#
#--------------------------------------------------------------------------------
def calculate_scheduled_light():
    global data

    dt_format = '%H:%M'
    now = time.strftime(dt_format)

    if data[yellow_mode] == 0:
        # yellow is always right before green
        data[yellow_start] = str(datetime.strptime(data[green_start], dt_format) - datetime.strptime(green_notice, dt_format))[:-3]

        hr, m = data[yellow_start].split(delim)
        if len(hr) == 1:
            data[yellow_start] = "0%s" % data[yellow_start]

        if data[red_start] > data[green_start]:
            if data[red_start] <= now or now < data[yellow_start]:
                return red
            elif now >= data[yellow_start] and now < data[green_start]:
                return yellow
            else:
                return green
        else:
            if now >= data[yellow_start] and now < data[green_start]:
                return yellow
            elif now < data[red_start] or now >= data[green_start]:
                return green
            else:
                return red
    else:
        if data[red_start] < data[yellow_start] < data[green_start]:
            if now < data[red_start] or now >= data[green_start]:
                return green
            elif now >= data[red_start] and now < data[yellow_start]:
                return red
            elif now >= data[yellow_start] and now < data[green_start]:
                return yellow

        elif data[red_start] < data[green_start] < data[yellow_start]:
            if now < data[red_start] or now >= data[yellow_start]:
                return yellow
            elif now >= data[red_start] and now < data[green_start]:
                return red
            elif now >= data[green_start] and now < data[yellow_start]:
                return green

        elif data[green_start] < data[yellow_start] < data[red_start]:
            if now < data[green_start] or now >= data[red_start]:
                return red
            elif now >= data[green__start] and now < data[yellow_start]:
                return green
            elif now >= data[yellow_start] and now < data[red_start]:
                return yellow

        elif data[green_start] < data[red_start] < data[yellow_start]:
            if now < data[green_start] or now >= data[yellow_start]:
                return yellow
            elif now >= data[green__start] and now < data[red_start]:
                return green
            elif now >= data[red_start] and now < data[yellow_start]:
                return red

        elif data[yellow_start] < data[red_start] < data[green_start]:
            if now < data[yellow_start] or now >= data[green_start]:
                return green
            elif now >= data[yellow_start] and now < data[red_start]:
                return yellow
            elif now >= data[red_start] and now < data[green_start]:
                return red

        elif data[yellow_start] < data[green_start] < data[red_start]:
            if now < data[yellow_start] or now >= data[red_start]:
                return red
            elif now >= data[yellow_start] and now < data[green_start]:
                return yellow
            elif now >= data[green_start] and now < data[red_start]:
                return green

        return red

#--------------------------------------------------------------------------------
#
#  name: get_current_light
#  desc: determine which light should be active
#
#--------------------------------------------------------------------------------
def get_current_light():
    global data

    read_light_config()

    return data[override] if data[override] else data[scheduled]

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
        override: '',
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

    print(data)
    with open(config_file, 'w') as f:
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

    if data.get(yellow_mode) == False:
        data[yellow_mode] = 0
    else:
        if data.get(yellow_mode) is None:
            data[yellow_start] = ''
            data[yellow_mode] = 0

    if data.get(override) is None:
        data[override] = ''

    if data.get(saved) is None:
        data[saved] = calculate_scheduled_light()

    #don't take the file value
    data[scheduled] = calculate_scheduled_light()

    if data[saved] != data[scheduled]:
        data[saved] = ''
        data[override] = ''

    # bkd - all these values need validating

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

    light = calculate_scheduled_light()

    print(data)

    if data[override]:
        lights = {
            red:red if data[override] == red else gray,
            green:green if data[override]  == green else gray,
            yellow:yellow if data[override] == yellow else gray,
            override:True
        }
    else:
        lights = {
            red:red if light == red else gray,
            green:green if  light == green else gray,
            yellow:yellow if light == yellow else gray,
            override:False
        }

    y_h, y_m = green_notice.split(":")

    y_m = int(y_m)

    times = {
        red:data[red_start],
        green:data[green_start],
        yellow:y_m if data[yellow_mode] == 0 else data[yellow_start],
        mode: data[yellow_mode]
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

    # was the scheduled value submitted?
    if new_led == data[scheduled]:
        data[override] = ""
        data[saved] = ""

        # writing the config will trigger the watchdog to update the LED
        write_time_config()

        return redirect(url_for(index))

    # continue if the scheduled value was not submitted

    if new_led == red:
        data[override] = red
    elif new_led == green:
        data[override] = green
    elif new_led == yellow:
        data[override] = yellow

    # save the scheduled value
    data[saved] = data[scheduled]

    # writing the config will trigger the watchdog to update the LED
    write_time_config()

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
    global data, green_notice


    # get the expected parameters
    if request.method == 'POST':
        new_green = request.form[green]
        new_red = request.form[red]
        new_yellow = request.form[yellow]
        new_mode = request.form[yellow_mode]

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
        g_h, g_m = new_green.split(delim)
        r_h, r_m = new_red.split(delim)
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

        if new_yellow < 10:
            green_notice = "00:0%d" % new_yellow
        else:
            green_notice = "00:%d" % new_yellow

        data[yellow_mode] = 0

    else:
        try:
            y_h, y_m = new_yellow.split(delim)
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
    data[saved] = ''
    data[override] = ''

    # writing the config will trigger the watchdog to update the LED
    write_time_config()

    return redirect(url_for(index))

#--------------------------------------------------------------------------------
#
#  name: activate_light
#  desc: enable the correct light
#
#--------------------------------------------------------------------------------
def activate_light():
    with open(config_file, 'r') as f:
        d = json.load(f)

    led = ''
    d[scheduled] = calculate_scheduled_light()

    if d[override]:
        led = d[override]
    else:
        led = d[scheduled]

    if led == green:
        GPIO.output(g_io, True)
        GPIO.output(r_io, False)
        GPIO.output(y_io, False)

    elif led == red:
        GPIO.output(r_io, True)
        GPIO.output(g_io, False)
        GPIO.output(y_io, False)

    elif led == yellow:
        GPIO.output(y_io, True)
        GPIO.output(r_io, False)
        GPIO.output(g_io, False)

#--------------------------------------------------------------------------------
#
#  name: __main__
#  desc: the default function when the script is run
#
#--------------------------------------------------------------------------------
if __name__ == '__main__':
    src_path = "."

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(g_io, GPIO.OUT)
    GPIO.setup(r_io, GPIO.OUT)
    GPIO.setup(y_io, GPIO.OUT)

    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()

    read_light_config()

    sched = BackgroundScheduler(daemon=True)
    sched.add_job(activate_light, 'interval', seconds=1)
    sched.start()

    app.run(use_reloader=False, debug=True, host='0.0.0.0', port=80)
