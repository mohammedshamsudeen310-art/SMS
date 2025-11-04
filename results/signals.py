from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import Student
from academics.models import Subject, Enrollment
from django.utils import timezone

# 🔹 Auto-enroll new students
@receiver(post_save, sender=Student)
def auto_enroll_new_student(sender, instance, created, **kwargs):
    if created and instance.current_class:
        subjects = Subject.objects.filter(classroom=instance.current_class)
        for subject in subjects:
            Enrollment.objects.get_or_create(
                student=instance,
                subject=subject,
                defaults={"date_enrolled": timezone.now()}
            )

# 🔹 Update enrollments if student changes class
@receiver(pre_save, sender=Student)
def update_student_enrollments_on_class_change(sender, instance, **kwargs):
    if not instance.pk:
        # New student, handled by auto_enroll_new_student
        return

    # Get old instance from DB
    old_instance = Student.objects.get(pk=instance.pk)
    if old_instance.current_class != instance.current_class:
        # Remove enrollments for old class subjects
        old_subjects = Subject.objects.filter(classroom=old_instance.current_class)
        Enrollment.objects.filter(student=instance, subject__in=old_subjects).delete()

        # Add enrollments for new class subjects
        if instance.current_class:
            new_subjects = Subject.objects.filter(classroom=instance.current_class)
            for subject in new_subjects:
                Enrollment.objects.get_or_create(
                    student=instance,
                    subject=subject,
                    defaults={"date_enrolled": timezone.now()}
                )
