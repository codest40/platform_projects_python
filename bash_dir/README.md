# System Runners

### Network Watchman

A lightweight Bash-based network monitoring utility that continuously checks internet connectivity by probing multiple public endpoints. 
The script automatically installs itself as a user `systemd` service on first execution, ensuring persistent background monitoring with automatic restarts. 
When all configured targets become unreachable, it sends desktop notifications and records downtime events in rotating log files, providing a simple, dependency-light approach to workstation network availability monitoring.

## Usage
- Ensure your notify-send desktop notification is enabled
- chmod +x network_watchman.sh
- ./network_watchman.sh

- The first execution automatically installs and starts the script as a user systemd service. Subsequent executions detect the existing service and avoid creating duplicate instances.
