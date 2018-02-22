import copy
import sys
MAX_PLAYER = ""
MIN_PLAYER = ""
ALGORITHM = ""
DEPTH_LIMIT = 0
BOARD_CONFIG = []
ROW_VALUES = []
NEXT_MOVE = ""
NEAR_SIGHTED_VALUE = 0
INFINITY = sys.maxint
infinity = -sys.maxint - 1
TOTAL_NODES_VISITED = 0
ROW_TRACKER = {0:"H",1:"G",2:"F",3:"E",4:"D",5:"C",6:"B",7:"A"}
COL_TRACKER = {0:1,1:2,2:3,3:4,4:5,5:6,6:7,7:8}
"""This function reads the input file """
def fileRead():
    global MAX_PLAYER
    global MIN_PLAYER
    global ALGORITHM
    global DEPTH_LIMIT
    reader = open("input.txt", "r")
    PLAYER = reader.readline()
    PLAYER = PLAYER[0:len(PLAYER)-1]
    if PLAYER == "Star":
        MAX_PLAYER = "Star"
        MIN_PLAYER = "Circle"
    if PLAYER == "Circle":
        MAX_PLAYER = "Circle"
        MIN_PLAYER = "Star"
    ALGORITHM = reader.readline().strip("\n")
    DEPTH_LIMIT = reader.readline()
    BOARD_CONFIG_String = []
    i = 0
    while i < 8:
        BOARD_CONFIG_String.append(reader.readline().strip('\n'))
        i += 1
    i = 0
    while i < 8:
        arr = BOARD_CONFIG_String[i].split(',')
        BOARD_CONFIG.append(arr)
        i += 1
    values = reader.readline()
    ROW_VALUE = values.split(',')
    for i in ROW_VALUE:
        ROW_VALUES.append(i)
    return True
"""This function calculates and returns the utility function of a given state"""
def calculateUtility(config,player):
    state = config
    searchFor = player[0:1]
    sum = 0
    for i in range(8):
        for j in range(8):
            if state[i][j] == '0':
                continue
            s = state[i][j]
            if s[0:1]!='0':
                play = s[0:1]
                mult = int(s[1:2])
                val = 0
                if(play == "S"):
                    val = ROW_VALUES[7-i]
                elif(play == "C"):
                    val = ROW_VALUES[i]
                if(play == searchFor):
                    sum += mult*int(val)
                else:
                    sum -= mult*int(val)
    return sum
"""This method returns whether an action is feasible for Star for a given state """
def isFeasibleActionForStar(state,curri,currj,newi,newj):
    if newi < 0  or newi>7:
        return False
    if newj <0 or newj > 7:
        return False
    if state[newi][newj]!= '0':
        s = state[newi][newj]
        if s[0:1] == 'C':
            return False
        if s[0:1] == "S" and newi != 0:
            return False
    if newi == curri-2 and newj == currj -2:
        temp = state[curri-1][currj-1]
        if(temp[0:1]!="C")  :
            return False
    if newi == curri-2 and newj == currj + 2:
        temp = state[curri-1][currj+1]
        if(temp[0:1]!="C")  :
            return False
    if newi == curri-2 and newj == currj -2:
        temp = state[curri-1][currj-1]
        if(temp[0:1]!="C")  :
            return False

    return True
"""This method finds all the actions for a star at loc curri and currj and return it in 2D array"""
def findAllStartActions(curri,currj):
    result = []
    temp3 = [curri-1,currj-1]
    temp4 =  [curri-1,currj+1]
    temp1 = [curri-2,currj-2]
    temp2 = [curri - 2, currj + 2]
    result.append(temp1)
    result.append(temp2)
    result.append(temp3)
    result.append(temp4)
    return result
