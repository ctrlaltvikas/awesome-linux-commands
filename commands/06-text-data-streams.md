# 🧙 Text Wrangling & High-Throughput Stream Processing

Production one-liners for slicing logs, aggregating status codes, batch processing with parallel threads, and parsing JSON streams.

---

### 1. HTTP Status Code Histogram from Web Access Logs

Generate an instant frequency distribution and percentage share of HTTP response codes (`200`, `301`, `404`, `500`, `502`) from Nginx or Apache logs.

<!-- @id: text-http-status-histogram -->
<!-- @name: log-status-histogram -->
<!-- @category: Text & Streams -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: text, awk, logs, nginx, apache -->

```bash
awk '{status[$9]++} END {for (code in status) printf "%-6s : %8d requests\n", code, status[code]}' /var/log/nginx/access.log | sort -k 3 -nr
```

#### Flag / Logic Breakdown
| Element | Description |
| :--- | :--- |
| `$9` | Column 9 in standard Common Log Format corresponds to HTTP status code |
| `status[$9]++` | Hash-map counter incrementing each encountered code |
| `END {for ...}` | Iterates through captured status codes upon reading EOF |
| `sort -k 3 -nr` | Sorts output by total count descending |

---

### 2. Multi-Core Parallel Execution with `xargs -P`

Accelerate batch operations (e.g., image resizing, compression, hash checks, API pings) by distributing tasks across all available CPU cores.

<!-- @id: text-xargs-parallel -->
<!-- @name: xargs-parallel-execution -->
<!-- @category: Text & Streams -->
<!-- @risk: Mutating -->
<!-- @privilege: Normal -->
<!-- @tags: text, performance, xargs, parallel -->

```bash
find ./logs -name "*.log" -print0 | xargs -0 -P $(nproc) -I {} gzip -9 {}
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-print0` & `-0` | Delimit filenames by null bytes (`\0`) to safely handle spaces, quotes, and newlines in file paths |
| `-P $(nproc)` | Spawn concurrent worker processes equal to the number of available CPU cores |
| `-I {}` | Replace `{}` with each input file path |
| `gzip -9` | Maximum compression level |

---

### 3. Align Jagged Whitespace Data into Clean Terminal Tables

Format unaligned delimiter-separated terminal streams or output into neatly aligned columns.

<!-- @id: text-column-align -->
<!-- @name: column-table-align -->
<!-- @category: Text & Streams -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: text, formatting, column, terminal -->

```bash
cat /etc/passwd | cut -d: -f1,3,4,6,7 | column -t -s: -N USER,UID,GID,HOME,SHELL
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-t` | Determine number of columns and create an auto-spaced table |
| `-s:` | Define delimiter character (colon `:` in this case) |
| `-N ...` | Assign custom header labels to table columns |

---

### 4. Slice & Query Complex JSON Streams with `jq`

Extract nested keys, filter by condition, and output clean tab-delimited values.

<!-- @id: text-jq-query -->
<!-- @name: jq-nested-filter -->
<!-- @category: Text & Streams -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: text, json, jq, api -->

```bash
cat payload.json | jq -r '.items[] | select(.status == "error") | [.id, .error_code, .message] | @tsv'
```

#### Flag Breakdown
| Flag / Filter | Description |
| :--- | :--- |
| `-r` | Raw output mode: strips surrounding quotation marks from string outputs |
| `.items[]` | Unrolls items array into individual objects |
| `select(...)` | Filters objects matching the boolean condition |
| `@tsv` | Formats the resulting array as clean tab-separated values ready for `awk` or spreadsheet paste |


---

### 5. Generate Cryptographically Secure Passwords from `/dev/urandom`

Create a 24-character high-entropy alphanumeric password with special characters without installing third-party utilities.

<!-- @id: text-gen-password -->
<!-- @name: urandom-password-gen -->
<!-- @category: Text & Streams -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: text, security, random, password, urandom -->

```bash
tr -dc 'A-Za-z0-9!@#$%^&*()_+' < /dev/urandom | head -c 24; echo
```

#### Flag Breakdown
| Element | Description |
| :--- | :--- |
| `tr -dc '...'` | Delete and complement: filter stream strictly to the specified allowed character set |
| `< /dev/urandom` | Read from Linux kernel non-blocking entropy pool |
| `head -c 24` | Truncate output after exactly 24 bytes |
| `; echo` | Append newline character for clean terminal display |

---

### 6. Live Log Tail with Real-Time Colorized Keyword Highlighting

Follow a streaming log file while highlighting critical error words without buffering delays.

<!-- @id: text-tail-color-grep -->
<!-- @name: tail-colored-grep -->
<!-- @category: Text & Streams -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: text, logs, streaming, tail, grep -->

```bash
tail -f /var/log/syslog | grep --line-buffered -E --color=always 'error|fail|crit|exception|$'
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `tail -f` | Output appended data as the file grows |
| `--line-buffered` | Force `grep` to flush stdout on every newline (prevents output stuttering in pipelines) |
| `-E` | Extended regular expressions |
| `--color=always` | Preserve ANSI color codes even when piped |
| `'$'` | Matches end of every line so non-matching lines are still displayed without color |

---

### 7. Find Common Lines Across Two Lists Without Creating Temp Files

Compute the exact intersection of two unsorted text files using Bash process substitution.

<!-- @id: text-comm-intersection -->
<!-- @name: comm-process-substitution -->
<!-- @category: Text & Streams -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: text, diff, comm, set-theory -->

```bash
comm -12 <(sort list_a.txt) <(sort list_b.txt)
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-1` | Suppress lines unique to file 1 |
| `-2` | Suppress lines unique to file 2 |
| `-12` | Combined: outputs strictly lines present in BOTH files (intersection) |
| `<(...)` | Process substitution: runs sort in a FIFO subshell without writing temporary files to disk |

---

### 8. Fast Column Slicing from Delimited CSV/TSV Files

Extract specific fields rapidly without the overhead of heavy scripting runtimes.

<!-- @id: text-cut-columns -->
<!-- @name: cut-field-slicing -->
<!-- @category: Text & Streams -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: text, cut, csv, data -->

```bash
cut -d',' -f1,3,5 server_metrics.csv
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-d','` | Define delimiter character (comma `,`) |
| `-f1,3,5` | Extract columns 1, 3, and 5 |
