maxLevel = 5    # max number of forward pointers in a node

# This function creates nodes that contain a value, a level, and a list of forward pointers. The level signifies the node’s height in the skip list and the number of linked lists it’s part of, while the forward pointers link the node to others in the skip list.
def createNode(level, value):
    return [value, level, [None] * (level + 1)]


# This function creates a skip list with a header node that acts as the starting point for all search operations. It creates a header node with a maximum level and a value of -1, which serves as the starting point for all searches, and returns a list with two elements: 0 (the initial skip list level) and the header node.
def createSkipList():
    header = createNode(maxLevel, -1)
    return [0, header]


# this function ensures the skip list stays balanced by randomly assigning levels to new nodes to maintain a logarithmic distribution of nodes across levels.  It starts with a level of 0 and generates a random number between 0 and 1, incrementing the level if the number is less than 0.5 and the current level is less than the maximum. This level is used when creating a new node, helping maintain the skip list’s properties like logarithmic search time, though time complexity may vary with the skip list’s current maximum level.
def randomLevel():
    import random
    level = 0 
    while random.random() < 0.5 and level < maxLevel:
        level += 1
    return level


# This function is used for inserting new values. It starts by creating an update list to keep track of nodes that need to be updated, setting the current node to the header node, and iterating through the skip list levels from the highest to the lowest. It moves forward until the next node has a value greater than the value to be inserted, updating the update list with the current node. Once the correct position is found, the function creates a new node with a random level, updates the forward pointers of the new node, and updates the skip list’s highest level if the new node’s level is greater than the current highest level.
def insert(skipList, value):
    global maxLevel
    update = [None] * (maxLevel + 1)   # list of nodes that need to be updated
    current = skipList[1]   # start from the header node

    for i in range(skipList[0], -1, -1):    # start from the highest level and move down
        while current[2][i] and current[2][i][0] < value:   # move forward until the next node has a value greater than the value to be inserted
            current = current[2][i]
        update[i] = current   # update the update list with the current node

    current = current[2][0]   # move to the next node

    if current == None or current[0] != value:    # if the value is not already in the list, insert it
        rlevel = randomLevel()

        if rlevel > skipList[0]:    # if the new node has a higher level than the current highest level, update the update list
            for i in range(skipList[0] + 1, rlevel + 1):
                update[i] = skipList[1]
            skipList[0] = rlevel   # update the highest level
        
        node = createNode(rlevel, value)   # create the new node

        for i in range(rlevel + 1):   # update the forward pointers of the new node
            node[2][i] = update[i][2][i]
            update[i][2][i] = node


# This function is used for deleting values. It starts by creating an update list to keep track of nodes that need to be updated, setting the current node to the header node, and iterating through the skip list levels from the highest to the lowest. It moves forward until the next node has a value equal to the value to be deleted, updating the update list with the current node. Once the correct position is found, the function updates the forward pointers of the previous node to skip the node to be deleted, and decrements the skip list’s highest level if the node to be deleted is the highest node.
def delete(skipList, searchVal):
    global maxLevel
    update = [None] * (maxLevel + 1)
    current = skipList[1]

    for i in range(skipList[0], -1, -1):
        while current[2][i] and current[2][i][0][1] != searchVal:
            current = current[2][i]
        update[i] = current

    current = current[2][0]

    if current != None and current[0][1] == searchVal:
        for i in range(len(update)):
            if update[i] is not None and update[i][2][i] == current:
                update[i][2][i] = current[2][i] if len(current[2]) > i else None
        
        while skipList[0] > 0 and skipList[1][2][skipList[0]] == None:
            skipList[0] -= 1

# This function is used for finding values in the skip list. It starts by setting the current node to the header node and iterating through the skip list levels from the highest to the lowest. It moves forward until the next node has a value less than the value to be found, updating the current node. Once the correct position is found, the function moves to the next node and checks if the value is equal to the value to be found, returning True if found and False otherwise.
def search(skipList, value):
    current = skipList[1]

    for i in range(skipList[0], -1, -1):
        while current[2][i] and current[2][i][0][1] < value:
            current = current[2][i]

    current = current[2][0]

    if current and current[0][1] == value:
        return True, current[0]
    return False, None


# This function is used for displaying the skip list. It starts by setting the current node to the first node in the lowest level and iterating through the nodes in the skip list. It appends the values of the nodes to a list and sorts the list by score in descending order. It then displays the players in the leaderboard with their ranks, names, and scores.
def display(skipList):
    current = skipList[1][2][0]  # Start from the first node
    players = []
    while current:
        players.append((current[0][1], current[0][0]))
        current = current[2][0]  # Move to the next node
    
    players = sorted(players, key=lambda player: player[1], reverse=True)  # Sort the players by score in descending order

    leaderboard_text = ""
    for count, player in enumerate(players, start=1):    # Display the players in the leaderboard
        leaderboard_text += f"Rank: {count}, Player: {player[0]}, Score: {player[1]}\n"
    
    return leaderboard_text