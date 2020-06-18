# Computer Architecture

## Project

* [Implement the LS-8 Emulator](ls8/)

## Task List: add this to the first comment of your Pull Request

### Day 1: Get `print8.ls8` running

- [x] Inventory what is here step 0
- [x] Implement the `CPU` constructor step 1
- [x] Add RAM functions `ram_read()` and `ram_write()` step 2
- [x] Implement the core of `run()` step 3
- [x] Implement the `HLT` instruction handler step 4
- [x] Add the `LDI` instruction step 5
- [x] Add the `PRN` instruction step 6

### Day 2: Add the ability to load files dynamically, get `mult.ls8` running

- [x] Un-hardcode the machine code
- [x] Implement the `load()` function to load an `.ls8` file given the filename
      passed in as an argument
- [x] Implement a Multiply instruction (run `mult.ls8`)

### Day 3: Stack

- [x] Implement the System Stack and be able to run the `stack.ls8` program

### Day 4: Get `call.ls8` running

- [x] Implement the CALL and RET instructions
- [x] Implement Subroutine Calls and be able to run the `call.ls8` program

### Stretch

- [ ] Add the timer interrupt to the LS-8 emulator
- [ ] Add the keyboard interrupt to the LS-8 emulator
- [ ] Write an LS-8 assembly program to draw a curved histogram on the screen
