# Agent Architecture Notes

## Multi-Agent Patterns

### Current: Supervisor Pattern
Currently implemented with a supervisor agent that delegates tasks to sub-agents.

### Future: P2P Pattern (TODO)
Experiment with peer-to-peer agent communication where agents can call each other directly.

**Why experiment later:**
- More flexible but harder to debug
- Good for equal partnerships (e.g., two agents collaborating)
- Need to figure out: how do agents discover each other? What's the protocol?

---

## Design Decisions

### Memory
- **Short-term**: In-memory `ConversationHistory` (list of messages)
- **Long-term**: `history.md` file (simple text persistence)

### Tools
- Support both manual JSON schemas and Python function auto-generation
- For now, tools are in-memory only

### Execution Loop
- ReAct-style: think → act → observe → repeat
- Max iterations to prevent infinite loops
