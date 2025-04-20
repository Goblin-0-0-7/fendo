def findPath(start_coordinates: tuple[int, int], end_coordinates: tuple[int, int], fields: list['Field']):
    ''' Checks if any path between two coordinates, blocked only by walls, exists'''
    dist_x = end_coordinates[0] - start_coordinates[0]
    dist_y = end_coordinates[1] - start_coordinates[1]
    
    horizontal_direction = 'E' if dist_x > 0 else 'W'
    vertical_direction = 'S' if dist_y > 0 else 'N'
    
    path = pathStep(start_coordinates[0], start_coordinates[1], horizontal_direction, vertical_direction, end_coordinates, fields)
    if path:
        return True
    else:
        return False

def pathStep(x, y, horizontal_direction: str, vertical_direction: str, end_coordinates: tuple[int, int], fields: list['Field'], steps: list[str] = []):
    if not checkPathBlocked(vertical_direction, fields[x,y]) and y != end_coordinates[1]:
        step = 1 if vertical_direction == 'S' else -1
        path = pathStep(x, y + step, horizontal_direction, vertical_direction, end_coordinates, fields, steps + [vertical_direction])
        if path:
            return path
    if not checkPathBlocked(horizontal_direction, fields[x,y]) and x != end_coordinates[0]:
        step = 1 if horizontal_direction == 'E' else -1
        path = pathStep(x + step, y, horizontal_direction, vertical_direction, end_coordinates, fields, steps + [horizontal_direction])
        if path:
            return path
    
    if x == end_coordinates[0] and y == end_coordinates[1]:
        return steps
    return False

def findValidPath(start_coordinates: tuple[int, int], end_coordinates: tuple[int, int], fields: list['Field']):
    ''' Checks if a path between start and end coordinates exists and is valid under the T-Movement rules. '''
    dist_x = end_coordinates[0] - start_coordinates[0]
    dist_y = end_coordinates[1] - start_coordinates[1]
    
    horizontal_direction = 'E' if dist_x > 0 else 'W'
    vertical_direction = 'S' if dist_y > 0 else 'N'
    
    path = pathValidStep(start_coordinates[0], start_coordinates[1], horizontal_direction, vertical_direction, end_coordinates, fields)
    if path:
        return True
    else:
        return False

def pathValidStep(x, y, horizontal_direction, vertical_direction, end_coordinates, fields: list['Field'], steps: list[str] = []):
    if not checkPathBlocked(vertical_direction, fields[x,y]) and y != end_coordinates[1]:
        if steps and steps[-1] == horizontal_direction and (horizontal_direction in steps) and (vertical_direction in steps): # check if the direction was already switched
            return False
        step = 1 if vertical_direction == 'S' else -1
        if not fields[x,y + step].getPawn():
            path = pathValidStep(x, y + step, horizontal_direction, vertical_direction, end_coordinates, fields, steps + [vertical_direction])
            if path:
                return path
    if not checkPathBlocked(horizontal_direction, fields[x,y]) and x != end_coordinates[0]:
        if steps and steps[-1] == vertical_direction and (horizontal_direction in steps) and (vertical_direction in steps):  # check if the direction was already switched
            return False
        step = 1 if horizontal_direction == 'E' else -1
        if not fields[x + step,y].getPawn():
            path = pathValidStep(x + step, y, horizontal_direction, vertical_direction, end_coordinates, fields, steps + [horizontal_direction])
            if path:
                return path
    
    if x == end_coordinates[0] and y == end_coordinates[1]:
        return steps
    return False

def checkPathBlocked(direction: str, field: 'Field'):
    if field.getWall(direction):
        return True
    return False


class Area():
    
    def __init__(self):
        self.fields: list['Field'] = []
        self.owner = 0
        
    def getOwner(self):
        return self.owner

    def setOwner(self, owner: int):
        if owner != 0 and owner != 1 and owner != 2:
            raise ValueError('Invalid player number')
        self.owner = owner
        
    def getFields(self) -> list['Field']:
        return self.fields
    
    def addField(self, field: 'Field'):
        self.fields.append(field)


def findAreas(undesignated_fields: list['Field'], board: 'Board') -> list['Area']:
    areas: list['Area'] = []
    while undesignated_fields:
        startField = undesignated_fields[0]
        area = searchArea(startField, board)
        areas.append(area)
        for field in area.getFields():
            undesignated_fields.remove(field)

    return areas


def searchArea(startField: 'Field', board: 'Board') -> 'Area':
    area = Area()
    area.addField(startField)
    
    valid_neighbors = getValidNeighbors(startField, board)   
    #step = 0 # debug variable 
    while valid_neighbors:
        next_neighbors = []
        for neighbor in valid_neighbors:
            for next in getValidNeighbors(neighbor, board):
                if next not in next_neighbors:
                    next_neighbors.append(next)
            area.addField(neighbor)
        valid_neighbors = []
        for next_neighbor in next_neighbors:
            if next_neighbor not in area.getFields():
                valid_neighbors.append(next_neighbor)
        #step += 1 # debug
        #printAreaFields(step, area, board) # debug function
    
    return area


def getValidNeighbors(field: 'Field', board: 'Board') -> list['Field']:
    neighbors = []
    for direction in ['N', 'E', 'S', 'W']:
        if not checkPathBlocked(direction, field):
            neighbor_coords = field.getNeighborCoordsFast(direction)
            if neighbor_coords:
                neighbors.append(board.getField(neighbor_coords))
    return neighbors

def findOwner(area: 'Area') -> int:
    ''' Returns the owner of the area, if there is one. Otherwise returns 0. '''
    owners = []
    for field in area.getFields():
        pawn = field.getPawn()
        if pawn:
            owners.append(pawn.getPlayer())
    if len(set(owners)) == 1:
        return owners[0]
    else:
        return 0
    

# Debug functions

def printAreaFields(step: int, area: 'Area', board: 'Board'):
    size = board.getSize()
    grid = []
    for y in range(size):
        row = []
        for x in range(size):
            if board.getField((x,y)) in area.getFields():
                row.append('X')
            else:
                row.append('O')
        row_str = ' '.join(row)
        grid.append(row_str)
    print('\n')
    print("Step:" + str(step))
    print('\n'.join(grid))