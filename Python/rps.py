# Daniel Katz and William Carter
from random import randint

user_input = input('Pick rock paper or scisors: ')
cpu_choice = randint(0,2)
dict_choice = {'rock':0, 'paper':1, 'scisors':2}
reverse_choice = dict_choice
reverse_choice = {value:key for key, value in dict_choice.items()}

user_choice = dict_choice[user_input]

output_combine = str(cpu_choice) + str(user_choice)

output_dict = {'00': 'tie', '11':'tie', '22':'tie',
               '01':'you win', '02': 'you lose',
               '10':'you lose', '12': 'you win',
               '20':'you win', '21': 'you lose'}

print('user input is ' + user_input)
print('computer choice is ' + reverse_choice[cpu_choice])

print(output_dict[output_combine])
