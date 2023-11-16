''' Defines the CSVision class with the main layout. '''
import customtkinter as ctk
import sys
from gui.header_panel import HeaderPanel
from gui.chart_view import ChartView
from utils.csv_data_manager import CSVDataManager


class CSVision(ctk.CTk):
    ''' Functionalities and layout of the main application. '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # security events
        self.bind('<Escape>', self.close_application)
        self.protocol('WM_DELETE_WINDOW', self.close_application)

        # Init members
        self._window_title = 'CSVision'
        self._icon = 'resources/CSVision_light.ico'
        self._width = 1500
        self._height = 900
        self._res_width = True
        self._res_height = True
        self._min_width = 900
        self._min_height = 600

        # Settings
        self.title(self._window_title)
        self.iconbitmap('resources/CSVision_light.ico')
        self.geometry(f'{self._width}x{self._height}+{int(self.winfo_screenwidth() / 2 - self._width / 2)}+{int(self.winfo_screenheight() / 2 - self._height / 2)}')
        self.minsize(self._min_width, self._min_height)
        self.resizable(self._res_width, self._res_height)

        # Configure the positioning
        self.grid_columnconfigure(0, weight=1, uniform='column')

        self.grid_rowconfigure(0, weight=20, uniform='row')                 # Content
        self.grid_rowconfigure(1, weight=1, uniform='row', minsize=50)      # Toolbar

        # Initilize widgets
        self.content_frame = ctk.CTkFrame(self)
        self.toolbar_frame = ToolbarPanel(self)

        # Layout widgets
        self.content_frame.grid(row=0, column=0, sticky='news')
        self.toolbar_frame.grid(row=1, column=0, sticky='news')

    def close_application(self, event=None):
        ''' Close the application. '''
        self.destroy()
        sys.exit(0)


class ConentPanel(ctk.CTkFrame):
    ''' Manage the content. '''
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Configure the positioning
        self.grid_columnconfigure(0, weight=1, uniform='column')  # Searchbar and header panels
        self.grid_columnconfigure(1, weight=5, uniform='column')  # Chart view
        self.grid_rowconfigure(0, weight=1, uniform='row')

        # Initilize widgets
        self.header_panel = HeaderPanel(self)
        self.chart_view = ChartView(self)

        # Layout widgets
        self.header_panel.grid(row=0, column=0, sticky='news')
        self.chart_view.grid(row=0, column=1, sticky='news')


class ToolbarPanel(ctk.CTkFrame):
    ''' Manage the toolbar. '''
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Configure the positioning
        self.grid_columnconfigure(0, weight=1, uniform='column')  # Settings button
        self.grid_columnconfigure(1, weight=7, uniform='column')  # Progressbar
        self.grid_columnconfigure(2, weight=7, uniform='column')  # File entry
        self.grid_columnconfigure(3, weight=3, uniform='column')  # File open button
        self.grid_rowconfigure(0, weight=1, uniform='row')

        # Initilize widgets
        self.settings_button = ctk.CTkButton(self)
        self.progressbar = ctk.CTkProgressBar(self)
        self.file_entry = ctk.CTkEntry(self)
        self.file_open_button = ctk.CTkButton(self)

        # Layout widgets
        self.settings_button.grid(row=0, column=0, sticky='news')
        self.progressbar.grid(row=0, column=1, sticky='news')
        self.file_entry.grid(row=0, column=2, sticky='news')
        self.file_open_button.grid(row=0, column=3, sticky='news')
