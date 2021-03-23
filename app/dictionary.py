with open("static/dictionary.txt", 'r') as f:
    lines = f.readlines()
    the_dictionary = set()
    for line in lines:
        the_dictionary.add(line.strip())

print(the_dictionary)