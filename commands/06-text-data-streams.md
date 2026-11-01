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
