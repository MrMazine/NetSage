
# ⚡NetSage

Fast and reliable network diagnostics for IT, cybersecurity, and system administrators. Simplify troubleshooting, monitoring, and save precious time.

## ✨ Why Use NetSage?

NetSage is an all-in-one network diagnostics tool designed to make your daily IT, network administration, and cybersecurity tasks easier, faster, and more efficient.

- **Save Precious Time:** Quickly gather key network information without manually typing multiple commands.
- **Powerful Diagnostics:** Includes ping tests, traceroutes, port scans, ARP table checks, network statistics, internet speed tests, DNS checks, and much more.
- **Cross-Platform:** Works on both Windows and Linux (macOS partially supported).
- **Highly Customizable:** Easily adjust scanning settings, like adding new ports to the scan list, or targeting specific DNS servers.
- **Professional Results:** Outputs are organized and clear, making it easier to troubleshoot or create reports.

NetSage is ideal for:
- Network Administrators
- Cybersecurity Professionals
- System Administrators
- IT Support Technicians
- Penetration Testers

Instead of switching between dozens of tools or writing custom scripts each time — NetSage puts **everything in one place** to help you **win time**.

## ⚙️ How to Use

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MrMazine/NetSage.git
   cd NetSage
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the script:**
   ```bash
   python3 netsage.py
   ```

## 🔧 Customizing Parameters

- **Ports to Scan:**  
  Modify the `ports` list inside the `port_scan()` function:
  ```python
  def port_scan(host, ports=[80, 443, 22, 21, 3389, 8080, 8443, 53, 25]):
  ```
  ➔ Add any other ports you want inside the list!

- **Gateway IP Address:**  
  Default: `192.168.1.1`  
  You can input another IP manually when prompted.

- **Testing Hosts:**  
  Default hosts are `google.com` and `8.8.8.8`.  
  Change `test_host` or `dns_server` variables in the code if needed.

## 📦 Requirements

Python 3.7+ is required.

Install required packages:
```bash
pip install -r requirements.txt
```

Contents of **requirements.txt**:
```
pandas
ping3
psutil
speedtest-cli
```

## 📜 Features

- Local IP Detection
- Ping Test to Gateway, DNS, and External Host
- DNS Resolution Check
- Traceroute
- Open Ports Scanner
- Internet Speed Test (Download / Upload / Ping)
- Wi-Fi Signal Strength Checker
- Network Interface Statistics
- Network Path Analysis (MTR if available)
- DHCP Lease Info
- ARP Table
- Active Network Connections Viewer
- DNS Server Benchmarking
- Bandwidth Monitoring

All presented in a clear, interactive, and colorful terminal output.

## 🛡️ Permissions Notice

Some features (like Wi-Fi signal or DHCP leases) may require **administrative rights** (sudo on Linux, Run as Admin on Windows).

## ✍️ Attribution

Created and maintained by [MrMazine](https://github.com/MrMazine) 🚀

## 📚 Sources

- [Python Official Documentation](https://docs.python.org/3/)
- [ping3 PyPI Project](https://pypi.org/project/ping3/)
- [psutil Documentation](https://psutil.readthedocs.io/)
- [speedtest-cli PyPI Project](https://pypi.org/project/speedtest-cli/)
- [Stack Overflow](https://stackoverflow.com/)
- [MTR Documentation](https://github.com/traviscross/mtr)
