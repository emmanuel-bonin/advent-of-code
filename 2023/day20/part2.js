const fs = require('fs')
const { EventEmitter } = require('stream')

// const file = fs.readFileSync('./example2.txt').toString()
const file = fs.readFileSync('./input.txt').toString()

const lines = file.split('\n')

class Module extends EventEmitter{
  inputModules = []
  outputModules = []
  inputPulses = []

  constructor(name) {
    super()
    this.name = name
  }

  addInputModule(module) {
    this.inputModules.push(module)
  }

  addOutputModule(module) {
    this.outputModules.push(module)
  }

  handlePulse(_, pulse) {
    if (pulse === 'low') {
      this.emit('low_pulse')
    }
  }

  sendPulse() {
    const pulseToSend = this.inputPulses.shift()
    if (pulseToSend) {
      for (const m of this.outputModules) {
        m.handlePulse(this.name, pulseToSend)
      }
      for (const m of this.outputModules) {
        m.sendPulse()
      }
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
        this.inputPulses.push('high')
      } else if (this.state === 'on') {
        this.state = 'off'
        this.inputPulses.push('low')
      }
    }
  }
}

class Conjunction extends Module {
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
        this.inputPulses.push('high')
        allHighPulses = false
        break
      }
    }
    if (allHighPulses) {
      this.inputPulses.push('low')
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
    this.outputModules[0].handlePulse('low')
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
  let rx = null
  for (const f of Object.keys(flipflopsRaw)) {
    const m = new FlipFlop(f)
    flipflops[m.name] = m
  }
  for (const c of Object.keys(conjunctionsRaw)) {
    const m = new Conjunction(c)
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
        rx = new Module(outputRaw)
        rx.addInputModule(cModule)
        cModule.addOutputModule(rx)
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

  let run = true
  let buttonPressed = 0
  rx.on('low_pulse', () => {
    console.log('Button pressed', buttonPressed)
    run = false
  })
  const initialState1 = [
    'rq', 'dc', 'ql', 'jl', 'mr', 'jc', 'gv', 'mm', 'cc',
  ].map(() => 'off').reduce((a, b) => a + b)
  const initialState2 = [
    'bs', 'pn', 'vm', 'vj', 'zz', 'bt', 'jg', 'rr', 'mk',
  ].map(() => 'off').reduce((a, b) => a + b)
  const initialState3 = [
    'cn', 'bc', 'kp', 'jr', 'gn', 'jx', 'pq', 'bf',
  ].map(() => 'off').reduce((a, b) => a + b)
  const initialState4 = [
    'sb', 'vz', 'rk', 'bz', 'rl', 'rh', 'lg',
  ].map(() => 'off').reduce((a, b) => a + b)

  while (run) {
    buttonPressed++
    const newState1 = [
    'rq', 'dc', 'ql', 'jl', 'mr', 'jc', 'gv', 'mm', 'cc',
  ].map(n => flipflops[n].state).reduce((a, b) => a+b)
    const newState2 = [
    'bs', 'pn', 'vm', 'vj', 'zz', 'bt', 'jg', 'rr', 'mk',
  ].map(n => flipflops[n].state).reduce((a, b) => a+b)
    const newState3 = [
    'cn', 'bc', 'kp', 'jr', 'gn', 'jx', 'pq', 'bf',
  ].map(n => flipflops[n].state).reduce((a, b) => a+b)
    const newState4 = [
    'sb', 'vz', 'rk', 'bz', 'rl', 'rh', 'lg',
    ].map(n => flipflops[n].state).reduce((a, b) => a + b)

    // if (newState1 === initialState1) {
    //   console.log('flipflops 1 retruned to inital state after', buttonPressed)
    // }
    // if (newState2 === initialState2) {
    //   console.log('flipflops 2 retruned to inital state after', buttonPressed)
    // }
    // if (newState3 === initialState3) {
    //   console.log('flipflops 3 retruned to inital state after', buttonPressed)
    // }
    // if (newState4 === initialState4) {
    //   console.log('flipflops 4 retruned to inital state after', buttonPressed)
    // }
    button.push()
  }
}

main()
