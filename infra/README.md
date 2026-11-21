# Vagrant: 5 VM Environment

This Vagrantfile creates 5 vm with one command (`vagrant up`).
All VMs are in one shared private network, and you can connect to each of them over SSH.

| VM       | Role                       | IP            | RAM  | CPU |
| -------- | -------------------------- | ------------- | ---- | --- |
| `lb`     | Load balancer              | 192.168.56.10 | 1 GB | 1   |
| `db`     | Database                   | 192.168.56.11 | 2 GB | 2   |
| `consul` | Service discovery (Consul) | 192.168.56.12 | 1 GB | 1   |
| `app1`   | Application server #1      | 192.168.56.13 | 2 GB | 2   |
| `app2`   | Application server #2      | 192.168.56.14 | 2 GB | 2   |



- OS: **Ubuntu 24.04 LTS** (`bento/ubuntu-24.04`)
- Network: private (host-only) network `192.168.56.0/24`
- On every VM, the provisioning script:
  - creates the user `admin` with an SSH key and `sudo` without a password
  - turns off password login over SSH
  - turns off SSH login for `root`

---

## 1. Requirements

### Software

| Tool           | Version      | Download                                        |
| -------------- | ------------ | ----------------------------------------------- |
| VirtualBox     | 7.0 or newer | https://www.virtualbox.org/wiki/Downloads       |
| Vagrant        | 2.4 or newer | https://developer.hashicorp.com/vagrant/install |
| OpenSSH client | any          | built in on Linux, macOS and Windows 10/11      |
| Git            | any          | https://git-scm.com/downloads                   |

Check that everything is installed:

```bash
vagrant --version
VBoxManage --version
ssh -V
```

### Hardware

- **RAM:** the VMs need **8 GB** together. The host should have **16 GB** or more.
  With less RAM, some VMs may not start. 
- **Disk:** about **20 GB** of free space.

---

## 2. Project structure

```
.
├── Vagrantfile              # VM list and settings
├── provision/
│   ├── users_set_up.sh      # creates the admin user, SSH hardening
│   ├── consul_set_up.sh     # installs and starts the Consul server (consul VM only)
│   └── consul/
│       └── consul.hcl       # Consul server config
├── keys/
│   ├── admin                # PRIVATE key  (never commit!)
│   └── admin.pub            # public key   (copied to all VMs)
├── .gitignore
└── README.md
```

 **The `keys/` folder is not in the repository. Every user creates their own keys> (step 3). Without `keys/admin.pub`, `vagrant up` stops with an error.**

---

## 3. Create SSH keys

You need one key pair:
- `keys/admin`: **private** key. It stays on your computer only.
- `keys/admin.pub`: **public** key. Vagrant copies it to every VM.

Run all commands from the **project root folder** (where the `Vagrantfile` is).
### Linux

```bash
mkdir -p keys
ssh-keygen -t ed25519 -f keys/admin -C "admin@vagrant" -N ""
chmod 700 keys
chmod 600 keys/admin
chmod 644 keys/admin.pub
```

### macOS

The same as Linux (open the **Terminal** app):

```bash
mkdir -p keys
ssh-keygen -t ed25519 -f keys/admin -C "admin@vagrant" -N ""
chmod 700 keys
chmod 600 keys/admin
chmod 644 keys/admin.pub
```

### Windows (PowerShell)

Windows 10/11 already has OpenSSH. Open **PowerShell** in the project folder:

```powershell
New-Item -ItemType Directory -Force -Path keys
ssh-keygen -t ed25519 -f keys\admin -C "admin@vagrant"
```

When it asks for a passphrase, press Enter two times (empty passphrase).

Then give access to the private key only to your user.

---

## 3a. Create secrets (database password, app secret key, S3 keys)

**Linux / macOS:**

```bash
mkdir -p secrets
openssl rand -hex 24 > secrets/db_password
openssl rand -hex 32 > secrets/secret_key
openssl rand -hex 16 > secrets/s3_access_key
openssl rand -hex 32 > secrets/s3_secret_key
chmod 700 secrets
chmod 600 secrets/*
```

**Windows (PowerShell):**

```powershell
New-Item -ItemType Directory -Force -Path secrets | Out-Null
function New-HexSecret($bytes) {
    $b = New-Object byte[] $bytes
    [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($b)
    ($b | ForEach-Object { $_.ToString("x2") }) -join ""
}
New-HexSecret 24 | Set-Content -NoNewline secrets\db_password
New-HexSecret 32 | Set-Content -NoNewline secrets\secret_key
New-HexSecret 16 | Set-Content -NoNewline secrets\s3_access_key
New-HexSecret 32 | Set-Content -NoNewline secrets\s3_secret_key
```

