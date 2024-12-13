const fs = require('fs')

const input = fs.readFileSync('./input.txt').toString()

function parseFile() {
	const l = []
	const r = []
	input.split('\n').map(l => l.split(' ').filter(s => s.length)).filter(s => s.length).map(a => {
		l.push(parseInt(a[0]))
		r.push(parseInt(a[1]))
	})
	return [l.sort(), r.sort()]
}

function main() {
	const data = parseFile()
	console.log(data[0].map((n, i) => n * data[1].map(m => m === data[0][i]).reduce((a, b) => a + b)).reduce((a, b) => a + b))
}

main()
