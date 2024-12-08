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

    antinode_antenna_1 = Node.new
    antinode_antenna_1.instance_variable_set('@x', a.x)
    antinode_antenna_1.instance_variable_set('@y', a.y)
    antinode_antenna_1.instance_variable_set('@type', '#')
    existing_antinode_antenna_1 = antinodes.find {|an| an.x == antinode_antenna_1.x && an.y == antinode_antenna_1.y }
    if existing_antinode_antenna_1 == nil
    then
      antinodes.push(antinode_antenna_1)
    end
    antinode_antenna_2 = Node.new
    antinode_antenna_2.instance_variable_set('@x', a.x)
    antinode_antenna_2.instance_variable_set('@y', a.y)
    antinode_antenna_2.instance_variable_set('@type', '#')
    existing_antinode_antenna_2 = antinodes.find {|an| an.x == antinode_antenna_2.x && an.y == antinode_antenna_2.y }
    if existing_antinode_antenna_2 == nil
    then
      antinodes.push(antinode_antenna_2)
    end

    diffx = a.x - o.x
    diffy = a.y - o.y
    an_x = a.x + diffx
    an_y = a.y + diffy
    while (an_x >= 0 && an_x < max_x && an_y >= 0 && an_y < max_y)
      antinode = Node.new
      antinode.instance_variable_set('@x', an_x)
      antinode.instance_variable_set('@y', an_y)
      antinode.instance_variable_set('@type', '#')
      if antinode.x >= 0 && antinode.x < max_x && antinode.y >= 0 && antinode.y < max_y
      then
        existing_antinode = antinodes.find {|an| an.x == antinode.x && an.y == antinode.y }
        if existing_antinode == nil
        then
          antinodes.push(antinode)
        end
      end
      an_x += diffx
      an_y += diffy
    end

    diffx = o.x - a.x
    diffy = o.y - a.y
    an_x = o.x + diffx
    an_y = o.y + diffy
    while (an_x >= 0 && an_x < max_x && an_y >= 0 && an_y < max_y)
      antinode = Node.new
      antinode.instance_variable_set('@x', an_x)
      antinode.instance_variable_set('@y', an_y)
      antinode.instance_variable_set('@type', '#')
      if antinode.x >= 0 && antinode.x < max_x && antinode.y >= 0 && antinode.y < max_y
      then
        existing_antinode = antinodes.find {|an| an.x == antinode.x && an.y == antinode.y }
        if existing_antinode == nil
        then
          antinodes.push(antinode)
        end
      end
      an_x += diffx
      an_y += diffy
    end
  }
}

p antinodes.length()
