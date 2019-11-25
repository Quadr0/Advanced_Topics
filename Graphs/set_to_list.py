
def set_to_list(orig_set): 
    adj_list = [set() for i in range(max(j[0] for j in orig_set) + 1)]
    for i in orig_set:
        a = i[0]
        b = i[1]
        adj_list[a].add(b)
        adj_list[b].add(a)
    adj_list = [list(i) for i in adj_list]
    return adj_list

def list_to_matrix(adj_list):
    length = len(adj_list)
    matrix = [[0 for i in range(length)] for j in range(length)]
    for i, cur_set in enumerate(adj_list):
        for j in cur_set:
            matrix[i][j] = 1

    return matrix

def main():
    orig_set = {(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,3),(3,2),(3,4),(4,3)}
    adj_list = set_to_list(orig_set)
    print('adj list is {}'.format(adj_list))
    matrix = list_to_matrix(adj_list)
    print('\nadj matrix is:')
    for i in matrix:
        print(i)

main()