"""This method performs Star actions and prints the actions made """
def starStep(stat,depth):
    state = copy.deepcopy(stat)
    for i in range(8):
        for j in range(8):
            s = state[i][j]
            if s=='0':
                continue
            if s[0:1]=='S':
                arr = findAllStartActions(i,j)
                for a in arr:
                    if isFeasibleActionForStar(stat,i,j,a[0],a[1]):
                        state2 = copy.deepcopy(state)
                        print "This star action is Fesible" + str(ROW_TRACKER[i]) + str(COL_TRACKER[j]) + "-" + str(
                            ROW_TRACKER[a[0]]) + str(COL_TRACKER[a[1]])
                        print state
                        temp = resultStarAction(state2, i, j, a[0], a[1])
                        # print resultStarAction(state2, i, j, a[0], a[1])
                        print temp
                        circleStep(temp)
"""This method returns whether an action is feasible for Circle for a given state """
def isFeasibleActionForCircle(state,curri,currj,newi,newj):
    if newi < 0  or newi>7:
        return False
    if newj <0 or newj > 7:
        return False
    if state[newi][newj]!= '0':
        s = state[newi][newj]
        if s[0:1] == 'S':
            return False
        if s[0:1] == "C" and newi != 7:
            return False
    if newi == curri+2 and newj == currj -2:
        temp = state[curri+1][currj-1]
        if(temp[0:1]!="S")  :
            return False
    if newi == curri+2 and newj == currj + 2:
        temp = state[curri+1][currj+1]
        if(temp[0:1]!="S")  :
            return False
    if newi == curri+2 and newj == currj -2:
        temp = state[curri+1][currj-1]
        if(temp[0:1]!="S")  :
            return False

    return True
"""This method finds all the actions for a circle at loc curri and currj and return it in 2D array"""
def findAllCircleActions(curri,currj):
    result = []
    temp3 = [curri+1,currj-1]
    temp4 =  [curri+1,currj+1]
    temp1 = [curri+2,currj-2]
    temp2 = [curri + 2, currj + 2]
    result.append(temp1)
    result.append(temp2)
    result.append(temp3)
    result.append(temp4)
    return result
"""This method performs Star actions and prints the actions made """
def circleStep(stat,depth):
    performedSteps = 0
    state = copy.deepcopy(stat)
    for i in range(8):
        for j in range(8):
            s = state[i][j]
            if s=='0':
                continue
            if s[0:1]=='C':
                arr = findAllCircleActions(i,j)
                if arr:
                    for a in arr:
                        state2 = copy.deepcopy(state)
                        if isFeasibleActionForCircle(state,i,j,a[0],a[1]):
                            performedSteps+=1
                            print "This Circle action is Fesible" + str(ROW_TRACKER[i]) + str(COL_TRACKER[j]) + "-" + str(ROW_TRACKER[a[0]]) + str(COL_TRACKER[a[1]])
                            print state
                            temp = resultCircleAction(state2,i,j,a[0],a[1])

                            print temp
                            starStep(temp)
"""Take a Star step and return new State  , but the action must be a valid action otherwise the output will generate a state which can never be possible """
def resultStarAction(stat,curri,currj,newi,newj):

    state = copy.deepcopy(stat)

    if newi == curri -2 :
        if newj == currj -2:
            state[curri-1][currj-1]='0'
        if newj == currj + 2:
            state[curri-1][currj+1]='0'

    if state[newi][newj]!='0':
        st = state[newi][newj]

        count = int(st[1:])
        count +=1
        state[newi][newj] = st[0:1] + str(count)
    if state[newi][newj]=='0':
        state[newi][newj] = "S1"
    state[curri][currj]='0'

    return state
"""This method generates the result of the action for a circle step """
def resultCircleAction(stat, curri, currj, newi, newj):
    state = copy.deepcopy(stat)

    if newi == curri +2 :
        if newj == currj -2:
            state[curri+1][currj-1]='0'
        if newj == currj + 2:
            state[curri+1][currj+1]='0'

    if state[newi][newj]!='0':
        st = state[newi][newj]

        count = int(st[1:])
        count +=1
        state[newi][newj] = st[0:1] + str(count)
    if state[newi][newj]=='0':
        state[newi][newj] = "C1"
    state[curri][currj]='0'

    return state
