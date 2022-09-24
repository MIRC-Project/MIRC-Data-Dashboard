# Flask app and db models imports
from app import db
from app.models import Download, Upload

# Data Visualization library imports
from bokeh.plotting import figure
from bokeh.io import output_file, show, save
from bokeh.models import HoverTool, DatetimeTickFormatter, FuncTickFormatter

# Helper libraries
import numpy as np
from datetime import datetime as dt

# Lookup table
lkup = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}

def throughput(year, month, day):   # Plots throughput vs timestamp
    # dl_bytes - Sent bytes during download
    # dl_elapsed - Elapsed time of download measurement
    # dl_time - Start time in UTC of download
    dl_bytes = Download.query.filter_by(year=year, month=month, day=day).with_entities(Download.bytes_acked).order_by(Download.year, Download.month, Download.day, Download.time).all()
    dl_elapsed = Download.query.filter_by(year=year, month=month, day=day).with_entities(Download.elapsed_time).order_by(Download.year, Download.month, Download.day, Download.time).all()
    dl_time = Download.query.filter_by(year=year, month=month, day=day).with_entities(Download.year, Download.month, Download.day, Download.time).order_by(Download.year, Download.month, Download.day, Download.time).all()

    # up_bytes - Received bytes during upload
    # up_elapsed - Elapsed time of upload measurement
    # up_time - Start time in UTC of upload
    up_bytes = Upload.query.filter_by(year=year, month=month, day=day).with_entities(Upload.bytes_received).order_by(Upload.year, Upload.month, Upload.day, Upload.time).all()
    up_elapsed = Upload.query.filter_by(year=year, month=month, day=day).with_entities(Upload.elapsed_time).order_by(Upload.year, Upload.month, Upload.day, Upload.time).all()
    up_time = Upload.query.filter_by(year=year, month=month, day=day).with_entities(Upload.year, Upload.month, Upload.day, Upload.time).order_by(Upload.year, Upload.month, Upload.day, Upload.time).all()

    # Convert start times from string to DateTime object
    dl_time = [dt.strptime('{}-{}-{} {}'.format(a[0], a[1], a[2], a[3]), "%Y-%m-%d %H:%M:%S") for a in dl_time]
    up_time = [dt.strptime('{}-{}-{} {}'.format(a[0], a[1], a[2], a[3]), "%Y-%m-%d %H:%M:%S") for a in up_time]

    # dl_speed - download throughput (Mbit/s) = sent bytes (dl_bytes) * 8 bits / Elapsed time in micro-seconds (dl_elapsed) 
    # up_speed - upload throughput (Mbit/s) = received bytes (up_bytes) * 8 bits / Elapsed time in micro-seconds (up_elapsed)
    # See https://github.com/m-lab/ndt-server/blob/main/spec/ndt7-protocol.md
    dl_speed = [float('nan') if a[0] is None or b[0] is None else 8 * a[0]/b[0] for a,b in zip(dl_bytes, dl_elapsed)]
    up_speed = [float('nan') if a[0] is None or b[0] is None else 8 * a[0]/b[0] for a,b in zip(up_bytes, up_elapsed)]

    # Graph HTML output path
    output_file("./app/static/throughput.html")

    # Plot title
    title = 'Average Throughput for {} {} {}'.format(lkup[month], day, year)

    # Plot config
    p = figure(x_axis_type="datetime", x_axis_label='Date (Year/Month/Day Hour:Min:Sec)', y_axis_label='Throughput (Mbit/s)', height=350, title=title)
    p.title.text_font_size = '16pt'
    p.xaxis.major_label_orientation = np.pi/4   # radians, "horizontal", "vertical", "normal"
    p.sizing_mode = 'stretch_width'

    # Download plot
    p.line(x=dl_time, y=dl_speed, color='red', legend_label="Download (MBit/s)")
    p.circle(x=dl_time, y=dl_speed, color='red', legend_label="Download (MBit/s)")

    # Upload plot
    p.line(x=up_time, y=up_speed, color='blue', legend_label="Upload (MBit/s)")
    p.circle(x=up_time, y=up_speed, color='blue', legend_label="Upload (MBit/s)")

    # Plot tools
    p.add_tools(HoverTool(tooltips=[("y", "@y"), ("x", "@x{%Y/%m/%d %H:%M:%S}")], formatters={'@x' : 'datetime'}))
    p.xaxis[0].formatter=DatetimeTickFormatter(
        years = ['%Y/%m/%d %H:%M:%S'],
        months = ['%Y/%m/%d %H:%M:%S'],
        days = ['%Y/%m/%d %H:%M:%S'],
        hours = ['%Y/%m/%d %H:%M:%S'],
        minutes = ['%Y/%m/%d %H:%M:%S'],
        seconds = ['%Y/%m/%d %H:%M:%S']
        )
    save(p)     # Save graph to output path

