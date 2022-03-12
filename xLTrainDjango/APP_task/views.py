from django.shortcuts import render, redirect
from APP_task.tasks_funcs import solve_quadratic_equation
from random import randint

def Tasks(request):
    return redirect('task_first')


def TaskFirst(request):
    if request.method == "POST":
        try:
            a = float(request.POST['a'])
            b = float(request.POST['b'])
            c = float(request.POST['c'])
        except ValueError:
            return render(request, 'APP_task/task_first.html', context={'invalid': 'Invalid value'})

        roots = solve_quadratic_equation(a, b, c)

        return render(request, 'APP_task/task_first.html', context={'roots': roots})

    return render(request, 'APP_task/task_first.html')


def TaskSecond(request):
    if request.method == "POST":
        random_int = randint(1, 100)
        if random_int <= 6:
            return render(request, 'APP_task/task_second.html', context={'result': 'RED'})
        elif 6 < random_int <= 20:
            return render(request, 'APP_task/task_second.html', context={'result': 'GREEN'})
        elif 20 < random_int <= 100:
            return render(request, 'APP_task/task_second.html', context={'result': 'BLUE'})

    return render(request, 'APP_task/task_second.html')
