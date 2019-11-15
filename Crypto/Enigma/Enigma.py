# global variables, cannot be modified inside a
# function, unless you use the keyword 'global'
# before modifying it in said function
# ex:
# def foo():
#   global SCRAMBLER_1 # now i can modify the SCRAMBLER_1 variable
#   SCRAMBLER_1[0] = "A" # obviously don't do this, but you may use as example

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

SCRAMBLER_1 = "NBCJGOLXREFWIVYUMTKSHADPZQ" # scrambler settings if set to 0
SCRAMBLER_2 = "KVDPHSRFTXQYMEZGONUAWILCJB" # scrambler settings if set to 0
SCRAMBLER_3 = "CDVQBSUNMAEFIZPYXJLRHKTGOW" # scrambler settings if set to 0

scrambler_list = [SCRAMBLER_1, SCRAMBLER_2, SCRAMBLER_3]
CONST_SCRAMBLER_LIST = tuple(scrambler_list)
plugboard = dict()

def main():
    message = input("Enter a message to encrypt: ").upper()
    swap_scrambler()
    scrambler_offset()
    set_plugboard()
    print(encrypt(message))

def encrypt(message):
    output = ''
    first = 0
    second = 0
    for i in message:
        if i not in ALPHABET:
            output += i
            continue
        
        output += encrypt_char(i)
        first, second = rotate_cypher(first, second)
    
    return output

def encrypt_char(char):
    char = scrambler_list[0][ord(char) - 65]
    char = scrambler_list[1][ord(char) - 65]
    char = scrambler_list[2][ord(char) - 65]
    if char in plugboard.keys():
        char = plugboard[char]
    
    return char

def rotate_cypher(first, second):
    first += 1
    rotate(0)
    if first == 26:
        first = 0
        rotate(1)
        second += 1
        if second == 26:
           second = 0
           rotate(2)

    return (first, second)

def rotate(scrambler_number):
    global scrambler_list
    cur_scrambler = scrambler_list[scrambler_number]
    cur_scrambler = cur_scrambler[25] + cur_scrambler[0:25]
    scrambler_list[scrambler_number] = cur_scrambler

def swap_scrambler():
    global scrambler_list
    order = input('Enter the order of the scrambles (1, 2, and 3) separated by a space: ')
    order = [int(i) for i in order.strip().split(' ')]
    for i in range(3):
        scrambler_list[i] = CONST_SCRAMBLER_LIST[order[i] - 1]

def scrambler_offset():
    global scrambler_list
    offset = input('Enter three integers between 0 and 25 separated by ' + 
                   'a space to change the inital offset of the cyphers ' +
                   'in the order of the user set cypher order: ')
    offset = [int(i) for i in offset.strip().split(' ')]
    for i in range(3):
        for _ in range(offset[i]):
            rotate(i)

def set_plugboard():
    global plugboard
    while True:
        add_to_plug = input('Enter in a letter pair or "stop" to not enter in any more pairs: ')
        add_to_plug = add_to_plug.strip().upper()
        if add_to_plug == 'STOP':
            break
        add_to_plug = [i for i in add_to_plug.split(' ')]

        if len(set(add_to_plug).intersection(plugboard.keys())) > 0:
            print('Please input a pair of keys that have not been inputed before')
            continue

        plugboard[add_to_plug[0]] = add_to_plug[1]
        plugboard[add_to_plug[1]] = add_to_plug[0]

main()
