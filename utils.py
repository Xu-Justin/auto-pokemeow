import mouse as _mouse
import keyboard as _keyboard
import time
import numpy as np
from PIL import ImageGrab
from PIL import ImageDraw
from PIL import ImageFont
import json
import logging
import random
import math
import screeninfo
import matplotlib.pyplot as plt
from types import SimpleNamespace

DRAW_OUTLINE_COLOR = 'red'
FONT = ImageFont.load_default()
DRAW_TEXT_OFFSET_Y = -20

def logger():
    log = logging.getLogger()
    log.setLevel(logging.NOTSET)
    console_handler = get_console_handler(logging.INFO)
    log.addHandler(console_handler)
    return log

def get_console_handler(level):
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler_format = '%(asctime)s | %(levelname)s: %(message)s'
    console_handler.setFormatter(logging.Formatter(console_handler_format))
    return console_handler

class config:
    def load(file):
        with open(file, 'r') as f:
            return json.load(f)
    
    def validate_panel(panel):
        if type(panel) not in (list, tuple): raise TypeError(f'Unexpected panel type : {type(panel)}')
        xmin, ymin, xmax, ymax = panel
        if xmin > xmax: raise ValueError(f'Unexpected xmin : {xmin} greater than xmax : {xmax}')
        if ymin > ymax: raise ValueError(f'Unexpected ymin : {ymin} greater than ymax : {ymax}')

    def validate_single_color(color):
        if type(color) != int: raise TypeError(f'Unexpected color type : {type(color)}')
        if color < 0 or color > 255: raise ValueError(f'Unexpected color value : {color}')

    def validate_color(color):
        if type(color) not in (list, tuple): raise TypeError(f'Unexpected color type : {type(color)}')
        r, g, b = color
        config.validate_single_color(r)
        config.validate_single_color(g)
        config.validate_single_color(b)
        
    def load_panel(cfg, key):
        panel = cfg[key]
        config.validate_panel(panel)
        return panel
        
    def load_input_panel(cfg):
        return config.load_panel(cfg, 'input_panel')

    def load_color_panel(cfg):
        return config.load_panel(cfg, 'color_panel')
    
    def load_colors(cfg):
        colors = cfg['colors']
        for _, color in colors.items():
            config.validate_color(color)
        return colors

    def load_color_tolerance(cfg):
        return cfg['color_tolerance']
    
    def load_balls(cfg):
        balls = cfg['balls']
        for key, details in balls.items():
            panel = details['panel']
            config.validate_panel(panel)
            catch_rarity = details['catch_rarity']
            balls[key] = SimpleNamespace()
            balls[key].name = key
            balls[key].panel = panel
            balls[key].catch_rarity = catch_rarity
        return balls
    
    def load_commands(cfg):
        return cfg['commands']

    def _load_kwargs(kwargs, _kwargs, key, default_value):
        kwargs[key] = _kwargs.get(key, default_value)

    def load_kwargs(cfg):
        _kwargs = cfg.get('kwargs', {})
        kwargs = {}
        config._load_kwargs(kwargs, _kwargs, 'sleep_after_iteration', [7, 20])
        config._load_kwargs(kwargs, _kwargs, 'sleep_after_command', [1.5, 2.5])
        config._load_kwargs(kwargs, _kwargs, 'sleep_after_move_cursor', [0.5, 2])
        config._load_kwargs(kwargs, _kwargs, 'cursor_duration', [0.1, 0.5])
        config._load_kwargs(kwargs, _kwargs, 'sleep_after_iteration_preview', 1)
        return kwargs

def get_screen_resolution():
    screen = screeninfo.get_monitors()[0]
    return screen.width, screen.height

def get_preview_panels(input_panel, color_panel, balls):
    panels = []
    panels.append(('input_panel', input_panel))
    panels.append(('color_panel', color_panel))
    for key, details in balls.items():
        panels.append((key, details.panel))
    
    width, height = get_screen_resolution()
    image = get_screen_image(0, 0, width, height)
    draw = ImageDraw.Draw(image)
    for name, panel in panels:
        xmin, ymin, xmax, ymax = panel
        draw.rectangle((xmin, ymin, xmax, ymax), outline=DRAW_OUTLINE_COLOR)
        draw.text((xmin, ymin + DRAW_TEXT_OFFSET_Y), name, font=FONT)
    return image


def random_xy(xmin, ymin, xmax, ymax):
    x = random.randint(xmin, xmax)
    y = random.randint(ymin, ymax)
    return x, y

class cursor:
    def move(x, y, duration=1):
        _mouse.move(x, y , absolute=True, duration=duration)

    def left_click():
        _mouse.click()

    def right_click():
        _mouse.right_click()

class keyboard:
    def write(text):
        _keyboard.write(text)

    def enter():
        _keyboard.press('enter')

def get_screen_image(xmin, ymin, xmax, ymax):
    return ImageGrab.grab(bbox = (xmin, ymin, xmax, ymax))

def average_image_color(image):
    return np.array(image).mean(axis=(0, 1))

def color_dif(color_1, color_2):
    value = 0
    for c1, c2 in zip(color_1, color_2):
        value += math.pow(abs(c1 - c2), 2)
    value = math.sqrt(value)
    return value
    
def match_color(source, colors, color_tolerance):
    result = None
    result_dif = None
    for name, color in colors.items():
        dif = color_dif(source, color)
        if dif < color_tolerance:
            if result is None or dif < result_dif:
                result = name
                result_dif = dif
    return result

def match_ball(rarity, balls):
    for _, ball in balls.items():
        if rarity in ball.catch_rarity:
            return ball
    return None

def sleep(second):
    time.sleep(second)

def display_image(image):
    plt.imshow(image)
    plt.show()