"""This function performs terminal test for the given state  """
def terminalTest(state,depth):
    global TOTAL_NODES_VISITED
    if depth >= int(DEPTH_LIMIT):
        return True
    starCount = 0
    starMovesCount = 0
    cicleMovesCount = 0
    circleCount = 0
    for i in range(8):
        for j in range(8):
            s = state[i][j]
            if s=='0':
                continue
            if s[0:1]=="S":
                starCount+=1
                arr = findAllStartActions(i,j)
                for a in arr :
                    state2 = copy.deepcopy(state)
                    if isFeasibleActionForStar(state2,i,j,a[0],a[1]):
                        starMovesCount+=1

            if s[0:1]=="C":
                circleCount+=1
                arr = findAllCircleActions(i,j)
                for a in arr:
                    state2 = copy.deepcopy(state)
                    if isFeasibleActionForCircle(state2,i,j,a[0],a[1]):
                        cicleMovesCount+=1

    if starCount == 0 or circleCount == 0 :
        # TOTAL_NODES_VISITED+=1
        return True
    elif cicleMovesCount == 0 and starMovesCount == 0:
        TOTAL_NODES_VISITED +=2
        return True
    return False
def MAX_VALUE(stat,Alpha,Beta,Depth):

    countMoves = 0
    state = copy.deepcopy(stat)
    depth = copy.deepcopy(Depth)
    alpha = copy.deepcopy(Alpha)
    beta = copy.deepcopy(Beta)
    global TOTAL_NODES_VISITED
    global NEXT_MOVE
    global NEAR_SIGHTED_VALUE
    TOTAL_NODES_VISITED += 1
    if terminalTest(state,depth):
        if depth == 0 : return calculateUtility(state,MAX_PLAYER)
        return calculateUtility(state,MAX_PLAYER)
    value = infinity
    if MAX_PLAYER == "Star":
        for i in range(8):
            for j in range(8):
                s = state[i][j]
                if s == '0':
                    continue
                if s[0:1] == 'S':
                    arr = findAllStartActions(i, j)
                    for a in arr:
                        if isFeasibleActionForStar(stat, i, j, a[0], a[1]):
                            countMoves+=1
                            state2 = copy.deepcopy(state)
                            temp = resultStarAction(state2, i, j, a[0], a[1])
                            tempVal = calculateUtility(temp,MAX_PLAYER)
                            value = max(value, MIN_VALUE(temp,Alpha,Beta,depth+1))
                            if value >= Beta:
                                return value
                            alpha = Alpha
                            Alpha = max(Alpha,value)
                            if(alpha!=Alpha) and depth == 0 :


                                NEXT_MOVE = str(ROW_TRACKER[i]) + str(COL_TRACKER[j]) + "-" + str(ROW_TRACKER[a[0]]) + str(
                                    COL_TRACKER[a[1]])
                                NEAR_SIGHTED_VALUE = tempVal


        if countMoves ==0 :
            value = max(value,MIN_VALUE(state,Alpha,Beta,depth+1))
            if value> Alpha:
                NEAR_SIGHTED_VALUE = calculateUtility(state,MAX_PLAYER)
            if value >= Beta :
                return value
            Alpha = max(Alpha,value)
        return value
    if MAX_PLAYER == "Circle":
        for i in range(8):
            for j in range(8):
                s = state[i][j]
                if s == '0':
                    continue
                if s[0:1] == 'C':
                    arr = findAllCircleActions(i, j)
                    if arr:
                        for a in arr:
                            if isFeasibleActionForCircle(state, i, j, a[0], a[1]):
                                countMoves += 1
                                state2 = copy.deepcopy(state)
                                temp = resultCircleAction(state2, i, j, a[0], a[1])
                                tempVal = calculateUtility(temp,MAX_PLAYER)
                                value = max(value, MIN_VALUE(temp, Alpha, Beta, depth+1))
                                if value >= Beta:
                                    return value
                                alpha = Alpha
                                Alpha = max(Alpha, value)
                                if(alpha!=Alpha) and depth == 0 :
                                    NEXT_MOVE = str(ROW_TRACKER[i]) + str(COL_TRACKER[j]) + "-" + str(
                                        ROW_TRACKER[a[0]]) + str(
                                        COL_TRACKER[a[1]])
                                    NEAR_SIGHTED_VALUE = tempVal
        if countMoves ==0 :
            value = max(value,MIN_VALUE(state,Alpha,Beta,depth+1))
            # if value> Alpha:
            NEAR_SIGHTED_VALUE = calculateUtility(state,MAX_PLAYER)
            if value >= Beta :
                return value
            Alpha = max(Alpha,value)
        return value
