import * as fs from 'fs'

class Processor {
	private _pointer: number = 0
	private _out: string[] = []
	private readonly _registers: Record<string, number> = {}
	private _isHalted: boolean = false

	constructor(registers: Record<string, number>) {
		this._registers = registers
	}

	private _parseComboOperand(operand: Omit<BitValue, '7'>): number {
		if (operand === '0' || operand === '1' || operand === '2' || operand === '3') {
			return parseInt(operand as string)
		} else if (operand === '4') {
			return this._registers['A']
		} else if (operand === '5') {
			return this._registers['B']
		} else if (operand === '6') {
			return this._registers['C']
		}
		throw new Error(`Invalid operand ${operand}`)
	}

	output(): string {
		return this._out.join(',')
	}

	execute(opSequence: string[]): void {
		while (!this._isHalted) {
			if (opSequence[this._pointer] === '0') {
				this.adv(opSequence[this._pointer + 1] as Omit<BitValue, '7'>)
			} else if (opSequence[this._pointer] === '1') {
				this.bxl(opSequence[this._pointer + 1] as Omit<BitValue, '7'>)
			} else if (opSequence[this._pointer] === '2') {
				this.bst(opSequence[this._pointer + 1] as Omit<BitValue, '7'>)
			} else if (opSequence[this._pointer] === '3') {
				this.jnz(opSequence[this._pointer + 1] as Omit<BitValue, '7'>)
			} else if (opSequence[this._pointer] === '4') {
				this.bxc(opSequence[this._pointer + 1] as Omit<BitValue, '7'>)
			} else if (opSequence[this._pointer] === '5') {
				this.out(opSequence[this._pointer + 1] as Omit<BitValue, '7'>)
			} else if (opSequence[this._pointer] === '6') {
				this.bdv(opSequence[this._pointer + 1] as Omit<BitValue, '7'>)
			} else if (opSequence[this._pointer] === '7') {
				this.cdv(opSequence[this._pointer + 1] as Omit<BitValue, '7'>)
			}
			if (this._pointer >= opSequence.length) {
				this._isHalted = true
			}
		}
	}

	adv(operand: Omit<BitValue, '7'>): void {
		const denominator = Math.pow(2, this._parseComboOperand(operand))
		this._registers['A'] = Math.trunc(this._registers['A'] / denominator)
		this._pointer += 2
	}

	bxl(operand: Omit<BitValue, '7'>): void {
		const value = parseInt(operand as string)
		this._registers['B'] ^= value
		this._pointer += 2
	}

	bst(operand: Omit<BitValue, '7'>): void {
		const value = this._parseComboOperand(operand as string)
		this._registers['B'] = (value % 8) & 0b111
		this._pointer += 2
	}

	jnz(operand: Omit<BitValue, '7'>): void {
		if (this._registers['A'] !== 0) {
			this._pointer = parseInt(operand as string)
		} else {
			this._pointer += 2
		}
	}

	bxc(_: Omit<BitValue, '7'>): void {
		this._registers['B'] ^= this._registers['C']
		this._pointer += 2
	}

	out(operand: Omit<BitValue, '7'>): void {
		const value = this._parseComboOperand(operand)
		this._out.push(((value % 8)).toString())
		this._pointer += 2
	}

	bdv(operand: Omit<BitValue, '7'>): void {
		const denominator = Math.pow(2, this._parseComboOperand(operand))
		this._registers['B'] = Math.trunc(this._registers['A'] / denominator)
		this._pointer += 2
	}

	cdv(operand: Omit<BitValue, '7'>): void {
		const denominator = Math.pow(2, this._parseComboOperand(operand))
		this._registers['C'] = Math.trunc(this._registers['A'] / denominator)
		this._pointer += 2
	}
}

type BitValue = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7'

(async () => {
	const lines = fs.readFileSync('example.txt', 'utf8').split('\n')
	let opSequence: string[] = []
	let opSequenceRaw: string = ''

	for (const line of lines) {
if (line.startsWith('Program:')) {
			opSequence = line.split(' ')[1].split(',')
			opSequenceRaw = line.split(' ')[1]
		}
	}

	// Every 8 iterations, it adds 10
	// wanted number is 2416754417035530
                     //2251799813685248
	//
	// in example, we need 117440 iterations to reach 035430
	// Every 64, 512, 4096, ... the length increases starting with a 0

	let currentA = 0
	let resultNum = Number(opSequence.join(''))
	let result = 0
	let resultStr = ''
	let pow = 0
	while (resultStr !== opSequenceRaw) {
		const processor = new Processor({
			A: currentA,
			B: 0,
			C: 0,
		})
		processor.execute(opSequence)
		resultStr = processor.output()
		if (parseInt(resultStr.split(',')[0]) === resultNum % 10) {
			console.log('For register A =', currentA, 'Output:', resultStr, parseInt(resultStr.split(',')[0]))
			resultNum = Math.floor(resultNum / 10)
			result += currentA * Math.pow(8, pow)
			pow++
			if (resultNum === 0) {
				break
			}
			console.log('new result num', resultNum)
		}
		// 	result = `${result.split(',')[0]}${result}`
		// 	resultNum = Math.floor(resultNum / 10)
		// 	currentA = currentA * 64 + parseInt(result.split(',')[0]) * 8
		// } else {
			currentA++
		// }
	}
	console.log(result)
})()

// let n = 2416754417035530
// let result = 0
// while (n > 0) {
// 	console.log((n%10)*8)
// 	n = Math.floor(n/10)
// }
