import json

from .gwb_io import GWBIo
from component  import parameter as cp

class SpaIo(GWBIo):
    
    def __init__(self):
        
        # the init file
        self.file = None
        
        # all the bytes values 
        self.background = []
        self.foreground = []
        
        # the process 
        self.options = None
        
        super().__init__(process = 'spa')
    
    def update_byte_list(self):
        """manually update the byte_list"""
        
        byte_list = [
            self.background,
            self.foreground
        ]
        
        return super().update_byte_list(byte_list)
    
    def update_params_list(self):
        """manually update the params list"""
        
        params_list = [
                self.options
            ]
        
        return super().update_params_list(params_list)
    
    def get_params_list(self):
        """get the params list for naming purposes (_ and no spaces)"""
        
        self.update_params_list()
        
        params = self.params_list
        
        return super().get_params_list(params)