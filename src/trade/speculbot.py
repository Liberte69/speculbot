import time
import requests

from datetime import datetime
from datetime import date
import yfinance as yf
from abc import ABC, abstractmethod

from utils.embedlogger import EmbedLogger

class SpeculBot(ABC):
    OPENING = time.time(hour=9, minute=31, second=2)
    CLOSING = time.time(hour=16, minute=0, second=0)

    def __init__(self, logger=EmbedLogger()):
        # Class properties
        self.url = None
        self.name = None
        self.num_API_calls = 0

        # Get symbols and relevant configurations
        self.open_config()

    @property
    def name(self):
        return self.name
    
    @property
    def url(self):
        return self.url
    
    @classmethod
    def is_market_open(cls):
        today = date.today().isoweekday()
        if today < 1 and today > 5: 
            return False

        now = datetime.now()
        if now < cls.OPENING and now > cls.CLOSING: 
            return False
    
        return True
    
    @abstractmethod
    def open_config(self):
        raise NotImplementedError(f"{type(self).__name__} fetch_data(symbols) not implemented")

    @abstractmethod
    def fetch_data(self, symbols):
        raise NotImplementedError(f"{type(self).__name__} fetch_data(symbols) not implemented")
    
    @abstractmethod
    def algorithm(self):
        raise NotImplementedError(f"{type(self).__name__} algorithm() not implemented")

    
    def send_notification(self, content: str):
        data = {
            "content" : content,
            "username" : self.name
        }

        result = requests.post(self.url, json=data)
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            pass

