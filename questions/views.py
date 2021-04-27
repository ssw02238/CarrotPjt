from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods, require_safe
from django.contrib.auth.decorators import login_required
from .models import Question
from .forms import QuestionForm

@require_safe
def indexing(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, 'questions/indexing.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def write(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('questions:indexing')
    else:
        form = QuestionForm()
    context = {
        'form': form,
    }
    return render(request, 'questions/write.html', context)


@require_POST
def deleting(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    if request.user == question.user:
        question.delete()
        return redirect('questions:indexing')
    return redirect('questions:detailing', question_pk)


@require_safe
def detailing(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    context = {
        'question': question,
    }
    return render(request, 'questions/detailing.html', context)