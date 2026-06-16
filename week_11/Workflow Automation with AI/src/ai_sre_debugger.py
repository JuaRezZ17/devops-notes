import os
import argparse
import subprocess
from openai import OpenAI


def run_command(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return result.stderr.strip()

    return result.stdout.strip()


def collect_pod_error(namespace, pod_name):
    current_logs = run_command([
        "kubectl", "logs", pod_name,
        "-n", namespace,
        "--tail=100"
    ])

    previous_logs = run_command([
        "kubectl", "logs", pod_name,
        "-n", namespace,
        "--previous",
        "--tail=100"
    ])

    pod_description = run_command([
        "kubectl", "describe", "pod", pod_name,
        "-n", namespace
    ])

    error_block = f"""
POD NAME:
{pod_name}

NAMESPACE:
{namespace}

CURRENT LOGS:
{current_logs}

PREVIOUS LOGS:
{previous_logs}

POD DESCRIPTION:
{pod_description}
"""

    return error_block


def ask_llm(error_block):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    system_prompt = """
You are a Senior SRE Engineer expert in Linux Internals, Kubernetes and container debugging.
Your task is to analyze Kubernetes pod failures and return exactly 3 concrete steps to fix the container crash.
Be direct, practical and specific.
"""

    user_prompt = f"""
Analyze this Kubernetes CrashLoopBackOff or container crash evidence.

Return exactly 3 steps.
Each step must include:
- What to check
- Why it matters
- The exact command or action to perform

Error evidence:
{error_block}
"""

    response = client.responses.create(
        model="gpt-5.5",
        instructions=system_prompt,
        input=user_prompt
    )

    return response.output_text


def main():
    parser = argparse.ArgumentParser(
        description="AI SRE Debugger for Kubernetes crashing pods"
    )

    parser.add_argument(
        "--namespace",
        required=True,
        help="Kubernetes namespace where the pod is running"
    )

    parser.add_argument(
        "--pod",
        required=True,
        help="Kubernetes pod name to debug"
    )

    args = parser.parse_args()

    error_block = collect_pod_error(args.namespace, args.pod)

    print("========== COLLECTED ERROR BLOCK ==========")
    print(error_block)

    print("========== AI SRE RECOMMENDATION ==========")
    recommendation = ask_llm(error_block)
    print(recommendation)


if __name__ == "__main__":
    main()