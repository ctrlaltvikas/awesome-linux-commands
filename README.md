# 🐧 Awesome Linux Commands

<p align="center">
  <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Linux-Dark.svg" width="80" height="80" alt="Linux Logo" />
</p>

<p align="center">
  <strong>A curated collection of modern CLI utilities, 3 AM production incident forensics, socket inspection, and stream-processing power one-liners.</strong>
  <br />
  <em>Every single flag dissected. Every command safety-tiered. No cryptic blind copy-pasting.</em>
</p>

<p align="center">
  <a href="https://github.com/vikaskyadav/awesome-linux-commands/stargazers"><img src="https://img.shields.io/github/stars/vikaskyadav/awesome-linux-commands?style=for-the-badge&logo=github&color=10b981&labelColor=080b11" alt="GitHub Stars" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-06b6d4?style=for-the-badge&labelColor=080b11" alt="License" /></a>
  <a href="https://github.com/vikaskyadav/awesome-linux-commands/pulls"><img src="https://img.shields.io/badge/PRs-Welcome-8b5cf6?style=for-the-badge&labelColor=080b11" alt="PRs Welcome" /></a>
  <a href="https://vikaskyadav.github.io/awesome-linux-commands/"><img src="https://img.shields.io/badge/Live_Catalog-Interactive_Web_App-10b981?style=for-the-badge&labelColor=080b11" alt="Live Web App" /></a>
</p>

<p align="center">
  🌐 <strong>Live Interactive Web Catalog:</strong> <a href="https://vikaskyadav.github.io/awesome-linux-commands/">vikaskyadav.github.io/awesome-linux-commands</a>
</p>

---

## ✨ Why This Project?

Most command cheat sheets on GitHub are flat, uncurated walls of text listing commands like `ls`, `cd`, and `pwd` without context or explanation. When production breaks at 3 AM, engineers don't need man pages—they need:

