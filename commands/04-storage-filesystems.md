# 💾 Storage, Filesystems & Inode Disasters

Essential commands to recover from out-of-disk panics, diagnose inode exhaustion, benchmark storage I/O, and prune runaway system logs.

---

### 1. Diagnose & Trace Inode Exhaustion

When Linux reports `No space left on device` even though `df -h` shows plenty of free gigabytes, the filesystem has run out of available inodes (caused by millions of tiny files or session tokens).

<!-- @id: storage-inode-audit -->
<!-- @name: inode-exhaustion-audit -->
<!-- @category: Storage -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: storage, inodes, disk-full, forensics -->

```bash
df -i
```

#### Follow-up: Find Directory Storing the Most Inodes
```bash
sudo find /var/spool /tmp /var/lib -xdev -printf '%h\n' | sort | uniq -c | sort -k 1 -nr | head -15
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-i` (in `df`) | List inode counts and percentage used instead of byte block sizes |
| `-xdev` (in `find`) | Do not descend into directories on separate mounted filesystems |
| `-printf '%h\n'` | Print only the parent directory path for each file |
| `uniq -c` | Count number of occurrences (files per directory) |

---

### 2. Sweep the Largest Files Exceeding 500MB

Rapidly find massive core dumps, runaway log files, or abandoned database snapshots consuming drive capacity.

<!-- @id: storage-large-files -->
<!-- @name: find-large-files -->
<!-- @category: Storage -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: storage, disk-space, find, cleanup -->

```bash
sudo find / -xdev -type f -size +500M -exec ls -lh {} + | awk '{print $5, $9}' | sort -hr
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-xdev` | Stay within the root filesystem; prevents searching through virtual `/proc` or NFS mounts |
| `-type f` | Search exclusively for files |
| `-size +500M` | Match files strictly greater than 500 Megabytes |
| `awk '{print $5, $9}'` | Display size and full absolute file path |

---

### 3. Vacuum Runaway Systemd Journal Logs

Reclaim gigabytes of storage occupied by accumulated `systemd-journald` binary logs without rebooting or stopping the logging daemon.

<!-- @id: storage-vacuum-journal -->
<!-- @name: journalctl-vacuum -->
<!-- @category: Storage -->
<!-- @risk: Mutating -->
<!-- @privilege: Sudo -->
<!-- @tags: storage, systemd, logs, cleanup -->