def MIN_VALUE(stat,Alpha,Beta,Depth):
    global TOTAL_NODES_VISITED
    global NEXT_MOVE
    TOTAL_NODES_VISITED += 1
    countMoves = 0
    state = copy.deepcopy(stat)
    depth = copy.deepcopy(Depth)
    alpha = copy.deepcopy(Alpha)
    beta = copy.deepcopy(Beta)
    if terminalTest(state,depth):
        if depth == 0:
            return calculateUtility(state,MAX_PLAYER)
        return calculateUtility(state,MAX_PLAYER)
    value = INFINITY
    if MIN_PLAYER == "Star":
        for i in range(8):
            for j in range(8):
                s = state[i][j]
                if s == '0':
                    continue
                if s[0:1] == 'S':
                    arr = findAllStartActions(i, j)
                    for a in arr:
                        if isFeasibleActionForStar(stat, i, j, a[0], a[1]):
                            countMoves += 1
                            state2 = copy.deepcopy(state)
                            temp = resultStarAction(state2, i, j, a[0], a[1])
                            tempVal = calculateUtility(temp,MAX_PLAYER)
                            value = min(value, MAX_VALUE(temp,Alpha,Beta,depth+1))
                            if value <= Alpha:
                                return value
                            beta = Beta
                            Beta = min(Beta,value)
                            # if beta != Beta and MAX_PLAYER == "Circle":
                            #     NEXT_MOVE = str(ROW_TRACKER[i]) + str(COL_TRACKER[j]) + "-" + str(
                            #         ROW_TRACKER[a[0]]) + str(
                            #         COL_TRACKER[a[1]])
                            #     NEAR_SIGHTED_VALUE = tempVal


        if countMoves ==0 :
            value = min(value,MAX_VALUE(state,Alpha,Beta,depth+1))
            if value <= Alpha :
                return value
            Beta  = max(Beta,value)
        return value
    if MIN_PLAYER == "Circle":
        for i in range(8):
            for j in range(8):
                s = state[i][j]
                if s == '0':
                    continue
                if s[0:1] == 'C':
                    arr = findAllCircleActions(i, j)
                    if arr:
                        for a in arr:
                            if isFeasibleActionForCircle(state, i, j, a[0], a[1]):
                                countMoves += 1
                                state2 = copy.deepcopy(state)
                                temp = resultCircleAction(state2, i, j, a[0], a[1])
                                value = min(value, MAX_VALUE(temp, Alpha, Beta, depth+1))
                                if value <= Alpha:
                                    return value
                                beta = Beta
                                Beta = min(Beta, value)
                                # if beta != Beta and MAX_PLAYER =="Circle":
                                #     NEXT_MOVE = str(ROW_TRACKER[i]) + str(COL_TRACKER[j]) + "-" + str(
                                #         ROW_TRACKER[a[0]]) + str(
                                #         COL_TRACKER[a[1]])
                                #     NEAR_SIGHTED_VALUE = tempVal
        if countMoves ==0 :
            value = min(value,MAX_VALUE(state,Alpha,Beta,depth+1))
            if value <= Alpha :
                return value
            Beta  = max(Beta,value)
        return value
    """
def MAX_VALUE_MINIMAX(stat,Depth):

    countMoves = 0
    state = copy.deepcopy(stat)
    depth = copy.deepcopy(Depth)
    global TOTAL_NODES_VISITED
    global NEXT_MOVE
    global NEAR_SIGHTED_VALUE
    TOTAL_NODES_VISITED += 1
    if terminalTest(state,depth):
        return calculateUtility(state,MAX_PLAYER)
    value = infinity
    if MAX_PLAYER == "Star":
        for i in range(8):
            for j in range(8):
                s = state[i][j]
                if s == '0':
                    continue
                if s[0:1] == 'S':
                    arr = findAllStartActions(i, j)
                    for a in arr:
                        if isFeasibleActionForStar(stat, i, j, a[0], a[1]):
                            countMoves+=1
                            state2 = copy.deepcopy(state)
                            temp = resultStarAction(state2, i, j, a[0], a[1])
                            tempVal = calculateUtility(temp,MAX_PLAYER)
                            val = value
                            value =  max(value, MIN_VALUE_MINIMAX(temp,depth+1))
                            if val!=value :
                                NEAR_SIGHTED_VALUE = tempVal
                                NEXT_MOVE = str(ROW_TRACKER[i]) + str(COL_TRACKER[j]) + "-" + str(
                                    ROW_TRACKER[a[0]]) + str(
                                    COL_TRACKER[a[1]])
        if countMoves!=0:
            return value

        if countMoves ==0 :
            return max(value,MIN_VALUE_MINIMAX(state,depth+1))
    if MAX_PLAYER == "Circle":
        for i in range(8):
            for j in range(8):
                s = state[i][j]
                if s == '0':
                    continue
                if s[0:1] == 'C':
                    arr = findAllCircleActions(i, j)
                    if arr:
                        for a in arr:
                            if isFeasibleActionForCircle(state, i, j, a[0], a[1]):
                                countMoves += 1
                                state2 = copy.deepcopy(state)
                                temp = resultCircleAction(state2, i, j, a[0], a[1])
                                tempVal = calculateUtility(temp, MAX_PLAYER)
                                val = value
                                value = max(value, MIN_VALUE_MINIMAX(temp,depth+1))
                                if(val!=value):
                                    NEAR_SIGHTED_VALUE = tempVal
                                    NEXT_MOVE = str(ROW_TRACKER[i]) + str(COL_TRACKER[j]) + "-" + str(
                                        ROW_TRACKER[a[0]]) + str(
                                        COL_TRACKER[a[1]])
        if countMoves!= 0:
            return value
        if countMoves ==0 :
            return max(value,MIN_VALUE_MINIMAX(state,depth+1))
def MIN_VALUE_MINIMAX(stat,Depth):
    global TOTAL_NODES_VISITED
    global NEXT_MOVE
    TOTAL_NODES_VISITED += 1
    countMoves = 0
    state = copy.deepcopy(stat)
    depth = copy.deepcopy(Depth)
    if terminalTest(state,depth):
        if depth == 0:
            return calculateUtility(state,MAX_PLAYER)
        return calculateUtility(state,MAX_PLAYER)
    value = INFINITY
    if MIN_PLAYER == "Star":
        for i in range(8):
            for j in range(8):
                s = state[i][j]
                if s == '0':
                    continue
                if s[0:1] == 'S':
                    arr = findAllStartActions(i, j)
                    for a in arr:
                        if isFeasibleActionForStar(stat, i, j, a[0], a[1]):
                            countMoves += 1
                            state2 = copy.deepcopy(state)
                            temp = resultStarAction(state2, i, j, a[0], a[1])

                            value = min(value, MAX_VALUE_MINIMAX(temp,depth+1))
        if countMoves!= 0 :
            return value
        if countMoves ==0 :
            return min(value,MAX_VALUE(state,depth+1))
    if MIN_PLAYER == "Circle":
        for i in range(8):
            for j in range(8):
                s = state[i][j]
                if s == '0':
                    continue
                if s[0:1] == 'C':
                    arr = findAllCircleActions(i, j)
                    if arr:
                        for a in arr:
                            if isFeasibleActionForCircle(state, i, j, a[0], a[1]):
                                countMoves += 1
                                state2 = copy.deepcopy(state)
                                temp = resultCircleAction(state2, i, j, a[0], a[1])
                                value =   min(value, MAX_VALUE_MINIMAX(temp,depth+1))
        if countMoves!=0:
            return value
        if countMoves ==0 :
            return min(value,MAX_VALUE_MINIMAX(state,depth+1))
            """