1. **Immediate Solutions to Urgent Production Fires** (Ghost disk leaks, I/O bottlenecks, zombie processes, port collisions).
2. **Flag Dissection** — Never run `tar -xzvf` or `ss -tulpn` blindly again. Every letter is mapped in a clean table.
3. **Safety & Risk Stratification** — Explicit visual indicators for read-only vs state-mutating commands.
4. **The Modern Terminal Renaissance** — Direct side-by-side upgrades from 40-year-old coreutils to blazingly fast Rust/Go alternatives (`bat`, `eza`, `ripgrep`, `duf`, `btop`, `fd`).
5. **Interactive Web Portal** — Instant fuzzy search and 1-click clipboard copy at [vikaskyadav.github.io/awesome-linux-commands](https://vikaskyadav.github.io/awesome-linux-commands/).

---

## 🧭 Universal Safety & Risk Stratification

Every command in this repository is rated with a risk indicator:

| Level | Badge | Meaning |
| :--- | :--- | :--- |
| **Safe** | 🟢 `SAFE` | Read-only diagnostic query. Zero risk of modifying system state or dropping connections. |
| **Mutating** | 🟡 `MUTATING` | Alters files, logs, processes, or temporary kernel settings. |
| **Destructive** | 🔴 `DESTRUCTIVE` | High risk of permanent data loss or service disruption if arguments are misconfigured. |
| **Privilege** | 🛡️ `REQUIRES SUDO` | Elevated root permissions required to inspect foreign processes or system devices. |

---

## ⚡ The Modern CLI Renaissance (Coreutils ➡️ Rust & Go)

Upgrade your daily terminal ergonomics with modern replacements built for high performance and visual clarity:

| Classic Unix Tool | Modern Alternative | Language | Key Advantages | Quick Command |
| :--- | :--- | :--- | :--- | :--- |
| `ls` | **[eza](https://github.com/eza-community/eza)** | Rust | Git status icons, aligned columns, tree view, colorized permissions | `eza -lah --icons --git` |
| `cat` | **[bat](https://github.com/sharkdp/bat)** | Rust | Syntax highlighting for 150+ languages, Git diff gutter, auto-pager | `bat --style=numbers,changes app.log` |
| `grep` | **[ripgrep (rg)](https://github.com/BurntSushi/ripgrep)** | Rust | SIMD-accelerated, auto-skips `.gitignore` and binary files, 10x faster | `rg -i -C 3 'search_term'` |
| `find` | **[fd](https://github.com/sharkdp/fd)** | Rust | Intuitive syntax, regex default, colorized output, skips hidden/.git | `fd -e log -e txt` |
| `top` / `htop` | **[btop](https://github.com/aristocratos/btop)** | C++ | Real-time CPU/GPU/memory/disk/network graphs, mouse support | `btop --utf-force` |
| `df` | **[duf](https://github.com/muesli/duf)** | Go | Clean visual tables, auto-groups physical devices vs virtual filesystems | `duf --sort usage` |
| `du` | **[dust](https://github.com/bootandy/dust)** | Rust | Interactive ASCII disk space tree-map, instant largest-folder identification | `dust -d 3 -n 15 /var` |
| `ps` | **[procs](https://github.com/dalance/procs)** | Rust | Colored process tree, TCP/UDP listening port binding visibility | `procs --tree nginx` |
| `curl` | **[curlie](https://github.com/rs/curlie)** | Go | Speed of `curl` with the human-friendly colored JSON output of `httpie` | `curlie -v POST api.dev/v1/login` |
| `cd` | **[zoxide (z)](https://github.com/ajeetdsouza/zoxide)** | Rust | Frecency-based smart jumping across deeply nested directories | `z project` |
| `diff` | **[delta](https://github.com/dandavison/delta)** | Rust | Syntax-highlighted side-by-side terminal diffs with line numbering | `git diff \| delta --side-by-side` |
| `man` | **[tldr](https://github.com/tldr-pages/tldr)** | Community | 5 practical, copy-pasteable real-world examples instead of 5,000-line manuals | `tldr tar` |

---

## 🚨 3 AM Incident Response & Production Triage

### 1. Identify "Ghost" Deleted Files Consuming 100% Disk Space
When `df -h` reports 100% full but `du -sh /*` accounts for only a fraction, unlinked files held open by running processes are the culprit:

```bash
sudo lsof +L1 | sort -k 7 -nr | head -20
```

| Flag | Meaning |
| :--- | :--- |
| `+L1` | Filter for open files whose hard-link count is strictly less than 1 (unlinked from disk, yet held open by a process) |
| `sort -k 7 -nr` | Sort numerically in descending order by column 7 (file size in bytes) |
| `head -20` | Show top 20 largest disk-consuming unlinked files |

> 🟢 **Safety:** Safe &nbsp;|&nbsp; 🛡️ **Privilege:** Sudo Required  
> 💡 **Remedy:** Check PID in column 2. Restart or reload the owning daemon (e.g., `sudo systemctl restart nginx`) to close the descriptor and immediately free disk space.

---

### 2. Isolate Disk I/O Saturation Bottlenecks
Pinpoint which process is thrashing disk throughput and driving up system `iowait`:

```bash
sudo iotop -o -b -n 3 -d 1
```

| Flag | Meaning |
| :--- | :--- |
| `-o` | Only show processes or threads actively performing I/O |
| `-b` | Batch mode: non-interactive stream output (suitable for scripts and SSH sessions) |
| `-n 3` | Exit after 3 samples |
| `-d 1` | 1-second sample delay |

> 🟢 **Safety:** Safe &nbsp;|&nbsp; 🛡️ **Privilege:** Sudo Required

---

### 3. Diagnose Out-Of-Memory (OOM) Killer Sacrifices
Inspect the kernel ring buffer to verify if the Linux OOM Killer terminated critical services, complete with human-readable timestamps:

```bash
sudo dmesg -T --level=emerg,alert,crit,err | grep -i -E 'oom|killed process|out of memory'
```

| Flag | Meaning |
| :--- | :--- |
| `-T` | Print human-readable calendar timestamps rather than uptime seconds |
| `--level=...` | Restrict output to emergency, alert, critical, and error log levels |
| `grep -i -E` | Case-insensitive extended regex matching memory termination events |

> 🟢 **Safety:** Safe &nbsp;|&nbsp; 🛡️ **Privilege:** Sudo Required

---

### 4. Locate Sockets & Ports Causing Address Conflicts (`EADDRINUSE`)
Find the exact PID and command preventing your service from binding to port 8080 or 443:

```bash
sudo ss -tulpn 'sport = :8080 or sport = :443'
```

| Flag | Meaning |
| :--- | :--- |
| `-t` | Show TCP sockets |
| `-u` | Show UDP sockets |
| `-l` | Filter for listening sockets only |
| `-p` | Display the process identifier (PID) and executable name |
| `-n` | Do not resolve service port numbers to strings (numeric display for speed) |
| `'sport = ...'` | Socket filter expression restricting output to specific source ports |

> 🟢 **Safety:** Safe &nbsp;|&nbsp; 🛡️ **Privilege:** Sudo Required

---

### 5. Hunt & Identify Zombie Processes and Their Parents
Locate defunct (`Z`) state processes and reveal the Parent PID (`PPID`) that failed to call `wait()`:

```bash
ps -eo stat,ppid,pid,user,comm | awk '$1 ~ /^[Zz]/ {print "Zombie PID: " $3 " | Parent PPID: " $2 " (" $5 ")"}'
```

| Flag / Expression | Meaning |
| :--- | :--- |
| `-eo ...` | Custom output format: state (`stat`), parent PID (`ppid`), process PID (`pid`), user, command (`comm`) |
| `awk '$1 ~ /^[Zz]/'` | Match any process whose state begins with `Z` (Zombie/Defunct) |

> 🟢 **Safety:** Safe &nbsp;|&nbsp; 🛡️ **Privilege:** Normal  
> 💡 **Remedy:** Zombies cannot be killed with `kill -9 <PID>` because they are already dead. Send `SIGHUP` or `SIGCHLD` to the Parent PID, or restart the parent daemon.

---

### 6. Diagnose High Load Average: CPU-Bound vs I/O-Blocked
Determine whether a load spike is caused by CPU run-queue saturation or threads blocked on disk I/O:

```bash
vmstat -w -t 1 5
```

| Flag | Meaning |
| :--- | :--- |
| `-w` | Wide output: prevents column truncation on systems with large CPU/RAM configurations |
| `-t` | Append real-world timestamp to each sample line |
| `1 5` | Sample every 1 second, run 5 times |

* **CPU Saturated:** `procs -> r` consistently exceeds total CPU cores.
* **I/O Blocked:** `procs -> b` > 0 and `cpu -> wa` is elevated.

> 🟢 **Safety:** Safe &nbsp;|&nbsp; 🛡️ **Privilege:** Normal

---

## 🌐 Networking & Socket Forensics

### 1. High-Level Socket State Distribution & Connection Backlogs
Audit socket state allocation in milliseconds directly via `netlink`:

```bash
ss -s
```

> 🟢 **Safety:** Safe &nbsp;|&nbsp; 🛡️ **Privilege:** Normal

---

### 2. Dissect HTTP Request Latency Waterfall (DNS, TCP, TLS, TTFB)
Trace latency down to the microsecond for any HTTP/HTTPS endpoint:

```bash
curl -w "\n┌─ Latency Metrics ───────────────────────┐\n│ DNS Resolution:     %{time_namelookup}s\n│ TCP Handshake:      %{time_connect}s\n│ TLS Handshake:      %{time_appconnect}s\n│ Pre-transfer Time:  %{time_pretransfer}s\n│ Time To First Byte: %{time_starttransfer}s\n│ Total Duration:     %{time_total}s\n└─────────────────────────────────────────┘\n" -o /dev/null -s https://api.github.com
```

> 🟢 **Safety:** Safe &nbsp;|&nbsp; 🛡️ **Privilege:** Normal

---

### 3. Colored, Single-Line Network Interface & IP Summary

```bash
ip -br -c addr show
```

| Flag | Meaning |
| :--- | :--- |
| `-br` | Brief mode: outputs one line per interface |
| `-c` | Color mode: green for `UP`, red for `DOWN` |

> 🟢 **Safety:** Safe &nbsp;|&nbsp; 🛡️ **Privilege:** Normal

---

## 💾 Storage, Filesystems & Inode Disasters

### 1. Inode Exhaustion Audit
When Linux says `No space left on device` but `df -h` shows gigabytes free:

```bash
# Check inode saturation percentage
df -i

# Find directories containing the highest number of files
sudo find /var/spool /tmp /var/lib -xdev -printf '%h\n' | sort | uniq -c | sort -k 1 -nr | head -15
```

> 🟢 **Safety:** Safe &nbsp;|&nbsp; 🛡️ **Privilege:** Sudo Recommended

---

### 2. Find Top 10 Largest Files Exceeding 500MB

```bash
sudo find / -xdev -type f -size +500M -exec ls -lh {} + | awk '{print $5, $9}' | sort -hr
```

> 🟢 **Safety:** Safe &nbsp;|&nbsp; 🛡️ **Privilege:** Sudo Required

---

### 3. Reclaim Space: Vacuum Systemd Journal Logs

```bash
sudo journalctl --vacuum-size=500M --vacuum-time=14d
```

> 🟡 **Mutating:** Deletes archived systemd logs older than 14 days or exceeding 500MB &nbsp;|&nbsp; 🛡️ **Privilege:** Sudo Required

---

## 🧙 Text Wrangling & Stream Processing

### 1. HTTP Status Code Frequency Distribution

```bash
awk '{status[$9]++} END {for (code in status) printf "%-6s : %8d requests\n", code, status[code]}' /var/log/nginx/access.log | sort -k 3 -nr
```

> 🟢 **Safety:** Safe &nbsp;|&nbsp; 🛡️ **Privilege:** Normal

---

### 2. Multi-Core Parallel Execution with `xargs -P`

Accelerate batch processing using all available CPU cores:

```bash
find ./logs -name "*.log" -print0 | xargs -0 -P $(nproc) -I {} gzip -9 {}
```

> 🟡 **Mutating:** Compresses matching files in parallel &nbsp;|&nbsp; 🛡️ **Privilege:** Normal

---

## 📁 Repository Structure

```text
awesome-linux-commands/
├── README.md                           # Master GitHub documentation
├── index.html                          # Interactive dark-mode web application (GitHub Pages)
├── metadata.json                       # Machine-readable command catalog database
├── .nojekyll                           # Preserves assets on GitHub Pages
├── LICENSE                             # MIT License
├── CONTRIBUTING.md                     # Community contribution guidelines
├── commands/                           # Modular domain command files
│   ├── 01-modern-replacements.md       # Rust & Go next-gen terminal utilities
│   ├── 02-incident-response.md         # Production triage, zombie hunting, open descriptors
│   ├── 03-networking-sockets.md        # ss, curl waterfall, tcpdump, mtr
│   ├── 04-storage-filesystems.md       # Inodes, large files, journalctl vacuum, disk benchmarks
│   ├── 05-security-auditing.md         # SUID audit, getcap, failed SSH logins
│   └── 06-text-data-streams.md         # awk histograms, xargs -P parallelization, jq, column
├── scripts/
│   └── build_catalog.py                # Automated parser, validator, and JSON generator
└── docs/
    └── LAUNCH_KIT.md                   # Ready-to-publish social copy for HN, Reddit, Twitter/X
```

---

## 🤝 Contributing

Contributions are welcomed! If you have a high-impact Linux command, modern CLI alternative, or battle-tested one-liner:

1. Check existing commands in `commands/` or search the [web portal](https://vikaskyadav.github.io/awesome-linux-commands/).
2. Follow the standard metadata comment structure and flag breakdown table format.
3. Run the validator:
   ```bash
   python3 scripts/build_catalog.py
   ```
4. Open a Pull Request! See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📜 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

<p align="center">
  Crafted with care by <strong><a href="https://github.com/vikaskyadav">Vikas Yadav</a></strong>
  <br />
  If you find this project valuable, please give it a ⭐️ on GitHub!
</p>
