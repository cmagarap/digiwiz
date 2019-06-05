from django.urls import include, path

from .views import classroom, staff, students, teachers

urlpatterns = [
    path('', classroom.home, name='home'),

    path('staff/', include(([
        path('', staff.dashboard, name='dashboard'),
        path('course-requests/', staff.CourseRequestsView.as_view(), name='course_requests'),
        path('course-requests/accept-course/<int:course_pk>/', staff.accept_course, name='accept_course'),
        path('course-requests/reject-course/<int:course_pk>/', staff.reject_course, name='reject_course')
    ], 'classroom'), namespace='staff')),

    path('student/', include(([
        path('', students.MyCoursesListView.as_view(), name='mycourses_list'),
        path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
        path('enroll/<int:pk>/', students.enroll, name='enroll'),
        path('unenroll/<int:pk>/', students.unenroll, name='unenroll')
    ], 'classroom'), namespace='students')),

    path('teacher/', include(([
        path('', teachers.CourseListView.as_view(), name='course_change_list'),
        path('ajax/load-lessons/', teachers.load_lessons, name='ajax_load_lessons'),
        path('course/add/', teachers.CourseCreateView.as_view(), name='course_add'),
        path('course/<int:pk>/', teachers.CourseUpdateView.as_view(), name='course_change'),
        path('course/<int:pk>/delete/', teachers.delete_course, name='course_delete'),
        path('course/<int:course_pk>/lesson/<int:lesson_pk>/', teachers.edit_lesson, name='lesson_edit'),
        path('course/<int:course_pk>/lesson/<int:lesson_pk>/delete/',
             teachers.delete_lesson, name='lesson_delete'),
        path('enrollment-requests/', teachers.EnrollmentRequestsListView.as_view(), name='enrollment_requests_list'),
        path('enrollment-requests/accept/<int:taken_course_pk>', teachers.accept_enrollment, name='enrollment_accept'),
        path('enrollment-requests/reject/<int:taken_course_pk>', teachers.reject_enrollment, name='enrollment_reject'),
        path('lesson/add/', teachers.add_lesson, name='lesson_add'),
        path('profile/', teachers.profile, name='profile'),
        path('quiz/add/', teachers.add_quiz, name='quiz_add'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]
