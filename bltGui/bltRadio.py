from bltButton import *
from bearlibterminal import terminal
from bltControl import bltControl as Control

class bltRadio(Control):
    def __init__(self, owner, x, y, control_list=None, label=""):
        Control.__init__(self, ['changed'])
        self.owner = owner
        if not control_list:
            self.control_list = []
        else:
            self.control_list = control_list
        self.frame_element = False
        self.x = x
        self.y = y
        self.dirty = True
        self.label = label


        self.control_list.append(
            bltCheckBoxButton(self.owner, 1 + x, 1 + y, label="Option 1", checked=False, function=bltButton.select))
        self.control_list.append(
            bltCheckBoxButton(self.owner, 1 + x, 2 + y, label="Option 2", checked=True, function=bltButton.select))
        self.control_list.append(
            bltCheckBoxButton(self.owner, 1 + x, 3 + y, label="Option 3", checked=False, function=bltButton.select))


    def draw(self):

        if self.dirty:
            terminal.puts(self.owner.pos.x + self.x, self.owner.pos.y + self.y, self.label)
            if self.control_list:
                for c in self.control_list:
                    c.dirty = True
                    c.draw()
            self.dispatch('changed', self.selected())
            self.dirty = False



    def update(self):
        if self.control_list:
            change_result = (-1, False)
            for i, c in enumerate(self.control_list):
                result = i, c.update()
                if result[1]:
                    self.dispatch('changed', c.label)
                    change_result = result
            if change_result[1]:
                for i, c in enumerate(self.control_list):
                    if i != change_result[0]:
                        #print "Changed others"
                        c.checked = False
                        c.dirty = True
                        self.dirty = True

    def selected(self):
        for i, c in enumerate(self.control_list):
            if c.checked:
                return c.label