def MAX_VALUE_MINIMAX(stat,Depth,Alpha,Beta):
    countMoves = 0
    state = copy.deepcopy(stat)
    depth = copy.deepcopy(Depth)
    global TOTAL_NODES_VISITED
    global NEXT_MOVE
    global NEAR_SIGHTED_VALUE
    TOTAL_NODES_VISITED += 1
    if terminalTest(state,depth):
        return calculateUtility(state,MAX_PLAYER)
    value = infinity
    if MAX_PLAYER == "Star":
        for i in range(8):
            for j in range(8):
                s = state[i][j]
                if s == '0':
                    continue
                if s[0:1] == 'S':
                    arr = findAllStartActions(i, j)
                    for a in arr:
                        if isFeasibleActionForStar(stat, i, j, a[0], a[1]):
                            countMoves+=1
                            state2 = copy.deepcopy(state)
                            temp = resultStarAction(state2, i, j, a[0], a[1])
                            tempVal = calculateUtility(temp,MAX_PLAYER)
                            val = value
                            value =  max(value, MIN_VALUE_MINIMAX(temp,depth+1,Alpha,Beta))
                            if value >= Beta:
                                continue
                            alpha = Alpha
                            Alpha = max(Alpha, value)
                            if alpha != Alpha and depth == 0 :
                                NEAR_SIGHTED_VALUE = tempVal
                                NEXT_MOVE = str(ROW_TRACKER[i]) + str(COL_TRACKER[j]) + "-" + str(
                                    ROW_TRACKER[a[0]]) + str(
                                    COL_TRACKER[a[1]])
        if countMoves!=0:
            return value
        if countMoves ==0 :
            value = max(value,MIN_VALUE_MINIMAX(state,depth+1,Alpha,Beta))
            if value > Alpha :
                NEAR_SIGHTED_VALUE = calculateUtility(state,MAX_PLAYER)
            return value
    if MAX_PLAYER == "Circle":
        for i in range(8):
            for j in range(8):
                s = state[i][j]
                if s == '0':
                    continue
                if s[0:1] == 'C':
                    arr = findAllCircleActions(i, j)
                    if arr:
                        for a in arr:
                            if isFeasibleActionForCircle(state, i, j, a[0], a[1]):
                                countMoves += 1
                                state2 = copy.deepcopy(state)
                                temp = resultCircleAction(state2, i, j, a[0], a[1])
                                tempVal = calculateUtility(temp, MAX_PLAYER)
                                val = value
                                value = max(value, MIN_VALUE_MINIMAX(temp,depth+1,Alpha,Beta))
                                if value >= Beta:
                                    continue
                                alpha = Alpha
                                Alpha = max(Alpha, value)
                                if alpha != Alpha and depth == 0 :
                                    NEAR_SIGHTED_VALUE = tempVal
                                    NEXT_MOVE = str(ROW_TRACKER[i]) + str(COL_TRACKER[j]) + "-" + str(
                                        ROW_TRACKER[a[0]]) + str(
                                        COL_TRACKER[a[1]])
        if countMoves!= 0:
            return value
        if countMoves ==0 :
            value = max(value, MIN_VALUE_MINIMAX(state, depth + 1, Alpha,Beta))
            if value > Alpha:
                NEAR_SIGHTED_VALUE = calculateUtility(state, MAX_PLAYER)
            return value
