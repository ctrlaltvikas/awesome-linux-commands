# 🚀 Modern CLI Replacements (The Rust & Go Era)

A curated matrix of next-generation command-line tools that replace legacy Unix coreutils with blazing speed, modern sensible defaults, syntax highlighting, and ergonomic design.

---

### 1. `eza` — Next-Gen Replacement for `ls`

<!-- @id: modern-eza -->
<!-- @name: eza -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: ls -->
<!-- @tags: rust, navigation, files, git -->

```bash
eza -lah --icons --git --group-directories-first
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-l` | Display extended file details (permissions, size, owner, modification time) in long table format |
| `-a` | List all files, including hidden dotfiles (`.env`, `.gitignore`) |
| `-h` | Display human-readable file sizes (`KiB`, `MiB`, `GiB`) |
| `--icons` | Render file-type and programming language glyph icons |
| `--git` | Track and display file Git status (`M` modified, `N` new, `I` ignored) |
| `--group-directories-first` | Sort directories ahead of individual files for cleaner scanning |

#### Why It Beats `ls`
Legacy `ls` requires multiple non-standard flags to display color and offers zero Git awareness. `eza` provides aligned column spacing, Git integration out of the box, and native tree views via `eza --tree`.

---

### 2. `bat` — Syntax-Highlighting Replacement for `cat`

<!-- @id: modern-bat -->
<!-- @name: bat -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: cat -->
<!-- @tags: rust, viewer, syntax-highlighting, git -->

```bash
bat --style=numbers,changes,grid --line-range :100 application.log
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `--style=numbers,changes,grid` | Render line numbers, Git diff markers (`+`, `-`), and clean ASCII borders |
| `--line-range :100` | Truncate output to the first 100 lines (avoids flooding the terminal) |

#### Why It Beats `cat`
`cat` prints raw uncolored streams without paging or syntax differentiation. `bat` auto-detects syntax for over 150 programming languages, integrates with Git diffs in the gutter, and automatically pipes through `less` when output exceeds screen height.

---

### 3. `ripgrep` (`rg`) — Lightning-Fast Replacement for `grep`

<!-- @id: modern-ripgrep -->
<!-- @name: ripgrep -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: grep -->
<!-- @tags: rust, search, regex, ultra-fast -->

```bash
rg -i -C 3 --type-add 'cfg:*.{yaml,yml,json,toml}' -tcfg 'jwt_secret'
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-i` | Case-insensitive matching |
| `-C 3` | Display 3 lines of leading and trailing context around each match |
| `--type-add '...'` | Define custom file type alias dynamically |
| `-tcfg` | Restrict search strictly to the defined configuration file extensions |

#### Why It Beats `grep`
`grep -rn` traverses ignored files, build directories, and binaries unless manually excluded. `ripgrep` automatically skips `.git/`, respects `.gitignore` rules, bypasses binary files, and utilizes SIMD acceleration for 5x–10x faster searches.

---

### 4. `fd` — Intuitive, User-Friendly Replacement for `find`

<!-- @id: modern-fd -->
<!-- @name: fd -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: find -->
<!-- @tags: rust, search, files, fast -->

```bash
fd -H -E 'node_modules' -E '.git' -e log -e txt
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-H` | Search hidden files and directories |
| `-E 'pattern'` | Exclude directories or file globs from traversal |
| `-e ext` | Filter strictly by file extension (`log`, `txt`) |

#### Why It Beats `find`
`find` syntax is notoriously arcane (`find . -name "*.log" -not -path "*/node_modules/*"`). `fd` defaults to colored output, smart-case regex matching, parallel directory walking, and automatic `.gitignore` respect.

---

### 5. `btop` — Visual Interactive Replacement for `top` and `htop`

<!-- @id: modern-btop -->
<!-- @name: btop -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: top, htop -->
<!-- @tags: c++, monitoring, cpu, memory, gpu, network -->

```bash
btop --utf-force
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `--utf-force` | Force high-fidelity Unicode graph rendering even in restricted terminal emulators |

#### Why It Beats `top`
`top` provides a static, dense wall of text. `btop` delivers responsive real-time graphing for CPU cores, memory utilization, disk I/O, network throughput, and GPU metrics with full mouse-click and interactive signal delivery (`SIGTERM`, `SIGKILL`).

---

### 6. `duf` — Visual Disk Usage Replacement for `df`

<!-- @id: modern-duf -->
<!-- @name: duf -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: df -->
<!-- @tags: go, storage, disk, visual -->

