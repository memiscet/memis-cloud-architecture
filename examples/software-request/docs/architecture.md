# Approach: support request priority

## Overview
Create a pure Python function `prioritize_requests(records)` in `src/priority.py`. Return a new list of IDs. Validate all records before sorting.

## Parts and responsibilities
The validator rejects missing/blank IDs, duplicates, and priorities outside urgent/normal. Stable ordering puts urgent records first while preserving input order within each priority. Standard-library unit tests exercise the public function.

## Information flow
Caller supplies a list of dictionaries; validation either raises ValueError or allows ordering; caller receives a new list. No files, network connections, or databases are used at runtime.

## Decisions and tradeoffs
Input order represents arrival so no date parsing is needed. A pure function is enough for the stated scope. No third-party dependencies are needed.

## Failure and recovery
Raise ValueError for malformed records. The caller corrects the records and retries. Do not return a partial result that conceals an invalid request.

## Constraints, assumptions, and open questions
Use the scope's Python and unittest choices. No open questions.
