class Node
  @x = 0
  @y = 0
  @type = ''

  def self.x
    @x
  end
  def x
    @x
  end

  def self.y
    @y
  end
  def y
    @y
  end

  def self.type
    @type
  end
  def type
    @type
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
      antenna.instance_variable_set('@x', x)
      antenna.instance_variable_set('@y', y)
      antenna.instance_variable_set('@type', c)
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
  antinode.instance_variable_set('@x', x)
  antinode.instance_variable_set('@y', y)
  antinode.instance_variable_set('@type', '#')

  if antinode.x >= 0 && antinode.x < max_x && antinode.y >= 0 && antinode.y < max_y
  then
    existing_antinode = antinodes.find {|an| an.x == antinode.x && an.y == antinode.y }
    if existing_antinode == nil
    then
      antinodes.push(antinode)
    end
  end
end

antinodes = []
antennas.each {
  |a|
  others = antennas.select {|e| e.type == a.type && (e.x != a.x || e.y != a.y)}
  others.each {
    |o|
    create_antinode(a.x + (a.x - o.x), a.y + (a.y - o.y), max_x, max_y, antinodes)
    create_antinode(o.x + (o.x - a.x), o.y + (o.y - a.y), max_x, max_y, antinodes)
  }
}

p antinodes.length()
