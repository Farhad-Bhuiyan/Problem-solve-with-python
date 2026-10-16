import math
visited_nodes = 0
pruned_nodes = 0
def alphabeta(tree, isMax, alpha, beta):

    global visited_nodes, pruned_nodes
    visited_nodes += 1
    # Leaf node
    if type(tree) == int:
        return tree
    # MAX player
    if isMax:
        value = -1000
        for i in range(len(tree)):
            value = max(value,
                        alphabeta(tree[i],
                        False,
                        alpha,
                        beta))
            alpha = max(alpha,value)



            if alpha >= beta:

                pruned_nodes += len(tree)-i-1

                break



        return value



    # MIN player

    else:

        value = 1000


        for i in range(len(tree)):


            value = min(value,
                        alphabeta(tree[i],
                        True,
                        alpha,
                        beta))


            beta = min(beta,value)



            if alpha >= beta:

                pruned_nodes += len(tree)-i-1

                break



        return value




# Driver Code


tree = [

    [
        3,
        5,
        2
    ],

    [
        9,
        12
    ],

    [
        5,
        23,
        23
    ]

]


answer = alphabeta(tree,
                   True,
                   -1000,
                   1000)



print("Optimal Value =",answer)

print("Visited Nodes =",visited_nodes)

print("Pruned Nodes =",pruned_nodes)