from bearlibterminal import terminal
import bltInput
from bltControl import bltControl as Control
import bltSkins


class bltSlider(Control):
    def __init__(self, owner, x, y, width, value,
                 min_val=0,
                 max_val=100,
                 style='default',
                 update_func=None,
                 direction='VERTICAL',
                 label=None,
                 skin='DOUBLE'
                 ):
        Control.__init__(self)
        self.owner = owner
        self.x = x
        self.y = y
        self.width = width
        self.value = value
        self.value = max(min(self.value, max_val), min_val)
        self.min_val = min_val
        self.max_val = max_val
        self.value_per_cell = ((max_val - min_val)) / float(width)
        self.style = style
        self.dragging = False
        self.click_x = None
        self.update_func = update_func
        self.direction = direction
        if label:
            self.label = label + ": "
        else:
            self.label = ""
        self.skin = bltSkins.SKINS[skin]
        self.dirty = True
        self.frame_element = False


    def draw(self):
        if self.dirty:
            #draw slider
            mouse = bltInput.mouse
            terminal.color('darker azure')
            #terminal.puts(self.x, self.y, "[U+2588]"*(self.width))

            if self.owner:
                layer = self.owner.layer
                x = self.owner.pos.x
                y = self.owner.pos.y
            else:
                layer = terminal.state(terminal.TK_LAYER)
                x = 0
                y = 0
            terminal.layer(layer)


            terminal.puts(self.x + x , self.y + y, self.skin['SLIDER_L'])
            terminal.puts(self.x+ 1 + x, self.y + y, self.skin['SLIDER_MID'] * (self.width-2))
            terminal.puts(self.x + x  +  self.width - 1, self.y + y, self.skin['SLIDER_R'])



            #print "Slider: Val: {0}, Vpc: {1}".format(self.value, self.value_per_cell)


            offset = 0

            if self.style == 'default':
                terminal.color('dark yellow')
                terminal.puts(self.calc_length(x), self.y + y, self.get_pip_str())
            elif self.style == 'level':

                #terminal.puts(self.x + x, self.y + y, self.skin['BACKGROUND'] * (int(self.value / self.value_per_cell)-offset ))
                #terminal.color('dark yellow')
                #terminal.puts(self.calc_length(x) , self.y + y, self.get_pip_str())

                terminal.color('darkest azure')
                max = self.calc_length(x) + 1 - (self.x + x)
                for i, x1 in enumerate(xrange(self.x + x, max + (self.x + x))):
                    char = self.skin['BACKGROUND']
                    terminal.puts(x1, self.y + y, char)
                terminal.color('dark yellow')
                terminal.puts(self.calc_length(x), self.y + y, self.skin['SLIDER_PIP'])
            elif self.style == 'fill':
                terminal.color('darker yellow')
                max =  self.calc_length(x)+1 - (self.x + x)
                if max > 1:
                    #print "Max: {0}".format(max)
                    for i, x1 in enumerate(xrange(self.x + x, max + (self.x + x))):
                        char = self.get_line_str(i, max)
                        terminal.puts(x1 , self.y + y, char)
                terminal.color('dark yellow')
                terminal.puts(self.calc_length(x), self.y + y, self.skin['SLIDER_PIP'])
            terminal.puts(self.x + x, self.y + y + 1, "[c=darker grey]{0}{1}".format(self.label, self.value))
        self.dirty = False

    def update(self):
        mouse = bltInput.mouse
        if self.owner:
            layer = self.owner.layer
            x = self.owner.pos.x
            y = self.owner.pos.y
        else:
            layer = terminal.state(terminal.TK_LAYER)
            x = 0
            y = 0

        if mouse.clicked_rect(self.x + x, self.y + y, self.width, 1):
            self.dragging = True

        if mouse.lbutton and self.dragging:
            #if self.click_x is None:
            #    self.click_x = mouse.cx - self.x
            #self.value = ((mouse.cx - self.x)+1) * self.value_per_cell
            self.set_length(x, mouse.cx)

            #print "Slider: Val: {0}, Vpc: {1}".format(self.value, self.value_per_cell)
            self.dispatch(self.value)
            self.dirty = True
        else:
            self.dragging = False
            self.click_x = None

    def resized(self):
        self.clear()
        self.width = self.owner.width - 4
        self.value_per_cell = ((self.max_val - self.min_val)) / float(self.width)
        self.dirty = True

    def clear(self):
        # print "Clearing Layer: {0}".format(self.layer)

        terminal.layer(self.owner.layer-1)
        terminal.clear_area(self.x, self.y, self.width, 1)

    def get_pip_str(self, value=None):
        if not value:
            value = self.value
        if value == self.min_val:
            return self.skin['SLIDER_L']
        elif value < self.max_val:
            return self.skin['SLIDER_PIP']
        else:
            return self.skin['SLIDER_R']

    def get_line_str(self, value, max):
        #print max
        if value <= 0:
            return self.skin['SLIDER_L']
        elif value < max-1:
            return self.skin['SLIDER_MID']
        else:
            return self.skin['SLIDER_R']


    def calc_length(self,x):
        length = self.x + x + int((self.value - self.min_val) / self.value_per_cell)

        return min(max(length, 0 + self.x + x ),self.width + self.x + x - 1)

    def set_length(self, x, mouse_x):
        self.value = (((mouse_x - (self.x + x))+1) * self.value_per_cell)
        self.value = int(max(min(self.value, self.max_val), self.min_val))
        if self.update_func:
            self.update_func(self.value)







