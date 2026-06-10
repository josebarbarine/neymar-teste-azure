from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash, jsonify, abort)
from flask_login import login_required, current_user
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/')
@login_required
def index():
    status_filter = request.args.get('status', '')
    query = Task.query.filter_by(user_id=current_user.id)
    if status_filter:
        query = query.filter_by(status=status_filter)
    tasks = query.order_by(Task.created_at.desc()).all()
    return render_template('tasks/index.html', tasks=tasks,
                           status_filter=status_filter)


@tasks_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('Título é obrigatório.', 'danger')
            return render_template('tasks/form.html', task=None)

        task = Task(
            title=title,
            description=request.form.get('description', '').strip(),
            priority=request.form.get('priority', 'medium'),
            user_id=current_user.id,
        )
        db.session.add(task)
        db.session.commit()
        flash('Tarefa criada com sucesso!', 'success')
        return redirect(url_for('tasks.index'))

    return render_template('tasks/form.html', task=None)


@tasks_bp.route('/<int:task_id>')
@login_required
def detail(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    return render_template('tasks/detail.html', task=task)


@tasks_bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('Título é obrigatório.', 'danger')
            return render_template('tasks/form.html', task=task)

        task.title = title
        task.description = request.form.get('description', '').strip()
        task.status = request.form.get('status', task.status)
        task.priority = request.form.get('priority', task.priority)
        db.session.commit()
        flash('Tarefa atualizada!', 'success')
        return redirect(url_for('tasks.index'))

    return render_template('tasks/form.html', task=task)


@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Tarefa removida.', 'info')
    return redirect(url_for('tasks.index'))


# --- REST API endpoints (bonus) ---

@tasks_bp.route('/api')
@login_required
def api_list():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([t.to_dict() for t in tasks])
