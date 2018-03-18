import math

from ComplexPlane import ComplexPlane
from FunctionPlot import FunctionPlot
from Slider import Slider
from SpectrumCanvas import SpectrumCanvas
from Utilities import float_range, integral

class SpectrumMain:
    def __init__(self):
        self.canvas = None
        self.plane = None
        self.func_plot = None
        self.freq_slider = None
        self.fourier_plot = None
        self.winding_freq_slider = None
        self.time_integral_slider = None
    
    def main(self):
        self.canvas = SpectrumCanvas(width = 800, height = 480)
        
        self.plane = ComplexPlane(30, 30, 200, 200)
        self.canvas.add_paintable(self.plane)
        
        self.func_plot = FunctionPlot(300, 30, 400, 100)
        self.canvas.add_paintable(self.func_plot)
        
        self.fourier_plot = FunctionPlot(300, 160, 400, 100)
        self.canvas.add_paintable(self.fourier_plot)
        
        self.freq_slider = Slider(300, 300, 400, 20, min_value = 0.01, max_value = 10, label = "Frequency")
        self.freq_slider.add_change_listener(self.update_all)
        self.canvas.add_paintable(self.freq_slider)
        
        self.winding_freq_slider = Slider(300, 350, 400, 20, min_value = 0.01, max_value = 10, label = "Winding frequency")
        self.winding_freq_slider.add_change_listener(self.update_winding)
        self.canvas.add_paintable(self.winding_freq_slider)
        
        self.time_integral_slider = Slider(300, 400, 400, 20, min_value = 1, max_value = 10, label = "Time integral size")
        self.time_integral_slider.add_change_listener(self.update_fourier)
        self.canvas.add_paintable(self.time_integral_slider)
        
        self.canvas.launch_window()
    
    def default_fourier(self, freq):
        v = self.time_integral_slider.value
        return self.fourier(freq, 0, v, 0.05)
    
    def fourier(self, freq, t1, t2, dt = 0.05):
        return integral(self.winding_func, t1, t2, dt, f = freq).real
    
    def winding_func(self, t, f):
        return self.func_plot.apply_function(t) * (math.e ** complex(0, -2 * math.pi * f * t))
    
    def update_winding(self, winding_freq):
        self.fourier_plot.set_highlighted_value(winding_freq)
        self.plane.plot_connected_points([self.winding_func(t, winding_freq) * 10 for t in float_range(0, 10, 0.05)])
    
    def update_fourier(self, _v):
        return self.fourier_plot.plot_function(self.default_fourier)

    def update_all(self, _v):
        self.func_plot.plot_function(lambda x: math.sin(2 * math.pi * x * self.freq_slider.value))
        self.update_fourier(self.time_integral_slider.value)
        self.update_winding(self.winding_freq_slider.value)

if __name__ == "__main__":
    SpectrumMain().main()