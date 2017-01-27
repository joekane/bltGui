
class bltControl(object):
    def __init__(self):
        self.subscribers = dict()

    def draw(self):
        pass

    def update(self):
        pass

    def resized(self):
        pass

    def clear(self):
        pass

    def register(self, obj, callback=None):
        if callback is None:
            callback = getattr(obj, 'get_dispatch')
        print "Registersd!"
        self.subscribers[obj] = callback
        print self.subscribers

    def unregister(self, obj):
        del self.subscribers[obj]

    def dispatch(self, value):
        for sub, callback in self.subscribers.iteritems():
            callback(value)

    def get_dispatch(self, value):
        pass