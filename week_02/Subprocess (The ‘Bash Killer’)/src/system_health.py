import subprocess
import sys

def check_system_health():
    print("--- System Health Report ---")

    # 1. Check disk space (df -h)
    try:
        df_result = subprocess.run(
            ["df", "-h"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        print("\n[DISC] Checking partitions (>80%):")
        lines = df_result.stdout.strip().split('\n')
        header = lines[0]
        
        found_issue = False
        for line in lines[1:]:
            parts = line.split()
            usage_str = parts[-2].replace('%', '')
            
            try:
                usage_int = int(usage_str)
                if usage_int > 80:
                    print(f"ALERT: {parts[0]} is at {usage_int}% (Mounted on {parts[-1]})")
                    found_issue = True
            except ValueError:
                continue
        
        if not found_issue:
            print("✅ All partitions are under the 80% threshold.")

    except subprocess.CalledProcessError as e:
        print(f"Error executing df: {e.stderr}", file=sys.stderr)

    # 2. Check Nginx (systemctl is-active)
    try:
        service = "nginx"
        status_result = subprocess.run(
            ["systemctl", "is-active", service],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"\n[SERVICE] {service}: {status_result.stdout.strip().upper()}")

    except subprocess.CalledProcessError as e:
        print(f"\n[SERVICE] Nginx: ERROR OR INACTIVE ❌")
        if e.stderr:
            print(f"Error details (stderr): {e.stderr}")
        else:
            print(f"Status reported: {e.output.strip()}")

if __name__ == "__main__":
    check_system_health()