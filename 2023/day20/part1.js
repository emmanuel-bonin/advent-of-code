const fs = require('fs')

// const file = fs.readFileSync('./example1.txt').toString()
// const file = fs.readFileSync('./example2.txt').toString()
const file = fs.readFileSync('./input.txt').toString()

const lines = file.split('\n')

class Module {
  lowPulses = 0
  highPulses = 0
  inputModules = []
  outputModules = []
  inputPulses = []

  constructor(name) {
    this.name = name
  }

  addInputModule(module) {
    this.inputModules.push(module)
  }

  addOutputModule(module) {
    this.outputModules.push(module)
  }

  handlePulse() { }

  sendPulse() {
    const pulseToSend = this.inputPulses.shift()
    for (const m of this.outputModules) {
      if (pulseToSend === 'high') {
        this.highPulses++
      } else if (pulseToSend === 'low') {
        this.lowPulses++
      } else if (!pulseToSend) {
        return []
      }
      console.log(`${this.name} -${pulseToSend}-> ${m.name}`)
      m.handlePulse(this.name, pulseToSend)
    }
    for (const m of this.outputModules) {
      m.sendPulse()
    }
  }
}

class FlipFlop extends Module {
  constructor(name) {
    super(name)
    this.state = 'off'
  }

  handlePulse(_, pulse) {
    if (pulse === 'low') {
      if (this.state === 'off') {
        this.state = 'on'
        // this.pulseToSend = 'high'
        this.inputPulses.push('high')
        // console.log(`${this.name} was off, now on and received low => sending high`)
      } else if (this.state === 'on') {
        this.state = 'off'
        // this.pulseToSend = 'low'
        this.inputPulses.push('low')
        // console.log(`${this.name} was on, now off and received low => sending high`)
      }
    } else if (pulse === 'high') {
      // console.log(`${this.name} received high => sending nothing`)
      // this.pulseToSend = undefined
    }
  }
}

class Conjonction extends Module {
  constructor(name) {
    super(name)
    this.inputPulsesReceived = {}
  }

  addInputModule(module) {
    this.inputModules.push(module)
    this.inputPulsesReceived[module.name] = 'low'
  }

  handlePulse(module, pulse) {
    this.inputPulsesReceived[module] = pulse
    let allHighPulses = true
    for (const p of Object.values(this.inputPulsesReceived)) {
      if (p === 'low') {
        // this.pulseToSend = 'high'
        this.inputPulses.push('high')
        // console.log(`${this.name} has a low pulse for an input => sending high`)
        allHighPulses = false
        break
      }
    }
    if (allHighPulses) {
        // console.log(`${this.name} has high pulses for all input => sending low`)
      this.inputPulses.push('low')
      // this.pulseToSend = 'low'
    }
  }
}

class Broadcaster extends Module {
  constructor() {
    super('broadcaster')
  }

  handlePulse(pulse) {
    this.inputPulses.push(pulse)
    this.sendPulse()
  }
}

class ButtonModule extends Module {
  constructor() {
    super('button')
  }

  push() {
    this.lowPulses++
    console.log('button -low-> broadcaster')
    this.outputModules[0].handlePulse('low')
    console.log()
  }
}






function main() {
  let broadcasterRaw = undefined
  const flipflopsRaw = {}
  const conjunctionsRaw = {}

  for (const line of lines) {
    if (line.includes('broadcaster')) {
      const arr = line.split('->')[1].split(',').map(s => s.trim())
      broadcasterRaw = arr
    } else if (line.includes('%')) {
      const name = line.split(' ')[0].split('%')[1]
      const arr = line.split('->')[1].split(',').map(s => s.trim())
      flipflopsRaw[name] = arr
    } else if (line.includes('&')) {
      const name = line.split(' ')[0].split('&')[1]
      const arr = line.split('->')[1].split(',').map(s => s.trim())
      conjunctionsRaw[name] = arr
    }
  }

  // Creating all modules object with no link between them all
  const button = new ButtonModule()
  const broadcaster = new Broadcaster()
  const flipflops = {}
  const conjunctions = {}
  for (const f of Object.keys(flipflopsRaw)) {
    const m = new FlipFlop(f)
    flipflops[m.name] = m
  }
  for (const c of Object.keys(conjunctionsRaw)) {
    const m = new Conjonction(c)
    conjunctions[m.name] = m
  }

  // Iterate over each connected modules of each module
  // And add them in the different inputModules and outputModules
  for (const k of Object.keys(flipflopsRaw)) {
    const fModule = flipflops[k]
    for (const outputRaw of flipflopsRaw[k]) {
      const fOutput = flipflops[outputRaw]
      const cOutput = conjunctions[outputRaw]
      if (fOutput) {
        fOutput.addInputModule(fModule)
        fModule.addOutputModule(fOutput)
      } else if (cOutput) {
        cOutput.addInputModule(fModule)
        fModule.addOutputModule(cOutput)
      } else {
        const output = new Module(outputRaw)
        output.addInputModule(fModule)
        fModule.addOutputModule(output)
      }
    }
  }
  for (const k of Object.keys(conjunctionsRaw)) {
    const cModule = conjunctions[k]
    for (const outputRaw of conjunctionsRaw[k]) {
      const fOutput = flipflops[outputRaw]
      const cOutput = conjunctions[outputRaw]
      if (fOutput) {
        fOutput.addInputModule(cModule)
        cModule.addOutputModule(fOutput)
      } else if (cOutput) {
        cOutput.addInputModule(cModule)
        cModule.addOutputModule(cOutput)
      } else {
        const output = new Module(outputRaw)
        output.addInputModule(cModule)
        cModule.addOutputModule(output)
      }
    }
  }
  for (const m of broadcasterRaw) {
    const fModule = flipflops[m]
    const cModule = conjunctions[m]
    if (fModule) {
      fModule.addInputModule(broadcaster)
      broadcaster.addOutputModule(fModule)
    } else if (cModule) {
      cModule.addInputModule(broadcaster)
      broadcaster.addOutputModule(cModule)
    }
  }
  button.addOutputModule(broadcaster)

  // All links between modules have been created
  // Let's broadcast first pulse and compute everything
  let lows = 0
  let highs = 0
  const BUTTON_TIMES = 1000

  for (let i = 0; i < BUTTON_TIMES; i++) {
    button.push()
  }

  lows += button.lowPulses
  highs += button.highPulses
  lows += broadcaster.lowPulses
  highs += broadcaster.highPulses
  for (const m of Object.values(flipflops)) {
    lows += m.lowPulses
    highs += m.highPulses
  }
  for (const m of Object.values(conjunctions)) {
    lows += m.lowPulses
    highs += m.highPulses
  }

  console.log('lows', lows)
  console.log('highs', highs)
  console.log(lows * highs)

  // console.log('broadcaster', broadcaster, broadcaster.outputModules)
  // console.log('flipflops', flipflops)
  // console.log('conjunctions', conjunctions)
}

main()
