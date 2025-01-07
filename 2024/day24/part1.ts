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
	let result = ''
	let finished = false
	while (!finished) {
		finished = true
		for (const gate of circuit.gates) {
			if (gate.leftInput.value === undefined || gate.rightInput.value === undefined) {
				finished = false
				continue
			}
			if (gate.type === 'AND') {
				gate.output.value = (gate.leftInput.value! & gate.rightInput.value!) as Binary
			} else if (gate.type === 'OR') {
				gate.output.value = (gate.leftInput.value! | gate.rightInput.value!) as Binary
			} else if (gate.type === 'XOR') {
				gate.output.value = (gate.leftInput.value! ^ gate.rightInput.value!) as Binary
			}
			const wire = circuit.wires.find((w) => w.name === gate.output.name)
			if (wire) {
				wire.value = gate.output.value
			} else {
				circuit.wires.push({ name: gate.output.name, value: gate.output.value })
			}
		}
		for (const gate of circuit.gates) {
			for (const wire of circuit.wires) {
				if (gate.leftInput.name === wire.name) {
					gate.leftInput = wire
				}
				if (gate.rightInput.name === wire.name) {
					gate.rightInput = wire
				}
			}
		}
	}
	const orderedGates = circuit.gates.sort((a, b) => a.output.name > b.output.name ? -1 : 1)
	for (const gate of orderedGates) {
		if (gate.output.name.startsWith('z')) {
			result += gate.output.value.toString()
		}
	}

	console.log(result, parseInt(result, 2))
}

main()
