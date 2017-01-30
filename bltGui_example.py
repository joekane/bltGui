from bltGui import bltFrame as Frame
from bltGui import *

sample_text = '''
        The textwrap module can be used to format text for output in situations
        where pretty-printing is desired.  It offers programmatic functionality similar
        to the paragraph wrapping or filling features found in many text editors.
        '''

terminal.open()
terminal.set("window: size={0}x{1}, cellsize=auto, title='bltGui Demo'; font: .\cp437_16x16_alpha_plus.png, size=16x16, codepage=437".format(80, 50))
terminal.set("input: filter={keyboard+, mouse+}")
terminal.composition(True)
terminal.refresh()



frame_list = []


def initilize():




    dkrgry = bltColor('darkest grey').trans(200)

    control_frame = Frame(55, 30, 20 ,15, "Control Test", visible=True, draggable=True, skin='SOLID')
    #control_frame.add_control(bltButton(control_frame, control_frame.width/2, 5, "X", length=10, function=bltButton.close))
    control_frame.add_control(bltCloseFrameButton(control_frame))
    control_frame.add_control(bltTextBox(control_frame,2,2, "Text Box", length=9))
    control_frame.add_control(bltCheckBoxButton(control_frame, 2, 4, label="CheckboxA"))
    control_frame.add_control(bltCheckBoxButton(control_frame, 2, 5, label="CheckboxB"))
    control_frame.add_control(bltCheckBoxButton(control_frame, 2, 6, label="CheckboxC"))

    radio = bltRadio(control_frame,2, 9, label="Radio Button")
    control_frame.add_control(radio)

    radio_listener = Frame(30, 45, 18, 4, title="Radio Selection")
    print "Radio Events: {0}".format(radio.subscribers)
    radio.register('changed', radio_listener)





    sample_text_frame = Frame(5,30 , 10,10, visible=True )
    sample_text_frame.text = sample_text
    sample_text_frame.add_control(bltResizeFrameButton(sample_text_frame))

    sample_text_frame.add_control(bltButton(sample_text_frame, 8, 14, "Show Controls", function=control_frame.show))





    color_grad = bltColor.color_map(['red', 'blue'], [0,5])
    #color_grad = []


    x = 40
    y = 3

    for i, c in enumerate(color_grad):
        f = Frame(x, y, 20, 10, title="Test Box {0}".format(i), draggable=True, visible=True, skin='DOUBLE')
        f.color_skin['BKCOLOR'] = c
        f.color_skin['COLOR'] = 'darkest grey'
        frame_list.append(f)

        frame_list[-1].add_control(bltResizeFrameButton(frame_list[-1]))
        x += 1
        y += 1

    key = bltInput.update()
    mouse = bltInput.mouse

    slider_r_value = 254
    slider_g_value = 0
    slider_b_value = 0
    slider_a_value = 255



    def update_r_val(value):
        global slider_r_value
        slider_r_value = value
    def update_g_val(value):
        global slider_g_value
        slider_g_value = value
    def update_b_val(value):
        global slider_b_value
        slider_b_value = value
    def update_a_val(value):
        global slider_a_value
        slider_a_value = value

    color_picker = Frame(30, 30, 18, 11, "Color Picker", visible=True, draggable=True)

    r_slider = bltSlider(color_picker, 2, 2, 14, slider_r_value, min_val=0, max_val=255, update_func=update_r_val, label='R', style='fill')
    g_slider = bltSlider(color_picker, 2, 4, 14, slider_g_value, min_val=0, max_val=255, update_func=update_g_val, label='G', style='fill')
    b_slider = bltSlider(color_picker, 2, 6, 14, slider_b_value, min_val=0, max_val=255, update_func=update_b_val, label='B', style='fill')
    a_slider = bltSlider(color_picker, 2, 8, 14, slider_a_value, min_val=0, max_val=255, update_func=update_a_val, label='A', style='fill')





    color_picker.add_control([r_slider, g_slider, b_slider, a_slider])
    color_picker.add_control(bltResizeFrameButton(color_picker))

    frame_list.append(color_picker)
    frame_list.append(control_frame)
    frame_list.append(sample_text_frame)
    frame_list.append(radio_listener)


    tb = bltTextBox(None, 25, 1, text="TEST")