```bash
duf --hide-fs tmpfs,devtmpfs --sort usage
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `--hide-fs ...` | Exclude virtual filesystems like `tmpfs` and `devtmpfs` to focus on real physical devices |
| `--sort usage` | Sort mounted volumes by percentage of storage consumed |

#### Why It Beats `df`
`df -h` yields misaligned tables that clutter output with dozens of loopback/snap devices. `duf` auto-groups physical devices, special filesystems, and network shares into color-coded ASCII progress bars.

---

### 7. `dust` — Visual Directory Disk Usage Replacement for `du`

<!-- @id: modern-dust -->
<!-- @name: dust -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: du -->
<!-- @tags: rust, disk-space, tree, forensics -->

```bash
dust -d 3 -n 15 /var
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-d 3` | Limit tree traversal depth to 3 subdirectories |
| `-n 15` | Show only the top 15 largest disk-consuming items |

#### Why It Beats `du`
`du -sh *` requires manual sorting (`| sort -hr | head`) and provides no hierarchical perspective. `dust` generates an instant ASCII bar chart visualizer showing exactly which nested directories eat storage.

---

### 8. `procs` — Modern Process Inspector Replacement for `ps`

<!-- @id: modern-procs -->
<!-- @name: procs -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: ps -->
<!-- @tags: rust, process, tree, ports -->

```bash
procs --tree --watch --interval 2 nginx
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `--tree` | Display process parent-child relationships in a hierarchical visual tree |
| `--watch` | Continuously refresh output in place like `watch` |
| `--interval 2` | Set poll update interval to 2 seconds |

#### Why It Beats `ps`
`ps aux` prints truncated, unaligned columns without clear context. `procs` displays color-coded CPU/memory bars, shows TCP and UDP port bindings bound to each process, and detects containerized Docker/cgroup environments.

---

### 9. `curlie` / `httpie` — Human-Friendly Replacement for `curl`

<!-- @id: modern-curlie -->
<!-- @name: curlie -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: curl -->
<!-- @tags: go, networking, http, api -->

```bash
curlie -v POST https://api.example.com/v1/auth username="admin" password="secret"
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-v` | Verbose mode: prints request headers, response headers, and response payload |
| `POST` | HTTP method |
| `key="val"` | Auto-serializes key-value arguments directly into a JSON body |

#### Why It Beats `curl`
Raw `curl` requires tedious JSON escaping (`-H "Content-Type: application/json" -d '{"username":"admin"}'`). `curlie` provides the speed and features of `curl` with the beautiful colored formatting, syntax highlighting, and ergonomic parameter syntax of `httpie`.

---

### 10. `zoxide` (`z`) — Smart Frecency Directory Jumper Replacement for `cd`

<!-- @id: modern-zoxide -->
<!-- @name: zoxide -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: cd -->
<!-- @tags: rust, navigation, productivity -->

```bash
z repo
```

#### Flag Breakdown
| Argument | Description |
| :--- | :--- |
| `repo` | Substring query matching your most frequently and recently visited directory (e.g., `/Users/vikas/Documents/GitHub/awesome-linux-commands`) |

#### Why It Beats `cd`
`cd` requires typing long absolute or relative paths with tab completion. `zoxide` remembers directory visits and calculates a "frecency" score (frequency + recency), letting you jump across deeply nested hierarchies in 2 keystrokes.

---

### 11. `delta` — Syntax-Highlighting Pager for `diff` & `git diff`

<!-- @id: modern-delta -->
<!-- @name: delta -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: diff -->
<!-- @tags: rust, git, diff, code-review -->

```bash
git diff | delta --side-by-side --line-numbers
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `--side-by-side` | Render changes in a dual-column side-by-side diff layout |
| `--line-numbers` | Show unified file line numbers alongside modified blocks |

#### Why It Beats `diff`
Default `diff -u` presents hard-to-read unified plus/minus blocks. `delta` brings GitHub/IDE-grade syntax highlighting, character-level diff highlighting, and side-by-side terminal comparisons.

---

### 12. `tldr` — Practical Example Cheat Sheets Replacement for `man`

<!-- @id: modern-tldr -->
<!-- @name: tldr -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: man -->
<!-- @tags: community, documentation, cheatsheet -->

```bash
tldr tar
```

#### Why It Beats `man`
Standard `man` pages are encyclopedic manuals written 30 years ago spanning thousands of lines. `tldr` provides 5 to 8 community-curated, copy-pasteable examples for the most common real-world use cases.


---

### 13. `hyperfine` — Statistical Benchmarking Replacement for `time`

<!-- @id: modern-hyperfine -->
<!-- @name: hyperfine -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: time -->
<!-- @tags: rust, benchmark, performance, profiling -->

```bash
hyperfine --warmup 3 'fd -e md' 'find . -name "*.md"'
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `--warmup 3` | Execute commands 3 times prior to timing to ensure disk caches are warm |
| `'cmd1' 'cmd2'` | Run statistical side-by-side comparison across multiple iterations |

