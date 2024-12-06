#include <iostream>
#include <fstream>
#include <list>
#include <map>
#include <thread>

typedef std::map<int, std::string> Map;

enum Direction {
  UP,
  RIGHT,
  DOWN,
  LEFT
};

struct Point {
  int x;
  int y;

  Point(const int x, const int y)
    : x(x)
    , y(y) {
  }
};

struct PointDirection : Point {
  Direction direction;

  PointDirection(const int x, const int y, Direction d)
    : Point(x, y)
    , direction(d) {
  }

  bool operator==(PointDirection p) const {
    return p.x == x && p.y == y && p.direction == direction;
  }

  bool operator<(const PointDirection& p) const {
    return p.direction < direction || (x < p.x || (x == p.x && y < p.y));
  }

  bool operator>(const PointDirection& p) const {
    return p.direction < direction || (x > p.x || (x == p.x && y > p.y));
  }
};

class Guard {
public:
  PointDirection position;
  std::map<PointDirection, bool> visited;
  bool stuckInMap;

  Guard(int x, int y, Direction d) : position(x, y, d), stuckInMap(false) {
    visited[position] = true;
  }
  Guard() : position(0, 0, UP), stuckInMap(false) {}

  void setPosition(PointDirection p) {
    position = p;
    visited[p] = true;
  }

  bool stillInMap(Map map) {
    return position.x >=0 && position.x < map[0].size() && position.y >= 0 && position.y < map.size();
  }

  void move(Map map) {
    PointDirection newPosition(0, 0, UP);

    switch (position.direction) {
      case UP:
        newPosition = this->_moveUp(map);
        break;
      case RIGHT:
        newPosition = this->_moveRight(map);
        break;
      case DOWN:
        newPosition = this->_moveDown(map);
        break;
      case LEFT:
        newPosition = this->_moveLeft(map);
        break;
    }
    if (visited[newPosition]) {
      stuckInMap = true;
    }
    if (stillInMap(map)) {
      position = newPosition;
      visited[position] = true;
    }
  }

private:
  PointDirection _moveUp(Map map) {
    if (position.y - 1 >= 0 && map[position.y - 1][position.x] == '#' || position.y - 1 >= 0 && map[position.y - 1][position.x] == 'O') {
      return PointDirection(position.x, position.y, RIGHT);
    } else {
      return PointDirection(position.x, position.y - 1, position.direction);
    }
  }

  PointDirection _moveRight(Map map) {
    if (position.x + 1 < map[0].size() && map[position.y][position.x + 1] == '#' || position.x + 1 < map[0].size() && map[position.y][position.x + 1] == 'O') {
      return PointDirection(position.x, position.y, DOWN);
    } else {
      return PointDirection(position.x + 1, position.y, position.direction);
    }
  }

  PointDirection _moveDown(Map map) {
    if (position.y + 1 < map.size() && map[position.y + 1][position.x] == '#' || position.y + 1 < map.size() && map[position.y + 1][position.x] == 'O') {
      return PointDirection(position.x, position.y, LEFT);
    } else {
      return PointDirection(position.x, position.y + 1, position.direction);
    }
  }

  PointDirection _moveLeft(Map map) {
    if (position.x - 1 >= 0 && map[position.y][position.x - 1] == '#' || position.x - 1 >= 0 && map[position.y][position.x - 1] == 'O') {
      return PointDirection(position.x, position.y, UP);
    } else {
      return PointDirection(position.x - 1, position.y, position.direction);
    }
  }
};

void print_map(Map map, Guard guard) {
  int y = 0;
  for (Map::iterator it = map.begin(); it != map.end(); it++) {
    std::string line = it->second;
    for (int x = 0; x < line.size(); x++) {
      for (std::map<PointDirection, bool>::iterator it = guard.visited.begin(); it != guard.visited.end(); it++) {
        if (it->first.x == x && it->first.y == y && line[x] != 'O') {
          line[x] = 'X';
        }
      }
    }
    std::cout << line << std::endl;
    y++;
  }
}

std::string hash(Map m) {
  std::string hash = "";
  int n = 0;
  for (Map::iterator it = m.begin(); it != m.end(); it++) {
    hash += it->second;
  }
  return hash;
}

std::list<Map> generateMapsToTest(Map map, Guard startGuard) {
  std::list<Map> maps;
  Direction currentDirection = startGuard.position.direction;

  startGuard.move(map);
  std::map<std::string, bool> alreadyTested;

  while (startGuard.stillInMap(map)) {
    Point prevPosition = startGuard.position;
    startGuard.move(map);

    if (startGuard.stillInMap(map) && (startGuard.position.x != prevPosition.x || startGuard.position.y != prevPosition.y)) {
      Map newMap = map;
      newMap[startGuard.position.y][startGuard.position.x] = 'O';
      std::string hashValue = hash(newMap);
      if (!alreadyTested[hashValue]) {
        maps.push_back(newMap);
        alreadyTested[hashValue] = true;
      }
    }
  }
  return maps;
}

void testMaps(std::list<Map> maps, PointDirection baseGuardPosition, int id, int *mapsStuck) {
  int testedMap = 0;
  for (std::list<Map>::iterator it = maps.begin(); it != maps.end(); it++) {
    Guard guard(baseGuardPosition.x, baseGuardPosition.y, baseGuardPosition.direction);
    while (guard.stillInMap(*it)) {
      if (guard.stuckInMap) {
        (*mapsStuck)++;
        break;
      }
      guard.move(*it);
    }
    testedMap++;
    std::cout << "[THREAD " << id << "] tested map: " << testedMap << "/" << maps.size() << " stuck in " << (*mapsStuck) << std::endl;
  }
  std::cout << "[THREAD " << id << "] stuck maps: " << *mapsStuck << std::endl;
}

int main() {
  std::string input = "./input.txt";

  std::string line;
  std::fstream file(input);
  Map map;
  PointDirection baseGuardPosition(0, 0, UP);

  int i = 0;
  while(std::getline(file, line)) {
    map[i] = line;
    for (int j = 0; j < line.size(); j++) {
      if (line[j] == '^') {
        baseGuardPosition = PointDirection(j, i, UP);
      }
    }
    i++;
  }

  std::list<Map> mapToTest = generateMapsToTest(map, Guard(baseGuardPosition.x, baseGuardPosition.y, baseGuardPosition.direction));
  std::cout << "maps to test: " << mapToTest.size() << std::endl;

  int testedMap = 0;
  const int nth = 8;
  std::list<std::thread *> threads;
  int mapsStuck = 0;

  i = 0;
  int n = 0;
  std::list<Map> threadMaps;
  for (std::list<Map>::iterator it = mapToTest.begin(); it != mapToTest.end(); it++) {

    threadMaps.push_back(*it);
    if (i == mapToTest.size() / nth) {
      threads.push_back(new std::thread(testMaps, threadMaps, baseGuardPosition, n, &mapsStuck));
      threadMaps.clear();
      n++;
      i = 0;
    } else {
      i++;
    }
  }
  threads.push_back(new std::thread(testMaps, threadMaps, baseGuardPosition, n, &mapsStuck));
  for (std::list<std::thread *>::iterator it = threads.begin(); it != threads.end(); it++) {
    (*it)->join();
  }

  std::cout << "maps stuck: " << mapsStuck << std::endl;

  return 0;
}
