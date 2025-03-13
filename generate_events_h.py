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
            if file.endswith((".c")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", errors='ignore') as f:
                        content = f.read()
                        # Use a simple regex to find DEFINE_EVENT macros
                        matches = re.findall(r"DEFINE_EVENT\((\w+)\)", content)
                        if matches:
                            event_names.extend(matches)
                except Exception as e:
                    print(f"Warning: Could not read file {file_path}: {e}")
    
    if not event_names:
        print("WARNING: No DEFINE_EVENT macros found. Check your source files.")
    return event_names

def find_handled_events(directory):
    handled_events = []
    event_hub_file = None
    
    # First, find the file containing the main EventHub_Process
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".c"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", errors='ignore') as f:
                        content = f.read()
                        # Look for non-weak EventHub_Process function
                        if "EventHub_Process" in content and "switch" in content and "case" in content:
                            # Skip if it's a weak implementation
                            if "__attribute__((weak))" in content and "EventHub_Process" in content:
                                continue
                            event_hub_file = file_path
                            print(f"Found EventHub_Process in: {file_path}")
                            
                            # Look for case statements in the file
                            case_pattern = r"case\s+(\w+):"
                            case_matches = re.findall(case_pattern, content)
                            if case_matches:
                                handled_events.extend(case_matches)
                                print(f"Found {len(case_matches)} case statements")
                            else:
                                print("Warning: No case statements found in EventHub_Process")
                            break
                except Exception as e:
                    print(f"Warning: Could not read file {file_path}: {e}")
        
        if event_hub_file:
            break
    
    if not event_hub_file:
        print("WARNING: Could not find EventHub_Process function with switch/case statements.")
    
    if not handled_events:
        print("WARNING: No handled events found in switch statement. Check your EventHub_Process function.")
    
    return handled_events

def write_to_events_file(event_names, script_dir):
    events_file = os.path.join(script_dir, "events.h")
    
    if not event_names:
        print(f"ERROR: No events found. Not generating {events_file}")
        return
    
    with open(events_file, "w") as f:
        f.write("/* This file is auto-generated. Do not modify. */\n")
        f.write("/* Run generate_events.h.py to gather all extern events in all subdirectory */\n\n")
        f.write("#ifndef EVENTS_H\n")
        f.write("#define EVENTS_H\n\n")
        f.write("typedef enum {\n")
        sorted_event_names = sorted(set(event_names))  # Sort the event names
        for event_name in sorted_event_names:
            line = f"    {event_name},\n"
            f.write(line)
        f.write("} Event_t;\n\n")
        f.write("#endif // EVENTS_H\n")
    
    print(f"Generated {events_file} with {len(sorted_event_names)} events")

def generate_event_statistics(event_names, handled_events, script_dir):
    # Convert to sets for easier processing
    all_events = set(event_names)
    handled = set(handled_events)
    
    # Find unhandled events
    unhandled = all_events - handled
    
    # Find events in switch that aren't defined (possible errors)
    undefined_handled = handled - all_events
    
    # Calculate handling rate
    total_events = len(all_events)
    total_handled = len(handled & all_events)  # Only count valid handled events
    handling_rate = (total_handled / total_events * 100) if total_events > 0 else 0
    
    # Generate statistics report
    stats_file = os.path.join(script_dir, "event_statistics.txt")
    with open(stats_file, "w") as f:
        f.write("====== Event Handling Statistics ======\n\n")
        f.write(f"Total defined events: {total_events}\n")
        f.write(f"Events properly handled in EventHub_Process: {total_handled}\n")
        f.write(f"Event handling rate: {handling_rate:.2f}%\n\n")
        
        if unhandled:
            f.write("=== Unhandled Events ===\n")
            f.write("The following events are defined but not handled in the EventHub_Process function:\n")
            for event in sorted(unhandled):
                f.write(f"- {event}\n")
            f.write("\n")
        else:
            f.write("All defined events are handled in the EventHub_Process function.\n\n")
        
        if undefined_handled:
            f.write("=== WARNING: Events handled but not defined ===\n")
            f.write("These events are handled in the switch statement but have no DEFINE_EVENT declaration:\n")
            for event in sorted(undefined_handled):
                f.write(f"- {event}\n")
            f.write("\n")
    
    print(f"Generated {stats_file}")
    return all_events, handled, unhandled, undefined_handled

def print_summary(all_events, handled, unhandled, undefined_handled):
    total_events = len(all_events)
    total_handled = len(handled & all_events)  # Only count valid handled events
    handling_rate = (total_handled / total_events * 100) if total_events > 0 else 0
    
    print("\n====== Summary ======")
    print(f"Total defined events: {total_events}")
    print(f"Events handled in EventHub_Process: {total_handled}")
    print(f"Event handling rate: {handling_rate:.2f}%")
    
    if unhandled:
        print(f"\nUnhandled events: {len(unhandled)}")
        # Print up to 5 examples if there are many
        examples = sorted(list(unhandled))[:min(5, len(unhandled))]
        if len(unhandled) <= 5:
            print(f"  {', '.join(examples)}")
        else:
            print(f"  {', '.join(examples)}... (see report for full list)")
    
    if undefined_handled:
        print(f"\nWARNING: {len(undefined_handled)} events handled but not defined")
        examples = sorted(list(undefined_handled))[:min(5, len(undefined_handled))]
        if len(undefined_handled) <= 5:
            print(f"  {', '.join(examples)}")
        else:
            print(f"  {', '.join(examples)}... (see report for full list)")

if __name__ == "__main__":
    current_directory = os.getcwd()
    directory = current_directory
    
    # Process command line arguments
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    
    print(f"Scanning directory: {directory}")
    
    # Find all defined events
    print("\nLooking for defined events...")
    event_names = find_event_names(directory)
    print(f"Found {len(set(event_names))} unique defined events")
    
    # Find all handled events
    print("\nLooking for handled events in EventHub_Process...")
    handled_events = find_handled_events(directory)
    print(f"Found {len(set(handled_events))} unique handled events")
    
    # Generate the header file
    write_to_events_file(set(event_names), directory)
    
    # Generate statistics
    all_events, handled, unhandled, undefined_handled = generate_event_statistics(
        event_names, handled_events, directory
    )
    
    # Print summary to console
    print_summary(all_events, handled, unhandled, undefined_handled)