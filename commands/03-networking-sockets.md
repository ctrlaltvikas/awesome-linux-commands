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


---

### 8. Pure Bash Remote TCP Port Reachability Check

Test if a remote host and TCP port is reachable and accepting connections using pure Bash with zero external dependencies (`nc`, `telnet`, or `nmap` not required).

<!-- @id: net-bash-tcp-check -->
<!-- @name: bash-tcp-test -->
<!-- @category: Networking -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: networking, bash, port-check, connectivity -->

```bash
timeout 2 bash -c '</dev/tcp/1.1.1.1/443' && echo "PORT OPEN" || echo "PORT CLOSED"
```

#### Why Run This
In minimal Alpine/container images where `telnet`, `nc`, and `curl` are missing, `/dev/tcp` allows instant connectivity checks directly inside Bash.

---

### 9. Query Remote TLS / SSL Certificate Expiration Dates

Extract the exact activation and expiry dates of a remote HTTPS certificate directly from the command line without opening a browser.

<!-- @id: net-openssl-cert-expiry -->
<!-- @name: openssl-cert-dates -->
<!-- @category: Networking -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: networking, tls, ssl, certificates, openssl -->

```bash
echo | openssl s_client -connect github.com:443 -servername github.com 2>/dev/null | openssl x509 -noout -dates
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-connect host:443` | Target endpoint and port |
| `-servername host` | Send SNI (Server Name Indication) header for virtual-hosted domains |
| `-noout -dates` | Suppress certificate body output and print strictly `notBefore` and `notAfter` timestamps |

---

### 10. Real-Time DNS Query Packet Sniffer

Capture outbound and inbound DNS lookup queries on port 53 to diagnose unresolved domain lookups or misconfigured DNS servers.

<!-- @id: net-tcpdump-dns -->
<!-- @name: tcpdump-dns-sniffer -->
<!-- @category: Networking -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: networking, dns, packet-capture, tcpdump -->

```bash
sudo tcpdump -nn -i any -c 20 udp port 53
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-nn` | Suppress domain and port name resolution for zero-delay output |
| `-i any` | Listen across all active interfaces |
| `-c 20` | Exit automatically after capturing 20 queries |
| `udp port 53` | Filter specifically for DNS traffic |

---

### 11. Instant Zero-Config HTTP Static File Server

Serve the current working directory over local HTTP for rapid file sharing or local web development.

<!-- @id: net-python-http-server -->
<!-- @name: python-http-server -->
<!-- @category: Networking -->
<!-- @risk: Mutating -->
<!-- @privilege: Normal -->
<!-- @tags: networking, http, python, web-server -->

```bash
python3 -m http.server 8080 --bind 127.0.0.1
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-m http.server` | Invoke Python's built-in HTTP server module |
| `8080` | Port to bind to |
| `--bind 127.0.0.1` | Restrict listening strictly to localhost for security |

---

### 12. Flush Local DNS Resolver Cache

Force local `systemd-resolved` to purge cached DNS entries and immediately re-query authoritative nameservers.

<!-- @id: net-flush-dns-cache -->
<!-- @name: resolvectl-flush-cache -->
<!-- @category: Networking -->
<!-- @risk: Mutating -->
<!-- @privilege: Sudo -->
<!-- @tags: networking, dns, cache, systemd-resolved -->

```bash
sudo resolvectl flush-caches
```

#### Verification
```bash
resolvectl statistics
```

---

### 13. Query Public IPv4 Address with Zero HTML Bloat

Retrieve your public-facing WAN IP address cleanly for automation scripts or CLI inspection.

<!-- @id: net-curl-public-ip -->
<!-- @name: curl-public-ip -->
<!-- @category: Networking -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: networking, ip, curl, public-ip -->

```bash
curl -s4 https://ifconfig.me
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-s` | Silent mode: suppresses progress bar |
| `-4` | Force IPv4 connection |
