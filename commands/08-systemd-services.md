# ⚙️ Systemd, Services & Boot Profiling

Manage systemd unit lifecycles, diagnose boot bottlenecks, inspect drop-in configuration overrides, and audit cgroup resource utilization.

---

### 1. Triage All Failed or Degraded Systemd Units

Quickly identify every failed service, mount, or timer currently causing system degradation.

<!-- @id: sysd-failed-units -->
<!-- @name: systemctl-failed -->
<!-- @category: Systemd & Services -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: systemd, services, triage, errors -->

```bash
systemctl --failed
```

#### Why Run This First
`systemctl --failed` queries systemd's state database directly to isolate broken or crashing units without digging through syslog.

---

### 2. Identify Boot Bottlenecks & Service Startup Delays

Pinpoint exactly which services delayed system boot time, sorted from slowest to fastest initialization.

<!-- @id: sysd-analyze-blame -->
<!-- @name: systemd-analyze-blame -->
<!-- @category: Systemd & Services -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: systemd, boot, performance, blame -->

```bash
systemd-analyze blame | head -15
```

#### Flag Breakdown
| Element | Description |
| :--- | :--- |
| `blame` | Prints an ordered list of services and the duration each took to initialize during boot |
| `head -15` | Limit output to the 15 slowest services |

---

### 3. Trace Boot Critical Chain Dependency Timeline

Print the time-critical dependency path that delayed system boot completion.

<!-- @id: sysd-analyze-critical-chain -->
<!-- @name: systemd-critical-chain -->
<!-- @category: Systemd & Services -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: systemd, boot, dependencies, critical-chain -->

```bash
systemd-analyze critical-chain
```

#### Why Run This
Unlike `blame` (which shows parallel services), `critical-chain` visualizes the sequential chain of services that blocked the multi-user or graphical target from finishing.

---

### 4. View Complete Service Unit & Drop-in Overrides

Display the full contents of a unit file alongside all active override configuration files in `/etc/systemd/system/`.

<!-- @id: sysd-cat-unit -->
<!-- @name: systemctl-cat-unit -->
<!-- @category: Systemd & Services -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: systemd, configuration, overrides, cat -->

```bash
systemctl cat nginx.service
```

#### Flag Breakdown
| Element | Description |
| :--- | :--- |
| `cat` | Concatenates the vendor `/lib/systemd/system/` file with all `/etc/systemd/system/*.service.d/*.conf` drop-ins |

---

### 5. Query Specific Service Runtime Properties Programmatically

Extract clean machine-readable runtime properties (e.g. active timestamp, main PID, substate) without parsing human-readable status text.

<!-- @id: sysd-show-properties -->
<!-- @name: systemctl-show-props -->
<!-- @category: Systemd & Services -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: systemd, properties, automation, pids -->

```bash
systemctl show -p ActiveEnterTimestamp,SubState,MainPID nginx.service
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-p PropertyName` | Restrict output to specific comma-separated systemd D-Bus properties |

---

### 6. List All Scheduled Systemd Timers (Modern Cron)

View all active and pending systemd timer jobs, next trigger schedules, and elapsed durations since last execution.

<!-- @id: sysd-list-timers -->
<!-- @name: systemctl-list-timers -->
<!-- @category: Systemd & Services -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: systemd, timers, cron, scheduling -->

```bash
systemctl list-timers --all
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `--all` | Show inactive and disabled timers alongside active scheduled jobs |

---

### 7. Hierarchical Cgroup Process Tree per Service

Visualize which processes and worker threads belong to which systemd service slices.

<!-- @id: sysd-cgls-tree -->
<!-- @name: systemd-cgls-tree -->
<!-- @category: Systemd & Services -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: systemd, cgroups, process-tree, slices -->

```bash
systemd-cgls
```

#### Why Run This
Provides a clear view of child workers (e.g. PHP-FPM pools, Celery workers) organized under their parent systemd service slice.

---

### 8. Real-Time Cgroup Resource Consumption Top (`systemd-cgtop`)

Interactive top-like monitor showing real-time CPU, memory, and I/O consumption grouped by systemd service slice.

<!-- @id: sysd-cgtop-monitor -->
<!-- @name: systemd-cgtop-monitor -->
<!-- @category: Systemd & Services -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: systemd, cgroups, monitoring, top -->

```bash
systemd-cgtop -m -n 3
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-m` | Order service slices by memory consumption |
| `-n 3` | Exit after 3 iterations |

---

### 9. Stream Service Logs Within a Specific Time Window

Filter journalctl logs for a specific unit over a precise historical time range without piping through `less`.

<!-- @id: sysd-journal-unit-window -->
<!-- @name: journalctl-unit-window -->
<!-- @category: Systemd & Services -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: systemd, logs, journalctl, time-window -->

```bash
sudo journalctl -u nginx.service --since "30 min ago" --no-pager
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-u unit` | Filter strictly to the specified systemd unit |
| `--since "..."` | Filter events after a relative or absolute timestamp |
| `--no-pager` | Print directly to standard output |

---

### 10. Reload Systemd Manager Configuration

Notify systemd to rescan unit files on disk after adding or modifying drop-in overrides.

<!-- @id: sysd-daemon-reload -->
<!-- @name: systemctl-daemon-reload -->
<!-- @category: Systemd & Services -->
<!-- @risk: Mutating -->
<!-- @privilege: Sudo -->
<!-- @tags: systemd, reload, config -->

```bash
sudo systemctl daemon-reload
```
