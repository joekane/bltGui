from bearlibterminal import terminal

class bltColor(str):
    def __new__(cls, value, *args, **kwargs):
        # explicitly only pass value to the str constructor
        if isinstance(value, str):
            if any(char.isdigit() for char in value):
                value = value.replace(" ", "")
        return super(bltColor, cls).__new__(cls, value)

    def __init__(self, color):
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

    def blend(self, color2, bias=0.5):
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
