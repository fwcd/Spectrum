from Paintable import Paintable
from Utilities import float_str

class Slider(Paintable):
    def __init__(self, x, y, width, height, min_value, max_value, label = None):
        super().__init__()
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scroller_width = min(width / 8, 20)
        self.listeners = []
        
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value
        self.value_per_pixel = (max_value - min_value) / width
        self.label = label
        
        self.background_color = "gray"
        self.scroller_color = "gray"
        self.label_color = "white"
        
        self.dragging = False
        self.last_mouse_x = None
    
    def add_change_listener(self, value_consumer_func):
        self.listeners.append(value_consumer_func)
    
    def on_mouse_drag(self, event):
        if self.dragging or self.scroller_box_contains(event.x, event.y):
            if self.last_mouse_x != None:
                dx = event.x - self.last_mouse_x
                self.value += self.value_per_pixel * dx
                
                for listener in self.listeners:
                    listener(self.value)
            
            self.last_mouse_x = event.x
            self.dragging = True
            self.needs_repaint = True
    
    def on_mouse_release(self, _event):
        self.dragging = False
        self.last_mouse_x = None
    
    # Override
    def setup_canvas(self):
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease>", self.on_mouse_release)
    
    # Override
    def paint_me(self):
        self.draw("create_rectangle", self.x, self.y, self.x + self.width, self.y + self.height, outline = self.background_color)
        
        x, y, w, h = self.get_scroller_box()
        self.draw("create_rectangle", x, y, x + w, y + h, fill = self.scroller_color, outline = "")
        
        formatted_value = float_str(self.value)
        t = formatted_value if self.label == None else self.label + ": " + formatted_value
        self.draw("create_text", self.x, self.y + (self.height * 1.5), text = t, fill = self.label_color)
    
    def get_normalized_value(self):
        return (self.value - self.min_value) / (self.max_value - self.min_value)
    
    def scroller_box_contains(self, x, y):
        s_x, s_y, s_w, s_h = self.get_scroller_box()
        return x > s_x and x < (s_x + s_w) and y > s_y and y < (s_y + s_h)
    
    def get_scroller_box(self):
        x_range = self.width - self.scroller_width
        x = self.x + (self.get_normalized_value() * x_range)
        
        return (x, self.y, self.scroller_width, self.height)