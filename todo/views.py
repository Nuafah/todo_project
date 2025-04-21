from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Todo
from .forms import TodoForm
import json


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('taskboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def homepage_view(request):
    if request.user.is_authenticated:
        return redirect('taskboard')
    return render(request, 'homepage.html')


@login_required
def add_todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

@login_required
def edit_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == "POST":
        form = TodoForm(request.POST, request.FILES, instance=todo)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": form.errors}, status=400)
    else:
        form = TodoForm(instance=todo)
    return render(request, "partials/edit_todo_form.html", {"form": form, "todo": todo})


@login_required
def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=405)




@login_required
def taskboard_view(request):
    todos = Todo.objects.filter(user=request.user)
    status_columns = [
        {'key': 'pending', 'label': 'Pending'},
        {'key': 'in_progress', 'label': 'In Progress'},
        {'key': 'done', 'label': 'Done'},
    ]
    form = TodoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect('taskboard')
    return render(request, 'taskboard.html', {
        'todos': todos,
        'status_columns': status_columns,
        'form': form
    })


@csrf_exempt
@login_required
def update_status_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            todo_id = data.get("id")
            new_status = data.get("status")
            todo = Todo.objects.get(id=todo_id, user=request.user)
            todo.status = new_status
            todo.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


