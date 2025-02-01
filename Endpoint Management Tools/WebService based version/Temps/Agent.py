from flask import Flask, jsonify
import LibAgentManager

app = Flask(__name__)


@app.route('/api/ram', methods=['GET'])
def ramUsage():
    usage = manager.get_system_usage()
    tm = (f"Memory Usage: {usage['memory_used']}MB / {usage['memory_total']}MB")
    print(tm)
    return jsonify({"ram_usage": f"{tm}"})


@app.route('/api/cpu', methods=['GET'])
def cpuUsage():
    cpu_percent = manager.cpu_usage()
    return jsonify({"cpu": f"{cpu_percent}"})


@app.route('/api/noprocess', methods=['GET'])
def noProcess():
    noP = manager.get_running_processes_count()
    return jsonify({"no_process": f"{noP}"})


@app.route('/api/restart', methods=['GET'])
def restart():
    manager.restart_system()
    return jsonify({"message": "soccess"})


if __name__ == '__main__':
    app.run(debug=True)
