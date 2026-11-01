# 🖥️ Hardware, CPU Topology & Thermals

Inspect physical server hardware, CPU core topology, NUMA configurations, RAM hardware specs, PCI bus trees, and live thermal throttling.

---

### 1. Map CPU Cores, Sockets, NUMA Nodes & Cache Hierarchy

Print an extended table mapping every logical thread to its physical CPU socket, core ID, NUMA node, and L1/L2/L3 cache allocations.

<!-- @id: hw-lscpu-extended -->
<!-- @name: lscpu-topology -->
<!-- @category: Hardware & Thermals -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: hardware, cpu, numa, topology, lscpu -->

```bash
lscpu -e=CPU,CORE,SOCKET,NODE,L1d,L1i,L2,L3
```

#### Why Run This
Critical when tuning thread affinity (`taskset`) on dual-socket AMD EPYC or Intel Xeon servers to prevent cross-NUMA latency and cache thrashing.

---

### 2. Audit Physical RAM Stick Hardware Without Rebooting

Inspect motherboard DIMM slots, installed memory capacity, speeds (MT/s), DDR type, and manufacturer without physical access to the chassis.

<!-- @id: hw-dmidecode-ram -->
<!-- @name: dmidecode-memory -->
<!-- @category: Hardware & Thermals -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: hardware, memory, ram, dmidecode, ddr -->

```bash
sudo dmidecode -t memory | grep -E 'Size|Speed|Type:|Manufacturer|Locator' | grep -v 'No Module Installed'
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-t memory` | Query DMI/SMBIOS memory controller and memory device tables |
| `grep -v ...` | Filter out unoccupied empty DIMM slots |

---

### 3. Hardware PCI Bus Topology Tree with Kernel Drivers

Display the complete PCI Express bus tree showing bridge hierarchies and the active Linux kernel driver module managing each device.

<!-- @id: hw-lspci-tree -->
<!-- @name: lspci-bus-tree -->
<!-- @category: Hardware & Thermals -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: hardware, pci, lspci, drivers -->

```bash
lspci -tv -k
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-t` | Tree view: renders PCI bridges, endpoints, and switch controllers as an ASCII tree |
| `-v` | Verbose mode |
| `-k` | Show kernel driver in use and kernel modules claiming each device |

---

### 4. USB Bus & Device Tree with Negotiated Transfer Speeds

Inspect all USB host controllers, hubs, connected peripherals, and their active negotiated bitrates (e.g. `480M`, `5000M`, `10000M`).

<!-- @id: hw-lsusb-tree -->
<!-- @name: lsusb-bus-tree -->
<!-- @category: Hardware & Thermals -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: hardware, usb, lsusb, peripherals -->

```bash
lsusb -tv
```

#### Why Run This
Verify whether a high-speed USB 3.2 NVMe enclosure or capture card accidentally negotiated down to USB 2.0 (480M) speeds due to a bad cable.

---

### 5. Monitor Live CPU Core Temperatures & Fan Speeds

Check CPU die package temperatures, per-core thermal limits, and cooling fan RPM via kernel sensor drivers (`lm-sensors`).

<!-- @id: hw-sensors-temps -->
<!-- @name: sensors-temperatures -->
<!-- @category: Hardware & Thermals -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: hardware, thermal, cpu, temperature, fan -->

```bash
sensors
```

#### Key Fields to Watch
* `Package id 0`: Overall CPU package temperature.
* `crit`: Temperature threshold where CPU triggers hardware thermal throttling.
* `fan1`: Fan rotation speed in RPM.

---

### 6. Real-Time CPU Power Consumption & Package Wattage (`turbostat`)

Measure actual CPU electrical power draw (Watts), core package temperatures, and hardware frequency transitions.

<!-- @id: hw-turbostat-power -->
<!-- @name: turbostat-power-metrics -->
<!-- @category: Hardware & Thermals -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: hardware, cpu, power, wattage, turbostat -->

```bash
sudo turbostat --quiet --interval 2 --show PkgWatt,CoreTmp,Avg_MHz
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `--quiet` | Suppress initial hardware configuration dump |
| `--interval 2` | Sample hardware counters every 2 seconds |
| `--show ...` | Display only Package Wattage (`PkgWatt`), Core Temp (`CoreTmp`), and Average Frequency (`Avg_MHz`) |

---

### 7. Audit Motherboard BIOS / UEFI Firmware Details

Retrieve system motherboard vendor, BIOS/UEFI version string, and firmware release date without accessing the BIOS setup menu.

<!-- @id: hw-dmidecode-bios -->
<!-- @name: dmidecode-bios-version -->
<!-- @category: Hardware & Thermals -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: hardware, bios, uefi, firmware, dmidecode -->

```bash
sudo dmidecode -t bios | grep -E 'Vendor|Version|Release Date'
```
