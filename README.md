# NetSage

**NetSage** is a smart and lightweight tool designed for network administrators, cybersecurity professionals, IT technicians, and anyone who needs to perform fast and accurate network diagnostics.  
It helps **save precious time** by automating port scanning and service checking tasks, making your network management and troubleshooting more efficient.

---

## 🚀 Why Use NetSage?

- **Save Time:** Automated port and service scanning in one go.
- **Flexible:** Easily modify port lists according to your network environment.
- **Reliable:** Built for quick detection of open ports, active services, and potential security weaknesses.
- **Practical:** Perfect for network audits, cybersecurity checks, troubleshooting downtime, and IT maintenance.

Whether you are maintaining a corporate infrastructure, auditing your own systems, or working in cybersecurity, **NetSage** can make your job faster and easier.

---

## ⚙️ How It Works

1. **Add Your Target IPs or Hosts:** Customize the script to target the machines you want to scan.
2. **Configure the Ports List:**  
   You can easily modify the list of ports you want to scan, depending on your needs (e.g., SSH, HTTP, FTP, custom services).
3. **Run the Tool:**  
   Launch the script and let NetSage perform the scan and display results clearly.

---

## ⚙️ Customization
### Changing Ports to Scan
By default, the script scans common ports like `80 (HTTP)`, `443 (HTTPS)`, `22 (SSH)`, `21 (FTP)`, and `3389 (RDP)`.

To **add** or **modify** the list of ports:

- Find this function inside the code:
     ```python
     def port_scan(host, ports=[80, 443, 22, 21, 3389]):
- Add more ports into the ports list. (Example — adding SMTP (25) and MySQL (3306)) :
     ```python
     def port_scan(host, ports=[80, 443, 22, 21, 3389, 25, 3306]):

## 🖥 Requirements
- Python 3.7+
- Internet connection (for external tests like speed test)
### Install dependencies:
```bash
pip install -r requirements.txt

## 🏆 Attribution
Created and maintained by **MrMazine**.

## 📢 Final Note
This tool was built to help IT and cybersecurity professionals save time and energy, allowing you to focus on fixing network issues instead of searching for them.

Contributions, suggestions, and improvements are always welcome!
