#!/usr/bin/env python3
"""
Network Diagnostic Tool by MrMazine
GitHub: https://github.com/MrMazine
"""

import os
import platform
import subprocess
import socket
import time
import datetime
import pandas as pd
from ping3 import ping
import psutil
import speedtest


# Color codes for terminal output - these may not work on all terminals - you can add more colors if needed
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clear the terminal screen based on the OS"""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def print_header(text):
    """Print colored header text"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.END}\n")

def print_section(text):
    """Print colored section text"""
    print(f"{Colors.BLUE}{Colors.BOLD}» {text}{Colors.END}")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    """Print informational message"""
    print(f"{Colors.CYAN}• {text}{Colors.END}")

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except OSError:  # Catching specific OS-related errors
        return "Unknown"

def ping_host(host, count=4):
    """Ping a host and return statistics"""
    try:
        if platform.system() == "Windows":
            cmd = f"ping -n {count} {host}"
        else:
            cmd = f"ping -c {count} {host}"           
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"{Colors.RED}Ping failed: {e}{Colors.END}"

def measure_latency(host, samples=5):
    """Measure average latency to a host"""
    delays = []
    for _ in range(samples):
        delay = ping(host, unit='ms')
        if delay is not None:
            delays.append(delay)
        time.sleep(0.5)
    
    if delays:
        avg = sum(delays) / len(delays)
        return {
            "Target": host,
            "Samples": len(delays),
            "Average (ms)": round(avg, 2),
            "Minimum (ms)": round(min(delays), 2),
            "Maximum (ms)": round(max(delays), 2),
            "Packet Loss": f"{round((samples - len(delays))/samples*100, 1)}%"
        }
    return {"Error": f"Could not measure latency to {host}"}

def trace_route(host):
    """Perform a traceroute to a host"""
    try:
        if platform.system() == "Windows":
            cmd = f"tracert {host}"
        else:
            cmd = f"traceroute {host}"
            
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
        return result.stdout
    except subprocess.SubprocessError as e:
        return f"{Colors.RED}Traceroute failed: {e}{Colors.END}"

def path_analysis(target="8.8.8.8"):
    """Analyze network path with mtr (if available)"""
    try:
        if platform.system() == "Windows":
            return f"{Colors.YELLOW}Install WinMTR for Windows path analysis{Colors.END}"
        
        cmd = f"mtr --report --report-cycles 5 {target}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
        return result.stdout if result.stdout else f"{Colors.YELLOW}Install mtr for path analysis (apt install mtr){Colors.END}"
    except subprocess.SubprocessError as e:
        return f"{Colors.RED}Path analysis failed: {e}{Colors.END}"

def check_dns_lookup(host="google.com"):
    """Check DNS resolution"""
    try:
        ip_address = socket.gethostbyname(host)
        return f"{Colors.GREEN}DNS resolution for {host}: {ip_address}{Colors.END}"
    except socket.gaierror:
        return f"{Colors.RED}DNS lookup failed for {host}{Colors.END}"

def dns_benchmark(servers=["8.8.8.8", "1.1.1.1", "9.9.9.9"]):
    """Benchmark different DNS servers"""
    results = []
    for server in servers:
        start = time.time()
        try:
            socket.gethostbyname_ex("example.com", None, server)
            latency = (time.time() - start) * 1000  # ms
            results.append({"DNS Server": server, "Latency (ms)": round(latency, 2)})
        except socket.gaierror:
            results.append({"DNS Server": server, "Latency (ms)": "Timeout"})    
    return pd.DataFrame(results)

def port_scan(host, ports=[80, 443, 22, 21, 3389]):
    """Check if common ports are open"""
    results = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            results.append(f"{Colors.GREEN}Port {port} is OPEN{Colors.END}")
        else:
            results.append(f"{Colors.YELLOW}Port {port} is CLOSED or filtered{Colors.END}")
        sock.close()
    return results

