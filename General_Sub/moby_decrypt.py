import general_substitution as gs 
alphabet = 'abcdefghijklmnopqrstuvwxyz'
frequency_text = 'nytimes_news_articles.txt'
cyphered_text = 'moby_dick_secret.txt' 

def get_freq(article_name):
    freq_dict = {i: 0 for i in alphabet}
    with open(article_name, 'r') as file:
        for line in file:
            line.strip().lower()
            for i in line:
                if i in alphabet:
                    freq_dict[i] += 1
    total_letters = sum(freq_dict.values())
    freq_percent = {i: 0 for i in alphabet}
    for i in freq_dict.keys():
        freq_percent[i] = round((freq_dict[i] / total_letters) * 100, 3)
    return freq_percent

def freq_pair(clear, uncrypted, num_letters):
    clear_freq = get_freq(frequency_text)
    reverse_clear_freq = {x: y for y, x in clear_freq.items()}
    cypher_freq = get_freq(cyphered_text)
    reverse_cypher_freq = {x: y for y, x in cypher_freq.items()}
    change_dict = dict()
    for i in range(num_letters):
        largest_letter_clear = max(clear_freq.values())
        largest_letter_cypher = max(cypher_freq.values())
        letter_clear = reverse_clear_freq[largest_letter_clear]
        letter_cypher = reverse_cypher_freq[largest_letter_cypher]
        clear_freq.pop(letter_clear)
        cypher_freq.pop(letter_cypher)
        change_dict[letter_cypher] = letter_clear

    return change_dict

def freq_change(clear, uncrypted, num_letters):
    ct = {i:i for i in alphabet}
    ct['a'] = 'e' 
    ct['b'] = 's'
    ct['c'] = 't'
    ct['d'] = 'u'
    ct['e'] = 'c'
    ct['f'] = 'v'
    ct['g'] = 'w'
    ct['h'] = 'b'
    ct['i'] = 'x'
    ct['j'] = 'y'
    ct['k'] = 'z'
    ct['l'] = 'f'
    ct['m'] = 'g'
    ct['n'] = 'h'
    ct['o'] = 'i'
    ct['p'] = 'j'
    ct['q'] = 'k'
    ct['r'] = 'l'
    ct['s'] = 'm'
    ct['t'] = 'a'
    ct['u'] = 'n'
    ct['v'] = 'o'
    ct['w'] = 'd'
    ct['x'] = 'p'
    ct['y'] = 'q'
    ct['z'] = 'r'

    count = 0
    with open(cyphered_text, 'r') as file:
        for line in file:
            if count >= 11:
                exit()
            count += 1
            temp_line = split(line.strip().lower())
            for i in range(len(temp_line)):
                cur_letter = temp_line[i]
                if cur_letter in alphabet:
                    temp_line[i] = ct[cur_letter]
            print(back_to_string(temp_line))

    for i, j in ct.items():
        print("{}    {}".format(i, j))
                    

def split(line):
    return [i for i in line]

def back_to_string(line):
    return ''.join(i for i in line)

def main():
    freq_change(frequency_text, cyphered_text,4)

main()
