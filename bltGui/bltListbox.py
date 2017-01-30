from bltButton import *
from bearlibterminal import terminal
from bltGui import bltSkins as Skins
from bltControl import bltControl as Control


class bltListbox(Control):
    def __init__(self, owner, x, y, items, collapse=False):
        Control.__init__(self, ['hover', 'changed'])
        self.owner = owner
        self.x = x
        self.y = y
        self.items = items
        self.frame_element = False
        self.dirty = True
        self.length = len(max(items, key=len))
        self.selected_index = None
        self.hover_index = -1
        self.hover = False

        self.colors = Skins.COLOR_SKINS['DEFAULT']

        self.collapse = collapse
        if self.collapse:
            self.expanded = False
        else:
            self.expanded = True

    def update(self):
        mouse = Input.mouse
        if self.owner:
            layer = self.owner.layer
            x = self.owner.pos.x
            y = self.owner.pos.y
        else:
            layer = terminal.state(terminal.TK_LAYER)
            x = 0
            y = 0

        if self.expanded:
            if mouse.hover_rect(self.x + x, self.y + y, self.length + 1, len(self.items)):
                if mouse.hover_rect(self.x + x + self.length, self.y + y, 1, 1) and self.collapse:

                    self.hover = True
                    if mouse.lbutton_pressed:
                        self.expanded = False
                        self.dirty = True
                else:
                    self.hover = True
                    self.hover_index = mouse.cy - (self.y + self.owner.pos.y)
                    if mouse.lbutton_pressed:
                        self.selected_index = mouse.cy - (self.y + self.owner.pos.y)
                        self.dispatch('changed', self.selected_index)
                        if self.collapse:
                            self.expanded = False
                    self.dirty = True
            else:
                if self.hover:
                    self.dirty = True
                self.hover = False
                self.pressed = False
                self.hover_index = -1
        elif mouse.hover_rect(self.x + x + self.length, self.y + y, 1, 1) and self.collapse:
            self.hover = True
            if mouse.lbutton_pressed:
                self.expanded = True

        else:
            self.hover = False
            if self.collapse:
                self.expanded = False

    def draw(self):
        if self.dirty and self.expanded:
            for i, item in enumerate(self.items):
                color = self.colors['COLOR']
                bkcolor = self.colors['BKCOLOR']
                if i == self.hover_index:
                    color = self.colors['HOVER']
                    bkcolor = self.colors['BKHOVER']
                if i == self.selected_index:
                    color = self.colors['SELECTED']
                    bkcolor = self.colors['BKSELECTED']

                if bkcolor is not None:
                    terminal.puts(self.x + self.owner.pos.x, self.y + self.owner.pos.y + i, "[c={0}]".format(bkcolor) + str("[U+2588]" * (self.length+1)))
                terminal.puts(self.x + self.owner.pos.x, self.y + self.owner.pos.y + i, "[c={0}]{2}".format(color, bkcolor, item))

            if self.collapse:
                bkcolor = self.colors['SELECTED']
                terminal.puts(self.x + self.owner.pos.x + self.length, self.y + self.owner.pos.y,
                              "[c={0}]".format(bkcolor) + str("[U+2588]"))
                terminal.puts(self.x + self.owner.pos.x + self.length, self.y + self.owner.pos.y,
                              "[c={0}]".format(color) + str("[U+25BC]"))
            self.dirty = False
        if self.dirty and not self.expanded:

            color = self.colors['COLOR']
            bkcolor = self.colors['BKCOLOR']


            i = self.selected_index


            if bkcolor is not None:
                terminal.puts(self.x + self.owner.pos.x, self.y + self.owner.pos.y , "[c={0}]".format(bkcolor) + str("[U+2588]" * self.length))
            if self.selected_index is not None:
                item = self.items[i]
                terminal.puts(self.x + self.owner.pos.x, self.y + self.owner.pos.y, "[c={0}]{2}".format(color, bkcolor, item))

            if self.collapse:
                bkcolor = self.colors['BKCOLOR']
                terminal.puts(self.x + self.owner.pos.x + self.length, self.y + self.owner.pos.y,
                              "[c={0}]".format(bkcolor) + str("[U+2588]"))
                terminal.puts(self.x + self.owner.pos.x + self.length, self.y + self.owner.pos.y,
                              "[c={0}]".format(color) + str("[U+25B2]"))

            self.dirty = False