def MIN_VALUE_MINIMAX(stat,Depth,Alpha,Beta):
    global TOTAL_NODES_VISITED
    global NEXT_MOVE
    TOTAL_NODES_VISITED += 1
    countMoves = 0
    state = copy.deepcopy(stat)
    depth = copy.deepcopy(Depth)
    if terminalTest(state,depth):
        if depth == 0:
            return calculateUtility(state,MAX_PLAYER)
        return calculateUtility(state,MAX_PLAYER)
    value = INFINITY
    if MIN_PLAYER == "Star":
        for i in range(8):
            for j in range(8):
                s = state[i][j]
                if s == '0':
                    continue
                if s[0:1] == 'S':
                    arr = findAllStartActions(i, j)
                    for a in arr:
                        if isFeasibleActionForStar(stat, i, j, a[0], a[1]):
                            countMoves += 1
                            state2 = copy.deepcopy(state)
                            temp = resultStarAction(state2, i, j, a[0], a[1])

                            value = min(value, MAX_VALUE_MINIMAX(temp,depth+1,Alpha,Beta))
                            Beta = min(Beta, value)
        if countMoves!= 0 :
            return value
        if countMoves ==0 :
            return min(value,MAX_VALUE(state,depth+1,Alpha,Beta))
    if MIN_PLAYER == "Circle":
        for i in range(8):
            for j in range(8):
                s = state[i][j]
                if s == '0':
                    continue
                if s[0:1] == 'C':
                    arr = findAllCircleActions(i, j)
                    if arr:
                        for a in arr:
                            if isFeasibleActionForCircle(state, i, j, a[0], a[1]):
                                countMoves += 1
                                state2 = copy.deepcopy(state)
                                temp = resultCircleAction(state2, i, j, a[0], a[1])
                                value =   min(value, MAX_VALUE_MINIMAX(temp,depth+1,Alpha,Beta))
                                Beta = min(Beta, value)
        if countMoves!=0:
            return value
        if countMoves ==0 :
            return min(value,MAX_VALUE_MINIMAX(state,depth+1,Alpha,Beta))
