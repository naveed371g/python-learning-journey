sentence = input("Enter a sentence: ")
words = sentence.split()

# Creates a dictionary where the word is the key and its length is the value
word_lengths = {word: len(word.strip(".,!?")) for word in words}
print(word_lengths)
print("\nWord Lengths:")
for word, length in word_lengths.items():
    print(f"- '{word}': {length} characters")


print(type({}.)
