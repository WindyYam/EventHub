#ifndef EVENT_HUB_H
#define EVENT_HUB_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdbool.h>
#include <string.h>
#include <stdint.h>

#define DEFINE_EVENT(x)

// events.h is generated automatically using generate_events_h.py, which simply grab all DEFINE_EVENT eventName lines from your source file into events.h as enum
// but you are also welcome to write it all by yourself
#include "events.h"

// This macro is preferred way of sending event as it has debug print for event name. 
// Sending event is safe from ISR as well
#define SEND_EVENT(evt_name) { \
    EventHub_DebugPrint("Event %s\n", #evt_name); \
    EventHub_SendEvent(evt_name);\
}

void EventHub_SendEvent(Event_t event);
// implement in user code
void EventHub_Process(Event_t event);
// weak callback, implement it in user code
void EventHub_DebugPrint(const char* format, ...);
#ifdef __cplusplus
}
#endif
#endif /* EVENT_HUB_H */
