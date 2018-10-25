
class MySentence:
    def __init__(self, sentence):
        self.list = sentence.split()
        self.counter = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.counter >= len(self.list):
            raise StopIteration
        else:
            self.counter +=1
            return self.list[self.counter - 1]

def mysentence(sentence):
    counter = 0
    words = sentence.split()
    while counter < len(words):
        yield words[counter]
        counter += 1


sentence = mysentence('This is a Sentence')

for word in sentence:
    print(word)
