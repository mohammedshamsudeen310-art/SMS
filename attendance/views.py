# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from .models import AttendanceSession, AttendanceRecord
# from .forms import AttendanceSessionForm
# from academics.models import Enrollment

# @login_required
# def create_attendance_session(request):
#     if request.method == 'POST':
#         form = AttendanceSessionForm(request.POST)
#         if form.is_valid():
#             attendance_session = form.save(commit=False)
#             attendance_session.teacher = request.user
#             attendance_session.save()

#             # Auto-populate all students in that subject
#             enrollments = Enrollment.objects.filter(subject=attendance_session.subject)
#             for enroll in enrollments:
#                 AttendanceRecord.objects.create(
#                     session=attendance_session,
#                     student=enroll.student,
#                     status='Absent'  # default
#                 )

#             return redirect('mark_attendance', session_id=attendance_session.id)
#     else:
#         form = AttendanceSessionForm()
#     return render(request, 'attendance/create_session.html', {'form': form})


# @login_required
# def mark_attendance(request, session_id):
#     session = get_object_or_404(AttendanceSession, id=session_id)
#     records = session.records.select_related('student').all()

#     if request.method == 'POST':
#         for record in records:
#             status = request.POST.get(str(record.id))
#             record.status = status
#             record.save()
#         session.end_time = timezone.now()
#         session.save()
#         return redirect('attendance_list')

#     return render(request, 'attendance/mark_attendance.html', {
#         'session': session,
#         'records': records
#     })