def render():
    for f in frame_list:

        f.draw()

def update():
    frame_list.sort(key=lambda x: x.layer, reverse=True)
    for f in frame_list:
        f.update()


def draw_demo():
    terminal.layer(1)

    background = Frame(1, 1, 78, 23, bkcolor='20,20,20', frame=False, visible=True, layer=0)

    x, y = 4, 2

    terminal.color('230,230,230')

    terminal.puts(x - 2, y, "[c=amber]1. [/c]Set alpha.")
    color_a = bltColor('flame')
    terminal.puts(x, y + 1, "[c={0}]{0}[/c].trans(128) = [c={1}]{0}".format(color_a, color_a.trans(128)))

    y += 3

    terminal.puts(x - 2, y, "[c=amber]2. [/c]Multiply color by float.")
    color_a = bltColor('green')
    terminal.puts(x, y + 1, "[c={0}]{0}[/c] * 0.25 = [c={1}]{0}".format(color_a, color_a * 0.25))

    y += 3

    terminal.puts(x - 2, y, "[c=amber]3. [/c]Multiply two colors.")
    color_a = bltColor('sky')
    color_b = bltColor('purple')
    terminal.puts(x, y + 1, "[c={0}]{0}[/c] * [c={1}]{1}[/c] = [c={2}]Result".format(color_a,
                                                                                     color_b,
                                                                                     color_a * color_b))

    y += 3

    terminal.puts(x - 2, y, "[c=amber]4. [/c]Subtract two colors.")
    color_a = bltColor('sky')
    color_b = bltColor('purple')
    terminal.puts(x, y + 1,
                  "[c={0}]{0}[/c] - [c={1}]{1}[/c] = [c={2}]Result".format(color_a,
                                                                           color_b,
                                                                           color_a - color_b))

    y += 3

    terminal.puts(x - 2, y, "[c=amber]5. [/c]Add two colors.")
    color_a = bltColor('sky')
    color_b = bltColor('purple')
    terminal.puts(x, y + 1,
                  "[c={0}]{0}[/c] + [c={1}]{1}[/c] = [c={2}]Result".format(color_a,
                                                                           color_b,
                                                                           color_a + color_b))

    y += 3

    terminal.puts(x - 2, y, "[c=amber]6. [/c]Blend two colors w/ bias.")
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

    terminal.puts(x - 2, y, "[c=amber]7. [/c]Color map.[c=grey] bltColor.color_map(color_list, key_list)[/c]")
    color_list = ['red', 'orange', 'yellow', 'green', 'purple']
    key_list = [0, 25, 30, 50, 60]
    cmap = bltColor.color_map(color_list, key_list)
    for c in cmap:
        terminal.puts(x, y + 1, "[c={0}][U+2588]".format(c))
        x += 1

    background.draw()

initilize()
#draw_demo()

list_frame = Frame(3,5,9,6, "", frame=True, draggable=False)
content_frame = bltShowListFrame(12,5,25,20, "", frame=True, draggable=False)

list_box = bltListbox(list_frame, 1, 1, ['Item 1', 'Item 2', 'Item 3', 'Item 4'])
list_frame.add_control(list_box)
content_frame.add_control(bltResizeFrameButton(content_frame))
list_box.register('changed', content_frame)


modal = bltModalFrame(45,5,7,7, "Modal", frame=True, draggable=True)
modal.add_control(bltResizeFrameButton(modal))


frame_list.append(list_frame)
frame_list.append(content_frame)
frame_list.append(modal)

while True:
    key = bltInput.update()

    if key in [terminal.TK_CLOSE, terminal.TK_ESCAPE]:
        break

    update()
    render()


    terminal.refresh()






terminal.close()
