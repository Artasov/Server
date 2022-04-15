from random import randint

from django.shortcuts import render, redirect

from APP_task.tasks_funcs import solve_quadratic_equation
from .models import Item

STRS = [
    'BLUE',
    'BLUE',
    'GREEN',
    'BLUE',
    'RED',
    'GREEN',
    'BLUE',
    'GREEN',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'GREEN',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'GREEN',
    'RED',
    'GREEN',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'GREEN',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'GREEN',
    'BLUE',
    'BLUE',
    'GREEN',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'RED',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'GREEN',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'RED',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'GREEN',
    'BLUE',
    'BLUE',
    'RED',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'GREEN',
    'BLUE',
    'BLUE',
    'BLUE',
    'GREEN',
    'BLUE',
    'BLUE',
    'BLUE',
    'GREEN',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'BLUE',
    'RED',
    'BLUE',
    'BLUE',
    'BLUE',
]


def Tasks(request):
    # for i in range(len(STRS)):
    #     item = Item(color=STRS[i], item_number=i+1)
    #     item.save()

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
        item_number = request.POST['item_number']
        item_color = Item.objects.get(item_number=item_number).color

        # GUESS
        guess = False
        random_int = randint(1, 100)
        if random_int <= 6:
            guess_color = 'RED'
            if guess_color == item_color:
                guess = True
            return render(request, 'APP_task/task_second.html', context={'result': 'RED', 'guess': guess, 'item_number': item_number})
        elif 6 < random_int <= 20:
            guess_color = 'GREEN'
            if guess_color == item_color:
                guess = True
            return render(request, 'APP_task/task_second.html', context={'result': 'GREEN', 'guess': guess, 'item_number': item_number})
        elif 20 < random_int <= 100:
            guess_color = 'BLUE'
            if guess_color == item_color:
                guess = True
            return render(request, 'APP_task/task_second.html', context={'result': 'BLUE', 'guess': guess, 'item_number': item_number})

    return render(request, 'APP_task/task_second.html')