def min_round_trip(year, month, day):
    # dl_min_rtt - Min roundtrip time during download
    # dl_time - Start time in UTC of download
    dl_min_rtt = Download.query.filter_by(year=year, month=month, day=day).with_entities(Download.min_rtt).order_by(Download.year, Download.month, Download.day, Download.time).all()
    dl_time = Download.query.filter_by(year=year, month=month, day=day).with_entities(Download.year, Download.month, Download.day, Download.time).order_by(Download.year, Download.month, Download.day, Download.time).all()

    # up_min_rtt - Min roundtrip time during upload
    # up_time - Start time in UTC of upload
    up_min_rtt = Upload.query.filter_by(year=year, month=month, day=day).with_entities(Upload.min_rtt).order_by(Upload.year, Upload.month, Upload.day, Upload.time).all()
    up_time = Upload.query.filter_by(year=year, month=month, day=day).with_entities(Upload.year, Upload.month, Upload.day, Upload.time).order_by(Upload.year, Upload.month, Upload.day, Upload.time).all()

    # Convert start times from string to DateTime object
    dl_time = [dt.strptime('{}-{}-{} {}'.format(a[0], a[1], a[2], a[3]), "%Y-%m-%d %H:%M:%S") for a in dl_time]
    up_time = [dt.strptime('{}-{}-{} {}'.format(a[0], a[1], a[2], a[3]), "%Y-%m-%d %H:%M:%S") for a in up_time]

    # Checks for NANs
    dl_min_rtt = [float('nan') if a[0] is None else a[0] for a in dl_min_rtt]
    up_min_rtt = [float('nan') if a[0] is None else a[0] for a in up_min_rtt]

    # Graph HTML output path
    output_file("./app/static/min-round-trip.html")

    # Graph title
    title = 'Minimum Round Trip Time for {} {} {}'.format(lkup[month], day, year)

    # Plot config
    p = figure(x_axis_type="datetime", x_axis_label='Date (Year/Month/Day Hour:Min:Sec)', y_axis_label='Round Trip Time (ms)', height=350, title=title)
    p.title.text_font_size = '16pt'
    p.xaxis.major_label_orientation = np.pi/4   # radians, "horizontal", "vertical", "normal"
    p.sizing_mode = 'stretch_width'

    # Download plot for min roundtrip
    p.line(x=dl_time, y=dl_min_rtt, color='red', legend_label="Download - Min RTT (ms)")
    p.circle(x=dl_time, y=dl_min_rtt, color='red', legend_label="Download - Min RTT (ms)")

    # Upload plot for min roundtrip
    p.line(x=up_time, y=up_min_rtt, color='blue', legend_label="Upload - Min RTT (ms)")
    p.circle(x=up_time, y=up_min_rtt, color='blue', legend_label="Upload - Min RTT (ms)")

    # Plot tools
    p.add_tools(HoverTool(tooltips=[("y", "@y"), ("x", "@x{%Y/%m/%d %H:%M:%S}")], formatters={'@x' : 'datetime'}))
    p.xaxis[0].formatter=DatetimeTickFormatter(
        years = ['%Y/%m/%d %H:%M:%S'],
        months = ['%Y/%m/%d %H:%M:%S'],
        days = ['%Y/%m/%d %H:%M:%S'],
        hours = ['%Y/%m/%d %H:%M:%S'],
        minutes = ['%Y/%m/%d %H:%M:%S'],
        seconds = ['%Y/%m/%d %H:%M:%S']
        )
    save(p)     # Save graph to output path

