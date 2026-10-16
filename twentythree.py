import math
board=[
['X','O','X'],
['O','X',' '],
[' ',' ','O']
]
visited_nodes=0
pruned_nodes=0
def checkWinner():
    for row in board:
        if row[0]==row[1]==row[2] and row[0]!=' ':
            return row[0]
    for col in range(3):
        if board[0][col]==board[1][col]==board[2][col]:
            return board[0][col]
    return None
def minimax(isMax,alpha,beta):
    global visited_nodes,pruned_nodes
    visited_nodes += 1
    result=checkWinner()
    if result=="X":

        return 1



    if result=="O":

        return -1




    if isMax:


        value=-1000



        for i in range(3):

            for j in range(3):


                if board[i][j]==' ':


                    board[i][j]='X'


                    score=minimax(False,
                                  alpha,
                                  beta)


                    board[i][j]=' '



                    value=max(value,score)


                    alpha=max(alpha,value)



                    if alpha>=beta:


                        pruned_nodes+=1

                        return value



        return value




    else:


        value=1000



        for i in range(3):

            for j in range(3):


                if board[i][j]==' ':


                    board[i][j]='O'


                    score=minimax(True,
                                  alpha,
                                  beta)


                    board[i][j]=' '



                    value=min(value,score)


                    beta=min(beta,value)



                    if alpha>=beta:

                        pruned_nodes+=1

                        return value
        return value

result=minimax(True,
               -1000,
               1000)

print("Game Evaluation =",result)

print("Visited Nodes =",visited_nodes)

print("Pruned Nodes =",pruned_nodes)