def get_network_stats():
    """Get network interface statistics"""
    stats = []
    interfaces = psutil.net_io_counters(pernic=True)
    
    for interface, data in interfaces.items():
        stats.append({
            "Interface": interface,
            "Bytes Sent": data.bytes_sent,
            "Bytes Received": data.bytes_recv,
            "Packets Sent": data.packets_sent,
            "Packets Received": data.packets_recv,
            "Errors In": data.errin,
            "Errors Out": data.errout,
            "Drops In": data.dropin,
            "Drops Out": data.dropout
        })
    return pd.DataFrame(stats)

def monitor_bandwidth(duration=10):
    """Monitor bandwidth usage over time"""
    start_time = time.time()
    initial_stats = psutil.net_io_counters()
    
    print_info(f"Monitoring network usage for {duration} seconds...")
    print_info("Press Ctrl+C to stop early\n")
    
    try:
        while time.time() - start_time < duration:
            time.sleep(1)
            current_stats = psutil.net_io_counters()
            
            sent = (current_stats.bytes_sent - initial_stats.bytes_sent) / 1024
            recv = (current_stats.bytes_recv - initial_stats.bytes_recv) / 1024
            
            print(f"  {Colors.CYAN}Upload: {sent:.2f} KB/s | Download: {recv:.2f} KB/s{Colors.END}", end='\r')
            initial_stats = current_stats
    except KeyboardInterrupt:
        pass
    
    print_success("\nBandwidth monitoring complete.")

def get_wifi_signal():
    """Get Wi-Fi signal strength"""
    try:
        if platform.system() == "Windows":
            cmd = "netsh wlan show interfaces"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            for line in result.stdout.split('\n'):
                if "Signal" in line:
                    return line.strip()
        else:  # Linux
            cmd = "iwconfig 2>/dev/null | grep -i quality"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
            if result.stdout:
                return result.stdout.strip()
            return f"{Colors.YELLOW}Run with 'sudo' for Wi-Fi signal info{Colors.END}"
        
        return f"{Colors.YELLOW}Signal strength information not available{Colors.END}"
    except (subprocess.SubprocessError, OSError) as e:
        return f"{Colors.RED}Error getting signal strength: {e}{Colors.END}"
    
_a = ['h', 't', 't', 'p', 's', ':', '/', '/']
_b = ['g', 'i', 't', 'h', 'u', 'b', '.', 'c', 'o', 'm', '/']

def check_dhcp_lease():
    """Check DHCP lease information"""
    try:
        if platform.system() == "Windows":
            cmd = "ipconfig /all"
        else:
            cmd = "cat /var/lib/dhcp/dhclient.leases 2>/dev/null || echo 'DHCP lease file not found'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
        return result.stdout
    except (subprocess.SubprocessError, OSError) as e:
        return f"{Colors.RED}DHCP lease check failed: {e}{Colors.END}"

def _generate_attribution():
    parts = [''.join(_a), ''.join(_b), ''.join(_c)]
    return ''.join(parts)
_c = ['M', 'r', 'M', 'a', 'z', 'i', 'n', 'e']

def get_adapter_info():
    """Get detailed network adapter information"""
    adapters = []
    for name, addrs in psutil.net_if_addrs().items():
        adapter = {"Interface": name}
        for addr in addrs:
            if addr.family == socket.AF_INET:
                adapter["IPv4"] = addr.address
                adapter["Netmask"] = addr.netmask
            elif addr.family == socket.AF_INET6:
                adapter["IPv6"] = addr.address
            elif addr.family == psutil.AF_LINK:
                adapter["MAC"] = addr.address
        adapters.append(adapter)
    
    return pd.DataFrame(adapters)

def speed_test():
    """Perform an internet speed test"""
    try:
        print_info("Running speed test... This may take a moment")
        st = speedtest.Speedtest()
        st.get_best_server()
        
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        ping_result = st.results.ping
        
        return {
            "Download Speed (Mbps)": round(download_speed, 2),
            "Upload Speed (Mbps)": round(upload_speed, 2),
            "Ping (ms)": round(ping_result, 2),
            "Server": st.results.server['host']
        }
    except (subprocess.SubprocessError, OSError) as e:
        return {"Error": f"{Colors.RED}Speed test failed: {str(e)}{Colors.END}"}

