# decorators.py
from functools import wraps
import plot_utils as utils
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

class PlotDecorator:
    def __init__(self, customize_plot=True, adjust_margins=True):
        self.customize_plot = customize_plot
        self.adjust_margins = adjust_margins

    def __call__(self, plot_func):
        @wraps(plot_func)
        def wrapper(fig, data, transactions, ticker):
            start_time = time.time()
            logging.info(f"Starting plot for {ticker} using {plot_func.__name__}")

            try:
                # Call the original plot function
                plot_func(fig, data, transactions, ticker)

                # Customize the plot if enabled
                if self.customize_plot:
                    ax = fig.gca()
                    utils.customize_plot(ax, ticker, plot_func.__name__)

                # Adjust margins if enabled
                if self.adjust_margins:
                    self.adjust_margins_func(fig)

                # Draw the canvas
                fig.canvas.draw()

            except Exception as e:
                logging.error(f"Error while plotting {ticker} using {plot_func.__name__}: {e}")
                raise

            end_time = time.time()
            logging.info(f"Completed plot for {ticker} using {plot_func.__name__} in {end_time - start_time:.2f} seconds")

            return fig

        return wrapper

    @staticmethod
    def adjust_margins_func(fig):
        """Adjust margins based on the current size of the canvas."""
        width, height = fig.get_size_inches() * fig.dpi
        left_margin = utils.LEFT_MARGIN_LARGE if width < 800 else utils.LEFT_MARGIN_SMALL
        right_margin = utils.RIGHT_MARGIN_LARGE if width < 800 else utils.RIGHT_MARGIN_SMALL
        top_margin = utils.TOP_MARGIN_LARGE if height < 600 else utils.TOP_MARGIN_SMALL
        bottom_margin = utils.BOTTOM_MARGIN_LARGE if height < 600 else utils.BOTTOM_MARGIN_SMALL
        fig.subplots_adjust(left=left_margin, bottom=bottom_margin, right=1-right_margin, top=1-top_margin)