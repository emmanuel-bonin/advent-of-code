import * as fs from 'fs'

type Key = {
	columns: number[]
	maxHeight?: number
}

type Lock = {
	pins: number[]
	maxHeight?: number
}

function readFile() {
	const keys: Key[] = []
	const locks: Lock[] = []

	const linesGroup = fs.readFileSync('input.txt').toString().split('\n\n')

	for (const group of linesGroup) {
		let lines = group.split('\n')
		const key: Key = { columns: [] }
		const lock: Lock = { pins: [] }

		if (lines[0] === '#####') {
			lines = lines.filter(l => l.length > 0)
			lines.shift()
			lock.maxHeight = lines.length - 1
			lock.pins.push(0, 0, 0, 0, 0)
			for (const line of lines) {
				for (let i = 0; i < line.length; i++) {
					lock.pins[i] += line[i] === '#' ? 1 : 0
				}
			}
			locks.push(lock)
		} else {
			lines = lines.filter(l => l.length > 0)
			lines.pop()
			key.maxHeight = lines.length - 1
			key.columns.push(0, 0, 0, 0, 0)
			for (const line of lines) {
				for (let i = 0; i < line.length; i++) {
					key.columns[i] += line[i] === '#' ? 1 : 0
				}
			}
			keys.push(key)
		}
	}
	return { keys, locks }
}

function main() {
	const { keys, locks } = readFile()

	let result = 0
	for (const lock of locks) {
		for (const key of keys) {
			let matches = true
			let overlap = -1
			for (let i = 0; i < key.columns.length; i++) {
				if (key.maxHeight > lock.maxHeight || key.columns[i] + lock.pins[i] > 5) {
					overlap = i
					matches = false
					break
				}
			}
			if (matches) {
				result++
			}
		}
	}

	console.log(result)
}

main()
