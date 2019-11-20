# Daniel Katz, November 2019

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

SCRAMBLER_1 = "NBCJGOLXREFWIVYUMTKSHADPZQ" # scrambler settings if set to 0
SCRAMBLER_2 = "KVDPHSRFTXQYMEZGONUAWILCJB" # scrambler settings if set to 0
SCRAMBLER_3 = "CDVQBSUNMAEFIZPYXJLRHKTGOW" # scrambler settings if set to 0

# Creates a list a list where each entry is a cypher.
scrambler_list = [SCRAMBLER_1, SCRAMBLER_2, SCRAMBLER_3]

# Dicionary for the plugboard that will be filled in in set_plugboard()
plugboard = dict()

def main():
    # Get the message from the user and convert it to upper case so it 
    # works with the encyption.
    message = input("Enter a message to encrypt: ").upper()

    # Calls independant function that use global variables to store information about:
    # cypher order, individual cipher offset, and plugboard settings.
    swap_scrambler()
    scrambler_offset()
    set_plugboard()

    # Print out the starting position and offset of each of the cyphers,
    # with the alphabet above them for ease of reading. 
    print('\nHere are the initial cypher settings before encryption:')
    for i in scrambler_list:
        print(ALPHABET + '\n' + i + '\n')

    # Print the encypted message
    print(encrypt(message))

# Function that will encrypt the inputed message.
def encrypt(message):
    # Start an output variable that the encypted message
    # will be continuously appended to.
    output = ''

    # Variables to track cypher rotation position.
    first = 0
    second = 0

    # Iterate through each character in the message and encrypt and append it
    # if it is a letter or just appned if not a letter.
    for i in message:
        if i not in ALPHABET:
            output += i
            continue
        
        # Append the encypted letter to the output.
        output += encrypt_char(i)

        # Rotate the cyoher appropriately after each single encryption,
        # and store the counters for the cyphers in their respective variables.
        first, second = rotate_cypher(first, second)
    
    # Return the fully encrypted message.
    return output

def encrypt_char(char):
    # Pass the char along each cypher, using the ascii value to find
    # as the index to find the next char in the process.
    char = scrambler_list[0][ord(char) - 65]
    char = scrambler_list[1][ord(char) - 65]
    char = scrambler_list[2][ord(char) - 65]

    # If the char after all the cyphers is plugged into the plugboard.
    # If it is, change the char to its pair.
    if char in plugboard.keys():
        char = plugboard[char]
    
    # Return the totally encrypted char.
    return char

# Function to rotate the cyphers after each encryption.
def rotate_cypher(first, second):

    # The first cypher will always be rotated after each encyption,
    # so this code rotates it and increases the counter by one.
    first += 1
    rotate(0)

    # If the first cypher has made one full rotation, rotate the second 
    # and update the counter, as well as reset the counter for the first cypher.
    if first == 26:
        first = 0
        rotate(1)
        second += 1

        # Do the same action as the above one, but use rotate 
        # the third cypher and reset the counter for the second cypher.
        if second == 26:
           second = 0
           rotate(2)

    # Return the counters for the cyphers in a tuple.
    return (first, second) 

# Rotate each individual cypher based on the inputed char
def rotate(scrambler_number):
    # Allow the scrambler_list to be globally modified in the function.
    global scrambler_list

    # Get the scrmabler to rotate into a varibale, and modify it so
    # that it rotates to the right one letter, and then add it back
    # to the cur_scrambler list.
    cur_scrambler = scrambler_list[scrambler_number]
    cur_scrambler = cur_scrambler[25] + cur_scrambler[0:25]
    scrambler_list[scrambler_number] = cur_scrambler

def swap_scrambler():
    # Allow the swap_scrambler to be modified globally.
    global scrambler_list

    # Create a copy of the inputed scrambler_list that will be used to
    # modify the global scrambler_list based on user input
    orig_scrambler_list = tuple(scrambler_list)

    # Get the user input of the cyphers and put it into a list.
    order = input('Enter the order of the cyphers (1, 2, and 3) separated by a space: ')
    order = [int(i) for i in order.strip().split(' ')]

    # Make sure the user enters in a valid input.
    while len(set(order).intersection({1, 2, 3})) < 3:
        print('Please enter a valid input')
        order = input('Enter the order of the cyphers (1, 2, and 3) separated by a space: ')
        order = [int(i) for i in order.strip().split(' ')]

    # For each cypher, change the position of it in the 
    for i in range(3):
        scrambler_list[i] = orig_scrambler_list[order[i] - 1]

def scrambler_offset():
    # Allow the scrambler_list to be modified globally.
    global scrambler_list

    # Get the input of each individual offset for each cypher and turn it into
    # a list filled with the inputs, while doing some error catching, such
    # as making sure negative numbers work and being efficient if a number
    # entered would cause more than a full rotaion. 
    offset = input('Enter three integers between 0 and 25 separated by ' + 
                   'a space to change the inital offset of the cyphers ' +
                   'in the order of the user set cypher order: ')
    offset = [abs(int(i)) for i in offset.strip().split(' ')]
    
    # For each cypher, rotate it based on how much the user specified. 
    for i in range(3):
        for _ in range(offset[i] % 26):
            rotate(i)

def set_plugboard():
    # Allow the plugboard to globally modified. 
    global plugboard

    # Keep prompting the user to enter in a letter pair or 'stop'.
    # If a letter pair is entered, it will put into the plugboard dictionary
    # two items. The letter pair going both ways. If 'stop' is enter, the loop
    # will break and the encyption will continue.
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
