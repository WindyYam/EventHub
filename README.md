# EventHub
A simple implementation of event processing aim at embedded system

You need ActionScheduler module as well, see https://github.com/WindyYam/ActionScheduler

To use it, in your source files, include the header, and declare:

```
Event_t yourEventName1;
Event_t yourEventName2;
```

Send the event from your code in this form
```
SEND_EVENT(yourEventName1);
SEND_EVENT_EXT(yourEventName2, 123);
```

Then, somewhere in your user code, you should implement this weak function to overwrite the default one:

```
void EventHub_Process(Event_t const* event)
{
	if(EVENT_MATCH(yourEventName1, event))
	{
		//...
	}
	else if(EVENT_MATCH(yourEventName2, event))
	{
		uint8_t extra = *event;
		//...
	}
}
```

And then, run generate_events_h.py from the root of your source file, which will generate a events.h header file
containing all the events as extern variables.

The general idea is to use the memory address of each Event_t variable as the unique identifier, so to get rid of
enum definition

The value of the Event_t (which is uint8_t) can be an extra data to your processing

Use ActionScheduler for queue and get rid of ISR context, which means you can send event from ISR context as well