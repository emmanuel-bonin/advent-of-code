import * as fs from 'fs'

type Binary = 0 | 1

type Wire = {
	name: string
	value?: Binary
}

type GateType = 'AND' | 'OR' | 'XOR'
type Gate = {
	leftInput: Wire
	rightInput: Wire
	output: Wire
	type: GateType
}

type Circuit = {
	wires: Wire[]
	gates: Gate[]
}

function readFile(): Circuit {
	const f = fs.readFileSync('input.txt', 'utf8')
	const circuit: Circuit = {
		gates: [],
		wires: [],
	}

	const lines = f.split('\n')

	for (let line of lines) {
		line = line.trim()
		if (line.includes(':')) {
			const [name, value] = line.split(': ')
			circuit.wires.push({ name, value: parseInt(value) as Binary })
		} else if (line !== '') {
			const [left, output] = line.split(' -> ')
			const inputs = left.split(' ')
			const leftInput = circuit.wires.find((w) => w.name === inputs[0]) ?? { name: inputs[0] }
			const rightInput = circuit.wires.find((w) => w.name === inputs[2]) ?? { name: inputs[2] }
			const gate: Gate = {
				leftInput: leftInput,
				rightInput: rightInput,
				output: { name: output },
				type: inputs[1] as GateType,
			}
			circuit.gates.push(gate)
		}
	}

	return circuit
}

function main() {
	const circuit = readFile()

	const addGates: Gate[] = []
	const resultWires: Wire[] = []
	for (const gate of circuit.gates) {
		if (gate.type === 'AND') {
			if (gate.leftInput.name.startsWith('x') && gate.rightInput.name.startsWith('y')) {
				addGates.push({ leftInput: gate.leftInput, rightInput: gate.rightInput, output: gate.output, type: 'AND' })
			} else if (gate.rightInput.name.startsWith('x') && gate.leftInput.name.startsWith('y')) {
				addGates.push({ leftInput: gate.rightInput, rightInput: gate.leftInput, output: gate.output, type: 'AND' })
			}
		}
		if (gate.output.name.startsWith('z')) {
			resultWires.push(gate.output)
		}
	}
	const findFinalWire = (wire: Wire): Wire => {
		if (wire.name.startsWith('z')) {
			return wire
		}
		for (const gate of circuit.gates) {
			if (gate.leftInput.name === wire.name || gate.rightInput.name === wire.name) {
				return findFinalWire(gate.output)
			}
		}
	}
	for (const gate of addGates.sort((a, b) => a.leftInput.name < b.leftInput.name ? -1 : 1)) {
		const leftWire = findFinalWire(gate.leftInput)
		console.log('Final wire of', gate.leftInput.name, 'is', leftWire)
		// const rightWire = findFinalWire(gate.rightInput)
		// console.log('Final wire of', gate.rightInput.name, 'is', rightWire)
	}
}

main()
