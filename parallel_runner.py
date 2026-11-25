
import os
import subprocess
import sys
from pathlib import Path


# Project root directory.
PROJECT_DIR = Path(__file__).resolve().parent

# Number of simultaneous executions.
TOTAL_RUNS = 2

# Folder for separate execution logs.
RESULTS_DIR = PROJECT_DIR / "parallel-results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Store all running processes.
processes = []


print("=" * 60)
print("GCT BEHAVE - PARALLEL EXECUTION")
print(f"Starting {TOTAL_RUNS} simultaneous executions")
print("=" * 60)


# Start all three executions without waiting for one to finish.
for run_number in range(1, TOTAL_RUNS + 1):

    run_id = f"run_{run_number}"

    # Give each process its own execution ID.
    process_env = os.environ.copy()
    process_env["GCT_RUN_ID"] = run_id

    # Use a separate log file for each execution.
    log_path = RESULTS_DIR / f"{run_id}.log"
    log_file = open(log_path, "w", encoding="utf-8")

    # Run the same complete Behave suite.
    command = [
        sys.executable,
        "-m",
        "behave",
        "features/gct_tests.feature",
        "--tags=not @intentional_failure",
        "--no-capture"
    ]

    print(f"Launching {run_id}...")

    process = subprocess.Popen(
        command,
        cwd=PROJECT_DIR,
        env=process_env,
        stdout=log_file,
        stderr=subprocess.STDOUT
    )

    processes.append({
        "run_id": run_id,
        "process": process,
        "log_file": log_file,
        "log_path": log_path
    })


print("\nAll three executions have been launched!")
print("Waiting for the executions to finish...\n")


# Wait for each execution and collect its exit code.
for item in processes:

    exit_code = item["process"].wait()
    item["log_file"].close()

    if exit_code == 0:
        status = "PASSED"
    else:
        status = "FAILED"

    print(
        f"{item['run_id']}: {status} "
        f"(Exit code: {exit_code})"
    )

    print(f"Log: {item['log_path']}")


print("\n" + "=" * 60)
print("PARALLEL EXECUTION COMPLETED")
print("=" * 60)
