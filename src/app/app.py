from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@database/project_db'
db = SQLAlchemy(app)

# モデルクラスの定義

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    deadline = db.Column(db.Date)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    assignee = db.Column(db.String(255))
    deadline = db.Column(db.Date)
    progress = db.Column(db.Integer)

# データベースのテーブル作成処理
@app.before_first_request
def create_tables():
    db.create_all()

# ルートとビュー関数の定義

@app.route('/')
def index():
    # プロジェクト一覧を取得
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/project/create', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        # フォームからプロジェクト情報を取得
        title = request.form['title']
        description = request.form['description']
        start_date = request.form['start_date']
        deadline = request.form['deadline']

        # プロジェクトを作成してデータベースに保存
        project = Project(title=title, description=description, start_date=start_date, deadline=deadline)
        db.session.add(project)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create_project.html')

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    # プロジェクトの詳細情報を取得
    project = Project.query.get(project_id)

    # プロジェクトに紐づくタスク一覧を取得
    tasks = Task.query.filter_by(project_id=project_id).all()

    return render_template('project_detail.html', project=project, tasks=tasks)

@app.route('/task/<int:task_id>', methods=['GET', 'POST'])
def task_detail(task_id):
    task = Task.query.get(task_id)

    if request.method == 'POST':
        # タスクの進捗を更新
        task.progress = int(request.form['progress'])
        db.session.commit()

    return render_template('task_detail.html', task=task)

@app.route('/task/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        # タスクを作成
        project_id = int(request.form['project_id'])
        title = request.form['title']
        description = request.form['description']
        assignee = request.form['assignee']
        deadline = request.form['deadline']
        progress = 0

        task = Task(project_id=project_id, title=title, description=description,
                    assignee=assignee, deadline=deadline, progress=progress)
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('project_detail', project_id=project_id))

    # プロジェクト一覧を取得してタスク作成画面を表示
    projects = Project.query.all()
    return render_template('create_task.html', projects=projects)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
