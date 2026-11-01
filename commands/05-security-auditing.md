# 🛡️ Security, Auditing & Privilege Guards

Audit suspicious binary permissions, identify privilege escalation vectors, inspect listening attack surfaces, and track brute-force authentication attempts.

---

### 1. Audit SUID and SGID Executables

Detect binaries configured with SUID (`4000`) or SGID (`2000`) permissions that execute with elevated root or group privileges (prime targets for privilege escalation).

<!-- @id: sec-find-suid -->
<!-- @name: find-suid-binaries -->
<!-- @category: Security -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: security, suid, privilege-escalation, audit -->

```bash
sudo find / -perm /6000 -type f -exec ls -ld {} + 2>/dev/null
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-perm /6000` | Match files where either SUID bit (`4000`) or SGID bit (`2000`) is set |
| `-type f` | Search exclusively for executable files |
| `2>/dev/null` | Suppress permission-denied warnings from virtual filesystems |

---

### 2. Inspect Linux Kernel Capabilities on Binaries

Modern Linux splits root privilege into discrete capabilities (`CAP_NET_RAW`, `CAP_SYS_ADMIN`, `CAP_SETUID`). Audit which binaries hold elevated capabilities without full root SUID.

<!-- @id: sec-getcap-audit -->
<!-- @name: getcap-binaries -->
<!-- @category: Security -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: security, capabilities, linux-kernel, audit -->

```bash
sudo getcap -r /usr /bin /sbin /usr/local 2>/dev/null
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-r` | Recursively inspect subdirectories |
| `/usr /bin ...` | Search primary executable storage paths |

---

### 3. Track Failed SSH Brute-Force Login Attempts by IP

Aggregate failed SSH authentication attempts to identify active IP reconnaissance or brute-force dictionaries.

<!-- @id: sec-ssh-failed-logins -->
<!-- @name: ssh-failed-logins -->
<!-- @category: Security -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: security, ssh, brute-force, auth -->

```bash
sudo journalctl -u ssh -u sshd -n 2000 --no-pager | grep -i "Failed password" | awk '{for(i=1;i<=NF;i++) if($i=="from") print $(i+1)}' | sort | uniq -c | sort -nr | head -15
```

#### Flag Breakdown
| Element | Description |
| :--- | :--- |
| `-u ssh -u sshd` | Extract logs for both Debian/Ubuntu (`ssh`) and RHEL/Fedora (`sshd`) systemd units |
| `-n 2000` | Process the last 2,000 log lines |
| `awk ...` | Extracts the IP address token following the `from` keyword |
| `sort | uniq -c | sort -nr` | Counts and sorts attacking IPs by frequency in descending order |

---

### 4. Locate World-Writable Files Outside Safe Temporary Directories

Find sensitive configuration or script files accidentally marked world-writable (`chmod 777`), enabling non-privileged users to inject code.

<!-- @id: sec-world-writable -->
<!-- @name: find-world-writable -->
<!-- @category: Security -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: security, permissions, chmod, hardening -->

```bash
sudo find /etc /opt /var/www -type f -perm -0002 -ls
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-perm -0002` | Match files where the "others" write permission bit is enabled |
| `-ls` | Print detailed file mode, owner, group, and size |
