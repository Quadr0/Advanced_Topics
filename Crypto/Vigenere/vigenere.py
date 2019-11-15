import numpy as np
alphabet = 'abcdefghijklmnopqrstuvwxyz'
double_alphabet = alphabet * 2
file_name = 'temp.txt'
 
def open_file(file_name):
    output = ''
    with open(file_name, 'r') as file:
        for line in file:
            output += line

    return output

def one_line(message):
    output = ''
    for line in message:
        for i in line:
            i = i.lower()
            if i in alphabet:
                output += i

    return output

def encrypt_char(character, to_shift_by):
    start = ord(character) - 97
    n = ord(to_shift_by) - 97

    return double_alphabet[start + n]

def vigenere_encrypt(message, keyphrase):
    counter = 0
    message = message.lower()
    keyphrase = keyphrase.lower()
    output = ''
    for i in message:
        if i in alphabet:
            output += encrypt_char(i, keyphrase[counter])
        else:
            output += i

        if counter == len(keyphrase) - 1:
            counter = 0
        else:
            counter += 1

    return output

def find_rep(message, length):
    prev_finds = dict()
    output = list()
    for i in range(len(message) - length + 1):
        cur_string = message[i : i+length]
        if cur_string in prev_finds.keys():
            output.append(i - prev_finds[cur_string])
        prev_finds[cur_string] = i
    return output

def find_factors(number):
    output = list()
    for i in range(3, number+1):
        if number % i == 0:
            output.append(i)

    return output

def main():
    cur_file = open_file(file_name)
    message = one_line(cur_file)
    rep_len = list()
    for i in range(4,5):
        rep_len.append(find_rep(message, i))
    print(rep_len)

main()
