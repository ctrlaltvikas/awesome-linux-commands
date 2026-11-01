# 🐳 Containers, Namespaces & cgroups

Low-level Linux primitives underpinning Docker, Podman, and Kubernetes: namespace isolation, namespace entering, cgroups v2 resource ceilings, and capability auditing.

---

### 1. Audit All Linux Namespaces on the Host (`lsns`)

List all active Linux kernel namespaces (Network, PID, Mount, IPC, UTS, User), their unique namespace inode IDs, and the root process owning each.

<!-- @id: cont-lsns-audit -->
<!-- @name: lsns-namespace-audit -->
<!-- @category: Containers & Namespaces -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: containers, namespaces, lsns, docker, k8s -->

```bash
sudo lsns -t net,pid,mnt
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-t net,pid,mnt` | Filter namespace types to Network, PID, and Mount (the core container isolation boundaries) |

---

### 2. Enter a Container Network Namespace Directly from Host (`nsenter`)

Run host diagnostic tools (like `ss`, `ip`, or `tcpdump`) inside a container's isolated network stack without needing `docker exec` or container root access.

<!-- @id: cont-nsenter-network -->
<!-- @name: nsenter-network-namespace -->
<!-- @category: Containers & Namespaces -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: containers, nsenter, networking, debug -->

```bash
sudo nsenter -t 1234 -n ss -tulpn
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-t 1234` | Target Process ID running inside the container |
| `-n` | Enter only the network namespace of the target process |
| `ss -tulpn` | Command executed within that network namespace |

---

### 3. Spawn an Isolated Lightweight Container with Pure Linux (`unshare`)

Create a private sandbox with isolated Mount, Network, and PID namespaces using built-in Linux kernel primitives without Docker or runtime daemons.

<!-- @id: cont-unshare-sandbox -->
<!-- @name: unshare-pure-container -->
<!-- @category: Containers & Namespaces -->
<!-- @risk: Mutating -->
<!-- @privilege: Sudo -->
<!-- @tags: containers, namespaces, unshare, sandbox -->

```bash
sudo unshare --mount --net --pid --fork bash
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `--mount` | Unshare the mount namespace (changes to mounts do not leak to host) |
| `--net` | Unshare the network namespace (spawns with private loopback) |
| `--pid` | Unshare the PID namespace (spawned shell becomes PID 1) |
| `--fork` | Fork the specified program as a child of unshare |

---

### 4. Read Live Memory Consumption via cgroups v2

Query the exact bytes of RAM currently consumed by a service or container slice directly from the Linux cgroup filesystem.

<!-- @id: cont-cgroup-memory-current -->
<!-- @name: cgroup-memory-current -->
<!-- @category: Containers & Namespaces -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: cgroups, memory, containers, resource-limits -->

```bash
cat /sys/fs/cgroup/system.slice/nginx.service/memory.current | awk '{printf "%.2f MB\n", $1/1024/1024}'
```

#### Why Run This
cgroups v2 unifies resource controllers under `/sys/fs/cgroup`. This command reads true real-time kernel memory tracking without process table overhead.

---

### 5. Check cgroups v2 Hard Memory Ceiling Before OOM

Inspect the hard memory threshold (`memory.max`) configured for a service before the kernel triggers the cgroup OOM killer.

<!-- @id: cont-cgroup-memory-max -->
<!-- @name: cgroup-memory-max -->
<!-- @category: Containers & Namespaces -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: cgroups, memory, oom, limits -->

```bash
cat /sys/fs/cgroup/system.slice/nginx.service/memory.max
```

#### Output Meaning
* `max`: No hard memory limit enforced (unbounded host RAM usage).
* Numeric value (e.g., `536870912`): Memory limit in bytes (512 MB).

---

### 6. Inspect Linux Capabilities Bounding Set (`capsh`)

Audit which POSIX capabilities (e.g., `CAP_NET_BIND_SERVICE`, `CAP_SYS_ADMIN`, `CAP_NET_RAW`) are granted or dropped in the current execution context.

<!-- @id: cont-capsh-print -->
<!-- @name: capsh-capabilities -->
<!-- @category: Containers & Namespaces -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: containers, security, capabilities, capsh -->

```bash
capsh --print
```

#### Why Run This
Essential when debugging container permission denials where a process running as `root` (UID 0) inside a container still cannot perform network sniffing or mounts due to dropped capabilities.

---

### 7. List All Named Network Namespaces (`ip netns`)

Display all named network namespaces managed via the `iproute2` subsystem.

<!-- @id: cont-ip-netns-list -->
<!-- @name: ip-netns-list -->
<!-- @category: Containers & Namespaces -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: containers, networking, namespaces, iproute2 -->

```bash
ip netns list
```

---

### 8. Execute Command Inside Named Network Namespace

Run network inspection commands inside an isolated network namespace without switching your current terminal shell.

<!-- @id: cont-ip-netns-exec -->
<!-- @name: ip-netns-exec -->
<!-- @category: Containers & Namespaces -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: containers, networking, namespaces, ip-netns -->

```bash
sudo ip netns exec mynet ip link show
```

#### Flag Breakdown
| Argument | Description |
| :--- | :--- |
| `exec mynet` | Target named network namespace |
| `ip link show` | Diagnostic command to run within that isolated network stack |

---

### 9. Detect Hypervisor or Container Virtualization Technology

Determine instantly whether the current host is bare-metal, a cloud virtual machine, or a containerized instance.

<!-- @id: cont-detect-virt -->
<!-- @name: systemd-detect-virt -->
<!-- @category: Containers & Namespaces -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: virtualization, containers, hardware, systemd -->

```bash
systemd-detect-virt
```

#### Output Examples
* `none`: Bare-metal hardware
* `kvm`, `vmware`, `amazon`: Virtual Machine hypervisors
* `docker`, `podman`, `lxc`, `wsl`: Container environments
