import * as fs from 'fs'
import { intersection, omit } from 'lodash'

function readInput(): string[] {
	return fs.readFileSync('input.txt').toString().split('\n').filter(l => l.length)
}

function main() {
	const lines = readInput()
	const computersByName: Record<string, string[]> = {}

	for (const line of lines) {
		const names = line.split('-')

		if (computersByName[names[0]]) {
			computersByName[names[0]].push(names[1])
		} else {
			computersByName[names[0]] = [names[1]]
		}
		if (computersByName[names[1]]) {
			computersByName[names[1]].push(names[0])
		} else {
			computersByName[names[1]] = [names[0]]
		}
	}

	let computersGroups: string[][] = []
	let i = 0
	for (const computer of Object.keys(computersByName)) {
		// computersGroups.push([computer])
		for (const child of computersByName[computer]) {
			const inter = intersection(computersByName[computer], computersByName[child])
			if (inter.length) {
				for (const c of inter) {
					computersGroups.push([computer, child, c])
				}
			}
		}
		i++
	}
	computersGroups = computersGroups.filter(g => g.length === 3).map(g => g.sort())
	const uniqComputersGroups: string[][] = []
	for (const group of computersGroups) {
		let found = false
		for (const c of group) {
			if (c.startsWith('t')) {
				found = true
				break
			}
		}
		if (!found) {
			continue
		}
		const groupStr = group.join('-')
		if (!uniqComputersGroups.find(g => g.join('-') === groupStr)) {
			uniqComputersGroups.push(group)
		}
	}
	console.log(uniqComputersGroups.length)
}

main()
