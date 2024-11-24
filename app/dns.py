import subprocess
import json
import os
from datetime import datetime
import uuid

def analyze_dns_health(domain: str):
    try:
        # Path to the compiled Go binary
        go_binary_path = os.path.join(os.getcwd(), "dnssec-analyzer", "cmd", "dnssec-analyzer", "dnssec-analyzer.exe")

        # Run the Go tool with the domain as an argument
        result = subprocess.run(
            [go_binary_path, domain],
            capture_output=True, text=True
        )
        
        print(f"Standard Output:\n{result.stdout}")  # For debugging
        print(f"Standard Error:\n{result.stderr}")  # For debugging

        # Check if the tool ran successfully
        if result.returncode == 0:
            raise Exception(f"DNSSEC analysis failed: {result.stderr.strip()}")

        # Default status and error messages
        status = "healthy"
        error_messages = []

        # Parse output lines to detect errors and set status
        for line in result.stdout.splitlines():
            if "ERROR" in line:
                status = "issues_found"
                error_messages.append(line.strip())  # Collect error lines

        # Format error messages into a single string, or empty if no errors
        error_detail = "; ".join(error_messages) if error_messages else ""

        # Construct the desired output structure
        analysis_result = {
                "domain": domain,
                "status": status,
                "error": error_detail
        }

        return analysis_result

    except Exception as e:
        raise Exception(f"Error running DNSSEC tool: {str(e)}")
