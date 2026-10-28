# Scope: support request priority

## Problem and people
A support coordinator needs urgent requests to appear before normal requests while retaining arrival order within each priority.

## Intended result
A function accepts request records and returns their IDs in priority order. Input order represents arrival order. Each record has a unique nonempty string ID and a priority of urgent or normal. Invalid records are rejected as a whole rather than silently dropped.

## Success measures
Behavior tests demonstrate stable priority ordering, rejection of invalid priorities, rejection of duplicate IDs, and an empty result for empty input.

## Included
Ordering valid records and rejecting invalid records. The function must leave input unchanged.

## Excluded
A user interface, persistence, authentication, integrations, and timestamps.

## Constraints
Python 3.11+, standard library only. Use unittest for verification.

## Assumptions
The input sequence already reflects arrival order. Record validation can report ValueError to the developer calling the function.

## Open questions
None for this example.
