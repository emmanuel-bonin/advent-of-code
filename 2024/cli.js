const fs = require('fs')
const path = require('path')
const {configDotenv} = require('dotenv')

env = configDotenv().parsed

const LANGUAGES = ['js', 'ts', 'py', 'rb', 'pl', 'c', 'cpp', 'go', 'sql']

function help(msg) {
	console.log(`
Runtime Error: ${msg}

Usage: npm run cli <command> [args]

Commands:
	init <day_number> <part> <language> 								Initialize a new day with selected language
	run <day_number> <part_number> <input|...> 	Run part of the day on input or another file(.txt) (default example for example.txt)

Languages (corresponding to language's file extensions):
	${LANGUAGES.join(', ')}

day_number: Just a number between 1 and 25
part_number: 1 or 2
	`)
}

function parseArgs(argv) {
	if (process.argv.length < 4) {
		throw new Error('Missing command')
	}
	const args = argv.slice(2)
	const cmd = args.shift()

	switch (cmd) {
		case 'init':
			if (args.length < 3) {
				throw new Error('Missing day number or language')
			}
			if (Number.isNaN(parseInt(args[0])) || parseInt(args[0]) < 1 || parseInt(args[0]) > 25) {
				throw new Error('Invalid day number. Must be between 1 and 25')
			}
			if (Number.isNaN(parseInt(args[1])) || parseInt(args[1]) < 1 || parseInt(args[1]) > 2) {
				throw new Error('Invalid part number. Must be either 1 or 2')
			}
			if (!LANGUAGES.includes(args[2])) {
				throw new Error(`Invalid language ${args[2]}. Must be one of ${LANGUAGES.join(', ')}`)
			}
			break
		case 'run':
			if (args.length < 3) {
				throw new Error('Missing day number, part number or input type')
			}
			if (Number.isNaN(parseInt(args[0])) || parseInt(args[0]) < 1 || parseInt(args[0]) > 25) {
				throw new Error('Invalid day number. Must be between 1 and 25')
			}
			if (Number.isNaN(parseInt(args[1])) || parseInt(args[1]) < 1 || parseInt(args[1]) > 2) {
				throw new Error('Invalid part number. Must be either 1 or 2')
			}

			break
	}
	return [cmd, ...args]
}

async function init(day, part, language) {
	const dir = `./day${day}`
	const file = `part${part}.${language}`

	if (!fs.existsSync(dir)) {
		fs.mkdirSync(dir)
	}
	if (fs.existsSync(path.join(dir, file))) {
		throw new Error(`File ${file} already exists`)
	}
	if (!fs.existsSync(`./day${day}/input.txt`)) {
		const input = await fetch(`https://adventofcode.com/${env.YEAR}/day/${day}/input`, {
			headers: {'Cookie': `session=${env.SESSION}`}
		})
		fs.writeFileSync(`./day${day}/input.txt`, await input.text())
	}
	if (!fs.existsSync(`./day${day}/example.txt`)) {
		fs.writeFileSync(`./day${day}/example.txt`, `your example`)
	}

	if (part === '2') {
		if (!fs.existsSync(path.join(dir, `part1.${language}`))) {
			fs.writeFileSync(path.join(dir, file), `content of part2`)
		} else {
			fs.writeFileSync(path.join(dir, file), fs.readFileSync(path.join(dir, `part1.${language}`)))
		}
	}
	fs.writeFileSync(path.join(dir, file), `content of part1`)
}

async function run(cmd, args) {
	switch (cmd) {
		case 'init':
			await init(args[0], args[1], args[2])
			break
		case 'run':
			const [day, part, input] = args
			require(`./day${day}/part${part}`)(input)
			break
		default:
			help('Invalid command')
			break
	}
}

(async () => {
	// npm run cli <command=init|run>
	// npm run cli init <day_number> <language=js|ts|py|rb|pl|c|cpp|go|sql>
	// npm run cli run <day_number> <part_number>

	try {
		const [cmd, ...args] = parseArgs(process.argv)

		await run(cmd, args)
	} catch (err) {
		help(err.message)
		process.exit(1)
	}
})()
