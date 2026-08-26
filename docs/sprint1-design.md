# Sprint 1 Architectural Design Document

## 1. Initial Stakeholder Questions & Outcomes
Before designing the software structure, a strategic question phase was executed to uncover hidden business constraints and define strict scope boundaries.

*   **Log Data Format:** Confirmed as plain text with a single line entry structure following a predictable token pattern: `TIMESTAMP LEVEL SERVICE_NAME: message`.
*   **Definition of System Failure:** Explicitly restricted to `ERROR`, `CRITICAL`, and `FATAL` levels. `WARNING` and `INFO` levels are confirmed as out of scope for this sprint.
*   **Log Volume Scaling:** Confirmed to scale anywhere from 50 lines to 200,000+ lines per file, requiring an architecture with a flat memory ceiling.
*   **File Processing Scope:** Strictly limited to processing one single file at a time.
*   **Target Output Delivery:** Restricted to printing directly to the terminal screen.
*   **Filtering Parameters:** Ad-hoc time and service-level filtering were intentionally rejected as out of scope to avoid scope creep.
*   **Error Prioritization:** Confirmed that output statistics must group unique failures sorted by highest frequency count first.
*   **User Interaction Mode:** Tool execution must occur via command-line arguments, avoiding an interactive user prompt loop.

---

## 2. Identified Gaps & Architectural Adjustments
During the technical review, three structural flaws were identified in the initial logic. They were closed as follows:

### Gap 1: The False-Positive Parsing Trap
*   *The Flaw:* Searching for failure keywords (like "ERROR") anywhere in the raw text row would trigger false positives if the keyword was embedded inside a benign user message text field.
*   *The Fix:* Implemented a strict splitting limit capped at 3 whitespace cuts. This safely isolates the true severity log-level token exclusively at Index 2, completely decoupling it from the message string.

### Gap 2: The Multi-Line Stack Trace Contradiction
*   *The Flaw:* Attempting to handle multi-line log exceptions introduced an active programmatic contradiction where a line lacking a timestamp was parsed simultaneously as "malformed" data and "continuation" data.
*   *The Fix:* Streamlined the logic to enforce a stateless, per-line execution design. Multi-line stack traces are officially out of scope for Sprint 1. Any line failing the strict structural timestamp verification is treated exclusively as a malformed row, logged on a counter, and skipped.

### Gap 3: Token Index Calculation Arithmetic
*   *The Flaw:* A simple counting assumption miscalculated token indexing, incorrectly tracking the severity level position at Index 1 instead of accounting for the whitespace separating the calendar date and clock time fields.
*   *The Fix:* Corrected string parsing metrics to map the date string to Index 0, the time string to Index 1, and the target severity level keyword directly to Index 2.

---

## 3. High-Level System Architecture (Plain English Prose)

### Component 1: Execution Ingestion & Gateway Validation
The tool boots inside the shell environment and reads passed command line strings. Before opening data pipes, a defensive verification gate checks for file presence, readable structural formatting, and file byte volume. If paths point to missing or dead data blocks, the process terminates cleanly with a human-readable feedback loop.

### Component 2: Memory-Safe Line-By-Line Streaming
The application connects to the verified file location using a low-overhead serial data stream. Rather than dumping the entire file footprint into active system RAM, it reads exactly one row at a time. It evaluates each row independently, ensuring optimal system performance regardless of the input data size.

### Component 3: Targeted Token Inspection
As rows exit the stream, a parsing rule slices the text using a strict maximum cut ceiling. The parsing engine targets the exact token slot containing system status labels. Non-matching status entries are immediately discarded from memory, while real failure markers trigger structural data assembly.

### Component 4: Deduplication & Fault Handling
Extracted failures enter a local associative mapping index. The application aggregates issues by using the complete text string as a strict matching key, incrementing an integer counter for repeating rows. If the program hits lines that break our absolute string formatting patterns, it bypasses the row, flags a fault counter, and keeps running.

### Component 5: Sorted Data Presentation Summary
Upon reaching the file end, data connections close safely. The application pulls the aggregated fault statistics index and applies a descending sort operation by frequency counter values. It then displays a highly clean summary dashboard on the console window for operational personnel.