```bash
sudo journalctl --vacuum-size=500M --vacuum-time=14d
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `--vacuum-size=500M` | Delete oldest journal logs until total disk usage falls below 500MB |
| `--vacuum-time=14d` | Purge any journal entries older than 14 days |

---

### 4. Block Device Architecture, Filesystem Types & UUIDs

Display an organized ASCII tree of all physical NVMe/SATA drives, partitions, LVM volume groups, and mount points with filesystem formats.

<!-- @id: storage-lsblk-tree -->
<!-- @name: lsblk-filesystem-tree -->
<!-- @category: Storage -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: storage, partitions, lvm, lsblk -->

```bash
lsblk -o NAME,FSTYPE,SIZE,FSAVAIL,FSUSE%,MOUNTPOINTS,UUID
```

#### Flag Breakdown
| Column | Description |
| :--- | :--- |
| `NAME` | Device identifier (e.g., `nvme0n1p1`, `sda`) |
| `FSTYPE` | Filesystem signature (`ext4`, `xfs`, `btrfs`, `zfs`) |
| `SIZE` & `FSAVAIL` | Total capacity and available unallocated space |
| `MOUNTPOINTS` | Active filesystem mount target directory |
| `UUID` | Universally Unique Identifier for `/etc/fstab` configuration |

---

### 5. Benchmark True Sequential Storage Write Speed Without Cache

Measure actual raw hardware write throughput by bypassing Linux kernel dirty page writeback buffers.

<!-- @id: storage-dd-benchmark -->
<!-- @name: dd-disk-benchmark -->
<!-- @category: Storage -->
<!-- @risk: Mutating -->
<!-- @privilege: Normal -->
<!-- @tags: storage, benchmark, dd, performance -->

```bash
dd if=/dev/zero of=./speedtest.tmp bs=1M count=1024 conv=fdatasync status=progress && rm -f ./speedtest.tmp
```

#### Flag Breakdown
| Parameter | Description |
| :--- | :--- |
| `bs=1M count=1024` | Write a total of 1 Gigabyte using 1 Megabyte chunk blocks |
| `conv=fdatasync` | Forces physical flush of data to disk before completing benchmark (eliminates RAM cache distortion) |
| `status=progress` | Display real-time MB/s throughput speed indicator |


---

### 6. Monitor Data Pipe Progress with Visual Progress Bar (`pv`)

Add real-time throughput metrics, elapsed time, total transfer percentage, and ETA to any Unix pipeline.

<!-- @id: storage-pv-progress -->
<!-- @name: pv-pipe-progress -->
<!-- @category: Storage -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: storage, pipeline, progress, pv -->

```bash
pv database.sql | gzip -9 > database.sql.gz
```

#### Why Run This
When piping gigabytes of data through `gzip`, `dd`, or `mysql`, standard Unix tools give zero visual feedback. `pv` (Pipe Viewer) wraps the stream with a dynamic progress bar and MB/s throughput display.

---

### 7. Securely Shred & Overwrite Sensitive Files

Cryptographically destroy sensitive tokens, SSH private keys, or passwords by overwriting them with random data passes before unlinking.

<!-- @id: storage-shred-wipe -->
<!-- @name: shred-secure-delete -->
<!-- @category: Storage -->
<!-- @risk: Destructive -->
<!-- @privilege: Normal -->
<!-- @tags: storage, security, shred, wiping -->

```bash
shred -u -z -n 3 secret.key
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-u` | Truncate and remove the file after overwriting |
| `-z` | Add a final overwrite pass with zeros (`0x00`) to hide shredding signatures |
| `-n 3` | Overwrite file contents 3 times with cryptographic pseudo-random data |

---

### 8. Find and Audit Empty Files & Directories

Identify zero-byte files created by failed software builds or stalled application runs.

<!-- @id: storage-find-empty -->
<!-- @name: find-empty-files -->
<!-- @category: Storage -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: storage, files, cleanup, find -->

```bash
find . -type f -empty -not -path '*/.git/*'
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-type f` | Search exclusively for regular files |
| `-empty` | Match files that contain 0 bytes |
| `-not -path ...` | Exclude Git metadata directory |

---

### 9. Emergency Remount of Read-Only Root Filesystem

Recover from filesystem errors that caused the Linux kernel to drop the root partition into read-only mode (`EROFS`).

<!-- @id: storage-remount-rw -->
<!-- @name: mount-remount-rw -->
<!-- @category: Storage -->
<!-- @risk: Mutating -->
<!-- @privilege: Sudo -->
<!-- @tags: storage, recovery, mount, kernel -->

```bash
sudo mount -o remount,rw /
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-o remount,rw` | Instruct the kernel VFS layer to switch the existing mount to read-write mode |
| `/` | Mount point target |

---

### 10. Audit NVMe SSD Health & Remaining Wear Life

Query the NVMe drive controller for temperature, spare capacity, and percentage of endurance consumed (wear indicator).

<!-- @id: storage-nvme-smart -->
<!-- @name: nvme-smart-log -->
<!-- @category: Storage -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: storage, nvme, ssd, hardware, health -->

```bash
sudo nvme smart-log /dev/nvme0n1 | grep -E 'percentage_used|critical_warning|temperature'
```

#### Flag Breakdown
| Element | Description |
| :--- | :--- |
| `smart-log` | Retrieves SMART / Health Information log page from drive firmware |
| `/dev/nvme0n1` | NVMe controller and namespace path |
| `grep ...` | Extracts drive temperature and hardware endurance wear percentage |
