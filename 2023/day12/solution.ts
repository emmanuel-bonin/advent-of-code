import fs from 'fs';
// import { input, output, part } from '../solver';
const part: number = 2
const input = fs.readFileSync('./input.txt').toString()
const output = console.log

const remainingArrangements = new Map<number, number>();
let springs: string[];
let groups: number[];

const countAllArrangements = () => {
    const repeats = part === 1 ? 1 : 5;
    let line: string, springRow: string[], groupRow: string[];
    let arrangements = 0;
    for (line of input.trim().split('\n')) {
        [springRow, groupRow] = line.split(' ').map(c => Array(repeats).fill(c));
        springs = springRow.join('?').split('');
        groups = groupRow.join(',').split(',').map(Number);
        console.log('spring', springs, 'groups', groups)
        arrangements += countRowArrangements()!;
        remainingArrangements.clear();
    }
    return arrangements;
};

const countRowArrangements = (s = 0, g = 0) => {
    if (s >= springs.length) {
        return g >= groups.length ? 1 : 0;
    } else if (!remainingArrangements.has(g * springs.length + s)) {
        let arrangements = 0;
        if (canPlaceRemainingGroups(s, g)) {
            if (canPlaceGroup(s, g)) {
                arrangements += countRowArrangements(s + 1 + groups[g], g + 1)!;
            }
            if (springs[s] !== '#') {
                arrangements += countRowArrangements(s + 1, g)!;
            }
        }
        remainingArrangements.set(g * springs.length + s, arrangements);
    }
    return remainingArrangements.get(g * springs.length + s);
};

const canPlaceRemainingGroups = (s: number, g: number) => {
    console.log('canPlaceRemainingGroups: ', s, 'g', g)
    for (; g < groups.length; g++) {
        console.log('s', s, 'g', g)
        s += groups[g] + 1;
    }
    console.log('canPlaceRemainingGroups: ', s, springs.length, s >= springs.length)
    return s <= springs.length + 1;
};

const canPlaceGroup = (s: number, g: number) => {
    for (let i = s; i < s + groups[g]; i++) {
        if (!springs[i] || springs[i] === '.') return false;
    }
    return springs[s + groups[g]] !== '#';
};

output(countAllArrangements());
