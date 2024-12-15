import * as fs from 'fs'

type Case = {
	x: number
	y: number
	type: '#' | 'O'
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
				walls.push({ x, y, type })
				width = x+1
				height = y+1
			} else if (type === 'O') {
				boxes.push({ x, y, type })
			} else if (type === '<' || type === '^' || type === '>' || type === 'v') {
				moveSequence.push(type)
			} else if (type === '@') {
				robot = { x, y }
			}
		}
	}
	return {
		walls,
		boxes,
		robot: robot!,
		moveSequence,
		width,
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
				process.stdout.write('O')
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
	const nextBox = boxes.find(b => b.x === nextCase.x && b.y === nextCase.y)
	if (nextBox) {
		if (!moveItem(nextBox, dirX, dirY, walls, boxes)) {
			return false
		}
	}
	item.x += dirX
	item.y += dirY
	return true
}

function main() {
	const config = parseFile('input.txt')

	for (const move of config.moveSequence) {
		let dirX = 0
		let dirY = 0
		switch (move) {
			case '<':
				dirX = -1
				break
			case '>':
				dirX = 1
				break
			case '^':
				dirY = -1
				break
			case 'v':
				dirY = 1
				break
		}
		moveItem(config.robot, dirX, dirY, config.walls, config.boxes)
	}
	let result = 0
	for (const box of config.boxes) {
		result += 100 * box.y + box.x
	}
	console.log(result)
}

main()
