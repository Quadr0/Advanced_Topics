#Authors: William Carter and Daniel Katz
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def get_cypher_alphabet(keyphrase):
    keyphrase = keyphrase.lower()
    
    cypher_alph = ""
    for i in keyphrase:
        if not i in  alphabet:
            continue
        if not i in cypher_alph:
            cypher_alph += i
    for i in alphabet:
        if not i in cypher_alph:
            cypher_alph += i
    print(cypher_alph)
    return cypher_alph

def encrypt(keyphrase, message):
    message.lower()
    cypher_alph = get_cypher_alphabet(keyphrase)
    enc_dict = {alphabet[i] : cypher_alph[i] for i in range(26)}
    enc_message = ""
    for i in message:
        if ord(i) >= 97 and ord(i) < 123:
            enc_message += enc_dict[i]
        else:
            enc_message += i
    return enc_message

def decrypt(keyphrase, message):
    message.lower()
    cypher_alph = get_cypher_alphabet(keyphrase)
    enc_dict = {cypher_alph[i] : alphabet[i] for i in range(26)}
    print(enc_dict)
    enc_message = ""
    for i in message:
        if ord(i) >= 97 and ord(i) < 123:
            enc_message += enc_dict[i]
        else:
            enc_message += i
    return enc_message


def main():
    message = "hello, im will"
    keyphrase = "zebra"
    encrypted= encrypt(keyphrase, message)
    decrypted = decrypt(keyphrase, encrypted)
    print(encrypted)
    print(decrypted)
