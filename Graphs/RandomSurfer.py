from random import randint
from sys import setrecursionlimit

setrecursionlimit(10**9)

def file_to_set(file_name):
    with open(file_name, 'r') as file:
        num_tuples = int(file.readline().strip())
        all_sets = set()
        for i in range(num_tuples):
            tuple_edge = file.readline().strip().split(',')
            all_sets.add((int(tuple_edge[0]), int(tuple_edge[1])))
        return all_sets


def set_to_list(orig_set): 
    adj_list = [set() for i in range(max(max(j[0], j[1]) for j in orig_set) + 1)]
    for i in orig_set:
        a = i[0]
        b = i[1]
        adj_list[a].add(b)
    adj_list = [list(i) for i in adj_list]
    return adj_list

def list_to_matrix(adj_list):
    length = len(adj_list)
    matrix = [[0 for i in range(length)] for j in range(length)]
    for i, cur_set in enumerate(adj_list):
        for j in cur_set:
            matrix[i][j] = 1

    return matrix


def random_surf(adj_list, cur_page, page_counter,  pages_visited):
    page_counter[cur_page] += 1
    if pages_visited >= 2000:
        return page_counter
    
    link_or_page = randint(1, 100)
    if link_or_page < 85 and len(adj_list[cur_page]) > 0:
        rand_link = randint(0, len(adj_list[cur_page]) - 1)
        cur_page = adj_list[cur_page][rand_link]
        return random_surf(adj_list, cur_page, page_counter, pages_visited+1)
    else:
        cur_page = randint(0, len(adj_list) - 1)
        return random_surf(adj_list, cur_page, page_counter, pages_visited+1)

def main():
    orig_set = {(0,1),(0,2),(2,3),(4,0)}
    #orig_set = file_to_set('web_graph_1.txt')
    adj_list = set_to_list(orig_set)
    print(adj_list)
    page_counter = [0 for i in range(len(adj_list))]
    rand_start = randint(0, len(adj_list) - 1) 
    page_counter = random_surf(adj_list, rand_start, page_counter, 0)
    for i in range(len(page_counter)):
        print(page_counter[i] / sum(page_counter))

main()
