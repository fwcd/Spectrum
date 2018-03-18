class Paintable:
    def __init__(self):
        self.canvas_items = []
        self.childs = []
        self.needs_repaint = True
        
        # Initialized when added to a SpectrumCanvas
        self.parent = None
        self.canvas = None
    
    def add_child(self, paintable):
        self.childs.append(paintable)
        self.needs_repaint = True
    
    def paint(self):
        if self.needs_repaint:
            self.clear()
            self.paint_me()
            for child in self.childs:
                child.paint()
            self.needs_repaint = False
    
    def repaint_later(self):
        self.needs_repaint = True
    
    def clear(self):
        while len(self.canvas_items) > 0:
            self.canvas.delete(self.canvas_items.pop())
    
    def bind(self, bound_input, bound_function):
        self.parent.bind(bound_input, bound_function)
    
    def draw(self, canvas_method_name, *args, **kwargs):
        self.canvas_items.append(self.canvas.__getattribute__(canvas_method_name)(*args, **kwargs))
    
    def setup_canvas(self):
        pass
        
    def paint_me(self):
        pass