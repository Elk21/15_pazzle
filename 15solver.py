import pprint
import numpy as np
import time

pp = pprint.PrettyPrinter(indent=4)
size = 4


def puzz_breadth_first(start, end):
    """
    Breadth First algorithm
    Сопоставляет каждому расположению плиток сумму расстояний от текущей позиции каждой плитки до её целевой позиции
    """
    start_time = time.time()

    print("Breadth First algorithm")
    front = [[start]]
    expanded = []
    expanded_nodes = 0
    while front:
        i = 0
        for j in range(1, len(front)):  # minimum
            if len(front[i]) > len(front[j]):
                i = j
        path = front[i]
        front = front[:i] + front[i + 1:]
        endnode = path[-1]
        if endnode in expanded:
            continue
        for k in moves(endnode):
            if k in expanded:
                continue
            front.append(path + [k])
        expanded.append(endnode)
        expanded_nodes += 1
        if endnode == end: break
    print("Expanded nodes:", expanded_nodes)

    # pp.pprint(path)
    elapsed_time = time.time() - start_time
    print("Elapsed time: ", elapsed_time)
    return path


def puzz_astar(start, end):
    """
    A* algorithm
    Число ходов, требуемых для решения, не меньше, чем число плиток, находящихся не на своих местах
    """
    start_time = time.time()
    print("A* algorithm")
    front = [[heuristic_1(start), start]]  # optional: heuristic_1
    expanded = []
    expanded_nodes = 0
    while front:
        i = 0
        for j in range(1, len(front)):
            if front[i][0] > front[j][0]:
                i = j
        path = front[i]
        front = front[:i] + front[i + 1:]
        endnode = path[-1]
        if endnode == end:
            break
        if endnode in expanded:
            continue
        for k in moves(endnode):
            if k in expanded:
                continue
            newpath = [path[0] + heuristic_1(k) - heuristic_1(endnode)] + path[1:] + [k]
            front.append(newpath)
            expanded.append(endnode)
        expanded_nodes += 1
    print("Expanded nodes:", expanded_nodes)

    elapsed_time = time.time() - start_time
    print("Elapsed time: ", elapsed_time)
    # pp.pprint(path)
    return path


def moves(mat):
    """
    Returns a list of all possible moves
    """
    output = []

    m = eval(mat)
    i = 0
    while 0 not in m[i]:
        i += 1
    j = m[i].index(0)  # blank space (zero)

    if i > 0:
        m[i][j], m[i - 1][j] = m[i - 1][j], m[i][j]  # move up
        output.append(str(m))
        m[i][j], m[i - 1][j] = m[i - 1][j], m[i][j]

    if i < size - 1:
        m[i][j], m[i + 1][j] = m[i + 1][j], m[i][j]  # move down
        output.append(str(m))
        m[i][j], m[i + 1][j] = m[i + 1][j], m[i][j]

    if j > 0:
        m[i][j], m[i][j - 1] = m[i][j - 1], m[i][j]  # move left
        output.append(str(m))
        m[i][j], m[i][j - 1] = m[i][j - 1], m[i][j]

    if j < size - 1:
        m[i][j], m[i][j + 1] = m[i][j + 1], m[i][j]  # move right
        output.append(str(m))
        m[i][j], m[i][j + 1] = m[i][j + 1], m[i][j]

    return output


def heuristic_1(puzz):
    """
    Counts the number of misplaced tiles
    """
    misplaced = 0
    compare = 0
    m = eval(puzz)
    for i in range(size):
        for j in range(size):
            if m[i][j] != compare:
                misplaced += 1
            compare += 1
    return misplaced


def heuristic_2(puzz):
    """
    Manhattan distance
    """
    distance = 0
    m = eval(puzz)
    for i in range(size):
        for j in range(size):
            if m[i][j] == 0:
                continue
            distance += abs(i - (m[i][j] / size)) + abs(j - (m[i][j] % size))
    return distance


def str_to_int_array(string):
    if type(string[0]) == int:
        string = string[1:]
    toret = []
    for e in string:
        arr = []
        for x in e.split('],'):
            ar = []
            lst = x.replace('[', '').replace(']', '').replace(' ', '').split(',')
            for i in lst:
                ar.append(int(i))
            arr.append(ar)
        toret.append(arr)
    return toret


if __name__ == '__main__':
    puzzle = str([[5, 1, 2, 3, 4],
                  [11, 6, 7, 8, 9],
                  [10, 0, 12, 13, 14],
                  [15, 16, 17, 18, 19],
                  [20, 21, 22, 23, 24]])

    end = str([[0, 1, 2, 3, 4],
               [5, 6, 7, 8, 9],
               [10, 11, 12, 13, 14],
               [15, 16, 17, 18, 19],
               [20, 21, 22, 23, 24]])
    size = 5

    puzzle = str([[4, 1, 2, 3],
                  [8, 5, 6, 7],
                  [9, 0, 10, 11],
                  [12, 13, 14, 15]])

    end = str([[0, 1, 2, 3],
               [4, 5, 6, 7],
               [8, 9, 10, 11],
               [12, 13, 14, 15]])
    size = 4

    # puzzle = str([[3, 1, 2],
    #               [4, 7, 5],
    #               [6, 0, 8]])
    #
    # end = str([[0, 1, 2],
    #            [3, 4, 5],
    #            [6, 7, 8]])
    # size = 3

    astar = puzz_astar(puzzle, end)
    astar = str_to_int_array(astar)
    print("Solution:")
    print(np.array(astar))

    breadth = puzz_breadth_first(puzzle, end)
    breadth = str_to_int_array(breadth)
    print("Solution:")
    print(np.array(breadth))
