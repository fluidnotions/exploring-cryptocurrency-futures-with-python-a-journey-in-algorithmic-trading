"""
This type stub file was generated by pyright.
"""

import threading

class BinanceSocketManager(threading.Thread):
    def __init__(self, stream_url) -> None:
        ...
    
    def add_connection(self, stream_name, url): # -> None:
        ...
    
    def stop_socket(self, conn_key): # -> None:
        ...
    
    def run(self): # -> None:
        ...
    
    def close(self): # -> None:
        ...
    

