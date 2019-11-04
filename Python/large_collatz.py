prev_places = dict()
for i in range(2,1000000-1):
    init_i = i
    cur_seq = 0
    while(init_i != 1):
        if(init_i in prev_places.keys()):
            cur_seq += prev_places[init_i]
            break

        if(init_i % 2 == 0):
            init_i = init_i / 2
        else:
            init_i = 3 * init_i + 1
        cur_seq += 1

    prev_places[i] = cur_seq
  
inv_dict = {v: k for k, v in prev_places.items()}

print(inv_dict[max(inv_dict.keys())])
