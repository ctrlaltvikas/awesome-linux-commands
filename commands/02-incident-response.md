# 🚨 3 AM Incident Response & Production Triage

High-impact forensic one-liners to diagnose and resolve production fires: disk space anomalies, CPU/IO saturation, memory runaway, and hung processes.

---

### 1. Identify "Ghost" Deleted Files Holding 100% Disk Space

When `df -h` shows 100% full but `du -sh /*` accounts for only 20GB, unlinked files held open by running processes are the culprit.

<!-- @id: incident-deleted-files -->
<!-- @name: lsof-deleted-files -->
<!-- @category: Incident Response -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: storage, disk-full, forensics, lsof -->

```bash
sudo lsof +L1 | sort -k 7 -nr | head -20
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `+L1` | List open files with a hard-link count strictly less than 1 (unlinked from filesystem, yet held by a file descriptor) |
| `sort -k 7 -nr` | Sort numerically in descending order by column 7 (file size in bytes) |
| `head -20` | Display the 20 largest disk-consuming unlinked files |

#### Incident Remedy
Identify the `PID` from column 2. Restart or reload the offending daemon (e.g., `sudo systemctl restart nginx`) to release the file descriptor and free the disk space immediately.

---

### 2. Isolate Disk I/O Saturation Bottlenecks

Detect which exact process and thread is thrashing disk read/write bandwidth and causing high system `iowait`.

<!-- @id: incident-io-saturation -->
<!-- @name: iotop-saturation -->
<!-- @category: Incident Response -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: performance, io, disk, iotop, sysadmin -->

```bash
sudo iotop -o -b -n 3 -d 1
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-o` | Only show processes or threads currently actively performing I/O |
| `-b` | Batch mode: non-interactive stream output (suitable for logging, ssh, and scripts) |
| `-n 3` | Run 3 iterations before exiting |
| `-d 1` | Sample interval of 1 second between updates |

---

### 3. Diagnose Out-Of-Memory (OOM) Killer Sacrifices

Inspect the kernel log ring buffer to determine if the Linux OOM Killer terminated critical services, complete with human-readable timestamps.

<!-- @id: incident-oom-killer -->
<!-- @name: dmesg-oom-killer -->
<!-- @category: Incident Response -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: memory, oom, kernel, crash, dmesg -->

```bash
sudo dmesg -T --level=emerg,alert,crit,err | grep -i -E 'oom|killed process|out of memory'
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-T` | Print human-readable timestamps (`Sun Nov 1 22:15:00 2026`) instead of uptime seconds |
| `--level=...` | Filter kernel ring buffer messages to emergency, alert, critical, and error priorities |
| `grep -i -E` | Case-insensitive extended regex matching memory termination events |

---

### 4. Locate Sockets & Ports Causing Address Conflicts (EADDRINUSE)

Pinpoint the exact PID, command name, and user holding a TCP/UDP port preventing your service from binding.

<!-- @id: incident-port-conflict -->
<!-- @name: ss-port-conflict -->
<!-- @category: Incident Response -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: networking, ports, ss, conflicts -->

```bash
sudo ss -tulpn 'sport = :8080 or sport = :443'
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-t` | Include TCP sockets |
| `-u` | Include UDP sockets |
| `-l` | Filter for listening sockets only |
| `-p` | Display the process identifier (PID) and executable name |
| `-n` | Do not resolve service port numbers to service names (numeric display) |
| `'sport = ...'` | Socket filter expression restricting output to specific source ports |

---

### 5. Hunt & Identify Zombie Processes and Their Parents

Locate zombie (`Z`) state processes and reveal the Parent PID (`PPID`) that failed to reap its child via `wait()`.

<!-- @id: incident-zombie-hunt -->
<!-- @name: ps-zombie-hunt -->
<!-- @category: Incident Response -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: process, zombie, ppid, ps -->

```bash
ps -eo stat,ppid,pid,user,comm | awk '$1 ~ /^[Zz]/ {print "Zombie PID: " $3 " | Parent PPID: " $2 " (" $5 ")"}'
```

#### Flag Breakdown
| Flag / Arg | Description |
| :--- | :--- |
| `-e` | Select all running processes across all users |
| `-o ...` | Format custom columns: process state (`stat`), parent PID (`ppid`), PID (`pid`), owner (`user`), executable name (`comm`) |
| `awk '$1 ~ /^[Zz]/'` | Match any process whose state begins with `Z` (Zombie/Defunct) |

#### Incident Remedy
You cannot kill a zombie with `kill -9 <PID>` because it is already dead. You must send `SIGHUP` or `SIGCHLD` to the Parent PID, or restart the parent daemon to trigger init (`PID 1`) to reap it.

---

### 6. Diagnose High Load Average: CPU-Bound vs I/O-Blocked

Break down high Linux load averages into CPU run-queue saturation versus disk I/O wait blocked threads.

<!-- @id: incident-vmstat-load -->
<!-- @name: vmstat-triage -->
<!-- @category: Incident Response -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: cpu, memory, iowait, performance, vmstat -->

```bash
vmstat -w -t 1 5
```

#### Flag Breakdown
| Flag / Arg | Description |
| :--- | :--- |
| `-w` | Wide format: ensures columns never truncate or misalign on multi-core systems |
| `-t` | Append real-world timestamp to each sample line |
| `1 5` | Sample interval of 1 second, repeating 5 times |

#### Key Metrics to Read
* `procs -> r`: Processes waiting for CPU run-time. If `r` exceeds total CPU cores, CPU is saturated.
* `procs -> b`: Processes blocked in uninterruptible sleep (`D` state, usually waiting on disk or network I/O).
* `cpu -> wa`: Percentage of time CPU spent idling while waiting for outstanding disk I/O requests.

---

### 7. Find All Files Modified in the Last 15 Minutes

Track down rogue log writes, malware droppers, or configuration alterations during an active security or operational incident.

<!-- @id: incident-recent-files -->
<!-- @name: find-recent-modified -->
<!-- @category: Incident Response -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: files, forensics, security, find -->

```bash
sudo find /etc /var/log /tmp /opt -type f -mmin -15 -exec ls -lh {} +
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `/etc /var/log ...` | Restrict search to critical mutable and configuration directories |
| `-type f` | Search exclusively for regular files (ignores directory timestamps) |
| `-mmin -15` | Match files whose modification timestamp was updated less than 15 minutes ago |
| `-exec ls -lh {} +` | Batch-pass matched paths to `ls -lh` for size, permissions, and exact timestamp |

