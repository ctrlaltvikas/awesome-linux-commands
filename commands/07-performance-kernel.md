# ⚙️ Performance Observability & Kernel Runtime Tuning

Measure CPU saturation, inspect memory page states, bind processes to CPU cores, and adjust live kernel scheduler priorities.

---

### 1. Dynamically Adjust Process Scheduling Priority (`renice`)

Increase or decrease the CPU scheduling priority of a running process without restarting it.

<!-- @id: perf-renice-process -->
<!-- @name: renice-priority -->
<!-- @category: Performance & Kernel -->
<!-- @risk: Mutating -->
<!-- @privilege: Sudo -->
<!-- @tags: performance, cpu, scheduling, renice -->

```bash
sudo renice -n -5 -p 1234
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-n -5` | Set nice value to `-5` (negative values give higher priority/more CPU cycles; range `-20` to `19`) |
| `-p 1234` | Target Process ID (PID) |

---

### 2. Pin Process Execution to Specific CPU Cores (`taskset`)

Enforce CPU core affinity to prevent context-switching overhead and cache bouncing on multi-core NUMA systems.

<!-- @id: perf-taskset-affinity -->
<!-- @name: taskset-cpu-affinity -->
<!-- @category: Performance & Kernel -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: performance, cpu, affinity, numa, taskset -->

```bash
taskset -c 0,1 nginx -g "daemon off;"
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-c 0,1` | Restrict execution strictly to logical CPU cores 0 and 1 |

---

### 3. Inspect Kernel Dirty Memory Pages Waiting on Disk Flush

Determine how many megabytes of unwritten memory data are currently backed up in RAM waiting to be committed to disk.

<!-- @id: perf-proc-dirty-memory -->
<!-- @name: proc-dirty-memory -->
<!-- @category: Performance & Kernel -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: memory, performance, dirty-pages, kernel -->

```bash
cat /proc/meminfo | grep -E 'Dirty|Writeback|AnonPages'
```

#### Why Run This
When disk writes appear stalled or load spikes during heavy database operations, high `Dirty` memory numbers indicate the kernel is struggling to write dirty buffers back to slow storage.

---

### 4. Per-Process CPU Utilization Breakdown with `pidstat`

Monitor real-time user-space (`%usr`) vs kernel-space (`%system`) CPU consumption across individual processes.

<!-- @id: perf-pidstat-cpu -->
<!-- @name: pidstat-cpu-breakdown -->
<!-- @category: Performance & Kernel -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: performance, cpu, pidstat, sysstat -->

```bash
pidstat -u 1 3
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-u` | Report CPU utilization metrics |
| `1 3` | Sample every 1 second, repeat 3 times |

---

### 5. Apply Linux Kernel Runtime Parameters Without Rebooting

Instantly reload sysctl parameters from `/etc/sysctl.conf` into the active Linux kernel.

<!-- @id: perf-sysctl-reload -->
<!-- @name: sysctl-reload -->
<!-- @category: Performance & Kernel -->
<!-- @risk: Mutating -->
<!-- @privilege: Sudo -->
<!-- @tags: kernel, sysctl, performance, tuning -->

```bash
sudo sysctl -p /etc/sysctl.conf
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-p` | Load sysctl settings from the specified configuration file |

---

### 6. Safely Release Inactive Page Cache, Dentries & Inodes

Force cached read data and directory structures to be freed from RAM without dropping dirty data.

<!-- @id: perf-drop-caches -->
<!-- @name: drop-caches-safe -->
<!-- @category: Performance & Kernel -->
<!-- @risk: Mutating -->
<!-- @privilege: Sudo -->
<!-- @tags: memory, cache, drop_caches, performance -->

```bash
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
```

#### Flag / Step Breakdown
| Element | Description |
| :--- | :--- |
| `sync` | Flushes all dirty unwritten filesystem buffers to storage first (prevents data loss) |
| `echo 3` | Frees clean page cache (`1`), dentries and inodes (`2`), or both (`3`) |
| `sudo tee ...` | Safely writes value to root-owned procfs pseudo-file |
