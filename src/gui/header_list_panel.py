''' Defines the UI and logic for the header list panel. '''
import customtkinter as ctk


class HeaderListPanel(ctk.CTkFrame):
    ''' Manage the list of CSV headers. '''
    def __init__(self, parent):
        super().__init__(parent)