global finalValue
finalValue = 0
fileRead()
if ALGORITHM == "ALPHABETA":
    MY_OUTPUT_ALPHABETA = open("output.txt","w+")

    finalValue =  MAX_VALUE(BOARD_CONFIG, infinity, INFINITY, 0)
    if NEXT_MOVE != "":
        MY_OUTPUT_ALPHABETA.write(NEXT_MOVE + "\n")
    else:
        MY_OUTPUT_ALPHABETA.write("pass"+ "\n")
        NEAR_SIGHTED_VALUE = calculateUtility(BOARD_CONFIG, MAX_PLAYER)
    MY_OUTPUT_ALPHABETA.write(str(NEAR_SIGHTED_VALUE)+"\n")
    MY_OUTPUT_ALPHABETA.write(str(finalValue)+"\n")
    MY_OUTPUT_ALPHABETA.write(str(TOTAL_NODES_VISITED))
    MY_OUTPUT_ALPHABETA.close()
elif ALGORITHM == "MINIMAX" :
    MY_OUTPUT_MINIMAX = open("output.txt", "w+")
    finalValue = MAX_VALUE_MINIMAX(BOARD_CONFIG,0,infinity,INFINITY)
    if NEXT_MOVE != "":
        MY_OUTPUT_MINIMAX.write(NEXT_MOVE+ "\n")
    else:
        MY_OUTPUT_MINIMAX.write("pass"+ "\n")
        NEAR_SIGHTED_VALUE = calculateUtility(BOARD_CONFIG, MAX_PLAYER)
    MY_OUTPUT_MINIMAX.write(str(NEAR_SIGHTED_VALUE)+ "\n")
    MY_OUTPUT_MINIMAX.write(str(finalValue)+ "\n")
    MY_OUTPUT_MINIMAX.write(str(TOTAL_NODES_VISITED))
    MY_OUTPUT_MINIMAX.close()

