const fs = require('fs')

// const file = fs.readFileSync('./example.txt').toString()
const file = fs.readFileSync('./input.txt').toString()

const lines = file.split('\n')

function parseRule(line) {
  const rule = {
    name: null,
    conditions: [],
    default: null,
  }
  let [name, ruleRaw] = line.split('{')
  ruleRaw = ruleRaw.replace('}', '')
  const conditions = ruleRaw.split(',')
  rule.name = name
  rule.default = conditions[conditions.length - 1]
  for (const c of conditions) {
    if (c.includes('<')) {
      const s = c.split('<')
      const a = c.split(':')
      rule.conditions.push({
        field: s[0],
        maxValue: parseInt(s[1]),
        minValue: null,
        action: a[1],
      })
    } else if (c.includes('>')) {
      const s = c.split('>')
      const a = c.split(':')
      rule.conditions.push({
        field: s[0],
        maxValue: null,
        minValue: parseInt(s[1]),
        action: a[1],
      })
    }
  }
  return rule
}

function parsePart(line) {
  const part = {
    x: 0,
    m: 0,
    a: 0,
    s: 0,
  }
  line = line.replace('{', '').replace('}', '')
  const [xRaw, mRaw, aRaw, sRaw] = line.split(',')
  part.x = parseInt(xRaw.split('=')[1])
  part.m = parseInt(mRaw.split('=')[1])
  part.a = parseInt(aRaw.split('=')[1])
  part.s = parseInt(sRaw.split('=')[1])

  return part
}

function partMatchRule(part, rule) {
  for (const cond of rule.conditions) {
    if (cond.maxValue !== null) {
      if (part[cond.field] < cond.maxValue) {
        return { action: cond.action }
      }
    } else if (cond.minValue !== null) {
      if (part[cond.field] > cond.minValue) {
        return { action: cond.action }
      }
    }
  }
  return { action: rule.default }
}

function main() {
  rules = {}
  parts = []

  section = 0
  for (let i = 0; i < lines.length; i++) {
    if (lines[i] == '') {
      section++
      continue
    }
    if (section == 0) {
      const rule = parseRule(lines[i])
      rules[rule.name] = rule
    } else if (section == 1) {
      parts.push(parsePart(lines[i]))
    }
  }

  result = 0
  let finished = false
  while (!finished) {
    finished = true
    for (let i = 0; i < parts.length; i++) {
      let matchResult = partMatchRule(parts[i], rules['in'])
      while (matchResult.action !== 'A' && matchResult.action !== 'R') {
        matchResult = partMatchRule(parts[i], rules[matchResult.action])
      }
      if (matchResult.action === 'A') {
        result += parts[i].x + parts[i].m + parts[i].a + parts[i].s
      }
      delete parts[i]
      parts = parts.filter(a => a)
      finished = false
      break
    }
  }
  console.log(result)
}

main()
