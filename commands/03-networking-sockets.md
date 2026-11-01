# 🌐 Networking, Sockets & Packet Sleuthing

Modern commands and diagnostic one-liners for inspecting listening ports, connection state distribution, latency bottlenecks, and network traffic.

---

### 1. High-Level Socket State Distribution & Connection Backlogs

Inspect total socket allocation to detect socket leaks, high `TIME-WAIT` pile-ups, or `CLOSE-WAIT` application connection descriptor leaks.

<!-- @id: net-ss-summary -->
<!-- @name: ss-summary -->
<!-- @category: Networking -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: networking, ss, sockets, tcp, connections -->

```bash
ss -s
```

#### Why Run This First
`ss -s` queries kernel socket metrics directly via `netlink` without scanning `/proc`. It provides instantaneous counts of established, closed, orphaned, time-wait, and timewait-recycled sockets even under millions of active connections.

---

### 2. Trace HTTP Latency Waterfall (DNS, TCP, TLS, TTFB)

Dissect the exact microsecond latency timeline of an HTTP request: DNS resolution, TCP handshake, TLS negotiation, Time-To-First-Byte (TTFB), and transfer duration.

<!-- @id: net-curl-latency -->
<!-- @name: curl-timing-waterfall -->
<!-- @category: Networking -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: networking, http, curl, latency, ttfb -->

```bash
curl -w "\n┌─ Latency Metrics ───────────────────────┐\n│ DNS Resolution:     %{time_namelookup}s\n│ TCP Handshake:      %{time_connect}s\n│ TLS Handshake:      %{time_appconnect}s\n│ Pre-transfer Time:  %{time_pretransfer}s\n│ Time To First Byte: %{time_starttransfer}s\n│ Total Duration:     %{time_total}s\n└─────────────────────────────────────────┘\n" -o /dev/null -s https://api.github.com
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-w "..."` | Custom formatted timing variables extracted from `libcurl` engine |
| `-o /dev/null` | Discard server response body from stdout to keep terminal output clean |
| `-s` | Silent mode: suppresses default download progress meter |

---

### 3. Colored, Brief Interface & IP Assignment Overview

Display all local network interfaces, link states (UP/DOWN), and assigned IPv4/IPv6 addresses in clean single-line rows with native ANSI colors.

<!-- @id: net-ip-brief -->
<!-- @name: ip-brief-colored -->
<!-- @category: Networking -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: networking, ip, interfaces, routing -->

```bash
ip -br -c addr show
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-br` | Brief mode: prints each interface as a single standardized line |
| `-c` | Color mode: colors UP interfaces green and DOWN interfaces red |
| `addr show` | Display protocol addresses |

---

### 4. Determine Outbound Routing Path, Source IP & Next-Hop

Determine which local interface, source IP, and gateway the Linux kernel will choose to reach an external destination without generating traffic.

<!-- @id: net-ip-route-get -->
<!-- @name: ip-route-destination -->
<!-- @category: Networking -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: networking, routing, kernel, ip -->

```bash
ip route get 1.1.1.1
```

#### Why Run This
Avoids guesswork in multi-homed servers, VPNs, and container bridges. Returns the exact interface (`dev eth0`), local source address (`src 192.168.1.50`), and default gateway (`via 192.168.1.1`).

---

### 5. Sniff HTTP/HTTPS Traffic Without DNS Resolution Lag

Capture packet headers for HTTP/HTTPS traffic to diagnose dropped SYN packets or connection resets without getting stalled by slow reverse-DNS lookups.

<!-- @id: net-tcpdump-sniff -->
<!-- @name: tcpdump-web-traffic -->
<!-- @category: Networking -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: networking, packet-capture, tcpdump, security -->

```bash
sudo tcpdump -nn -i any -c 25 'tcp port 80 or tcp port 443'
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-nn` | Do not resolve hostnames or port names to strings (ensures zero DNS query latency) |
| `-i any` | Capture on all available network interfaces simultaneously |
| `-c 25` | Exit automatically after capturing 25 matching packets |
| `'tcp port ...'` | BPF filter expression matching web traffic |

---

### 6. Diagnose Packet Loss & Jitter with Continuous MTR Report

Combines `traceroute` and `ping` into an aggregated statistical report across every network hop to identify ISP or internal routing packet loss.

<!-- @id: net-mtr-report -->
<!-- @name: mtr-loss-report -->
<!-- @category: Networking -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: networking, mtr, traceroute, latency, packet-loss -->

```bash
mtr --report --report-cycles 10 --no-dns 8.8.8.8
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `--report` | Generate a summarized text table rather than continuous curses screen |
| `--report-cycles 10` | Send 10 probes to each hop before calculating average, best, worst, and loss % |
| `--no-dns` | Show numeric IP addresses to avoid DNS lookup overhead |

---

### 7. Monitor Real-Time Bandwidth Consumption by Process

Identify the exact running executable and PID saturating server upload or download throughput.

<!-- @id: net-nethogs-monitor -->
<!-- @name: nethogs-bandwidth -->
<!-- @category: Networking -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: networking, bandwidth, process, nethogs -->

```bash
sudo nethogs -v 3 eth0
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-v 3` | View mode: display transfer rates in Megabytes/sec (MB/s) |
| `eth0` | Network interface to monitor |
