# Names: Daniel Katz and Will Carter
word_values = [x for x in range(0, 26)] * 2
dict_name = 'd.txt'

def encrypt(message, n):
    message = message.upper()
    n = n % 26
    ascii_list = []
    for i in message:
        ascii_list.append(ord(i) - 65)

    for i in range(len(ascii_list)):
        temp_ascii = ascii_list[i]
        if temp_ascii >= 0 and temp_ascii < 26:
            ascii_list[i] = word_values[temp_ascii+n]

    out = ''
    for i in ascii_list:
        out += chr(i + 65)

    return out

def decrypt(message, n):
    return encrypt(message, -n)

def auto_break(message):
    dictionary = open_file(dict_name)
    points = dict()
    for i in range(1,27):
        curr_points = 0
        message = encrypt(message, 1)
        for string in dictionary:
            for j in range(len(message) - len(string)):
                if(message[j:j+len(string)] == string):
                    curr_points += 1
        points[i] = curr_points

    reverse_points = {x: y for y, x in points.items()}
    x = reverse_points[max(points.values())]
    
    return encrypt(message, x)


        

def open_file(filename):
    with open(filename, 'r') as file:
        dictionary = []
        for line in file:
            dictionary.append(line.upper().strip())
        return dictionary

def main():
    message = 'hello'
    print(message)
    x = encrypt(message, 18)
    print(x)
    y = auto_break(x)
    print(y)

main()
