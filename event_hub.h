#ifndef EVENT_HUB_H
#define EVENT_HUB_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdbool.h>
#include <string.h>
#include <stdint.h>

typedef uint32_t Event_t;

// events.h is generated automatically using generate_events_h.py, which simply grab all Event_t eventName lines from your source file into events.h with prefix extern
// but you are also welcome to write it all by yourself
#include "events.h"

#define EVENT_MATCH(evt_name, evt) (&evt_name == evt)
#define EVENT_VALUE(evt) (*evt)

// These 2 macros are preferred way of sending event. 
// The event is indeed the unique address of the uint32_t as unique identifier
// The value of uint32_t can act as extra data(e.g. a pointer) for the event message
// Sending event is safe from ISR as well
#define SEND_EVENT(evt_name) { \
    EventHub_DebugPrint("Event %s\n", #evt_name); \
    EventHub_SendEvent(&evt_name);\
}

#define SEND_EVENT_EXT(evt_name, extra) { \
    EventHub_DebugPrint("Event %s, %d\n", #evt_name, extra); \
    EventHub_SendEventExtra(&evt_name, extra); \
}

void EventHub_SendEvent(Event_t* event);
void EventHub_SendEventExtra(Event_t* event, uint32_t extra);
// implement in user code
void EventHub_Process(Event_t const* event);
// weak callback, implement it in user code
void EventHub_DebugPrint(const char* format, ...);
#ifdef __cplusplus
}
#endif
#endif /* EVENT_HUB_H */
