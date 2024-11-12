#include "event_hub.h"
#include "action_scheduler.h"

// A simple event queue implemented using ActionScheduler queue
static ActionReturn_t processTask(void const* arg)
{
    Event_t const* event = arg;
    EventHub_Process(event);
    return ACTION_ONESHOT;
}

// Since we not really care about the absolute time for the event process function to be fired, just "as soon as possible"
// So, schedule a delay 0 processTask function, together with event as the arg, so as it will run in the scheduler execution context as soon as possible
// Recommend to call SEND_EVENT() and SEND_EVENT_EXT() always, instead of these 2 functions
void EventHub_SendEvent(Event_t* event)
{
    (void)ActionScheduler_Schedule(0, processTask, (void *)event);
}

void EventHub_SendEventExtra(Event_t* event, uint32_t extra)
{
    *event = extra;
    (void)ActionScheduler_Schedule(0, processTask, (void *)event);
}

// The debug print, implement in user code
__attribute__((weak)) void EventHub_DebugPrint(const char* format, ...)
{
    (void)format;
}

// The event processor, you should implement in your user code
__attribute__((weak)) void EventHub_Process(Event_t const* event)
{
    EventHub_DebugPrint("EventHub_Process unimplemented!\n");
}