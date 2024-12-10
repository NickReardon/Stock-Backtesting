# decorators.py
import logging
import time
import plot_utils as utils
from mpl_canvas import MplCanvas

# Configure logging
logging.basicConfig(level=logging.INFO)

class PlotDecorator(MplCanvas):
    def __init__(self, base_canvas, customize_plot=True, adjust_margins=True):
        self.base_canvas = base_canvas
        self.customize_plot = customize_plot
        self.adjust_margins = adjust_margins
        MplCanvas.__init__(self)

    def plot(self, plot_func, data, ticker):
        start_time = time.time()
        logging.info(f"Starting plot for {ticker}")

        try:
            # Clear the canvas
            self.base_canvas.axes.clear()

            # Call the original plot function
            plot_func(self.base_canvas.axes, data, ticker)

            # Customize the plot if enabled
            if self.customize_plot:
                utils.customize_plot(self.base_canvas.axes, ticker, plot_func.__name__)

            # Adjust margins if enabled
            if self.adjust_margins:
                self.base_canvas.adjust_margins()

            # Draw the canvas
            self.base_canvas.draw()

        except Exception as e:
            logging.error(f"Error while plotting {ticker}: {e}")
            raise

        end_time = time.time()
        logging.info(f"Completed plot for {ticker} in {end_time - start_time:.2f} seconds")