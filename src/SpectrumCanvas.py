from tkinter import Tk, Canvas

class SpectrumCanvas:
    def __init__(self, width = 640, height = 480):
        self.width = width
        self.height = height
        
        self.refresh_rate = 1000 // 60 # ms
        self.background = "black"
        self.canvas_items = []
        
        self.root = Tk()
        self.root.title("Spectrum")
        self.root.minsize(width, height)
        self.root.maxsize(width, height)
        self.root.resizable(width = False, height = False)
        self.root.after(0, self.__paint_canvas)
        
        self.input_binds = {}
        
        self.canvas = Canvas(self.root, width = width, height = height, highlightthickness = 0)
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill = self.background)
        self.canvas.pack()
    
    def launch_window(self):
        self.root.mainloop()
    
    def bind(self, bound_input, bound_function):
        if not bound_input in self.input_binds:
            def run_inputs(*args, **kwargs):
                for func in self.input_binds[bound_input]:
                    func(*args, **kwargs)
            
            self.canvas.bind(bound_input, run_inputs)
            self.input_binds[bound_input] = [bound_function]
        else:
            self.input_binds[bound_input].append(bound_function)
    
    def __paint_canvas(self):
        # Updates the canvas
        
        for paintable in self.canvas_items:
            paintable.paint()
        
        self.root.after(self.refresh_rate, self.__paint_canvas)
    
    def add_paintable(self, paintable):
        # Adds an instance of Paintable to the canvas
        paintable.parent = self
        paintable.canvas = self.canvas
        paintable.setup_canvas()
        self.canvas_items.append(paintable)