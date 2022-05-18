from datetime import datetime

directory = '/home/jurek/Documents/Studia/VI/pracownia/elektrony/'


class ResultBuilder:

    def __init__(self, headers):
        self.text = []
        self.headers = headers

    def add(self, message):
        self.text.append(message)

    def save(self, filename):
        file = open(directory + datetime.now().strftime("%H_%M_%S_") + filename, "a")
        file.write('\t'.join(self.headers) + '\n')
        for message in self.text:
            file.write('\t'.join(message)+'\n')
        file.close()
        self.text = []


