import math
visited_nodes = 0
pruned_nodes = 0
def minimax(depth,index,isMax,scores,maxDepth):
    if depth == maxDepth:
        return scores[index]
    if isMax:
        left = minimax(depth+1,
                       index*2,
                       False,
                       scores,
                       maxDepth)

        right = minimax(depth+1,
                        index*2+1,
                        False,
                        scores,
                        maxDepth)
        return max(left,right)
    else:
        left = minimax(depth+1,
                       index*2,
                       True,
                       scores,
                       maxDepth)



        right = minimax(depth+1,
                        index*2+1,
                        True,
                        scores,
                        maxDepth)



        return min(left,right)





def alphabeta(depth,index,isMax,
              scores,maxDepth,
              alpha,beta):


    global visited_nodes,pruned_nodes


    visited_nodes += 1



    if depth == maxDepth:

        return scores[index]



    if isMax:


        value = -1000



        left = alphabeta(depth+1,
                         index*2,
                         False,
                         scores,
                         maxDepth,
                         alpha,
                         beta)



        value=max(value,left)



        alpha=max(alpha,value)



        if alpha >= beta:


            remaining = (2 ** (maxDepth-depth))-1

            pruned_nodes += remaining

            return value



        right = alphabeta(depth+1,
                          index*2+1,
                          False,
                          scores,
                          maxDepth,
                          alpha,
                          beta)



        value=max(value,right)



        return value




    else:


        value = 1000



        left = alphabeta(depth+1,
                         index*2,
                         True,
                         scores,
                         maxDepth,
                         alpha,
                         beta)



        value=min(value,left)



        beta=min(beta,value)



        if alpha >= beta:


            remaining=(2 ** (maxDepth-depth))-1

            pruned_nodes += remaining

            return value



        right = alphabeta(depth+1,
                          index*2+1,
                          True,
                          scores,
                          maxDepth,
                          alpha,
                          beta)



        value=min(value,right)



        return value





# Driver Code


scores=[]


n=int(input("Enter number of leaf nodes: "))


print("Enter leaf node values:")


for i in range(n):

    scores.append(int(input()))



maxDepth=int(math.log2(n))



minimax_value=minimax(0,
                      0,
                      True,
                      scores,
                      maxDepth)



print("\nMinimax Optimal Value =",
      minimax_value)



visited_nodes=0
pruned_nodes=0



alpha_value=alphabeta(0,
                      0,
                      True,
                      scores,
                      maxDepth,
                      -1000,
                      1000)



total_nodes=(2*n)-1



print("\nAlpha Beta Optimal Value =",
      alpha_value)


print("Total Nodes =",total_nodes)

print("Visited Nodes =",visited_nodes)

print("Pruned Nodes =",pruned_nodes)