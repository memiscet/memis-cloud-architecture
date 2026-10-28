# Experience: support request priority

## People and goals
The consumer is a developer building a coordinator's workflow. They need predictable ordering and a clear failure if the records are invalid.

## Main journey
The developer passes valid records. The function returns IDs ordered by urgency, preserving arrival order within each priority. The developer presents that result in their own workflow.

## Other outcomes
An invalid priority or duplicate ID raises ValueError with no partial result. Empty input returns an empty list. The original input remains unchanged.

## Accessibility and practical use
This project supplies no user interface. The future presentation layer must address coordinator access needs in its own scope. Here, deterministic output and understandable exceptions support the developer's use.

## Wording and thresholds
Priority values are exactly urgent and normal. Arrival order is the input sequence. No elapsed-time threshold is proposed.

## Assumptions and open questions
The caller handles the exception in its own workflow. None remain within this example.