def check_arp_table():
    """Check the ARP table"""
    try:
        if platform.system() == "Windows":
            cmd = "arp -a"
        else:
            cmd = "arp -n"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except (subprocess.SubprocessError, OSError) as e:
        return f"{Colors.RED}ARP table check failed: {e}{Colors.END}"

def check_network_connections():
    """Check active network connections"""
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED':
            connections.append({
                "Local Address": f"{conn.laddr.ip}:{conn.laddr.port}",
                "Remote Address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                "Status": conn.status,
                "PID": conn.pid
            })
    return pd.DataFrame(connections)

def main():
    clear_screen()
    print(f"{Colors.HEADER}{Colors.BOLD}=== Network Diagnostic Tool ==={Colors.END}")
    print(f"{Colors.CYAN}Created by {''.join(_c)} - {_generate_attribution()}{Colors.END}")
    print(f"Running on: {Colors.YELLOW}{platform.system()} {platform.release()}{Colors.END}")
    print(f"Local IP Address: {Colors.GREEN}{get_local_ip()}{Colors.END}")
    print(f"Current Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python Version: {Colors.YELLOW}{platform.python_version()}{Colors.END}\n")
    
    # Test targets
    gateway = input(f"{Colors.BLUE}Enter your gateway IP [192.168.1.1]: {Colors.END}").strip() or "192.168.1.1"
    dns_server = "8.8.8.8"  # Google DNS
    test_host = "google.com" 
    # Run diagnostics
    print_header("Basic Connectivity Tests")

    print_section(f"Pinging gateway ({gateway})")
    print(ping_host(gateway))
    
    print_section(f"Pinging DNS server ({dns_server})")
    print(ping_host(dns_server))
    
    print_section(f"Pinging external host ({test_host})")
    print(ping_host(test_host))
    
    print_header("DNS Check")
    print(check_dns_lookup(test_host))
    
    print_header("Traceroute to External Host")
    print(trace_route(test_host))
    
    print_header("Port Availability")
    for result in port_scan(test_host):
        print(result)
    
    print_header("Network Interface Statistics")
    print(get_network_stats().to_string(index=False))
    
    print_header("ARP Table")
    print(check_arp_table())
    
    print_header("Active Network Connections")
    conns = check_network_connections()
    if not conns.empty:
        print(conns.to_string(index=False))
    else:
        print_info("No established connections found")
    
    print_header("Internet Speed Test")
    speed_results = speed_test()
    for k, v in speed_results.items():
        print(f"{k}: {v}")
    
    # New functions execution
    print_header("Advanced Diagnostics")
    
    print_section("Network Latency Analysis")
    latency_results = measure_latency(test_host)
    for k, v in latency_results.items():
        print(f"{k}: {v}")
    
    print_section("Bandwidth Monitoring")
    monitor_bandwidth()
    
    print_section("Wi-Fi Signal Strength")
    print(get_wifi_signal())
    
    print_section("Network Path Analysis")
    print("Note: This requires mtr installed on Linux/Mac")
    print(path_analysis())
    
    print_section("DHCP Lease Information")
    print(check_dhcp_lease())
    
    print_section("Network Adapter Details")
    print(get_adapter_info().to_string(index=False))
    
    print_section("DNS Server Benchmark")
    print(dns_benchmark().to_string(index=False))
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}Diagnostic complete. All tests executed successfully.{Colors.END}")
    print(f"{Colors.YELLOW}Created by {''.join(_c)} - {_generate_attribution()}{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Script interrupted by user.{Colors.END}")
        exit(0)
    except SystemExit:
        print(f"\n{Colors.RED}Script interrupted by user or system exit.{Colors.END}")
        exit(0)
    except (OSError, subprocess.SubprocessError, ValueError) as e:
        print(f"\n{Colors.RED}An error occurred: {e}{Colors.END}")
        exit(1)
