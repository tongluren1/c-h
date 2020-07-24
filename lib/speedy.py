
class speedy:
    def __init__(self):
        self.file = open('./log.txt', 'w', encoding='utf-8')

    def print_text(self, text_=''):
        self.file.write(text_)

    def __del__(self):
        self.file.close()
