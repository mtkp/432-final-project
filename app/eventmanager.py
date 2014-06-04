# File:         eventmanager.py

# Authors:      Matt Kipps, Greg Parker
# Date:         June 2nd, 2014
# Class:        CSS 432 A
# Professor:    Brent Lagesse

# Assignment:   Final Project

# Description:
# Event manager passes events to and from every registered object.
# EM has 2 event queues - tick queue and event queue. This minimizes overhead
# by optimizing only ticking objects that care about clock ticks.
#
# Objects can be registered and unregistered from event notifications.
# This allows the program to deactivate modules that are out of focus.
#
# The EM itself is registered for ticks. At each tick, the EM actually
# flushes the event queue to all event listeners.

# python modules
import collections


class EventManager(object):
    def __init__(self):
        self.event_listeners = []
        self.tick_listeners = []
        self.event_queue = collections.deque()
        self.register_for_ticks(self)

    def register_for_events(self, listener):
        print "registering for events " + str(listener.__class__)
        self.event_listeners.append(listener)

    def unregister_for_events(self, listener):
        if listener in self.event_listeners:
            self.event_listeners.remove(listener)

    def register_for_ticks(self, listener):
        print "registering for ticks " + str(listener.__class__)
        self.tick_listeners.append(listener)

    def post_event(self, event):
        self.event_queue.append(event)

    def post_tick(self):
        for listener in self.tick_listeners:
            listener.tick()

    def tick(self):
        while len(self.event_queue) > 0:
            event = self.event_queue.popleft()
            for listener in self.event_listeners:
                listener.notify(event)