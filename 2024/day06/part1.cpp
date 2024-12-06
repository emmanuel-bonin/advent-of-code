#include <iostream>
#include <fstream>
#include <list>
#include <map>

struct Point {
  int x;
  int y;

  Point(const int x, const int y)
    : x(x)
    , y(y) {
  }

  bool operator==(Point& p) const {
    return p.x == x && p.y == y;
  }

  bool operator<(const Point& p) const {
    return x < p.x || (x == p.x && y < p.y);
  }

  bool operator>(const Point& p) const {
    return x > p.x || (x == p.x && y > p.y);
  }
};

struct MapPoint: Point {
  char type;

  MapPoint(const int x, const int y, const char type)
    : Point(x, y)
    , type(type) {
  }
};

enum Direction {
  UP,
  RIGHT,
  DOWN,
  LEFT
};

class Guard {
public:
  Point position;
  std::map<Point, bool> visited;
  Direction direction;

  Guard(int x, int y, Direction d) : position(x, y), direction(d) {
    visited[position] = true;
  }
  Guard() : position(0, 0) {}

  void setPosition(Point p) {
    position = p;
    visited[p] = true;
  }

  bool stillInMap(std::map<int, std::string> map) {
    return position.x >=0 && position.x < map[0].size() && position.y >= 0 && position.y < map.size();
  }

  void move(std::map<int, std::string> map) {
    switch (direction) {
      case UP:
        this->_moveUp(map);
        break;
      case RIGHT:
        this->_moveRight(map);
        break;
      case DOWN:
        this->_moveDown(map);
        break;
      case LEFT:
        this->_moveLeft(map);
        break;
    }
  }

private:
  void _moveUp(std::map<int, std::string> map) {
    if (position.y - 1 >= 0 && map[position.y - 1][position.x] == '#') {
      direction = RIGHT;
    } else {
      position.y -= 1;
      if (stillInMap(map)) {
        visited[position] = true;
      }
    }
  }

  void _moveRight(std::map<int, std::string> map) {
    if (position.x + 1 < map[0].size() && map[position.y][position.x + 1] == '#') {
      direction = DOWN;
    } else {
      position.x += 1;
      if (stillInMap(map)) {
        visited[position] = true;
      }
    }
  }

  void _moveDown(std::map<int, std::string> map) {
    if (position.y + 1 < map.size() && map[position.y + 1][position.x] == '#') {
      direction = LEFT;
    } else {
      position.y += 1;
      if (stillInMap(map)) {
        visited[position] = true;
      }
    }
  }

  void _moveLeft(std::map<int, std::string> map) {
    if (position.x - 1 >= 0 && map[position.y][position.x - 1] == '#') {
      direction = UP;
    } else {
      position.x -= 1;
      if (stillInMap(map)) {
        visited[position] = true;
      }
    }
  }
};

void print_map(std::map<int, std::string> map, Guard guard) {
  for (std::map<int, std::string>::iterator it = map.begin(); it != map.end(); it++) {
    std::string line = it->second;
    for (int i = 0; i < line.size(); i++) {
      if (guard.visited.find(Point(i, it->first)) != guard.visited.end()) {
        line[i] = 'X';
      }
    }
    std::cout << line << std::endl;
  }
}

int main() {
  std::string input = "./input.txt";

  std::string line;
  std::fstream file(input);
  std::map<int, std::string> map;
  Guard guard;

  int i = 0;
  while(std::getline(file, line)) {
    map[i] = line;
    for (int j = 0; j < line.size(); j++) {
      if (line[j] == '^') {
        guard.setPosition(Point(j, i));
        guard.direction = UP;
      }
    }
    i++;
  }
  while (guard.stillInMap(map)) {
    guard.move(map);
  }
  print_map(map, guard);

  std::cout << guard.visited.size() << std::endl;
  return 0;
}
