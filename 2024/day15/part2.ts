import * as fs from 'fs'
import * as readline from 'node:readline'

type Case = {
	x: number
	y: number
	type: '#' | '[' | ']'
}

type Box = {
	part1: Case
	part2: Case
}

type Robot = Omit<Case, 'type'>

type MoveSequence = Array<'<' | '^' | '>' | 'v'>

type InputConfig = {
	walls: Case[]
	boxes: Box[]
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
	const boxes: Box[] = []
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
				boxes.push({
					part1: { x: x * 2, y, type: '[' },
					part2: { x: x * 2 + 1, y, type: ']' },
				})
				boxes.push()
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

let ITERATION = 0

function debug(input: InputConfig, createFile = false, move?: string) {
	const filename = `./output/debug-${ ITERATION++ }.txt`
	let buffer = ''
	for (let y = 0; y < input.height; y++) {
		for (let x = 0; x < input.width; x++) {
			const wall = input.walls.find(w => w.x === x && w.y === y)
			const box1 = input.boxes.find(b => b.part1.x === x && b.part1.y === y)
			const box2 = input.boxes.find(b => b.part2.x === x && b.part2.y === y)
			const robot = input.robot.x === x && input.robot.y === y

			if (wall) {
				// process.stdout.write('#')
				buffer += '#'
			} else if (box1) {
				// process.stdout.write('[')
				buffer += '['
			} else if (box2) {
				// process.stdout.write(']')
				buffer += ']'
			} else if (robot) {
				// process.stdout.write(move ?? '@')
				buffer += move ?? '@'
			} else {
				// process.stdout.write('.')
				buffer += '.'
			}
		}
		// process.stdout.write('\n')
		buffer += '\n'
	}
	if (createFile) {
		fs.writeFileSync(filename, buffer)
	} else {
		console.log(buffer)
	}
	// process.stdout.write('\n')
}

function moveBox(item: Box, dirX: number, dirY: number, walls: Case[], boxes: Box[], operate = true) {
	if ([1, -1].includes(dirY)) {
		// Get the two cases next to the box in wanted direction
		const nextCase1 = { x: item.part1.x + dirX, y: item.part1.y + dirY }
		const nextCase2 = { x: item.part2.x + dirX, y: item.part2.y + dirY }

		// Check if the next cases are walls
		const nextWall1 = walls.find(w => w.x === nextCase1.x && w.y === nextCase1.y)
		const nextWall2 = walls.find(w => w.x === nextCase2.x && w.y === nextCase2.y)

		// If one of the next cases is a wall, the box can't move
		if (nextWall1 || nextWall2) {
			return false
		}

		// Get the boxes that are in the next cases
		const nextBox1 = boxes.find(b => b.part1.x === nextCase1.x && b.part1.y === nextCase1.y) || boxes.find(b => b.part2.x === nextCase1.x && b.part2.y === nextCase1.y)
		let nextBox2 = boxes.find(b => b.part1.x === nextCase2.x && b.part1.y === nextCase2.y) || boxes.find(b => b.part2.x === nextCase2.x && b.part2.y === nextCase2.y)

		// If the two boxes are the same, we only keep one
		if (nextBox1 && nextBox2 && nextBox1.part1.x === nextBox2.part1.x && nextBox1.part1.y === nextBox2.part1.y) {
			nextBox2 = undefined
		}

		// If the two next cases are boxes, we move them
		// If one of the two boxes can't move, we return false
		if (nextBox1 && nextBox2) {
			if (!moveBox(nextBox1, dirX, dirY, walls, boxes, false) || !moveBox(nextBox2, dirX, dirY, walls, boxes, false)) {
				return false
			}
			moveBox(nextBox1, dirX, dirY, walls, boxes, operate)
			moveBox(nextBox2, dirX, dirY, walls, boxes, operate)

			// If only one of the two next cases is a box, we try to move it and if it can we actually move it
		} else if (nextBox1) {
			if (!moveBox(nextBox1, dirX, dirY, walls, boxes, false)) {
				return false
			}
			moveBox(nextBox1, dirX, dirY, walls, boxes, operate)
			// If only one of the two next cases is a box, we try to move it and if it can we actually move it
		} else if (nextBox2) {
			if (!moveBox(nextBox2, dirX, dirY, walls, boxes, false)) {
				return false
			}
			moveBox(nextBox2, dirX, dirY, walls, boxes, operate)
		}
	} else if (dirX === -1) {
		// Get the next case next to the box in wanted direction
		const nextCase = { x: item.part1.x + dirX, y: item.part1.y + dirY }
		const nextWall = walls.find(w => w.x === nextCase.x && w.y === nextCase.y)
		if (nextWall) {
			return false
		}
		const nextBox = boxes.find(b => b.part2.x === nextCase.x && b.part2.y === nextCase.y)
		if (nextBox) {
			if (!moveBox(nextBox, dirX, dirY, walls, boxes)) {
				return false
			}
		}
	} else {
		const nextCase = { x: item.part2.x + dirX, y: item.part2.y + dirY }
		const nextWall = walls.find(w => w.x === nextCase.x && w.y === nextCase.y)
		if (nextWall) {
			return false
		}
		const nextBox = boxes.find(b => b.part1.x === nextCase.x && b.part1.y === nextCase.y)
		if (nextBox) {
			if (!moveBox(nextBox, dirX, dirY, walls, boxes)) {
				return false
			}
		}
	}

	if (operate) {
		item.part1.x += dirX
		item.part1.y += dirY
		item.part2.x += dirX
		item.part2.y += dirY
	}
	return true
}

function moveItem(item: Case | Robot, dirX: number, dirY: number, walls: Case[], boxes: Box[]) {
	const nextCase = { x: item.x + dirX, y: item.y + dirY }

	const nextWall = walls.find(w => w.x === nextCase.x && w.y === nextCase.y)
	if (nextWall) {
		return
	}
	const nextBox = boxes.find(b => b.part1.x === nextCase.x && b.part1.y === nextCase.y) || boxes.find(b => b.part2.x === nextCase.x && b.part2.y === nextCase.y)

	if (nextBox) {
		if (!moveBox(nextBox, dirX, dirY, walls, boxes)) {
			return
		}
	}
	item.x += dirX
	item.y += dirY
}

const keypress = async () => {
	process.stdin.setRawMode(true)
	return new Promise(resolve => process.stdin.once('data', (data) => {
		process.stdin.setRawMode(false)
		if (data[0] === 0x71) {
			process.exit(0)
		}
		if (data[2] === 0x41) {
			resolve('^')
		} else if (data[2] === 0x42) {
			resolve('v')
		} else if (data[2] === 0x43) {
			resolve('>')
		} else if (data[2] === 0x44) {
			resolve('<')
		}
		resolve(void 0)
	}))
}

async function main() {
	const interactive = process.argv.includes('--interactive')
	const config = parseFile('input.txt')


	if (interactive) {
		debug(config)
		while (1) {
		let dirX = 0
		let dirY = 0

		const move = await keypress()

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
		debug(config, false, move as string)
		}
	} else {
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
			result += 100 * box.part1.y + box.part1.x
		}
		console.log(result)
	}
}

main()
