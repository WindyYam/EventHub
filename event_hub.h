#ifndef EVENT_HUB_H
#define EVENT_HUB_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdbool.h>
#include "action_scheduler.h"
#include <string.h>

typedef uint32_t Event_t;

#ifndef DEBUG_PRINTF
#define DEBUG_PRINTF(fmt, ...)
#endif

// events.h is generated automatically using generate_events_h.py, which simply grab all Event_t eventName lines from your source file into events.h with prefix extern
// but you are also welcome to write it all by yourself
#include "events.h"

#define EVENT_MATCH(evt, val) (&evt == val)
// These 2 macros are preferred way of sending event. 
// The event is indeed the unique address of the uint8_t as unique identifier
// The value of uint8_t can act as extra data for the event message
// Sending event is safe from ISR as well
#define SEND_EVENT(evt) { \
    DEBUG_PRINTF("Event %s\n", #evt); \
    EventHub_SendEvent(&evt);\
}
#define SEND_EVENT_EXT(evt, extra) { \
    DEBUG_PRINTF("Event %s, %d\n", #evt, extra); \
    EventHub_SendEventExtra(&evt, extra); \
}

void EventHub_SendEvent(Event_t const* event);
void EventHub_SendEventExtra(Event_t* event, uint32_t extra);
// weak callback, implement it in user code
void EventHub_Process(Event_t const* event);

#ifdef __cplusplus
}
#endif
#endif /* EVENT_HUB_H */
