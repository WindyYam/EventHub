# EventHub
A simple implementation of event processing aim at embedded system

You need ActionScheduler module as well, see https://github.com/WindyYam/ActionScheduler

To use it, in your source files, include the header `event_hub.h`, and declare:

```
DEFINE_EVENT(your_event1)
DEFINE_EVENT(your_event2)
```

Send the event from your code in this form
```
SEND_EVENT(your_event1);
SEND_EVENT(your_event2);
```

Then, somewhere in your user code, you should implement this weak function to overwrite the default one:

```
#include "event_hub.h"

void EventHub_Process(Event_t event)
{
    switch(event)
    {
        case your_event1:
        {
            // Do something for your event
        }
        break;
        case your_event2:
        {
            // Do something for your event
        }
        break;
		default:
			// Log unknown event
		break;
    }
}
```

And then, run generate_events_h.py from the root of your source file, which will generate a events.h header file
containing all the events as enum. Suggest to integrate the .py script into your build system.

Use ActionScheduler for queue and get rid of ISR context, which means you can send event from ISR context as well

The whole idea of events is to decouple your modules, so that if you want a button event from button module to trigger
Led module behaviour(without registering onPress callback stuff from the button module, because it is complicated in code, and has ISR context issue), 
the EventHub is the most natural way(at the cost of dependency on EventHub), so button module and Led module don't need to know the others' existence