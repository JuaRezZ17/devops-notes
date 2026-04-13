# 1. Define a list of dictionaries representing five servers with different attributes (name, IP address, environment: “prod” or “dev”, uptime).
servers = [
    {"name": "Server_01", "ip": "192.168.1.10", "env": "prod", "uptime": 150},
    {"name": "Server_02", "ip": "10.0.0.5", "env": "dev", "uptime": 12},
    {"name": "Server_03", "ip": "192.168.1.20", "env": "prod", "uptime": 200},
    {"name": "Server_04", "ip": "10.0.0.15", "env": "dev", "uptime": 300},
    {"name": "Server_05", "ip": "192.168.1.30", "env": "prod", "uptime": 45}
]

# 2. Use a Set to uniquely identify which environments you have.
environments = set(s['env'] for s in servers)

# 3. Use a list comprehension to generate a new list containing only the IP addresses of the “prod” servers whose uptime is greater than 100 days.
critical_reports = [
    f"[{s['env'].upper()}] {s['ip']} - CRITICAL UPTIME"
    for s in servers 
    if s['env'] == 'prod' and s['uptime'] > 100
]

# 4. Output: Prints a formatted report of the following type: [PROD] 192.168.1.10 - CRITICAL UPTIME.
print("-" * 50)
print(f"Detected environments: {', '.join(environments)}")
print("-" * 50)

if critical_reports:
    print("CRITICAL SERVERS REQUIRING RESTART:")
    for report in critical_reports:
        print(report)
else:
    print("No critical servers detected.")

print("-" * 50)