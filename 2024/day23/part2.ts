import * as fs from 'fs'
import { uniq } from 'lodash'

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
	for (const computer of Object.keys(computersByName)) {
		const group = [computer]
		for (let i = 0; i < computersByName[computer].length - 1; i++) {
			for (let j = i + 1; j < computersByName[computer].length; j++) {
				if (computersByName[computersByName[computer][i]].includes(computersByName[computer][j])) {
					group.push(computersByName[computer][i], computersByName[computer][j])
				}
			}
		}
		if (group.length > 1) {
			computersGroups.push(uniq(group))
		}
	}

	let finished = false
	while (!finished) {
		finished = true
		for (let a = 0; a < computersGroups.length; a++) {
			for (let i = 0; i < computersGroups[a].length - 1; i++) {
				for (let j = i + 1; j < computersGroups[a].length; j++) {
					if (!computersByName[computersGroups[a][i]].includes(computersGroups[a][j])) {
						delete computersGroups[a]
						computersGroups = computersGroups.filter(g => g)
						finished = false
						break
					}
				}
				if (!finished) {
					break
				}
			}
			if (!finished) {
				break
			}
		}
	}
	computersGroups = computersGroups.map(g => g.sort())

	const uniqComputersGroups: string[][] = []
	for (const group of computersGroups) {
		const groupStr = group.join('-')
		if (!uniqComputersGroups.find(g => g.join('-') === groupStr)) {
			uniqComputersGroups.push(group)
		}
	}

	const largestGroup = uniqComputersGroups.sort((a, b) => b.length - a.length)[0]
	console.log(largestGroup.join(','))
}

main()
