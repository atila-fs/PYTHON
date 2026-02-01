import os
import subprocess
import signal
import time
from flask import Flask, render_template, redirect, url_for, request, session, send_file, Response
from auth import login_required, check_login
from executor import list_scripts, start_script, stop_script, get_log_path

app = Flask(__name__)
app.secret_key = '<Senha>'

SCRIPTS_DIR = '/opt/projects-ops/test-hub/scripts'
LOGS_DIR = '/opt/projects-ops/test-hub/logs'

@app.route('/', methods=['GET'])
@login_required
def index():
    scripts = list_scripts(SCRIPTS_DIR)
    running = session.get('running', {})
    return render_template('index.html', scripts=scripts, running=running)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password):
            session['user'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/start/<script>')
@login_required
def start(script):
    result = start_script(script, SCRIPTS_DIR, LOGS_DIR)
    if result:
        session.setdefault('running', {})[script] = result.pid
        session.modified = True
    return redirect(url_for('index'))

@app.route('/stop/<script>')
@login_required
def stop(script):
    running = session.get('running', {})
    pid = running.pop(script, None)
    if pid:
        stop_script(pid)
        session.modified = True
    return redirect(url_for('index'))

@app.route('/logs/<script>')
@login_required
def logs(script):
    log_path = get_log_path(script, LOGS_DIR)
    if os.path.exists(log_path):
        return send_file(log_path)
    return f"Log do script {script} não encontrado", 404

@app.route('/stream/<script>')
@login_required
def stream_log(script):
    log_path = get_log_path(script, LOGS_DIR)

    def generate():
        if not os.path.exists(log_path):
            yield 'data: Log não encontrado\n\n'
            return
        with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if line:
                    yield f'data: {line.strip()}\n\n'
                else:
                    time.sleep(0.5)

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5010)