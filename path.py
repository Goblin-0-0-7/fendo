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
    if direction == 'N' and field.getWall(direction):
        return True
    if direction == 'E' and field.getWall(direction):
        return True
    if direction == 'S' and field.getWall(direction):
        return True
    if direction == 'W' and field.getWall(direction):
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
        
    def getFields(self):
        return self.fields
    
    def addField(self, field: 'Field'):
        self.fields.append(field)


def findAreas(openFields, board_fields) -> list['Area']:
    areas: list['Area'] = []
    while openFields:
        startField = openFields[0]
        openFields, area = searchArea(startField, openFields, board_fields)
        areas.append(area)

    return areas


def searchArea(startField: 'Field', openFields: list['Field'], board_fields) -> tuple[list['Field'], 'Area']:
    area = Area()
    area.addField(startField)
    openFields.remove(startField)
    
    areaFields = []
    neighbors = getValidNeighbors(startField)
    areaFields.extend(neighbors)
    while openFields and neighbors:
        for neighbor in neighbors:
            neighbors = getValidNeighbors(neighbor)
        
    
    for field in openFields:
        if findPath(startField.getCoordinates(), field.getCoordinates(), board_fields):
            area.addField(field)
            openFields.remove(field)
        else:
            print("gapo")
    
    return openFields, area
    

def getValidNeighbors(field: 'Field', openFields) -> list['Field']:
    neighbors = []
    for direction in ['N', 'E', 'S', 'W']:
        if not checkPathBlocked(direction, field):
            neighbor = field.getNeighbor(direction)
            if neighbor in openFields:
            neighbors.append(neighbor)
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