import logging

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')
        self.handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(self.handler)

    def log(self, item):
        self.logger.info(item)
        print(item)
        
    