from collections import deque
def remove_duplicates(string):
    new_string = ''
    for char in string:
        if char not in new_string:
            new_string += char
    return new_string
    
def removechar(A,B):
    new_string = ''
    for char in B:
        if char not in A:
            new_string += char
    return new_string   
def ifcontains(A,B):
    for i in range(len(A)):
        if B in A[i]:
            return True
    return False
def read_map(file_path):
    with open(file_path, 'r') as file:
        size = int(file.readline().strip())
        map = [line.strip().split('.') for line in file.readlines()]
    
    
    
    return map
def update_map(map):
    size=len(map)
    for i in range(size):
        for j in range(size):
            if ifcontains(map[i][j], 'S'):
                if map[i][j] == 'S':
                    map[i][j] = '-'
                else:
                    map[i][j] = removechar('S', map[i][j])
            if ifcontains(map[i][j], 'B'):
                if map[i][j] == 'B':
                    map[i][j] = '-'
                else:
                    map[i][j] = removechar('B', map[i][j])
    for i in range(size):
        for j in range(size):
            room_data = map[i][j]
            if ifcontains(room_data, 'W'):
                map[i][j] = 'W'
                # Update stench in adjacent rooms
                if i > 0:
                    if map[i-1][j] == '-':
                        map[i-1][j] = 'S'
                    else:
                        map[i-1][j] += 'S'
                if i < size-1:
                    if map[i+1][j] == '-':
                        map[i+1][j] = 'S'
                    else:
                        map[i+1][j] += 'S'
                if j > 0:
                    if map[i][j-1] == '-':
                        map[i][j-1] = 'S'
                    else:
                        map[i][j-1] += 'S'
                if j < size-1:
                    if map[i][j+1] == '-':
                        map[i][j+1] = 'S'
                    else:
                        map[i][j+1] += 'S'
            
            elif ifcontains(room_data, 'P'):
                map[i][j] = 'P'
                # Update breeze in adjacent rooms
                if i > 0:
                    if map[i-1][j] == '-':
                        map[i-1][j] = 'B'
                    else:
                        map[i-1][j] += 'B'
                if i < size-1:
                    if map[i+1][j] == '-':
                        map[i+1][j] = 'B'
                    else:
                        map[i+1][j] += 'B'
                if j > 0:
                    if map[i][j-1] == '-':
                        map[i][j-1] = 'B'
                    else:
                        map[i][j-1] += 'B'
                if j < size-1:
                    if map[i][j+1] == '-':
                        map[i][j+1] = 'B'
                    else:
                        map[i][j+1] += 'B'
            else:
                map[i][j] = room_data
    for i in range(size):
        for j in range(size):
            map[i][j]=remove_duplicates(map[i][j])
    return map
def get_neighbors(map, position):
    neighbors = []
    if position[0] > 0:
        neighbors.append((position[0]-1, position[1]))  # Move up
    if position[0] < len(map)-1 :
        neighbors.append((position[0]+1, position[1]))  # Move down
    if position[1] > 0:
        neighbors.append((position[0], position[1]-1))  # Move left
    if position[1] < len(map[0])-1 :
        neighbors.append((position[0], position[1]+1))  # Move right
    return neighbors
def find_path(current_position, target_room, safe_rooms):
    queue = deque([(current_position, [])])
    visited = set()

    while queue:
        room, path = queue.popleft()
        if room == target_room:
            return path[1:] + [room]
                        
        visited.add(room)
        for neighbor in get_neighbors(updated_map, room):
            if neighbor in safe_rooms and neighbor not in visited:
                queue.append((neighbor, path + [room]))
    

    return None