def avg_round_trip(year, month, day):
    # dl_rtt - Average roundtrip time during download
    # dl_time - Start time in UTC of download
    dl_rtt = Download.query.filter_by(year=year, month=month, day=day).with_entities(Download.rtt).order_by(Download.year, Download.month, Download.day, Download.time).all()       
    dl_time = Download.query.filter_by(year=year, month=month, day=day).with_entities(Download.year, Download.month, Download.day, Download.time).order_by(Download.year, Download.month, Download.day, Download.time).all()

    # up_rtt - Average roundtrip time during upload
    # up_time - Start time in UTC of upload
    up_rtt = Upload.query.filter_by(year=year, month=month, day=day).with_entities(Upload.rtt).order_by(Upload.year, Upload.month, Upload.day, Upload.time).all()       
    up_time = Upload.query.filter_by(year=year, month=month, day=day).with_entities(Upload.year, Upload.month, Upload.day, Upload.time).order_by(Upload.year, Upload.month, Upload.day, Upload.time).all()

    # Convert start times from string to DateTime object
    dl_time = [dt.strptime('{}-{}-{} {}'.format(a[0], a[1], a[2], a[3]), "%Y-%m-%d %H:%M:%S") for a in dl_time]
    up_time = [dt.strptime('{}-{}-{} {}'.format(a[0], a[1], a[2], a[3]), "%Y-%m-%d %H:%M:%S") for a in up_time]

    # Checks for NANs
    dl_rtt = [float('nan') if a[0] is None else a[0] for a in dl_rtt]
    up_rtt = [float('nan') if a[0] is None else a[0] for a in up_rtt]

    # Graph HTML output path
    output_file("./app/static/avg-round-trip.html")

    # Plot title
    title = 'Average Round Trip Time for {} {} {}'.format(lkup[month], day, year)

    # Plot config
    p = figure(x_axis_type="datetime", x_axis_label='Date (Year/Month/Day Hour:Min:Sec)', y_axis_label='Round Trip Time (ms)', height=350, title=title)
    p.title.text_font_size = '16pt'
    p.xaxis.major_label_orientation = np.pi/4   # radians, "horizontal", "vertical", "normal"
    p.sizing_mode = 'stretch_width'

    # Download plot for average roundtrip
    p.line(x=dl_time, y=dl_rtt, color='red', legend_label="Download - Smoothed RTT (ms)")
    p.circle(x=dl_time, y=dl_rtt, color='red', legend_label="Download - Smoothed RTT (ms)")

    # Upload plot for average roundtrip
    p.line(x=up_time, y=up_rtt, color='blue', legend_label="Upload - Smoothed RTT (ms)")
    p.circle(x=up_time, y=up_rtt, color='blue', legend_label="Upload - Smoothed RTT (ms)")

    # Format y axis with prefixes.
    p.yaxis.formatter = FuncTickFormatter(code='''
    if (tick < 1e3){
        var unit = ''
        var num = (tick).toFixed(0)
    }
    else if (tick < 1e6){
        var unit = 'k'
        var num = (tick/1e3).toFixed(0)
    }
    else{
        var unit = 'M'
        var num = (tick/1e6).toFixed(0)
    }
    return `${num}${unit}`
    ''')
    
    # Plot tools
    p.add_tools(HoverTool(tooltips=[("y", "@y"), ("x", "@x{%Y/%m/%d %H:%M:%S}")], formatters={'@x' : 'datetime'}))
    p.xaxis[0].formatter=DatetimeTickFormatter(
        years = ['%Y/%m/%d %H:%M:%S'],
        months = ['%Y/%m/%d %H:%M:%S'],
        days = ['%Y/%m/%d %H:%M:%S'],
        hours = ['%Y/%m/%d %H:%M:%S'],
        minutes = ['%Y/%m/%d %H:%M:%S'],
        seconds = ['%Y/%m/%d %H:%M:%S']
        )
    save(p)     # Save graph to output path