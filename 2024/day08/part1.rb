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

antinodes = []
antennas.each {
  |a|
  others = antennas.select {|e| e.type == a.type && (e.x != a.x || e.y != a.y)}
  others.each {
    |o|
    antinode1 = Node.new
    antinode2 = Node.new

    antinode1.instance_variable_set('@x', a.x + (a.x - o.x))
    antinode1.instance_variable_set('@y', a.y + (a.y - o.y))
    antinode1.instance_variable_set('@type', '#')

    antinode2.instance_variable_set('@x', o.x + (o.x - a.x))
    antinode2.instance_variable_set('@y', o.y + (o.y - a.y))
    antinode2.instance_variable_set('@type', '#')

    if antinode1.x >= 0 && antinode1.x < max_x && antinode1.y >= 0 && antinode1.y < max_y
    then
      existing_antinode1 = antinodes.find {|an| an.x == antinode1.x && an.y == antinode1.y }
      if existing_antinode1 == nil
      then
        antinodes.push(antinode1)
      end
    end
    if antinode2.x >= 0 && antinode2.x < max_x && antinode2.y >= 0 && antinode2.y < max_y
    then
      existing_antinode2 = antinodes.find {|an| an.x == antinode2.x && an.y == antinode2.y }
      if existing_antinode2 == nil
      then
        antinodes.push(antinode2)
      end
    end
  }
}

p antinodes.length()
