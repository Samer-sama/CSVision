''' Defines the UI and logic for the selected header panel. '''
import customtkinter as ctk
from gui.header_list_panel import HeaderListPanel


class HeaderPanel(ctk.CTkFrame):
    ''' Manage the display of the selected headers. '''
    def __init__(self, parent):
        super().__init__(parent)
