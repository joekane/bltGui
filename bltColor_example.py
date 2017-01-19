# coding=utf8
from bearlibterminal import terminal

class bltColor(str):
    def __new__(cls, value, *args, **kwargs):
        # explicitly only pass value to the str constructor
        if isinstance(value, str):
            if any(char.isdigit() for char in value):
                value = value.replace(" ", "")
        return super(bltColor, cls).__new__(cls, value)

    def __init__(self, color):
        # long.__init__(self, terminal.color_from_name(color))

        if isinstance(color, str):
            self.colorname = color
            self.color = terminal.color_from_name(self.colorname)
        else:
            self.colorname = color
            self.color = color
            # super(bltColor, self).__init__()

    def __str__(self):
        """ Returns object as str for use in formatting tags """
        return str(self.colorname)


    def __add__(self, color2):
        r1, g1, b1, a1 = self.getRGB()
        r2, g2, b2, a2 = color2.getRGB()

        return bltColor(str(terminal.color_from_argb(
            a1,
            min(r1 + r2, 255),
            min(g1 + g2, 255),
            min(b1 + b2, 255),
        )))

    def __sub__(self, color2):
        r1, g1, b1, a1 = self.getRGB()
        r2, g2, b2, a2 = color2.getRGB()

        return bltColor(str(terminal.color_from_argb(
            a1,
            max(r1 - r2, 0),
            max(g1 - g2, 0),
            max(b1 - b2, 0),
        )))

    def __mul__(self, color2):
        if isinstance(color2, bltColor):
            r1, g1, b1, a1 = self.getRGB()
            r2, g2, b2, a2 = color2.getRGB()
            return bltColor(str(terminal.color_from_argb(
                a1,
                max(min(int(r1 * r2) // 255, 255), 0),
                max(min(int(g1 * g2) // 255, 255), 0),
                max(min(int(b1 * b2) // 255, 255), 0),
            )))
        else:
            r1, g1, b1, a1 = self.getRGB()
            r2, g2, b2, a2 = color2, color2, color2, 1.0
            return bltColor(str(terminal.color_from_argb(
                a1,
                max(min(int(r1 * r2), 255), 0),
                max(min(int(g1 * g2), 255), 0),
                max(min(int(b1 * b2), 255), 0),
            )))

    __rmul__ = __mul__

    @staticmethod
    def color_map(color_list, keylist):
        # TODO: List shoudl be tuple ( str , inex )
        total_len = keylist[-1]

        current_key = 0
        color_map = []
        for k, key in enumerate(keylist):
            color_map.append(bltColor(color_list[k]))
            try:
                interp_num = keylist[current_key+1] - keylist[current_key] - 1
                bias_inc = 1.0 / (interp_num + 2)
                bias = bias_inc
                for n in xrange(interp_num):
                    colorA = bltColor(color_list[current_key]).getRGB()
                    colorB = bltColor(color_list[current_key+1]).getRGB()

                    a = max(min(int(colorA[3] + ((colorB[3] - colorA[3]) * bias)), 255), 0)
                    r = max(min(int(colorA[0] + ((colorB[0] - colorA[0]) * bias)), 255), 0)
                    g = max(min(int(colorA[1] + ((colorB[1] - colorA[1]) * bias)), 255), 0)
                    b = max(min(int(colorA[2] + ((colorB[2] - colorA[2]) * bias)), 255), 0)

                    color_map.append(bltColor(str(terminal.color_from_argb(a, r, g, b))))
                    bias += bias_inc
                current_key += 1
            except:
                pass
        return color_map


    def getRGB(self):
        """ Provides RGB values of name, usually for use in alpha transparency """
        #red = 0
        #green = 0
        #blue = 0
        #alpha = 0

        #if isinstance(self.colorname, str):
        blue = (self.color >> 0) & 255
        green = (self.color >> 8) & 255
        red = (self.color >> 16) & 255
        alpha = (self.color >> 24) & 255
        #print alpha, red, green, blue



        return int(red), int(green), int(blue), int(alpha)

    def blend(self, color2, bias=0.5, alpha=255 ):
        """Returns bltColor halfway between this color and color2"""
        colorA = self.getRGB()
        colorB = color2.getRGB()

        a = max(min(int(colorA[3] + ((colorB[3] - colorA[3]) * bias)), 255), 0)
        r = max(min(int(colorA[0] + ((colorB[0] - colorA[0]) * bias)), 255), 0)
        g = max(min(int(colorA[1] + ((colorB[1] - colorA[1]) * bias)), 255), 0)
        b = max(min(int(colorA[2] + ((colorB[2] - colorA[2]) * bias)), 255), 0)

        return bltColor(str(terminal.color_from_argb(a, r, g, b)))

    def trans(self, alpha_value):
        """Returns a color with the alpha_value"""
        r, g, b, a= self.getRGB()
        #print alpha_value, r, g, b
        alpha_value = max(min(alpha_value, 255), 1)
        return bltColor(str(terminal.color_from_argb(alpha_value, r, g, b)))


def drawRect(x, y, width, height):
    for w in xrange(width):
        for h in xrange(height):
            terminal.printf(x + w, y + h, "[U+2588]")


terminal.open()
terminal.set("window: size=80x25, cellsize=auto, title='bltColor Example';"
            "font: default;"
            "input: filter={keyboard}")
terminal.composition(True)

key = None

while True:
    terminal.clear()

    terminal.color(bltColor('20, 20, 20'))
    drawRect(1,1, 78, 23)

    x, y = 4, 2

    terminal.color('230,230,230')

    terminal.puts(x-2, y, "[c=amber]1. [/c]Set alpha.")
    color_a = bltColor('flame')
    terminal.puts(x, y + 1, "[c={0}]{0}[/c].trans(128) = [c={1}]{0}".format(color_a, color_a.trans(128)))

    y += 3

    terminal.puts(x-2, y, "[c=amber]2. [/c]Multiply color by float.")
    color_a = bltColor('green')
    terminal.puts(x, y + 1, "[c={0}]{0}[/c] * 0.25 = [c={1}]{0}".format(color_a, color_a * 0.25))

    y += 3

    terminal.puts(x-2, y, "[c=amber]3. [/c]Multiply two colors.")
    color_a = bltColor('sky')
    color_b = bltColor('purple')
    terminal.puts(x, y + 1, "[c={0}]{0}[/c] * [c={1}]{1}[/c] = [c={2}]Result".format(color_a, color_b, color_a * color_b))

    y += 3

    terminal.puts(x-2, y, "[c=amber]4. [/c]Subtract two colors.")
    color_a = bltColor('sky')
    color_b = bltColor('purple')
    terminal.puts(x, y + 1,
                  "[c={0}]{0}[/c] - [c={1}]{1}[/c] = [c={2}]Result".format(color_a, color_b, color_a - color_b))

    y += 3

    terminal.puts(x-2, y, "[c=amber]5. [/c]Add two colors.")
    color_a = bltColor('sky')
    color_b = bltColor('purple')
    terminal.puts(x, y + 1,
                  "[c={0}]{0}[/c] + [c={1}]{1}[/c] = [c={2}]Result".format(color_a, color_b, color_a + color_b))

    y += 3

    terminal.puts(x-2, y, "[c=amber]6. [/c]Blend two colors w/ bias.")
    color_a = bltColor('red')
    color_b = bltColor('blue')
    terminal.puts(x, y + 1,
                  "[c={0}]{0}[/c].blend([c={1}]{1}[/c], 0.25) = [c={2}]Result".format(color_a,
                                                                                      color_b,
                                                                                      color_a.blend(color_b,
                                                                                                    bias=0.25)))
    terminal.puts(x, y + 2,
                  "[c={0}]{0}[/c].blend([c={1}]{1}[/c], 0.75) = [c={2}]Result".format(color_a,
                                                                                      color_b,
                                                                                      color_a.blend(color_b,
                                                                                                    bias=0.75)))

    y += 4

    terminal.puts(x-2, y, "[c=amber]7. [/c]Color map.[c=grey] bltColor.color_map(color_list, key_list)[/c]")
    color_list = ['red', 'orange', 'yellow', 'green', 'purple']
    key_list = [0,10,40,50,60]
    cmap = bltColor.color_map(color_list, key_list)
    for c in cmap:
        terminal.puts(x, y + 1, "[c={0}][U+2588]".format(c))
        x += 1

    terminal.refresh()


    key = terminal.read()
    if key in [terminal.TK_CLOSE, terminal.TK_ESCAPE]:
        break


terminal.close()
