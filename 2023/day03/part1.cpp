#include <iostream>
#include <cstdlib>
#include <sstream>
#include <string>
#include <fstream>
#include <list>
#include <sstream>

typedef struct s_number {
  int value;
  int start_x;
  int end_x;
  int y;
} Number;

typedef struct s_symbol {
  char value;
  int x;
  int y;
} Symbol;

bool number_next_to_symbol(Number n, Symbol s) {
  return s.x >= n.start_x -1 && s.x <= n.end_x + 1 && s.y >= n.y -1 && s.y <= n.y + 1;
}

int main() {
  //const std::string FILENAME = "./example.txt";
  const std::string FILENAME = "./input.txt";
  std::ifstream file(FILENAME);
  std::string line;
  std::list<Number> numbers;
  std::list<Symbol> symbols;

  int y = 0;
  while (std::getline(file, line)) {
    for (int i = 0; i < line.size(); i++) {
      if (line[i] >= '0' && line[i] <= '9') {
	std::stringstream ss;
	int j;
	for (j = i; line[j] && line[j] >= '0' && line[j] <= '9'; j++) {
	  ss << line[j];
	}
	Number n;
	ss >> n.value;
	n.start_x = i;
	n.end_x = j - 1;
	n.y = y;
	i = j - 1;
	numbers.push_back(n);
      } else if (line[i] != '.') {
	Symbol s;
	s.value = line[i];
	s.x = i;
	s.y = y;
	symbols.push_back(s);
      }
    }
    y++;
  }

  int result = 0;
  for (std::list<Number>::iterator nit = numbers.begin(); nit != numbers.end(); nit++)
    {
      for (std::list<Symbol>::iterator sit = symbols.begin(); sit != symbols.end(); sit++)
	{
	  if (number_next_to_symbol(*nit, *sit)) {
	    result += (*nit).value;
	  }
	}
    }

  std::cout << result << std::endl;

  return 0;
}
