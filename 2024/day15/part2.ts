import * as fs from 'fs'

type Case = {
	x: number
	y: number
	type: '#' | '[' | ']'
}

type Robot = Omit<Case, 'type'>

type MoveSequence = Array<'<' | '^' | '>' | 'v'>

type InputConfig = {
	walls: Case[]
	boxes: Case[]
	robot: Robot
	moveSequence: MoveSequence
	width: number
	height: number
}
function parseFile(filename: string): InputConfig {
	const input = fs.readFileSync(filename, 'utf8')
	const lines = input.split('\n')

	let width = 0
	let height = 0
	const walls: Case[] = []
	const boxes: Case[] = []
	let robot: Robot | null = null
	const moveSequence: MoveSequence = []

	for (let y = 0; y < lines.length; y++) {
		const line = lines[y]
		for (let x = 0; x < line.length; x++) {
			const type = line[x]
			if (type === '#') {
				walls.push({ x: x * 2, y, type })
				walls.push({ x: x * 2 + 1, y, type })
				width = x + 1
				height = y + 1
			} else if (type === 'O') {
				boxes.push({ x: x * 2, y, type: '[' })
				boxes.push({ x: x * 2 + 1, y, type: ']' })
			} else if (type === '<' || type === '^' || type === '>' || type === 'v') {
				moveSequence.push(type)
			} else if (type === '@') {
				robot = { x: x * 2, y }
			}
		}
	}
	return {
		walls,
		boxes,
		robot: robot!,
		moveSequence,
		width: width * 2,
		height,
	}
}

function debug(input: InputConfig) {
	for (let y = 0; y < input.height; y++) {
		for (let x = 0; x < input.width; x++) {
			const wall = input.walls.find(w => w.x === x && w.y === y)
			const box = input.boxes.find(b => b.x === x && b.y === y)
			const robot = input.robot.x === x && input.robot.y === y

			if (wall) {
				process.stdout.write('#')
			} else if (box) {
				process.stdout.write(box.type)
			} else if (robot) {
				process.stdout.write('@')
			} else {
				process.stdout.write('.')
			}
		}
		process.stdout.write('\n')
	}
	process.stdout.write('\n')
}

function moveItem(item: Case | Robot, dirX: number, dirY: number, walls: Case[], boxes: Case[]) {
	const nextCase = { x: item.x + dirX, y: item.y + dirY }

	const nextWall = walls.find(w => w.x === nextCase.x && w.y === nextCase.y)
	if (nextWall) {
		return false
	}
	if (dirY === 1 || dirY === -1) {
		const nextBoxPart1 = boxes.find(b => b.x === nextCase.x && b.y === nextCase.y)

		if (nextBoxPart1) {
			let nextBoxPart2: Case | undefined
			if (nextBoxPart1.type === '[') {
				nextBoxPart2 = boxes.find(b => b.x === nextCase.x + 1 && b.y === nextCase.y)
			} else if (nextBoxPart1.type === ']') {
				nextBoxPart2 = boxes.find(b => b.x === nextCase.x - 1 && b.y === nextCase.y)
			}

			if (!nextBoxPart2) {
				if (!moveItem(nextBoxPart1, dirX, dirY, walls, boxes) || !moveItem(nextBoxPart2, dirX, dirY, walls, boxes)) {
					return false
				}
			}
		}
	} else {
		const nextBox = boxes.find(b => b.x === nextCase.x && b.y === nextCase.y)
		if (nextBox) {
			if (!moveItem(nextBox, dirX, dirY, walls, boxes)) {
				return false
			}
		}
	}
	item.x += dirX
	item.y += dirY
	return true
}

async function main() {
	const config = parseFile('example.txt')

	debug(config)

	for (const move of config.moveSequence) {
		let dirX = 0
		let dirY = 0
		console.clear()
		switch (move) {
			case '<':
				console.log('<')
				dirX = -1
				break
			case '>':
				console.log('>')
				dirX = 1
				break
			case '^':
				console.log('^')
				dirY = -1
				break
			case 'v':
				console.log('v')
				dirY = 1
				break
		}
		moveItem(config.robot, dirX, dirY, config.walls, config.boxes)
		debug(config)
		await new Promise(resolve => setTimeout(resolve, 250))
	}
	let result = 0
	for (const box of config.boxes) {
		result += 100 * box.y + box.x
	}
	console.log(result)
}

main()
