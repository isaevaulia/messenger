from datetime import datetime

import requests
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from clientui import Ui_MainWindow


class Messenger(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, url):
        super().__init__()
        self.setupUi(self)
        self.url = url
        self.after_timestamp = 0

        self.sendButton.pressed.connect(self.button_pressed)

        self.load_messages

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_message)
        self.timer.start(1000)

    def pretty_print(self, message):
        """
        2020/09/08 10:00:23 Nick
        text

        """
        dt = datetime.fromtimestamp(message['timestamp'])
        dt = dt.strftime('%Y/%m/%d  %H:%M:%S')

        first_line = dt + '  ' + message['name']
        self.textBrowser.append(first_line)
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')

    def update_message(self):
        response = None
        try:
            response = requests.get(self.url+'/messages', params={'after_timestamp': self.after_timestamp})
        except:
            pass

        if response and response.status_code == 200:
            messages = response.json()['messages']
            for message in messages:
                self.pretty_print(message)
                self.after_timestamp = message['timestamp']

            return messages


    def load_messages(self):
        while self.update_message():
            pass


    def button_pressed(self):
        text = self.textInput.toPlainText()
        name = self.nameInput.text()
        data = {'name': name, 'text': text}
        response = None
        try:
            response = requests.post(self.url+'/send', json=data)
        except:
            pass
        if response and response.status_code == 200:
            self.textInput.clear()
        else:
            self.textBrowser.append('error')



app = QtWidgets.QApplication([])
window = Messenger('http://127.0.0.1:5000')
window.show()
app.exec_()