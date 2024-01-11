file = open("dictionary.txt", "r")
words = file.readlines()
file.close()

sanitized_words = []
word_length = 5

for word in words:
    if len(word)==(word_length+1):
        sanitized_words.append(word)
        
file = open("sanitized_words_1.txt", "a")
for word in sanitized_words:
    file.write(word)