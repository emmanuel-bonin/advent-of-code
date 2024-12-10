import * as fs from 'fs'

type Position = {
	x: number
	y: number
}

type Node = {
	value: string
	position: Position
	children: Node[]
}

type Map = string[]

function readFile(): Map {
	const file = fs.readFileSync("example.txt")

	return file.toString().split("\n").filter(s => s.length)
}

function positionInMap(map: Map, x: number, y: number): boolean {
	return x >= 0 && x < map[0].length && y >= 0 && y < map.length
}

function getChildNodes(map: Map, currentNode: Node): Node[] {
	const nextValue = (parseInt(currentNode.value) + 1).toString()
	if (currentNode.value === '9') {
		return [{ ...currentNode, children: [] }]
	}


	let children: Node[] = []

	if (positionInMap(map, currentNode.position.x + 1, currentNode.position.y) &&
		map[currentNode.position.y][currentNode.position.x + 1] === nextValue) {
		const child: Node = {
			value: nextValue,
			position: { x: currentNode.position.x + 1, y: currentNode.position.y },
			children: []
		}

		child.children = getChildNodes(map, child)
		children.push(child)
	}
	if (positionInMap(map, currentNode.position.x - 1, currentNode.position.y) &&
		map[currentNode.position.y][currentNode.position.x - 1] === nextValue) {
		const child: Node = {
			value: nextValue,
			position: { x: currentNode.position.x - 1, y: currentNode.position.y },
			children: []
		}

		child.children = getChildNodes(map, child)
		children.push(child)
	}
	if (positionInMap(map, currentNode.position.x, currentNode.position.y + 1) &&
		map[currentNode.position.y + 1][currentNode.position.x] === nextValue) {
		const child: Node = {
			value: nextValue,
			position: { x: currentNode.position.x, y: currentNode.position.y + 1 },
			children: []
		}

		child.children = getChildNodes(map, child)
		children.push(child)
	}
	if (positionInMap(map, currentNode.position.x, currentNode.position.y - 1) &&
		map[currentNode.position.y - 1][currentNode.position.x] === nextValue) {
		const child: Node = {
			value: nextValue,
			position: { x: currentNode.position.x, y: currentNode.position.y - 1 },
			children: []
		}

		child.children = getChildNodes(map, child)
		children.push(child)
	}
	return children
}

type DebugOpts = {
	lvl: number
}
function iterateNodes(nodes: Node[], score: number, opts?: DebugOpts): number {
	if (opts) {
		for (let i = 0; i < opts.lvl; i++) {
			process.stdout.write("  ")
		}
		console.log(`Node has ${nodes.length} children`)
	}

	if (nodes.length > 1) {
		score++
	}

	let result = 0
	for (const node of nodes) {
		if (opts) {
			for (let i = 0; i < opts.lvl; i++) {
				process.stdout.write("  ")
			}
			console.log(`Node(${node.value}) [${node.position.x}, ${node.position.y}] has ${node.children.length} children`)
		}

		if (node.value === '9') {
			result++
		}
		result += iterateNodes(node.children, score, opts ? { lvl: opts.lvl + 1 } : undefined)
	}
	return result
}

function main() {
	const map = readFile()
	const nodes: Node[] = []

	for (let y = 0; y < map.length; y++) {
		for (let x = 0; x < map[y].length; x++) {
			if (map[y][x] === '0') {
				const node: Node = { value: '0', position: { x, y }, children: [] }

				node.children = getChildNodes(map, node)
				nodes.push(node)
			}
		}
	}

	let result = 0
	for (const node of nodes) {
		const opts = { lvl: 1 }

		result += iterateNodes(node.children, 0)
	}
	console.log(result / 2)
}

main()
