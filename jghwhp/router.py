from collections import namedtuple


Event = namedtuple('Event', 'event_type repository callback')


class EventRouter(object):
    event_handlers = []

    def trigger_event_handlers(self, event_type, event_data):
        match = True
        for event_handler in self.event_handlers:
            if event_handler.repository != '*':
                match = event_handler.repository == event_data['respository']['full_name'] and match
            if event_handler.event_type:
                match = event_handler.event_type == event_type and match

            if match:
                event_handler.callback(event_type, event_data)

    def register_event(self, event_type, repository='*'):
        def wrap(callback):
            self.event_handlers.append(Event(event_type, repository, callback))
            return callback
        return wrap
