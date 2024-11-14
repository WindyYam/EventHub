# To use this script, you should declare all events in your source file in this form:
# DEFINE_EVENT(your_event1)
# DEFINE_EVENT(your_event2)
# DEFINE_EVENT(your_event3)
# then, execute this script from the root of your source files(that contains DEFINE_EVENT)
# It will generate events.h contain all the event as enum definition

import os
import re
import sys

def find_event_names(directory):
    event_names = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".c"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                    matches = re.findall(r"DEFINE_EVENT\((\w+)\)", content)
                    event_names.extend(matches)
    return event_names

def write_to_events_file(event_names, script_dir):
    events_file = os.path.join(script_dir, "events.h")
    with open(events_file, "w") as f:
        f.write("/* This file is auto-generated. Do not modify. */\n")
        f.write("/* Run generate_events.h.py to gather all extern events in all subdirectory */\n\n")
        f.write("#ifndef EVENTS_H\n")
        f.write("#define EVENTS_H\n")
        f.write("typedef enum{\n")
        sorted_event_names = sorted(set(event_names))  # Sort the event names
        for event_name in sorted_event_names:
            line = f"    {event_name},\n"
            f.write(line)
        f.write("}Event_t;\n")
        f.write("#endif\n")

if __name__ == "__main__":
    current_directory = os.getcwd()
    directory = current_directory
    if(len(sys.argv) > 1):
        directory = sys.argv[1]
    event_names = find_event_names(directory)
    write_to_events_file(set(event_names), directory)