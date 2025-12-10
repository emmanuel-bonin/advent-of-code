import math

class Box:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
        self.connected = []

    def __repr__(self):
        res = f'(x: {self.x}, y: {self.y}, z: {self.z}'
        if self.connected:
            res += ', connected: ' + str(len(self.connected))
        res += ')'
        return res

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

def compute_distance(box1: Box, box2: Box):
    return math.sqrt(math.pow(box2.x - box1.x, 2) + math.pow(box2.y - box1.y, 2) + math.pow(box2.z - box1.z, 2))

def main():
    f = open('example.txt', 'r')
    lines = [line.strip() for line in f.readlines()]
    f.close()

    boxes: list[Box] = []
    for line in lines:
        [x, y, z] = line.split(',')
        boxes.append(Box(int(x), int(y), int(z)))

    a = 0
    circuits: list[list[Box]] = []
    # while a < 1000:
    while a < 10:
        dist = math.inf
        b1 = None
        b2 = None
        for i in range(len(boxes)):
            for j in range(len(boxes)):
                if i == j or boxes[i] in boxes[j].connected or boxes[j] in boxes[i].connected:
                    continue
                new_d = compute_distance(boxes[i], boxes[j])
                if new_d < dist:
                    dist = new_d
                    b1 = boxes[i]
                    b2 = boxes[j]
        print('shortest dist', dist, 'between boxes', b1, b2)
        b1.connected.append(b2)
        b2.connected.append(b1)
        a += 1
    res = 1
    print(res)

main()
