const fs = require('fs')

// const file = fs.readFileSync('./example.txt').toString()
const file = fs.readFileSync('./input.txt').toString()

const lines = file.split('\n').filter(s => s.length)

function print_grid(grid) {
  let s = ''
  for (const row of grid.tiles) {
    for (const tile of row) {
      if (tile.type === '.' && tile.outgoingBeams.length === 0) {
        s += tile.type
      } else if (tile.type === '.' && tile.outgoingBeams.length === 1) {
        switch (tile.outgoingBeams[0].direction) {
          case 'left':
            s += '<'
            break
          case 'right':
            s += '>'
            break
          case 'up':
            s += '^'
            break
          case 'down':
            s += 'v'
            break
        }
      } else if (tile.type === '.' && tile.outgoingBeams.length > 1) {
        s += tile.outgoingBeams.length
      } else {
        s += tile.type
      }
    }
    s += '\n'
  }
  console.log(s)
}

class Tile {
  constructor(x, y, type, maxX, maxY) {
    this.x = x
    this.y = y
    this.maxX = maxX
    this.maxY = maxY
    this.type = type
    this.incomingBeams = []
    this.outgoingBeams = []
  }

  isEnergized() {
    return this.incomingBeams.length > 0
  }

  computeOutgoingBeams(direction) {
    const existingBeam = this.incomingBeams.find(b => b.direction === direction)
    if (existingBeam) {
      return []
    }
    this.incomingBeams.push({ x: this.x, y: this.y, direction })
    switch (direction) {
      case 'right':
        if ((this.type === '.' || this.type === '-') && this.x < this.maxX - 1) {
          this.outgoingBeams.push({ x: this.x + 1, y: this.y, direction })
        } else if (this.type === '\\' && this.y < this.maxY - 1) {
          this.outgoingBeams.push({ x: this.x, y: this.y + 1, direction: 'down' })
        } else if (this.type === '/' && this.y > 0) {
          this.outgoingBeams.push({ x: this.x, y: this.y - 1, direction: 'up' })
        } else if (this.type === '|') {
          if (this.y > 0) {
            this.outgoingBeams.push({ x: this.x, y: this.y - 1, direction: 'up' })
          }
          if (this.y < this.maxY - 1) {
            this.outgoingBeams.push({ x: this.x, y: this.y + 1, direction: 'down' })
          }
        }
        break
      case 'left':
        if ((this.type === '.' || this.type === '-') && this.x > 0) {
          this.outgoingBeams.push({ x: this.x - 1, y: this.y, direction })
        } else if (this.type === '\\' && this.y > 0) {
          this.outgoingBeams.push({ x: this.x, y: this.y - 1, direction: 'up' })
        } else if (this.type === '/' && this.y < this.maxY - 1) {
          this.outgoingBeams.push({ x: this.x, y: this.y + 1, direction: 'down' })
        } else if (this.type === '|') {
          if (this.y > 0) {
            this.outgoingBeams.push({ x: this.x, y: this.y - 1, direction: 'up' })
          }
          if (this.y < this.maxY - 1) {
            this.outgoingBeams.push({ x: this.x, y: this.y + 1, direction: 'down' })
          }
        }
        break
      case 'up':
        if ((this.type === '.' || this.type === '|') && this.y > 0) {
          this.outgoingBeams.push({ x: this.x, y: this.y - 1, direction })
        } else if (this.type === '\\' && this.x > 0) {
          this.outgoingBeams.push({ x: this.x - 1, y: this.y, direction: 'left' })
        } else if (this.type === '/' && this.x < this.maxX - 1) {
          this.outgoingBeams.push({ x: this.x + 1, y: this.y, direction: 'right' })
        } else if (this.type === '-') {
          if (this.x > 0) {
            this.outgoingBeams.push({ x: this.x - 1, y: this.y, direction: 'left' })
          }
          if (this.x < this.maxX - 1) {
            this.outgoingBeams.push({ x: this.x + 1, y: this.y, direction: 'right' })
          }
        }
        break
      case 'down':
        if ((this.type === '.' || this.type === '|') && this.y < this.maxY - 1) {
          this.outgoingBeams.push({ x: this.x, y: this.y + 1, direction })
        } else if (this.type === '\\' && this.x < this.maxX - 1) {
          this.outgoingBeams.push({ x: this.x + 1, y: this.y, direction: 'right' })
        } else if (this.type === '/' && this.x > 0) {
          this.outgoingBeams.push({ x: this.x - 1, y: this.y, direction: 'left' })
        } else if (this.type === '-') {
          if (this.x > 0) {
            this.outgoingBeams.push({ x: this.x - 1, y: this.y, direction: 'left' })
          }
          if (this.x < this.maxX - 1) {
            this.outgoingBeams.push({ x: this.x + 1, y: this.y, direction: 'right' })
          }
        }
        break
    }
    return this.outgoingBeams
  }
}

class Grid {
  constructor(sizeX, sizeY) {
    this.sizeX = sizeX
    this.sizeY = sizeY
    this.tiles = new Array(sizeY)
    this.beams = []
  }

  compute(x, y, direction) {
    this.beams.push({ x, y, direction })
    while (this.beams.length) {
      const b = this.beams.pop()
      this.beams.push(...this.tiles[b.y][b.x].computeOutgoingBeams(b.direction))
    }
  }

  addTile(x, y, type) {
    if (this.tiles[y] === undefined) {
      this.tiles[y] = new Array(this.sizeX)
    }
    this.tiles[y][x] = new Tile(x, y, type, this.sizeX, this.sizeY)
  }

  getTotalEnergized() {
    let res = 0
    for (let y = 0; y < this.sizeY; y++) {
      for (let x = 0; x < this.sizeX; x++) {
        if (this.tiles[y][x].isEnergized()) {
          res++
        }
      }
    }
    return res
  }
}

const grid = new Grid(lines.length, lines[0].length)
for (let y = 0; y < lines.length; y++) {
  for (let x = 0; x < lines[y].length; x++) {
    grid.addTile(x, y, lines[y][x])
  }
}

grid.compute(0, 0, 'right')
const res = grid.getTotalEnergized()
print_grid(grid)
console.log(res)