#### Why It Beats `time`
`time` executes a single run vulnerable to disk cache variance. `hyperfine` runs statistical sampling, computes standard deviation, flags outliers, and outputs an automated side-by-side comparison table.

---

### 14. `bandwhich` — Terminal Bandwidth Utilization Replacement for `iftop`

<!-- @id: modern-bandwhich -->
<!-- @name: bandwhich -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @replaces: iftop -->
<!-- @tags: rust, networking, bandwidth, process -->

```bash
sudo bandwhich --show-dns
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `--show-dns` | Show real-time DNS queries alongside active network connections |

#### Why It Beats `iftop`
`iftop` only reports raw IP addresses. `bandwhich` sniffs socket packets to map network bandwidth usage back to the exact running process name, connection state, and remote hostname.

---

### 15. `gdu` — Fast Interactive Disk Usage Analyzer Replacement for `ncdu`

<!-- @id: modern-gdu -->
<!-- @name: gdu -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: ncdu -->
<!-- @tags: go, storage, disk, interactive -->

```bash
gdu -d /var
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-d` | Target directory to analyze interactively |

#### Why It Beats `ncdu`
`ncdu` is single-threaded and struggles on multi-terabyte SSDs. `gdu` is written in Go with parallel multi-core traversal, scanning millions of files up to 5x faster with a responsive curses interface.

---

### 16. `sd` — Intuitive Find & Replace Replacement for `sed`

<!-- @id: modern-sd -->
<!-- @name: sd -->
<!-- @category: Modern CLI -->
<!-- @risk: Mutating -->
<!-- @replaces: sed -->
<!-- @tags: rust, text, regex, search-replace -->

```bash
sd 'https://api.old.com' 'https://api.new.com' config.json
```

#### Flag Breakdown
| Argument | Description |
| :--- | :--- |
| `'find'` | String or PCRE regex pattern to match |
| `'replace'` | Replacement string (supports capture groups `$1`, `$2`) |
| `config.json` | File to edit in place directly without requiring `-i` |

#### Why It Beats `sed`
`sed -i` has incompatible syntax between macOS (`sed -i ''`) and Linux (`sed -i`). `sd` uses cross-platform intuitive arguments, handles newlines safely, and uses standard regex patterns without escaping hell.

---

### 17. `doggo` — Human-Friendly, Colored DNS Client Replacement for `dig`

<!-- @id: modern-doggo -->
<!-- @name: doggo -->
<!-- @category: Modern CLI -->
<!-- @risk: Safe -->
<!-- @replaces: dig -->
<!-- @tags: go, dns, networking, colored -->

```bash
doggo A github.com @1.1.1.1 --time
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `A` | DNS record query type (`A`, `AAAA`, `MX`, `TXT`, `CNAME`) |
| `@1.1.1.1` | Specify custom nameserver resolver |
| `--time` | Display total DNS query response latency |

#### Why It Beats `dig`
`dig` returns verbose, cluttered comments that require `+short` to be usable. `doggo` provides clean, colorful, tabular output with built-in DoH (DNS-over-HTTPS) and DoT (DNS-over-TLS) support.

---

### 18. `ouch` — Painless Universal Compression Tool Replacement for `tar`

<!-- @id: modern-ouch -->
<!-- @name: ouch -->
<!-- @category: Modern CLI -->
<!-- @risk: Mutating -->
<!-- @replaces: tar -->
<!-- @tags: rust, compression, archives, universal -->

```bash
ouch decompress archive.tar.gz
```

#### Why It Beats `tar`
No need to remember whether you need `-xzvf`, `-xjvf`, or `-xvf`. `ouch` auto-detects archive format (`.zip`, `.tar.gz`, `.tar.bz2`, `.7z`, `.tar.zst`) from the file extension and decompresses cleanly with a progress bar.
