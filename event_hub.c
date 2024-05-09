#include "event_hub.h"

// A simple event queue implemented using ActionScheduler queue
static ActionReturn_t processTask(void* arg)
{
    Event_t const* event = (const char*)arg;
    EventHub_Process(event);
    return ACTION_ONESHOT;
}

// Recommend to call SEND_EVENT and SEND_EVENT_EXT always, instead of these 2
void EventHub_SendEvent(Event_t const* event)
{
    ActionScheduler_Schedule(0, processTask, (void *)event);
}

void EventHub_SendEventExtra(Event_t* event, uint8_t extra)
{
    *event = extra;
    ActionScheduler_Schedule(0, processTask, (void *)event);
}

// The event processor, you should implement in your user code
__attribute__((weak)) void EventHub_Process(Event_t const* event)
{
    DEBUG_PRINTF("EventHub_Process unimplemented!\n");
}