from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
from ..forms import SearchCourses, UserLoginForm
from ..models import (Course, Lesson, Quiz, Student,
                      Teacher, TakenQuiz)


class CourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'classroom/course_details.html'

    def get_context_data(self, **kwargs):
        student = None
        teacher = None
        if self.request.user.is_authenticated:
            if self.request.user.is_student:
                # if the logged in user is a student, check if he/she is enrolled in the displayed course
                student = self.request.user.student.taken_courses.filter(course__id=self.kwargs['pk']).first()
                teacher = None
                # kwargs['taken_quizzes'] = TakenQuiz.objects.filter(student=self.request.user.student)
            elif self.request.user.is_teacher:
                # if the logged in user is a teacher, check if he/she owns the displayed course
                teacher = self.request.user.courses.filter(id=self.kwargs['pk']).first()
                student = None

        kwargs['enrolled'] = student
        kwargs['owns'] = teacher
        kwargs['title'] = Course.objects.get(id=self.kwargs['pk'])

        kwargs['lessons'] = Lesson.objects.select_related('quizzes') \
            .select_related('course') \
            .filter(course__id=self.kwargs['pk']) \
            .order_by('number')

        return super().get_context_data(**kwargs)


def about(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:course_change_list')
        elif request.user.is_student:
            return redirect('students:mycourses_list')

    context = {
        'title': 'About Us',
        'courses': Course.objects.filter(status__iexact='approved').count(),
        'students': Student.objects.all().count(),
        'teachers': Teacher.objects.all().count(),
        'quizzes': Quiz.objects.all().count()
    }

    return render(request, 'classroom/about.html', context)


def contact_us(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:course_change_list')
        elif request.user.is_student:
            return redirect('students:mycourses_list')
        elif request.user.is_staff:
            return redirect('staff:dashboard')
    return render(request, 'classroom/contact.html', {'title': 'Contact Us'})


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:course_change_list')
        elif request.user.is_student:
            return redirect('students:mycourses_list')
        elif request.user.is_staff:
            return redirect('staff:dashboard')
    return render(request, 'classroom/home.html')


def login_view(request):
    next_link = request.GET.get('next')
    form = UserLoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect('home')
    else:
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)

            if next_link:
                return redirect(next_link)
            else:
                return redirect('/')

    return render(request, 'authentication/login.html', {'form': form, 'title': 'Login'})


def logout_view(request):
    logout(request)
    return redirect('/')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'authentication/register.html', {'title': 'Register'})


def browse_courses(request):
    query = None
    courses = Course.objects.filter(status__iexact='approved') \
        .annotate(taken_count=Count('taken_courses',
                                    filter=Q(taken_courses__status__iexact='enrolled'),
                                    distinct=True)) \
        .order_by('title')

    if request.user.is_authenticated:
        if request.user.is_student:
            student = request.user.student
            taken_courses = student.courses.values_list('pk', flat=True)
            courses = Course.objects.filter(status__iexact='approved') \
                .exclude(pk__in=taken_courses) \
                .annotate(taken_count=Count('taken_courses',
                                            filter=Q(taken_courses__status__iexact='enrolled'),
                                            distinct=True)) \
                .order_by('title')

    if 'search' in request.GET:
        form = SearchCourses(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('search')
            courses = Course.objects.filter(Q(title__icontains=query) |
                                            Q(description__icontains=query)) \
                .filter(status__iexact='approved')
    else:
        form = SearchCourses()

    context = {
        'title': 'Browse Courses',
        'form': form,
        'courses': courses,
        'search_str': query
    }
    return render(request, 'classroom/students/courses_list.html', context)
