import os

# Convert shell script: for i in {1..5} do; ddsh mtree create /data/col1/mtree$i; done
for i in range(1, 6):
    path = f"/data/col1/mtree{i}"
    command = f"ddsh mtree create {path}"
    
    # Run the command using os.system
    exit_code = os.system(command)
    
    if exit_code == 0:
        print(f"Created mtree: {path}")
    else:
        print(f"Error creating mtree {path} (exit code: {exit_code})")