---

### 8. List Top 10 Memory Consuming Processes Formatted in MB

Generate an accurate, human-readable breakdown of resident memory (RSS) consumed per process.

<!-- @id: incident-top-memory -->
<!-- @name: ps-top-memory -->
<!-- @category: Incident Response -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: memory, rss, triage, ps -->

```bash
ps -eo pid,user,rss,pmem,comm --sort=-rss | awk 'NR==1 {printf "%-8s %-12s %-12s %-8s %s\n", $1, $2, "RSS (MB)", $4, $5} NR>1 && NR<=11 {printf "%-8s %-12s %-12.1f %-8s %s\n", $1, $2, $3/1024, $4, $5}'
```

#### Flag Breakdown
| Element | Description |
| :--- | :--- |
| `-eo pid,user,rss,pmem,comm` | Extract Process ID, User, Resident Set Size in KB, % Memory, and Command |
| `--sort=-rss` | Sort by RSS in descending order (highest consumers first) |
| `awk ...` | Calculates and converts raw KiB column ($3) to Megabytes formatted with a single decimal place |


---

### 9. Identify Process Holding a File or Port Open with `fuser`

Find which process has an active file descriptor or mount lock on a specific file, directory, or socket.

<!-- @id: incident-fuser-file -->
<!-- @name: fuser-file-lock -->
<!-- @category: Incident Response -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: files, locks, fuser, triage -->

```bash
sudo fuser -v /var/log/nginx/access.log
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-v` | Verbose mode: displays PID, user, process name, and access type (`m` mmap, `f` open file, `r` root dir) |

---

### 10. Trace Relative Syscall Latency on Frozen Processes

Measure time elapsed between system calls to identify which kernel syscall is stalling an application.

<!-- @id: incident-strace-latency -->
<!-- @name: strace-relative-latency -->
<!-- @category: Incident Response -->
<!-- @risk: Mutating -->
<!-- @privilege: Sudo -->
<!-- @tags: performance, strace, latency, debugging -->

```bash
sudo strace -r -p 1234
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-r` | Print relative timestamp (microseconds elapsed since previous system call) |
| `-p 1234` | Attach directly to running Process ID |

---

### 11. Inspect Runtime Resource Limits of a Process

Check soft and hard limits for open file descriptors (`Max open files`), memory, and pending signals on a live process.

<!-- @id: incident-proc-limits -->
<!-- @name: proc-pid-limits -->
<!-- @category: Incident Response -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: process, limits, ulimit, ulimit-exceeded -->

```bash
cat /proc/1234/limits | grep -E 'Max open files|Max processes|Limit'
```

#### Why Run This
When applications crash with `Too many open files`, this command confirms whether the daemon inherited systemd's limits or hit its configured ceiling.

---

### 12. Diagnose Storage Queue Saturation & I/O Latency

Measure disk response latency (`await`), queue backlog (`aqu-sz`), and device utilization percentage (`%util`).

<!-- @id: incident-iostat-latency -->
<!-- @name: iostat-disk-latency -->
<!-- @category: Incident Response -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: storage, disk, iostat, latency, performance -->

```bash
iostat -xz 1 3
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-x` | Extended statistics: shows queue size, await latency, and service times |
| `-z` | Suppress output for devices that had zero activity during the sample |
| `1 3` | Sample every 1 second, repeat 3 times |

---

### 13. Audit System Reboot History & Kernel Crashes

Display full calendar timestamps of past system reboots, crashes, and unexpected shutdowns.

<!-- @id: incident-last-reboots -->
<!-- @name: last-reboot-history -->
<!-- @category: Incident Response -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: system, reboot, crash, uptime, forensics -->

```bash
last reboot -F -n 5
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-F` | Print full floating-point dates and times including year and seconds |
| `-n 5` | Limit output to the 5 most recent reboot events |

---

### 14. Query Priority 3 (Errors & Critical) Logs from Current Boot

Filter systemd journal strictly to errors, critical alerts, and emergencies from the active boot session.

<!-- @id: incident-journal-errors -->
<!-- @name: journalctl-current-errors -->
<!-- @category: Incident Response -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: logs, systemd, errors, triage -->

```bash
sudo journalctl -p 3 -xb --no-pager
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-p 3` | Filter log priority level 3 (`err`), 2 (`crit`), 1 (`alert`), and 0 (`emerg`) |
| `-x` | Append explanatory help text and catalog descriptions to known errors |
| `-b` | Restrict search to the current boot session only |
| `--no-pager` | Print directly to standard output without piping to `less` |
