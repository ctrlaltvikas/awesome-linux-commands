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


---

### 5. Make Critical Configuration Files Immutable Against Root Deletion

Prevent accidental modification or deletion of vital system files (like `/etc/resolv.conf` or `/etc/passwd`) by setting the filesystem immutable flag. Even `root` running `rm -rf` cannot delete or overwrite it.

<!-- @id: sec-chattr-immutable -->
<!-- @name: chattr-immutable -->
<!-- @category: Security -->
<!-- @risk: Mutating -->
<!-- @privilege: Sudo -->
<!-- @tags: security, permissions, chattr, hardening -->

```bash
sudo chattr +i /etc/resolv.conf
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `+i` | Set immutable attribute: file cannot be modified, overwritten, truncated, renamed, or unlinked |

#### To Remove Immutability Later:
```bash
sudo chattr -i /etc/resolv.conf
```

---

### 6. Inspect Extended Filesystem Attributes (`lsattr`)

Check which files have special kernel filesystem flags set (e.g., `i` immutable, `a` append-only).

<!-- @id: sec-lsattr-check -->
<!-- @name: lsattr-inspect -->
<!-- @category: Security -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: security, permissions, lsattr, audit -->

```bash
lsattr /etc/passwd /etc/shadow /etc/resolv.conf
```

---

### 7. Audit Orphaned Files Belonging to Deleted Users/Groups

Locate files whose UID or GID no longer exists in `/etc/passwd` or `/etc/group` (security risk if a new user is assigned that UID).

<!-- @id: sec-find-nouser -->
<!-- @name: find-orphaned-files -->
<!-- @category: Security -->
<!-- @risk: Safe -->
<!-- @privilege: Sudo -->
<!-- @tags: security, permissions, audit, users -->

```bash
sudo find / -xdev \( -nouser -o -nogroup \) -exec ls -ld {} + 2>/dev/null
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-nouser` | File owner UID has no corresponding entry in `/etc/passwd` |
| `-nogroup` | File group GID has no corresponding entry in `/etc/group` |
| `-xdev` | Restrict audit to current mounted filesystem |

---

### 8. Emergency User Account Lockout & Active Session Termination

Instantly lock a compromised user's password and terminate all of their running processes and interactive SSH shells.

<!-- @id: sec-lock-user-session -->
<!-- @name: lock-user-account -->
<!-- @category: Security -->
<!-- @risk: Mutating -->
<!-- @privilege: Sudo -->
<!-- @tags: security, auth, incident-response, users -->

```bash
sudo passwd -l compromised_user && sudo pkill -9 -u compromised_user
```

#### Flag Breakdown
| Command / Flag | Description |
| :--- | :--- |
| `passwd -l` | Lock user password hash in `/etc/shadow` (prepends `!` to hash) |
| `pkill -9 -u` | Immediately send `SIGKILL` to all processes owned by the specified user |

---

### 9. Real-Time Inspection of Logged-In Users & Commands (`w`)

View who is currently logged into the system, their originating IP address, idle duration, and the command their terminal is currently executing.

<!-- @id: sec-w-users -->
<!-- @name: w-active-users -->
<!-- @category: Security -->
<!-- @risk: Safe -->
<!-- @privilege: Normal -->
<!-- @tags: security, users, sessions, w -->

```bash
w -f
```

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-f` | Toggle display of the remote "From" column (displays originating client IP or hostname) |
