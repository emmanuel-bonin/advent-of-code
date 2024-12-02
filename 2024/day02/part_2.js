const fs = require('fs')

const input = fs.readFileSync('./input.txt').toString()

function parseFile() {
	const reports = []
	const data = input.split('\n').filter(l => l.length)

	for (const line of data) {
		reports.push(line.split(' ').map(n => parseInt(n)))
	}
	return reports
}

function getOrdering(n, m) {
	// ordering = 1 if order is ascending, -1 if descending, 0 if equal
	return n < m ? 1 : n > m ? -1 : 0
}

function isValid(report) {
	let firstOrdering = getOrdering(report[0], report[1])

	for (let i = 0; i < report.length - 1; i++) {
		const currentOrdering = getOrdering(report[i], report[i + 1])
		const diff = Math.max(report[i], report[i + 1]) - Math.min(report[i], report[i + 1])

		if (currentOrdering === 0 || firstOrdering !== currentOrdering) {
			return false
		} else if (diff < 1 || diff > 3) {
			return false
		}
	}
	return true
}

function isValidWithOneRemoval(report) {
	for (let i = 0; i < report.length; i++) {
		if (isValid([...report.slice(0, i), ...report.slice(i + 1)])) {
			return true
		}
	}
	return false
}

function main() {
	const data = parseFile()
	let result = 0

	for (const report of data) {
		if (isValid(report) || isValidWithOneRemoval(report)) {
			result++
		}
	}
	console.log(result)
}

main()
