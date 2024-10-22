from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Define variables for margins and font sizes
LEFT_MARGIN_SMALL = 0.05
LEFT_MARGIN_LARGE = 0.1
RIGHT_MARGIN_SMALL = 0.05
RIGHT_MARGIN_LARGE = 0.1
TOP_MARGIN_SMALL = 0.05
TOP_MARGIN_LARGE = 0.1
BOTTOM_MARGIN_SMALL = 0.1
BOTTOM_MARGIN_LARGE = 0.2

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.adjust_margins()

    def adjust_margins(self):
        # Adjust margins based on the current size of the canvas
        width, height = self.get_width_height()
        left_margin = LEFT_MARGIN_LARGE if width < 800 else LEFT_MARGIN_SMALL
        right_margin = RIGHT_MARGIN_LARGE if width < 800 else RIGHT_MARGIN_SMALL
        top_margin = TOP_MARGIN_LARGE if height < 600 else TOP_MARGIN_SMALL
        bottom_margin = BOTTOM_MARGIN_LARGE if height < 600 else BOTTOM_MARGIN_SMALL
        self.figure.subplots_adjust(left=left_margin, bottom=bottom_margin, right=1-right_margin, top=1-top_margin)