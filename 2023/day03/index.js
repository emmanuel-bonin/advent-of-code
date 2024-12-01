const fs = require('fs')
const readline = require('readline')

const FILENAME = './input.txt'

async function main() {
    const filestream = fs.createReadStream(FILENAME)
    const rl = readline.createInterface({
	input: filestream,
	crlfDelayL: Infinity
    })
    const numbers = []
    const symbols = []

    let y = 0
    for await (const line of rl) {
	for (let i = 0; i < line.length; i++) {
	    let tmp = ''
	    let j
	    if (line[i] >= '0' && line[i] <= '9') {
		for (j = i; line[j] && line[j] >= '0' && line[j] <= '9'; j++) {
		    tmp += line[j]
		}
		numbers.push({
		    value: Number(tmp),
		    start_x: i,
		    end_x: j - 1,
		    y: y,
		})
		i = j - 1;
	    } else if (line[i] !== '.') {
		symbols.push({
		    value: line[i],
		    x: i,
		    y: y,
		})
	    }
	}
	y++
    }

    let result = 0

    for (const n of numbers) {
	for (const s of symbols) {
	    if (s.x >= n.start_x -1 && s.x <= n.end_x + 1 && s.y >= n.y -1 && s.y <= n.y + 1) {
		result += n.value
	    }
	}
    }
    console.log(result)
}

main()
