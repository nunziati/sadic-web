import json
from channels.generic.websocket import WebsocketConsumer
import time

class ProgressConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        for i in range(1, 101):
            time.sleep(0.1)  # Simula il progresso
            self.send(json.dumps({"progress": i}))

        self.close()
