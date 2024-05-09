# *********************************************************************
# This file illustrates how to execute a command and get it's output
# *********************************************************************
import subprocess

# Execute the ls -l command and print the output
result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
print(result.stdout)