const fs = require('fs')

const f = fs.readFileSync('./example.txt').toString()

const lines = f.split('\n')

const cards = []

for (const line of lines) {
    console.log(line)
}
