#!/usr/bin/env python3
"""Put this PC to sleep after a countdown.

Usage:
    python sleep_timer.py            # sleep in 10 minutes (default)
    python sleep_timer.py 30         # sleep in 30 minutes
    python sleep_timer.py --cancel   # cancel a pending Windows shutdown/sleep

Works on Windows, macOS and Linux.
"""

import argparse
import platform
import subprocess
import sys
import time

DEFAULT_MINUTES = 10


def sleep_command():
    """Return the OS-specific command that suspends the machine."""
    system = platform.system()
    if system == "Windows":
        # SetSuspendState: hibernate=0, forcedSuspend=0, disableWakeEvents=0
        return ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"]
    if system == "Darwin":
        return ["pmset", "sleepnow"]
    # Linux: systemctl is the most portable modern option.
    return ["systemctl", "suspend"]


def cancel_windows():
    """Cancel a pending Windows shutdown (no-op elsewhere)."""
    if platform.system() == "Windows":
        subprocess.run(["shutdown", "/a"], check=False)
        print("Cancelled any pending shutdown.")
    else:
        print("--cancel only applies to Windows scheduled shutdowns.")


def countdown(minutes):
    total = int(minutes * 60)
    print(f"PC will sleep in {minutes} minute(s). Press Ctrl+C to cancel.")
    try:
        for remaining in range(total, 0, -1):
            mins, secs = divmod(remaining, 60)
            print(f"\rSleeping in {mins:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\rTime's up — putting the PC to sleep now.        ")
    except KeyboardInterrupt:
        print("\nSleep timer cancelled.")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Put this PC to sleep after a countdown.")
    parser.add_argument(
        "minutes",
        nargs="?",
        type=float,
        default=DEFAULT_MINUTES,
        help=f"Minutes until sleep (default: {DEFAULT_MINUTES}).",
    )
    parser.add_argument(
        "--cancel",
        action="store_true",
        help="Cancel a pending Windows scheduled shutdown.",
    )
    args = parser.parse_args()

    if args.cancel:
        cancel_windows()
        return

    if args.minutes <= 0:
        print("Minutes must be greater than 0.")
        sys.exit(1)

    if not countdown(args.minutes):
        return

    try:
        subprocess.run(sleep_command(), check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"Failed to put the PC to sleep: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
