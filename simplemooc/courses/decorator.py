from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import Courses, Enrollment

def enrollment_required(view_func):
    def _wrapper(request, *args, **kwargs):
        slug = kwargs['slug']
        course = get_object_or_404(Courses, slug=slug)
        #has_permission = request.user.is_staff
        has_permission = 1
        if not has_permission:
            try:
                enrollment = Enrollment.objects.get(
                    user=request.user, course=course
                )
            except ObjectDoesNotExist:
                message = "Desculpe, você não possui permissão para visualizar esta página"
            else:
                if enrollment.is_approved():
                    has_permission = True
                else:
                    message = 'A sua inscrição está pendente'
        if not has_permission:
            messages.error(request,message)
            return redirect('accounts:dashboard')
        request.course = course
        return view_func(request,*args,**kwargs)
    return _wrapper