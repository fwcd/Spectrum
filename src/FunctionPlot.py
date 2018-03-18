import math

from Paintable import Paintable
from Utilities import float_str, normalize

class FunctionPlot(Paintable):
    def __init__(self, x, y, width, height):
        super().__init__()
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.start = 0
        self.end = 10
        self.v_min = math.inf
        self.v_max = -math.inf
        self.highlighted_value = None
        
        self.func = math.sin
        self.line_color = "yellow"
        self.axis_color = "white"
        self.highlighted_value_color = "cyan"
        self.label_color = "gray"
        self.axis_arrow_size = 8
    
    def set_highlighted_value(self, value):
        self.highlighted_value = value
        self.needs_repaint = True
    
    def apply_function(self, x, value_if_absent = None):
        if self.func == None:
            return value_if_absent
        else:
            return self.func(x)
    
    def plot_function(self, plotted_function):
        self.func = plotted_function
        self.needs_repaint = True
    
    # Override
    def paint_me(self):
        last_x = None
        last_y = None
        min_x = self.x
        min_y = self.y
        max_x = self.x + self.width
        max_y = self.y + self.height
        
        # Draw value highlight
        if self.highlighted_value != None:
            line_x = min_x + normalize(self.highlighted_value, self.start, self.end) * self.width
            self.draw("create_line", line_x, min_y, line_x, max_y, fill = self.highlighted_value_color)
        
        # Draw function
        if self.func != None:
            for point_x, point_y in self.sample_points():
                if last_x != None and last_y != None:
                    self.draw("create_line", last_x, last_y, point_x, point_y, fill = self.line_color)
                
                last_x = point_x
                last_y = point_y
        
        # Draw x-axis
        self.draw("create_line", min_x, max_y, min_x, min_y, fill = self.axis_color)
        self.draw("create_line", min_x, min_y, min_x - self.axis_arrow_size, min_y + self.axis_arrow_size, fill = self.axis_color)
        self.draw("create_line", min_x, min_y, min_x + self.axis_arrow_size, min_y + self.axis_arrow_size, fill = self.axis_color)
        self.draw("create_text", min_x, max_y + (2 * self.axis_arrow_size), text = float_str(self.start), fill = self.label_color)
        self.draw("create_text", max_x, max_y + (2 * self.axis_arrow_size), text = float_str(self.end), fill = self.label_color)
        
        # Draw y-axis
        self.draw("create_line", min_x, max_y, max_x, max_y, fill = self.axis_color)
        self.draw("create_line", max_x, max_y, max_x - self.axis_arrow_size, max_y - self.axis_arrow_size, fill = self.axis_color)
        self.draw("create_line", max_x, max_y, max_x - self.axis_arrow_size, max_y + self.axis_arrow_size, fill = self.axis_color)
        self.draw("create_text", min_x - (2 * self.axis_arrow_size), min_y, text = float_str(self.v_max), fill = self.label_color)
        self.draw("create_text", min_x - (2 * self.axis_arrow_size), max_y, text = float_str(self.v_min), fill = self.label_color)
    
    def sample_points(self):
        values = list(self.sample_values())
        self.v_max = max([self.v_max, max(values)])
        self.v_min = min([self.v_min, min(values)])
        v_range = self.v_max - self.v_min
        i = 0
        
        for value in values:
            yield (self.x + i, self.y + self.height - (normalize(value, self.v_min, self.v_max, v_range) * self.height))
            i += 1
    
    def sample_values(self):
        step = (self.end - self.start) / self.width
        x = self.start
        
        while x < self.end:
            yield self.func(x)
            x += step