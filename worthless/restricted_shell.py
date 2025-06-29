#!/usr/bin/env python3
"""
Save this as: restricted_shell.py in your project root
"""

import os
import sys
import subprocess
import re

ALLOWED_COMMANDS = {
    'ls': r'^ls(\s+(-[alhtrR]+|\.)*)(\s+[a-zA-Z0-9._/\-\*]*)*$',
    'cat': r'^cat(\s+[a-zA-Z0-9._/\-]+)+$'
}

def validate_and_execute(command):
    """Validate command against whitelist and execute if allowed"""
    command = command.strip()
    
    if not command:
        return
    
    # Get the base command
    base_cmd = command.split()[0]
    
    if base_cmd not in ALLOWED_COMMANDS:
        print(f"Error: Command '{base_cmd}' not allowed. Only ls and cat are permitted.")
        return
    
    # Validate full command against regex
    if not re.match(ALLOWED_COMMANDS[base_cmd], command):
        print(f"Error: Command format not allowed: {command}")
        return
    
    try:
        # Execute the command safely
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.stdout:
            print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, file=sys.stderr, end='')
            
    except subprocess.TimeoutExpired:
        print("Error: Command timeout")
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) > 1:
        # Command passed as argument - for subprocess calls
        command = ' '.join(sys.argv[1:])
        validate_and_execute(command)
    else:
        # Interactive mode (shouldn't be used in CTF)
        print("Restricted Shell - Only 'ls' and 'cat' commands allowed")
        while True:
            try:
                command = input("$ ").strip()
                if command.lower() in ['exit', 'quit']:
                    break
                validate_and_execute(command)
            except (KeyboardInterrupt, EOFError):
                break

if __name__ == "__main__":
    main()