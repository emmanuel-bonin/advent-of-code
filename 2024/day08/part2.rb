class Node
  @x = 0
  @y = 0
  @type = ''

  def x
    @x
  end
  def x=(value)
    @x = value
  end

  def y
    @y
  end
  def y=(value)
    @y = value
  end

  def type
    @type
  end
  def type=(value)
    @type = value
  end
end

antennas = []

y = 0
max_x = 0
max_y = 0
File.readlines('input.txt', chomp: true).each do |line|
  x = 0
  line.each_char {
    |c|
    if (c != '.')
    then
      antenna = Node.new
      antenna.x = x
      antenna.y = y
      antenna.type = c
      antennas.push(antenna)
    end
    x = x + 1
  }
  max_x = x
  y = y + 1
end

max_y = y

def create_antinode(x, y, max_x, max_y, antinodes)
  antinode = Node.new
  antinode.x = x
  antinode.y = y
  antinode.type = '#'
  if antinode.x >= 0 && antinode.x < max_x && antinode.y >= 0 && antinode.y < max_y
  then
    existing_antinode = antinodes.find {|an| an.x == antinode.x && an.y == antinode.y }
    if existing_antinode == nil
    then
      antinodes.push(antinode)
    end
  end
end

def create_antinodes_in_line(a, b, max_x, max_y, antinodes)
  diffx = a.x - b.x
  diffy = a.y - b.y
  an_x = a.x + diffx
  an_y = a.y + diffy
  while (an_x >= 0 && an_x < max_x && an_y >= 0 && an_y < max_y)
    create_antinode(an_x, an_y, max_x, max_y, antinodes)
    an_x += diffx
    an_y += diffy
  end
end

antinodes = []
antennas.each {
  |a|
  others = antennas.select {|e| e.type == a.type && (e.x != a.x || e.y != a.y)}
  others.each {
    |o|

    # Create antinode at position of current antenna
    create_antinode(a.x, a.y, max_x, max_y, antinodes)

    # Create antinodes in line before current antenna
    create_antinodes_in_line(a, o, max_x, max_y, antinodes)

    # Create antinodes in line after other found antenna
    create_antinodes_in_line(o, a, max_x, max_y, antinodes)
  }
}

p antinodes.length()