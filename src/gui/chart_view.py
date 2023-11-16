''' Handles the matplotlib chart embedding and interactions.'''
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class ChartView(ctk.CTkFrame):
    ''' Manage the list of CSV headers. '''
    def __init__(self, parent):
        super().__init__(parent)
