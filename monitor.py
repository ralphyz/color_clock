import sys, json, time, datetime
from datetime import datetime
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import RPi.GPIO as GPIO

# start
# read file
# schedule tasks
# monitor files
#    when files change, delete schedules, reschedule
# max_instances = 1

#The job for scheduling the light change
schedule_id = "color_clock_id"

#The scheduler
schedule = None
light_job = None

# Global variables
config_file = 'config.json'
web_file = 'web.json'
red_start = 'red_start'
green_start = 'green_start'
yellow_start = 'yellow_start'
yellow_mode = 'yellow_mode'
override = 'override'
override_time = 'override_start'
active = 'active'
next_led = 'next'
delimiter = ':'

# Colors
red = 'red'
green = 'green'
yellow = 'yellow'

def_yellow_start = '07:40'
def_green_start = '07:45'
def_red_start = '20:45'

# GPIO Numbers
g_io = 17
r_io = 27
y_io = 22

data = {}

#--------------------------------------------------------------------------------
#
#  name: Handler
#  desc: define the pattern for the web config file
#
#--------------------------------------------------------------------------------
class Handler(PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        PatternMatchingEventHandler.__init__(self, patterns=[web_file], ignore_directories=True, case_sensitive=False)
    
    # Event is created, you can process it now
    #def on_created(self, event):
    #    schedule_light()

    # Config file is modified, read it
    def on_modified(self, event):
        read_web_config()


#--------------------------------------------------------------------------------
#
#  name: calculate_next_light
#  desc: determine which light should be active
#
#--------------------------------------------------------------------------------
def calculate_next_light(now=time.strftime('%H:%M')):
    global data

    new_time = datetime.now().strftime('%d:%m:%y:%H:%M')

    day, month, year, hour, minute = map(int, new_time.split(":"))

    add_day = False

    #if now < data[red_start] and now  < data[green_start] and now < data[yellow_start]:
        #today
    #    add_day = False
    if now > data[red_start] and now > data[green_start] and now > data[yellow_start]: # and data[override_time] != ''
        add_day = True

    if data[red_start] < data[yellow_start] < data[green_start]:
        if now < data[red_start] or now >= data[green_start]:
            if add_day:
                data[next_led] = red
                return datetime(year, month, day, int(data[red_start].split(":")[0]), int(data[red_start].split(":")[1])) + timedelta(days=1)
            else:
                data[next_led] = red
                return datetime(year, month, day, int(data[red_start].split(":")[0]), int(data[red_start].split(":")[1]))
        elif now >= data[red_start] and now < data[yellow_start]:
            data[next_led] = yellow
            return datetime(year, month, day, int(data[yellow_start].split(":")[0]), int(data[yellow_start].split(":")[1]))
        elif now >= data[yellow_start] and now < data[green_start]:
            data[next_led] = green
            return datetime(year, month, day, int(data[green_start].split(":")[0]), int(data[green_start].split(":")[1]))

    elif data[red_start] < data[green_start] < data[yellow_start]:
        if now < data[red_start] or now >= data[yellow_start]:
            if add_day:
                data[next_led] = red
                return datetime(year, month, day, int(data[red_start].split(":")[0]), int(data[red_start].split(":")[1])) + timedelta(days=1)
            else:
                data[next_led] = red
                return datetime(year, month, day, int(data[red_start].split(":")[0]), int(data[red_start].split(":")[1]))
        elif now >= data[red_start] and now < data[green_start]:
            data[next_led] = green
            return datetime(year, month, day, int(data[green_start].split(":")[0]), int(data[green_start].split(":")[1]))
        elif now >= data[green_start] and now < data[yellow_start]:
            data[next_led] = yellow
            return datetime(year, month, day, int(data[yellow_start].split(":")[0]), int(data[yellow_start].split(":")[1]))

    elif data[green_start] < data[yellow_start] < data[red_start]:
        if now < data[green_start] or now >= data[red_start]:
            if add_day:
                data[next_led] = green
                return datetime(year, month, day, int(data[green_start].split(":")[0]), int(data[green_start].split(":")[1])) + timedelta(days=1)
            else:
                data[next_led] = green
                return datetime(year, month, day, int(data[green_start].split(":")[0]), int(data[green_start].split(":")[1]))
        elif now >= data[green_start] and now < data[yellow_start]:
            data[next_led] = yellow
            return datetime(year, month, day, int(data[yellow_start].split(":")[0]), int(data[yellow_start].split(":")[1]))
        elif now >= data[yellow_start] and now < data[red_start]:
            data[next_led] = red
            return datetime(year, month, day, int(data[red_start].split(":")[0]), int(data[red_start].split(":")[1]))

    elif data[green_start] < data[red_start] < data[yellow_start]:
        if now < data[green_start] or now >= data[yellow_start]:
            if add_day:
                data[next_led] = green
                return datetime(year, month, day, int(data[green_start].split(":")[0]), int(data[green_start].split(":")[1])) + timedelta(days=1)
            else:
                data[next_led] = green
                return datetime(year, month, day, int(data[green_start].split(":")[0]), int(data[green_start].split(":")[1]))
        elif now >= data[green_start] and now < data[red_start]:
            data[next_led] = red
            return datetime(year, month, day, int(data[red_start].split(":")[0]), int(data[red_start].split(":")[1]))
        elif now >= data[red_start] and now < data[yellow_start]:
            data[next_led] = yellow
            return datetime(year, month, day, int(data[yellow_start].split(":")[0]), int(data[yellow_start].split(":")[1]))

    elif data[yellow_start] < data[red_start] < data[green_start]:
        if now < data[yellow_start] or now >= data[green_start]:
            if add_day:
                data[next_led] = yellow
                return datetime(year, month, day, int(data[yellow_start].split(":")[0]), int(data[yellow_start].split(":")[1])) + timedelta(days=1)
            else:
                data[next_led] = yellow
                return datetime(year, month, day, int(data[yellow_start].split(":")[0]), int(data[yellow_start].split(":")[1]))
        elif now >= data[yellow_start] and now < data[red_start]:
            data[next_led] = red
            return datetime(year, month, day, int(data[red_start].split(":")[0]), int(data[red_start].split(":")[1]))
        elif now >= data[red_start] and now < data[green_start]:
            data[next_led] = green
            return datetime(year, month, day, int(data[green_start].split(":")[0]), int(data[green_start].split(":")[1]))

    elif data[yellow_start] < data[green_start] < data[red_start]:
        if now < data[yellow_start] or now >= data[red_start]:
            if add_day:
                data[next_led] = yellow
                return datetime(year, month, day, int(data[yellow_start].split(":")[0]), int(data[yellow_start].split(":")[1])) + timedelta(days=1)
            else:
                data[next_led] = yellow
                return datetime(year, month, day, int(data[yellow_start].split(":")[0]), int(data[yellow_start].split(":")[1]))
        elif now >= data[yellow_start] and now < data[green_start]:
            data[next_led] = green
            return datetime(year, month, day, int(data[green_start].split(":")[0]), int(data[green_start].split(":")[1]))
        elif now >= data[green_start] and now < data[red_start]:
            data[next_led] = red
            return datetime(year, month, day, int(data[red_start].split(":")[0]), int(data[red_start].split(":")[1]))


    #shouldn't get here
    data[next_led] = red
    return datetime(year, month, day, int(data[red_start].split(":")[0]), int(data[red_start].split(":")[1]))


#--------------------------------------------------------------------------------
#
#  name: calculate_scheduled_light
#  desc: determine which light should be active
#
#--------------------------------------------------------------------------------
def calculate_scheduled_light(now=time.strftime('%H:%M')):
    global data
    
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
        print("got here")
        if now < data[green_start] or now >= data[red_start]:
            return red
        elif now >= data[green_start] and now < data[yellow_start]:
                return green
        elif now >= data[yellow_start] and now < data[red_start]:
                return yellow

    elif data[green_start] < data[red_start] < data[yellow_start]:
        if now < data[green_start] or now >= data[yellow_start]:
            return yellow
        elif now >= data[green_start] and now < data[red_start]:
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
        override: '',
        override_time: '',
        active: '',
        next_led: ''
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

    if data.get(yellow_start) is None:
        data[yellow_start] = def_yellow_start
        
    if data.get(override_time) is None:     
        data[override_time] = ''
        data[override] = ''
    elif data.get(override) is None:
        data[override_time] = ''
        data[override] = ''

    if data.get(yellow_mode) is None:
        data[yellow_mode] = True

#--------------------------------------------------------------------------------
#
#  name: read_web_config
#  desc: read the configuration file
#
#--------------------------------------------------------------------------------
def read_web_config():
    global data

    print("read web config")
    try:
        with open(web_file, 'r') as f:
            web_data = json.load(f)
    except:
        return

    web_red =  web_data.get(red_start, '')
    web_green =  web_data.get(green_start, '')
    web_yellow =  web_data.get(yellow_start, '')
    web_override =  web_data.get(override, '')
    web_override_time =  web_data.get(override_time, '')
    web_yellow_mode = web_data.get(yellow_mode, False)

    data[yellow_mode] = web_yellow_mode

    if web_override and web_override_time:
        h, m = web_override_time.split(delimiter)

        # make sure good values were sent
        if int(h) < 0 and int(h) > 24 and int(m) < 0 and int(m) > 59:
            return

        if web_override != red and web_override != green and web_override != yellow:
            return

        data[override] = web_override
        data[override_time] = web_override_time

        print("override")

    elif web_red and web_green and web_yellow:
        try:
            g_h, g_m = web_green.split(delimiter)
            y_h, y_m = web_yellow.split(delimiter)
            r_h, r_m = web_red.split(delimiter)

            # make sure good values were sent
            if int(g_h) < 0 and int(g_h) > 24 and int(g_m) < 0 and int(g_m) > 59 and int(r_h) < 0 and int(r_h) > 24 and int(r_m) < 0 and int(r_m) > 59:
                return

            # save the data
            data[red_start] = web_red
            data[green_start] = web_green
            data[yellow_start] = web_yellow
            data[override] = ''
            data[override_time] = ''

            print("schedule change")
        except:
            return

    activate_light()



    

#--------------------------------------------------------------------------------
#
#  name: activate_light
#  desc: enable the correct light
#
#--------------------------------------------------------------------------------
def activate_light():
    global light_job, schedule, data

    try:
        schedule.remove_job(schedule_id)
    except:
        pass

    led = ''

    scheduled = calculate_scheduled_light()
    print(scheduled)
    next_light_schedule = calculate_next_light()
    led = scheduled

    print(data[override])

    if data[override] == scheduled:
        data[override] = ''
        data[override_time] = ''

    if data[override_time] != '': 
        light_at_override = calculate_scheduled_light(data[override_time])

        if light_at_override != scheduled:
            data[override_time] = ''
            data[override] = ''
        else:
            led = data[override]

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
    
    #store the active and next LEDs - for the web server
    data[active] = led
    write_time_config()

    #Schedule the next event
    light_job = schedule.add_job(activate_light, trigger='date', next_run_time=next_light_schedule, id=schedule_id, max_instances=1, replace_existing=True)

    if schedule.state == 0:
        schedule.start()

    return led

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


    # watch the config file for changes
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()

    schedule = BackgroundScheduler(daemon=True)
    schedule.start()

    read_light_config()
    activate_light()

    while True:
        time.sleep(1)
