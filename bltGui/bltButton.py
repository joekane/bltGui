import bltInput as Input
from bearlibterminal import terminal
from bltControl import bltControl as Control

class bltButton(Control):
    def __init__(self, owner, x, y,  text, function=None, length=None):
        Control.__init__(self)
        self.owner = owner
        self.text = text
        self.x = x
        self.y = y

        if length is None:
            self.length = len(text)
        else:
            self.length = length

        self.x = x - self.length // 2
        self.y = y

        self.fore = 'white'
        self.back = 'blue'
        self.fore_alt = 'grey'
        self.back_alt = 'dark blue'

        if function is None:
            self.function = self.do_nothing
        else:
            self.function = function
        self.hover = False
        self.pressed = False
        self.dirty = True
        self.frame_element = False

    def draw(self):
        if self.dirty:
            mouse = Input.mouse

            if self.owner:
                layer = self.owner.layer
                x = self.owner.pos.x
                y = self.owner.pos.y
            else:
                layer = terminal.state(terminal.TK_LAYER)
                x = 0
                y = 0
            terminal.layer(layer)

            if self.hover:
                if self.pressed:
                    terminal.color('darkest grey')
                    terminal.puts(x + self.x, y + self.y, "[U+2584]" * self.length)
                    terminal.puts(x + self.x, y + self.y + 1, "[U+2588]" * self.length)
                    terminal.puts(x + self.x, y + self.y + 2, "[U+2580]" * self.length)
                    terminal.color('darker grey')
                    terminal.puts(x + self.x, y + self.y + 1, str(self.text).center(self.length, " "))
                    return self.function()
                terminal.color(self.back)
                terminal.puts(x + self.x, y + self.y, "[U+2584]" * self.length)
                terminal.puts(x + self.x, y + self.y + 1, "[U+2588]" * self.length)
                terminal.puts(x + self.x, y + self.y + 2, "[U+2580]" * self.length)
                terminal.color(self.fore)
                terminal.puts(x + self.x, y + self.y + 1, str(self.text).center(self.length, " "))
            else:
                terminal.color(self.back_alt)
                terminal.puts(x + self.x, y + self.y, "[U+2584]" * self.length)
                terminal.puts(x + self.x, y + self.y + 1, "[U+2588]" * self.length)
                terminal.puts(x + self.x, y + self.y + 2, "[U+2580]" * self.length)
                terminal.color(self.fore_alt)
                terminal.puts(x + self.x, y + self.y + 1, str(self.text).center(self.length, " "))
            self.dirty = False

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

        if mouse.hover_rect(self.x + x, self.y + y, self.length, 3):
            self.hover = True
            if mouse.lbutton_pressed:
                    return self.function(self)
            self.dirty = True
        else:
            if self.hover:
                self.dirty = True
            self.hover = False
            self.pressed = False

    def do_nothing(self):
        #print "Did Nothin'....."
        pass

    def close(self):
        #print "Close?"
        self.owner.visible = False
        self.owner.dirty = True
        pass

    def resize(self):
        #print "Resize!"
        self.owner.resizing = True
        pass

    def toggle(self):
        self.checked = not self.checked
        return self.checked

    def select(self):
        self.checked = True
        return self.checked

    def resized(self):
        pass


class bltCloseFrameButton(bltButton):
    def __init__(self, owner):
        bltButton.__init__(self, owner, owner.width - 1, 0,  "X", length=1, function=bltButton.close)
        self.frame_element = True
    def draw(self):
        if self.dirty:
            terminal.layer(self.owner.layer)
            if self.hover:
                terminal.color(self.back)
                terminal.puts(self.owner.pos.x + self.x, self.owner.pos.y + self.y, "[U+2588]" * self.length)
                terminal.color(self.fore)
                terminal.puts(self.owner.pos.x + self.x, self.owner.pos.y + self.y,
                              str(self.text).center(self.length, " "))
            else:
                terminal.color(self.back_alt)
                terminal.puts(self.owner.pos.x + self.x, self.owner.pos.y + self.y, "[U+2588]" * self.length)
                terminal.color(self.fore_alt)
                terminal.puts(self.owner.pos.x + self.x, self.owner.pos.y + self.y,
                              str(self.text).center(self.length, " "))
            self.dirty = False

    def resized(self):
        self.x = self.owner.width - 1

class bltResizeFrameButton(bltButton):
    def __init__(self, owner):
        bltButton.__init__(self, owner, owner.width - 1, owner.height-1,  "[U+2195]", length=1, function=bltButton.resize)
        self.frame_element = True

    def draw(self):
        if self.dirty:
            terminal.layer(self.owner.layer)
            if self.hover:
                terminal.color(self.back)
                terminal.puts(self.owner.pos.x + self.x, self.owner.pos.y + self.y, "[U+2588]" * self.length)
                terminal.color(self.fore)
                terminal.puts(self.owner.pos.x + self.x, self.owner.pos.y + self.y,
                              str(self.text).center(self.length, " "))
            else:
                terminal.color(self.back_alt)
                terminal.puts(self.owner.pos.x + self.x, self.owner.pos.y + self.y, "[U+2588]" * self.length)
                terminal.color(self.fore_alt)
                terminal.puts(self.owner.pos.x + self.x, self.owner.pos.y + self.y,
                              str(self.text).center(self.length, " "))
            self.dirty = False

    def resized(self):
        self.x = self.owner.width - 1
        self.y = self.owner.height - 1


class bltCheckBoxButton(bltButton):
    def __init__(self, owner, x, y, label="", checked=False, function=bltButton.toggle):
        bltButton.__init__(self, owner, x, y,  "( )", length=1, function=function)
        self.checked_text = "(X)"
        self.frame_element = False
        self.checked = checked
        self.label = label
        self.length = len(self.text)

    def draw(self):
        if self.dirty:
            if self.checked:
                text = self.checked_text
            else:
                text = self.text

            terminal.layer(self.owner.layer)
            if self.hover:
                terminal.color(self.back)
                terminal.puts(self.owner.pos.x + self.x, self.owner.pos.y + self.y, "[U+2588]" * self.length)
                terminal.color(self.fore)
                terminal.puts(self.owner.pos.x + self.x, self.owner.pos.y + self.y, text)
            else:
                terminal.color(self.back_alt)
                terminal.puts(self.owner.pos.x + self.x, self.owner.pos.y + self.y, "[U+2588]" * self.length)
                terminal.color(self.fore_alt)
                terminal.puts(self.owner.pos.x + self.x, self.owner.pos.y + self.y, text)
            terminal.puts(self.owner.pos.x + self.x + self.length + 1, self.owner.pos.y + self.y, self.label)
            self.dirty = False

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

        if mouse.hover_rect(self.x + x, self.y + y, self.length, 1):
            self.hover = True
            if mouse.lbutton_pressed:
                return self.function(self)
            self.dirty = True
        else:
            if self.hover:
                self.dirty = True
            self.hover = False
            self.pressed = False
        return False






