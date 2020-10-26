

def __init__(self, map):
    self.clone(map)

def __eq__(self, other) -> bool:
    for i in range(4):
        for j in range(4):
            if self.map[i][j] != other.map[i][j]:
                return False
    return True




