const fs = require('fs')

const input = fs.readFileSync('./input.txt').toString()

const lines = input.split('\n')

const NUMBER = {
    one: 1,
    two: 2,
    three: 3,
    four: 4,
    five: 5,
    six: 6,
    seven: 7,
    eight: 8,
    nine: 9
}

for (const line of lines) {
    for (let i of line) {
	console.log('i = ' + i)
    }
}
