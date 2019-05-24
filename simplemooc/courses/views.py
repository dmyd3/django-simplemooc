from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Courses, Enrollment
from .forms import ContactCourse

def index(request):
    courses = Courses.objects.all()
    template_name = "courses/index.html"

    context = {
        'courses':courses
    }

    return render(request, template_name, context)

def details(request, slug):
    #course = Courses.objects.get(pk=pk)
    #course = get_object_or_404(Courses, pk=pk)
    course = get_object_or_404(Courses, slug=slug)
    context = {}
    if request.method=="POST":
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid']='True'
            #form.send_mail(course)
            form.send_mail(course)
            print(form.cleaned_data)
            form = ContactCourse()            
    else:
        form = ContactCourse()

    context['course']= course
    context['form']= ContactCourse()
        
    template_name = 'courses/details.html'

    return render(request, template_name,context)

@login_required
def enrollment(request,slug)    :
    course = get_object_or_404(Courses, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )
    if created:
        enrollment.active()
        messages.success(request, "Você foi inscrito no curso com sucesso")
    else:
        messages.info(request, "Você já estava inscrito nesse curso")
    
    return redirect('accounts:dashboard')
