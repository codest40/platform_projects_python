#!/usr/bin/env bash

SERVICE_NAME="network-watchman"
SCRIPT_PATH="$(realpath "$0")"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SERVICE_DIR/$SERVICE_NAME.service"
TARGETS=("8.8.8.8" "1.1.1.1" "208.67.222.222")  # servers to ping
PING_INTERVAL=1                                  # seconds between pings
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$SCRIPT_DIR/logs/network_downtime.log"
ERR_FILE="$SCRIPT_DIR/logs/network_watchman.log"


# Are we already running under systemd?
if [ -n "$INVOCATION_ID" ]; then
    :
else
    mkdir -p "$SERVICE_DIR"

    if [ ! -f "$SERVICE_FILE" ]; then
        cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Network Watchman

[Service]
Type=simple
ExecStart=$SCRIPT_PATH
Restart=always
RestartSec=2

[Install]
WantedBy=default.target
EOF

        systemctl --user daemon-reload
        systemctl --user enable "$SERVICE_NAME.service"
        systemctl --user start "$SERVICE_NAME.service"

        echo "Installed and started as a systemd user service."
        exit 0
    fi

    if systemctl --user is-active --quiet "$SERVICE_NAME.service"; then
        echo "Network Watchman is already running as a systemd service."
        exit 0
    fi

    systemctl --user start "$SERVICE_NAME.service"
    echo "Started Network Watchman service."
    exit 0
fi

mkdir -p "$(dirname "$LOG_FILE")"

# ---------------------------
# Functions
# ---------------------------
send_alert() {
    local message="$1"
    # Desktop notification
    notify-send "Network Alert: " "$message"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $message" >> "$LOG_FILE"

    # Keep only 2 most recent entries
    tail -n 2 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
    tail -n 2 "$ERR_FILE" > "$ERR_FILE.tmp" && mv "$ERR_FILE.tmp" "$ERR_FILE"
}

check_network() {
    local down_count=0
    for t in "${TARGETS[@]}"; do
        if ! ping -c 1 -W 1 "$t" &> /dev/null; then
            down_count=$((down_count+1))
        fi
    done

    if [ $down_count -eq ${#TARGETS[@]} ]; then
        send_alert "Mr Engineeer, ALL NETWORK DOWN!"
    fi
}

# ---------------------------
# Main Loop
# ---------------------------
echo "Starting Network Watchman..."
while true; do
    check_network
    sleep $PING_INTERVAL
done

