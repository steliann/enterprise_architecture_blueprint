# Identity and Refresh Rules

## Principle

An objective ID identifies the **meaning of the objective**, not the source recommendation number or file position.

## Preserve an ID when

All material semantics remain equivalent:
- same intended future condition;
- same scope at the level relevant to acceptance;
- same primary business outcome(s);
- measures may be clarified or strengthened without changing the objective's identity;
- source recommendation may be rewritten or renumbered, provided the objective itself is still the same.

## Allocate a new ID when

Any of these occur:
- the target condition changes materially;
- the objective broadens/narrows enough to change acceptance;
- a different capability becomes the actual outcome rather than an implementation option;
- two old objectives are replaced by one new objective or one old objective splits into multiple outcomes;
- a recommendation ID is reused for unrelated semantics.

## Number allocation

- Determine the highest BO and TO number present in the historical package, including objectives that are no longer active when that history is available.
- Allocate monotonically above the historical maximum.
- Never fill numbering gaps by recycling old IDs.

Example: if `TO-015` is the highest historical ID and six new outcomes are required, allocate `TO-016` through `TO-021` even if some lower TOs are no longer active.

## Dates

- Preserve `created_date` for a preserved objective.
- Set `last_updated_date` when substantive content or mapping changes.
- A new objective receives both dates as the generation date.

## Supersession

If the full historical package is maintained, mark replaced objectives `objective_state: superseded` and reference the replacement in companion history/governance material. The active CSP portfolio should not silently reassign the old ID.
