
class bltControl(object):
    def __init__(self, events):
        self.subscribers = {event: dict() for event in events}
        print self.subscribers

    def get_subscribers(self, event):
        return self.subscribers[event]

    def draw(self):
        pass

    def update(self):
        pass

    def resized(self):
        pass

    def clear(self):
        pass

    def register(self, event, obj, callback=None):
        if callback is None:
            callback = getattr(obj, 'get_dispatch')
        print "Registersd!"
        self.get_subscribers(event)[obj] = callback
        print self.subscribers

    def unregister(self, event, obj):
        del self.get_subscribers(event)[obj]

    def dispatch(self, event, value):
        for sub, callback in self.get_subscribers(event).iteritems():
            callback(value)

    def get_dispatch(self, value):
        pass