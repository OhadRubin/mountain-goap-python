

# Prerequisites for JavaScript GOAP Port

## Essential Reading (Must Read)

### 1. GOAP Architecture Understanding
- **Read first**: `/CLAUDE.md` - The definitive GOAP guide in this repo
- **Key concepts**: Sensors vs Action states, goal priorities, state dependencies
- **Why**: You'll write broken code without understanding these fundamentals

### 2. JavaScript/Node.js Essentials  
- **ES6+ Classes**: Constructor patterns, inheritance, static methods
- **ES6 Modules**: import/export syntax, module resolution
- **Async Patterns**: Promises, async/await (replacing Python's threading)
- **Collections**: Map, Set, WeakMap for efficient lookups
- **Node.js Canvas**: Basic drawing API for game rendering

### 3. Algorithm Knowledge
- **A* Pathfinding**: How it works, heuristics, open/closed sets
- **Priority Queues**: Implementation with heaps, update operations
- **Game Loops**: Fixed timestep vs variable timestep patterns

## Quick Reference Resources

### JavaScript Specifics
```javascript
// Python dict → JavaScript Map
const state = new Map([['hp', 100], ['position', new Vector2(10, 10)]]);

// Python list comprehension → JavaScript map/filter
const enemies = agents.filter(agent => agent.faction !== playerFaction);

// Python threading locks → JavaScript doesn't need them (single-threaded)
// Just be careful with async operations
```

### GOAP Quick Concepts
- **Sensors**: Read world state (one condition each)
- **Goals**: Define success + priority (higher priority wins)  
- **Actions**: Change world state (preconditions → effects)
- **Planner**: A* to find action sequence achieving goals

## If You're Super Lazy

### Absolute Minimum Reading
1. Read `/CLAUDE.md` sections "The Three Core Components" and "State Dependencies"
2. Skim one JavaScript class tutorial
3. Look at the Python code structure in `/rpg_goap_python_example/`

### Copy-Paste Starting Points
- Use the Python class structure as a template
- Copy method names and convert syntax
- Start with Vector2 class (easiest to port)
- Priority queue has existing JavaScript implementations online

## Testing Strategy (Don't Skip This)

### Why Test GOAP Systems
- **State bugs are silent killers**: Agents just stop working
- **Pathfinding bugs cause infinite loops**: Your game freezes
- **Priority logic bugs**: Wrong goals get selected

### Easy Testing Approach  
1. **Unit tests**: Each class in isolation (Vector2, Action, Goal)
2. **Integration tests**: Agent with simple goal/action pairs
3. **Smoke tests**: Run full game for 10 turns without crashing

### Test-Driven Development Benefits
- **Catches bugs early**: Before they become hard to debug
- **Forces good architecture**: Testable code is usually better code  
- **Saves debugging time**: Tests pinpoint exact failure location
- **Refactoring confidence**: Change code without fear of breaking things

## Pro Tips for Lazy Developers

1. **Port incrementally**: Start with utils.js, test it, then move on
2. **Use TypeScript**: Catch type errors at compile time, not runtime
3. **Copy existing patterns**: Don't reinvent, adapt from Python version
4. **Test as you go**: Writing tests later is 10x harder
5. **Use debugger**: Step through A* algorithm to understand it visually

# Agent Implementation Guide: For the Extremely Lazy Developer

## Dear Lazy Developer,

I see you. You want to port this GOAP system to JavaScript, but you're already thinking about shortcuts. You're eyeing that plan and wondering which parts you can skip. You're probably going to copy-paste some code and "fix it later." 

**STOP.**

This document will show you why being lazy about this project will make you work 10x harder, and how following the plan is actually the laziest approach.

## The Lazy Developer's Paradox

### The "Quick and Dirty" Path (Looks Easy, Actually Hell)
```
1. Skip reading CLAUDE.md → Spend 3 days debugging state issues
2. Skip tests → Spend 2 days hunting undefined behavior  
3. Skip proper architecture → Rewrite everything when it becomes unmaintainable
4. Skip incremental development → Debug a 2000-line hairball
5. Skip understanding GOAP → Create agents that do random things

Total time: 2+ weeks of pain, frustration, and embarrassment
```

### The "Follow the Plan" Path (Looks Hard, Actually Easy)  
```
1. Read prerequisites → Save 3 days of confusion
2. Write tests → Catch bugs in 30 seconds instead of 30 minutes
3. Follow architecture → Code writes itself, easy to extend
4. Develop incrementally → Always have working code
5. Understand GOAP → Impress people with smart AI

Total time: 3-4 days of smooth, satisfying development
```

## Why Your Lazy Brain Should Care

### 1. The Pain of Debugging Without Tests
Imagine spending 4 hours trying to figure out why your agent just stands there doing nothing. No error messages. No stack traces. Just... nothing. Without tests, you have no idea which of your 47 classes is broken.

**With tests**: Run one command, see "Action.isValid() returns false", fix in 5 minutes.

### 2. The Horror of Spaghetti GOAP Code
GOAP systems are inherently complex. Cut corners on architecture and you get:
- Circular dependencies between goals and actions
- State mutations happening in random places  
- Agents that work in test but fail in production
- Code that only you can understand (and only for 2 weeks)

**Following the plan**: Clean separation of concerns, predictable behavior, code that makes sense.

### 3. The Ego Factor
You're a developer. You have pride. Do you want to:
- Ship buggy code that crashes randomly?
- Have other developers look at your code and cringe?
- Be known as "that person who writes unmaintainable code"?

OR

- Ship a clean, well-tested GOAP implementation?
- Have people say "wow, this is really well structured"?
- Be the person who others ask for architecture advice?

## The Lazy Developer's Implementation Strategy

### Phase 1: Setup (30 minutes)
```bash
mkdir rpg-goap-js && cd rpg-goap-js
npm init -y
npm install canvas jest
mkdir -p src/{goap,rpg} test
```

**Lazy tip**: Use the exact structure from the plan. Don't "improve" it.

### Phase 2: Test-First Development (This is Key)
For each class, write the test FIRST:
```javascript
// test/vector2.test.js
test('Vector2 distance calculation', () => {
  const v1 = new Vector2(0, 0);
  const v2 = new Vector2(3, 4);
  expect(v1.distanceTo(v2)).toBe(5);
});
```

**Why this is lazy**: You know exactly what to implement. No guessing.

### Phase 3: Copy-Paste-Adapt (Not Copy-Paste-Pray)
1. Copy the Python class structure
2. Convert Python syntax to JavaScript
3. Run your test
4. Fix until it passes
5. Move to next class

**Lazy benefit**: You're never stuck wondering "what do I implement next?"

### Phase 4: Integration (The Easy Part)
Because you followed the architecture and wrote tests, integration is just:
1. Wire the classes together
2. Run integration tests
3. Fix any interface mismatches
4. Done

## The Test-First Mindset for Lazy People

### Why Tests are Actually Lazy
- **Instant feedback**: Know immediately if your code works
- **Regression protection**: Change code without fear
- **Documentation**: Tests show how to use your classes
- **Debugging**: Failing test = exact problem location
- **Confidence**: Sleep well knowing your code works

### The "I Don't Have Time for Tests" Trap
**Time to write tests**: 20% of development time
**Time to debug without tests**: 60% of development time

Do the math. Tests save time.

### Easy Testing Strategy
1. **Start simple**: Test basic functionality first
2. **Use examples**: Copy test patterns from other JS projects
3. **Test the edges**: null inputs, empty arrays, boundary conditions
4. **Mock external dependencies**: Don't test the canvas API, test your logic

## Code Quality Rules for Lazy People

### 1. Use ESLint and Prettier
**Why**: Automatic code formatting and error detection. No thinking required.

### 2. Write Comments for Future You
```javascript
// This is wrong - your future self will hate you
function foo(a, b) { return a.x < b.y ? c : d; }

// This is right - your future self will thank you  
/**
 * Calculates if agent can reach target position
 * @param {Vector2} agentPos - Current agent position
 * @param {Vector2} targetPos - Desired target position  
 * @returns {boolean} True if path exists
 */
function canReachTarget(agentPos, targetPos) { ... }
```

### 3. Use TypeScript (Optional but Recommended)
**Lazy benefit**: Catch type errors at compile time, not runtime.

### 4. Follow the Single Responsibility Principle
**Each class should do one thing well.** This makes testing easy and debugging trivial.

## Motivation Maintenance

### When You Want to Cut Corners
Remember: **Technical debt is not free**. You will pay it back with interest, usually at the worst possible time (demo day, code review, production deployment).

### When You're Stuck
1. **Read the error message** (actually read it, don't just glance)
2. **Check your tests** (are they passing? are they comprehensive?)
3. **Compare with Python version** (what's different?)
4. **Use the debugger** (step through your code line by line)

### When You're Tempted to Skip Tests
Ask yourself: "Would I rather spend 10 minutes writing a test, or 2 hours debugging mysterious behavior?"

## Success Metrics

You'll know you're succeeding when:
- ✅ Your tests pass consistently
- ✅ You can explain how your code works to someone else
- ✅ Adding new features doesn't break existing ones
- ✅ You're not afraid to refactor
- ✅ Other developers can understand your code
- ✅ You sleep well at night

## Final Words

**You have a choice**: 
- Spend 2 weeks fighting with broken, untested code
- Spend 4 days building something you're proud of

The plan exists to make your life easier. Trust it. Follow it. Your future self will thank you.

And remember: **Good code is lazy code** - it does exactly what it needs to do, nothing more, nothing less, and it works every time.

Now stop reading and start coding. The sooner you start properly, the sooner you'll be done.

---

*P.S. If you skip this advice and end up with a buggy mess, don't come crying to the git history. The plan was right there.*