def solve_wumpus_world(updated_map):
    score = 0
    size = len(updated_map[0])
    # Find the starting position of the agent
    start_position = None
    for i in range(len(updated_map)):
        for j in range(len(updated_map[i])):
            if ifcontains(updated_map[i][j], 'A'):
                start_position = (i, j)
                break
        if start_position:
            break
        
    # Initialize variables
    game_over = False
    final_position = (size-1, 0)
    current_position = start_position
    gold_found = False
    exit_cave = False
    safe_rooms = []
    stench_rooms = []
    breeze_rooms = []
    path_explored = []
    empty_rooms = []
    
    path_explored.append(current_position)
    # Move until all gold is found or no more way to move
    while not game_over:
        move_to_next_room = False
        if ifcontains(updated_map[current_position[0]][current_position[1]],'W') or ifcontains(updated_map[current_position[0]][current_position[1]],'P'):
            score-=10000
            game_over=True
            break
        if current_position not in safe_rooms:
            safe_rooms.append(current_position)
        if current_position == final_position:
            # The agent exits the cave
            exit_cave = True
    
        if exit_cave and gold_found and current_position == final_position:
            score+=10
            break
        if exit_cave and gold_found:  
            path=find_path(current_position, final_position, safe_rooms) 
            for room in path:
                if current_position == room:
                            continue
                current_position = room
                path_explored.append(room)
                score -= 10
            continue
        # Check if this room in stench room but now don't have stench
        if not ifcontains(updated_map[current_position[0]][current_position[1]], 'S'):
            if current_position in stench_rooms:
                stench_rooms.remove(current_position)
    
        # Check if there is gold in the current room
        if 'G' in updated_map[current_position[0]][current_position[1]]:
            # Collect the gold and update the map
            if updated_map[current_position[0]][current_position[1]] =='G':
                updated_map[current_position[0]][current_position[1]] = '-'
            else:
                updated_map[current_position[0]][current_position[1]]=removechar('G',updated_map[current_position[0]][current_position[1]])
            score += 1000
            path_explored.append('G'+current_position.__str__())
            gold_found = True
        # Check if this is empty room
        if not ifcontains(updated_map[current_position[0]][current_position[1]], 'S') and not ifcontains(updated_map[current_position[0]][current_position[1]], 'B'):
            if current_position not in empty_rooms:
                empty_rooms.append(current_position)
            if current_position not in safe_rooms:
                safe_rooms.append(current_position)
            neigh=get_neighbors(updated_map,current_position)
            for i in neigh:
                if i not in safe_rooms:
                    safe_rooms.append(i)
            for i in neigh:
                if i not in path_explored:
                    # Move to the next room
                    current_position = i
                    path_explored.append(i)
                    score -= 10
                    move_to_next_room = True
                    break
            if move_to_next_room:
                continue    
        if ifcontains(updated_map[current_position[0]][current_position[1]], 'S'):
            if ifcontains(updated_map[current_position[0]][current_position[1]], 'B'):
                if current_position not in breeze_rooms:
                    breeze_rooms.append(current_position)
            # The current room has stench
            if current_position not in stench_rooms:
                stench_rooms.append(current_position)
            # move to the nearest empty room
            if empty_rooms:
                path = find_path(current_position, empty_rooms[-1], safe_rooms)
                if path:
                        for room in path:
                            if current_position == room:
                                continue
                            current_position = room
                            path_explored.append(room)
                            score -= 10
                        continue
        if ifcontains(updated_map[current_position[0]][current_position[1]], 'B'):
            # The current room has stench
            if current_position not in breeze_rooms:
                breeze_rooms.append(current_position)
            # move to the nearest empty room
            if empty_rooms:
                path = find_path(current_position, empty_rooms[-1], safe_rooms)
                if path:
                    for room in path:
                        current_position = room
                        path_explored.append(room)
                        score -= 10
                    continue
        neigh = get_neighbors(updated_map, current_position)
        for i in neigh:
            if i in safe_rooms and i not in path_explored:
                # Move to the next room
                current_position = i
                path_explored.append(i)
                score -= 10
                move_to_next_room = True
                break
        if move_to_next_room:
            continue  
        # Check if there is a safe room but not visited
        if safe_rooms:
            for i in safe_rooms:
                if i not in path_explored:
                    # Find a path to the target room through the safe rooms
                    

                    path = find_path(current_position, i, safe_rooms)
                    if path:
                        for room in path:
                            if current_position == room:
                                continue
                            current_position = room
                            path_explored.append(room)
                            score -= 10
                        move_to_next_room = True
                        break
        if move_to_next_room:
            continue
        
        # No more way to move, go and shoot the wumpus
        
        # Find the nearest stench room without breeze
        foundstench=False
        for i in stench_rooms:
            if i not in breeze_rooms:
                if i == current_position:
                    foundstench=True
                    break
                path = find_path(current_position, stench_rooms[0], safe_rooms)
                if path:
                    for room in path:
                        if current_position == room:
                            continue
                        current_position = room
                        
                        path_explored.append(room)
                        score -= 10
                foundstench=True
        if not foundstench:
            for i in stench_rooms:
                if i == current_position:
                    foundstench=True
                    break
                path = find_path(current_position, stench_rooms[0], safe_rooms)
                if path:
                    for room in path:
                        if current_position == room:
                            continue
                        current_position = room
                        
                        path_explored.append(room)
                        score -= 10
                foundstench=True
        if not ifcontains(updated_map[current_position[0]][current_position[1]], 'S'):
            if current_position in stench_rooms:
                stench_rooms.remove(current_position)
                continue
        if foundstench:
            
            if current_position[0]>0 and (current_position[0]-1,current_position[1]) not in safe_rooms:
                # Shoot up
                
                path_explored.append('Shoot the arrow up')
                score -= 100
                for i in range(current_position[0], -1, -1):
                    if ifcontains(updated_map[i][current_position[1]], 'W'):
                        if updated_map[i][current_position[1]] == 'W':
                            updated_map[i][current_position[1]] = '-'  # The wumpus is killed
                            path_explored.append('W ('+i.__str__()+', '+current_position[1].__str__()+')')
                        else:
                            updated_map[i][current_position[1]] = removechar('W', updated_map[i][current_position[1]])
                            path_explored.append('W ('+i.__str__()+', '+current_position[1].__str__()+')')
                updated_map=update_map(updated_map)
                if not ifcontains(updated_map[current_position[0]][current_position[1]], 'S'):
                    stench_rooms.remove(current_position)
                    continue
            if current_position[0]<size-1 and (current_position[0]+1,current_position[1]) not in safe_rooms:
                # Shoot down
                
                path_explored.append('Shoot the arrow down')
                score -= 100
                for i in range(current_position[0], size):
                    if ifcontains(updated_map[i][current_position[1]], 'W'):
                        if updated_map[i][current_position[1]] == 'W':
                            updated_map[i][current_position[1]] = '-'
                            path_explored.append('W ('+i.__str__()+', '+current_position[1].__str__()+')')
                        else:
                            updated_map[i][current_position[1]] = removechar('W', updated_map[i][current_position[1]])
                            path_explored.append('W ('+i.__str__()+', '+current_position[1].__str__()+')')
                updated_map=update_map(updated_map)
                if not ifcontains(updated_map[current_position[0]][current_position[1]], 'S'):
                    stench_rooms.remove(current_position)
                    continue
            if current_position[1]>0 and (current_position[0],current_position[1]-1) not in safe_rooms:
                # Shoot left
                
                path_explored.append('Shoot the arrow left')
                score -= 100
                for i in range(current_position[1], -1, -1):
                    if ifcontains(updated_map[current_position[0]][i], 'W'):
                        if updated_map[current_position[0]][i] == 'W':
                            updated_map[current_position[0]][i] = '-'
                            path_explored.append('W ('+current_position[0].__str__()+', '+i.__str__()+')')
                        else:
                            updated_map[current_position[0]][i] = removechar('W', updated_map[current_position[0]][i])
                            path_explored.append('W ('+current_position[0].__str__()+', '+i.__str__()+')')
                updated_map=update_map(updated_map)
                if not ifcontains(updated_map[current_position[0]][current_position[1]], 'S'):
                    stench_rooms.remove(current_position)
                    continue
            if current_position[1]<size-1 and (current_position[0],current_position[1]+1) not in safe_rooms:
                
                # Shoot right
                path_explored.append('Shoot the arrow right')
                score -= 100
                for i in range(current_position[1], size):
                    if ifcontains(updated_map[current_position[0]][i], 'W'):
                        if updated_map[current_position[0]][i] == 'W':
                            updated_map[current_position[0]][i] = '-'
                            path_explored.append('W ('+current_position[0].__str__()+', '+i.__str__()+')')
                        else:
                            updated_map[current_position[0]][i] = removechar('W', updated_map[current_position[0]][i])
                            path_explored.append('W ('+current_position[0].__str__()+', '+i.__str__()+')')
                updated_map=update_map(updated_map)
                if not ifcontains(updated_map[current_position[0]][current_position[1]], 'S'):
                    stench_rooms.remove(current_position)
                    continue
        #No more case left, move to breeze room
        if breeze_rooms:
            path=find_path(current_position, breeze_rooms[-1], safe_rooms)  
            if path:
                for room in path:
                    if current_position == room:
                            continue
                    current_position = room
                    path_explored.append(room)
                    score -= 10
        neigh=get_neighbors(updated_map,current_position)
        for i in neigh:
            if i not in path_explored:
                # Move to the next room
                current_position = i
                path_explored.append(i)
                score -= 10
                move_to_next_room = True
                break
        if move_to_next_room:
            continue 
    score+=10
    return path_explored, score
           
        
        
        
    

file_path = 'map4.txt'
map = read_map(file_path)
updated_map = update_map(map)
path, totalscore = solve_wumpus_world(updated_map)
print('Path explored: ', path)
print('Score: ', totalscore)