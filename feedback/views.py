from django.shortcuts import render, redirect
from .models import Student, Feedback
from django.contrib import messages

def home(request):
    return render(request, 'feedback/home.html')

def submit_feedback(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        department = request.POST['department']
        subject = request.POST['subject']
        message = request.POST['message']

        student, created = Student.objects.get_or_create(
            name=name, email=email, department=department
        )

        Feedback.objects.create(
            student=student,
            subject=subject,
            message=message
        )
        messages.success(request, "Feedback submitted successfully!")
        return redirect('submit_feedback')

    return render(request, 'feedback/submit_feedback.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username == 'admin' and password == 'admin123':
            request.session['admin'] = True
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('admin_login')

    return render(request, 'feedback/admin_login.html')

def admin_dashboard(request):
    if not request.session.get('admin'):
        return redirect('admin_login')

    feedbacks = Feedback.objects.select_related('student').all().order_by('-submitted_at')
    return render(request, 'feedback/admin_dashboard.html', {'feedbacks': feedbacks})

# Create your views here.
