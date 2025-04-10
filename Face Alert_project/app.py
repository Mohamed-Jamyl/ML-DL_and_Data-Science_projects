from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
import shutil
import os

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="1234")

UPLOAD_FOLDER = Path("static/unknown_pics")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

users = {"admin": "1234"}

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_session(session: dict = Depends(lambda: {})):
    return session

@app.get("/")
def select_camera(session: dict = Depends(get_session)):
    if "username" not in session:
        return RedirectResponse(url="/login")
    camera_ids = [0, 1]
    return {"camera_ids": camera_ids}

@app.get("/view_images/{cam_id}")
def view_images(cam_id: int, session: dict = Depends(get_session)):
    if "username" not in session:
        return RedirectResponse(url="/login")
    files = os.listdir(UPLOAD_FOLDER)
    filtered_files = [file for file in files if file.startswith(f'cam{cam_id}_')]
    return {"files": filtered_files}

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), session: dict = Depends(get_session)):
    if username in users and users[username] == password:
        session["username"] = username
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    raise HTTPException(status_code=400, detail="Invalid username or password")

@app.get("/logout")
def logout(session: dict = Depends(get_session)):
    session.pop("username", None)
    return RedirectResponse(url="/login")

@app.post("/upload")
def upload_file(file: UploadFile = File(...), session: dict = Depends(get_session)):
    if "username" not in session:
        return RedirectResponse(url="/login")
    file_location = UPLOAD_FOLDER / file.filename
    with file_location.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.1.106", port=5000, reload=True)






'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
import functools
from datetime import datetime

app = Flask(__name__)
app.secret_key = '1234'
UPLOAD_FOLDER = 'static/unknown_pics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

users = {'admin': '1234'}

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/')
@login_required
def select_camera():
    camera_ids = [0, 1]  
    return render_template('select_camera.html', camera_ids=camera_ids)

@app.route('/view_images/<int:cam_id>')
@login_required
def view_images(cam_id):
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    print(f"Files in upload folder: {files}")  # Debugging

    filtered_files = [file for file in files if file.startswith(f'cam{cam_id}_')]
    print(f"Filtered files: {filtered_files}")  # Debugging

    file_data = []
    for file in filtered_files:
        try:
            timestamp_str = file.split('_')[-1].split('.')[0]
            timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            timestamp = "Unknown"

        file_data.append({
            "filename": file,
            "timestamp": timestamp
        })

    print(f"File data being sent to template: {file_data}")  # Debugging

    return render_template('index.html', files=file_data, cam_id=cam_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('select_camera'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('select_camera'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='192.168.1.106', port=5000, debug=True)

'''


"""
from flask import Flask, render_template, request, redirect, url_for, session
import os
import functools

app = Flask(__name__)
app.secret_key = '1234'
UPLOAD_FOLDER = 'static/unknown_pics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

users = {'admin': '1234'}

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/')
@login_required
def select_camera():
    camera_ids = [0, 1]  
    return render_template('select_camera.html', camera_ids=camera_ids)

@app.route('/view_images/<int:cam_id>')
@login_required
def view_images(cam_id):
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    filtered_files = [file for file in files if file.startswith(f'cam{cam_id}_')]
    return render_template('index.html', files=filtered_files, cam_id=cam_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('select_camera'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('select_camera'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='192.168.1.103', port=5000, debug=True)


"""



