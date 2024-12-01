const fs = require('fs')

function usage(errorMsg) {
    console.error(
        `${errorMsg ?? ''}
        Usage: node aoc.js <cmd> [options]

        cmd:        options:
        init        <day_num>           initialize a new day with name formatted by dayXX with XX being <day_num> parameter
                                        create input.txt and example.txt
                                        create a basic part1.py and part2.py that both contain a file opening on example.txt
                                        and a basic line by line reading of the file being open (default to example.txt)

        run         <day_num> <part>    run the <part> of the specified day <day_num>
        `
    )
}

const AOC_PATH = '/Users/emmanuelbonin/Documents/adventOfCode/2023'

if (process.argv.length < 3) {
    usage()
    process.exit(1)
}

if (process.argv[2] === 'init') {
    if (process.argv.length < 4) {
        usage('init: Missing parameter <day_num>')
        process.exit(1)
    }
    if (Number(process.argv[3]) === NaN) {
        usage('Invalid <day_num> format. Must be a number')
        process.exit(1)
    }
    let dayNum = process.argv[3]
    if (Number(dayNum) < 10) {
        dayNum = `0${dayNum}`
    }
    day_directory = `${AOC_PATH}/day${dayNum}`
    try {
        fs.statSync(day_directory)
        console.error(`Directory "${day_directory}" already exists`)
        process.exit(1)
    } catch { }
    console.log(`Making directory "${day_directory}"...`)
    fs.mkdirSync(day_directory)
    fs.writeFileSync(`${day_directory}/input.txt`, '')
    fs.writeFileSync(`${day_directory}/example.txt`, '')
    fs.writeFileSync(`${day_directory}/NOTES.md`, '')
    fs.writeFileSync(`${day_directory}/part1.py`, `
def main():
  # f = open('./input.txt', 'r')
  f = open('./example.txt', 'r')
  lines = f.readlines()
  for l in lines:
    l = l.replace('\\n', '').strip()

if __name__ == "__main__":
  main()
`)
    fs.writeFileSync(`${day_directory}/part2.py`, '')
} else if (process.argv[2] === 'run') {
    if (process.argv.length < 5) {
        usage('run: Wrong parameters')
        process.exit(1)
    }
} else {
    usage(`${process.argv[2]}: Unknown command\n`)
    process.exit(1)
}