---

## 4. Do not commit the private key

Make sure `.gitignore` has these lines:

```gitignore
# SSH keys: every user creates their own
keys/

# Secrets: every user creates their own
secrets/

# Vagrant local state
.vagrant/
```

---

## 5. Commands

All commands run from the project root folder.

### Main commands

| Command                         | What it does                                                                              |
| ------------------------------- | ----------------------------------------------------------------------------------------- |
| `vagrant up`                    | Create and start **all** 5 VMs (the first run downloads the box, this can take some time) |
| `vagrant up app1`               | Start only one VM                                                                         |
| `vagrant status`                | Show the state of all VMs (`running`, `poweroff`, `not created`)                          |
| `vagrant ssh lb`                | Connect to a VM as the `vagrant` user                                                     |
| `vagrant halt`                  | Stop all VMs (data stays)                                                                 |
| `vagrant halt db`               | Stop one VM                                                                               |
| `vagrant reload`                | Restart VMs and apply Vagrantfile changes                                                 |
| `vagrant destroy -f`            | **Delete** all VMs (all data inside VMs is lost)                                          |
| `vagrant destroy -f app2`       | Delete one VM                                                                             |


### First start

```bash
vagrant up
vagrant status
```

Expected result:

```
lb                        running (virtualbox)
app1                      running (virtualbox)
app2                      running (virtualbox)
db                        running (virtualbox)
consul                    running (virtualbox)
```

---

## 6. Connect over SSH

There are two ways to connect.

### Option A: as the `vagrant` user (easy, for debugging)

```bash
vagrant ssh lb
vagrant ssh db
```

Vagrant uses its own key, so you don't need the `keys/` folder for this.

### Option B: as the `admin` user (main way)

Use the private key from `keys/` and the VM IP address.

**Linux / macOS:**

```bash
ssh -i keys/admin admin@192.168.56.10    # lb
ssh -i keys/admin admin@192.168.56.11    # db
ssh -i keys/admin admin@192.168.56.12    # consul
ssh -i keys/admin admin@192.168.56.13    # app1
ssh -i keys/admin admin@192.168.56.14    # app2
```

**Windows (PowerShell):**

```powershell
ssh -i keys\admin admin@192.168.56.10
```

---

## 7. Consul

The `consul` VM runs a **single Consul server** (service discovery) with the web UI.
For now, Consul runs standalone: the other VMs are not connected to it yet.

Consul is installed automatically by `provision/consul_set_up.sh` when the VM is created.

### Start and check

```bash
vagrant up consul
vagrant ssh consul
systemctl status consul    # should be "active (running)"
consul members             # 1 node, status "alive", type "server"
```

### Web UI

Open in the browser: http://192.168.56.12:8500

### Apply config changes

After you change `provision/consul/consul.hcl`, run:

```bash
vagrant provision consul --provision-with consul
```

## 8. Scaling app VMs

`APP_COUNT` in the `Vagrantfile` sets the number of app VMs (`app1..appN`, IPs `192.168.56.13`, `.14`, …).
All app IPs are added to the DB access rules and to the LB config.

If the infrastructure is already running, `vagrant up` does not update `db` and `lb`.
After you change `APP_COUNT`, re-provision them manually:

```bash
vagrant up                                  
vagrant provision db --provision-with db     
vagrant provision lb --provision-with lb     
```

## 9. Firewall(ufw)

Every VM runs `ufw` with **default deny incoming** and allow outgoing.
Rules are applied automatically on every `vagrant up` by `provision/firewall_set_up.sh`.

| VM       | Open port                                    | Allowed from                    |
| -------- | -------------------------------------------- | -------------                   |
|  all     | 22/tcp(ssh)                                  | anywhere                        |
| `lb`     | 80/tcp                                       | anywhere                        |
| `db`     | 5432/tcp(postgres), 833/tcp(seaweedfs s3)    | app VMs only                    |
| `consul` | 8500, 8600, 8300, 8301                       | private network 192.168.56.0/24 |
| `app1`   | 800/tcp                                      | lb only(192.168.56.10)          |
| `app2`   | 800/tcp                                      | lb only(192.168.56.10)          |

Re-apply rules without recreating VMs:

    vagrant provision --provision-with firewall

Check rules on a VM:

    vagrant ssh db -c "sudo ufw status verbose"

Blocked ports are dropped silently, so `nc` shows `timed out` instead of `refused`.