from Paintable import Paintable
from builtins import complex

class ComplexPlane(Paintable):
    def __init__(self, x, y, width, height):
        super().__init__()
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.points = []
        self.connected_points = []
        self.offset_x = width / 2
        self.offset_y = -(height / 2)
        self.scale = 5.0
        
        self.grid_line_distance = 10
        self.grid_line_color = "yellow"
        self.axis_color = "magenta"
        self.point_color = "white"
        self.point_size = 10
        
        self.last_mouse_x = None
        self.last_mouse_y = None
        self.dragging = False
    
    def plot_connected_points(self, points):
        self.connected_points = points
        self.needs_repaint = True
    
    def set_points(self, points):
        self.points = points
        self.needs_repaint = True
    
    def add_point(self, complex_point):
        self.points.append(complex_point)
        self.needs_repaint = True
    
    def on_mouse_drag(self, event):
        if self.dragging or self.in_bounds(event.x, event.y):
            if self.last_mouse_x != None and self.last_mouse_y != None:
                self.offset_x += event.x - self.last_mouse_x
                self.offset_y += event.y - self.last_mouse_y
                
            self.last_mouse_x = event.x
            self.last_mouse_y = event.y
            self.needs_repaint = True
            self.dragging = True
    
    def on_mouse_release(self, event):
        self.last_mouse_x = None
        self.last_mouse_y = None
        self.dragging = False
    
    # Override
    def setup_canvas(self):
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease>", self.on_mouse_release)
    
    # Override
    def paint_me(self):
        min_x = self.x
        max_x = self.x + self.width
        min_y = self.y
        max_y = self.y + self.height
        
        for x in range(min_x, max_x + 1):
            if self.to_complex_point(x, 0).real % self.grid_line_distance == 0:
                self.draw("create_line", x, min_y, x, max_y, fill = self.grid_line_color)
        for y in range(min_y, max_y + 1):
            if self.to_complex_point(0, y).imag % self.grid_line_distance == 0:
                self.draw("create_line", min_x, y, max_x, y, fill = self.grid_line_color)
        
        point_radius = self.point_size / 2
        
        for complex_point in self.points:
            x, y = self.to_pixel_pos(complex_point)
            
            if self.in_bounds(x, y):
                self.draw("create_oval", x - point_radius, y - point_radius, x + point_radius, y + point_radius, fill = self.point_color, outline = "")
        
        last_x = None
        last_y = None
        
        for complex_point in self.connected_points:
            x, y = self.to_pixel_pos(complex_point)
            
            if self.in_bounds(x, y):
                if last_x != None and last_y != None:
                    self.draw("create_line", last_x, last_y, x, y, fill = self.point_color)
                
                last_x = x
                last_y = y
        
    def to_pixel_pos(self, complex_point):
        return (self.x + self.offset_x + (complex_point.real * self.scale), self.y + self.height + self.offset_y - (complex_point.imag * self.scale))
    
    def to_complex_point(self, x, y):
        return complex((x - self.x - self.offset_x) / self.scale, -(y - self.y - self.height - self.offset_y) / self.scale)
    
    def in_bounds(self, x, y):
        return x >= self.x and x < (self.x + self.width) and y >= self.y and y < (self.y + self.height)