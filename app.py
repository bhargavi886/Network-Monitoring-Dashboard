from flask import Flask, render_template
import subprocess
import platform

app = Flask(__name__)

devices = [
    {"name": "Google DNS", "ip": "8.8.8.8"},
    {"name": "Cloudflare DNS", "ip": "1.1.1.1"},
    {"name": "Local Router", "ip": "192.168.1.1"}
]


def check_device(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"

    result = subprocess.run(
        ["ping", param, "1", ip],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        output = result.stdout

        if "time=" in output:
            latency = output.split("time=")[1].split("ms")[0] + " ms"
        elif "time<" in output:
            latency = "<1 ms"
        else:
            latency = "Unknown"

        return "Online", latency

    return "Offline", "N/A"


@app.route("/")
def dashboard():

    monitored_devices = []

    for device in devices:
        status, latency = check_device(device["ip"])

        monitored_devices.append({
            "name": device["name"],
            "ip": device["ip"],
            "status": status,
            "latency": latency
        })

    total = len(monitored_devices)
    online = sum(1 for d in monitored_devices if d["status"] == "Online")
    offline = total - online

    return render_template(
        "index.html",
        devices=monitored_devices,
        total=total,
        online=online,
        offline=offline
    )


if __name__ == "__main__":
    print("Starting Flask Server...")
    app.run(debug=True)