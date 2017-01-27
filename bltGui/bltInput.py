from bearlibterminal import terminal


class Mouse:
    def __init__(self):
        self.active_layer = 0
        pass

    @property
    def pos(self):
        return terminal.state(terminal.TK_MOUSE_X), terminal.state(terminal.TK_MOUSE_Y)

    @property
    def cx(self):
        return terminal.state(terminal.TK_MOUSE_X)

    @property
    def cy(self):
        return terminal.state(terminal.TK_MOUSE_Y)

    @property
    def lbutton_pressed(self):
        if key == terminal.TK_MOUSE_LEFT:
            #print "Clicked on Layer: {0}".format(self.active_layer)
            return True
        else:
            return False

    @property
    def rbutton_pressed(self):
        if key == terminal.TK_MOUSE_RIGHT:
            return True
        else:
            return False

    @property
    def lbutton(self):
        result = bool(terminal.state(terminal.TK_MOUSE_LEFT))
        return result

    @property
    def rbutton(self):
        result = bool(terminal.state(terminal.TK_MOUSE_RIGHT))
        return result

    def clicked_rect(self, x, y, w, h, buttton=None, layer=0):
        if buttton == 'LEFT':
            button_pressed = self.lbutton_pressed
        elif buttton == 'RIGHT':
            button_pressed = self.rbutton_pressed
        else:
            button_pressed = self.lbutton_pressed

        if button_pressed and x <= mouse.cx <= x + w - 1 and y <= mouse.cy <= y + h - 1:
            result = True
        else:
            return False

        if layer >= self.active_layer:
            #print "mod"
            self.active_layer = layer
            return result
        else:
            return False

    def hover_rect(self, x, y, w, h, layer=0):

        if x <= mouse.cx <= x + w - 1 and y <= mouse.cy <= y + h - 1:
            result = True
        else:
            return False

        if layer >= self.active_layer:
            #print "Layer {0} is > {1}, setting.".format(layer, self.active_layer)
            self.active_layer = layer
            return result
        else:
            return False


key = None
mouse = Mouse()


def update():
    global key
    mouse.active_layer = 0
    if terminal.has_input():
        key = terminal.read()
    else:
        key = None
    return key


def read_key_chr():
    return terminal.state(terminal.TK_CHAR)


def console_coords():
    global mouse
    return mouse.cx, mouse.cy


def clear():
    while terminal.has_input():
        terminal.read()




