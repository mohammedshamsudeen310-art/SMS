from django.db import migrations, models
import django.db.models.deletion

def migrate_classroom_data(apps, schema_editor):
    Student = apps.get_model('accounts', 'Student')
    ClassRoom = apps.get_model('academics', 'ClassRoom')

    for student in Student.objects.all():
        # Match classroom name to actual ClassRoom entry
        current_class_name = getattr(student, 'current_class_old', None)
        promoted_to_name = getattr(student, 'promoted_to_old', None)

        if current_class_name:
            current_class_obj = ClassRoom.objects.filter(name=current_class_name).first()
            if current_class_obj:
                student.current_class = current_class_obj

        if promoted_to_name:
            promoted_class_obj = ClassRoom.objects.filter(name=promoted_to_name).first()
            if promoted_class_obj:
                student.promoted_to = promoted_class_obj

        student.save()

def reverse_migration(apps, schema_editor):
    # Optional reverse step
    Student = apps.get_model('accounts', 'Student')
    for student in Student.objects.all():
        if student.current_class:
            student.current_class_old = student.current_class.name
        if student.promoted_to:
            student.promoted_to_old = student.promoted_to.name
        student.save()


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0006_alter_attendancerecord_student_and_more'),
        ('accounts', '0003_remove_student_address_remove_student_date_of_birth_and_more'),
    ]


    operations = [
        # 1️⃣ Rename old fields
        migrations.RenameField(
            model_name='student',
            old_name='current_class',
            new_name='current_class_old',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='promoted_to',
            new_name='promoted_to_old',
        ),

        # 2️⃣ Add new proper ForeignKeys
        migrations.AddField(
            model_name='student',
            name='current_class',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='students',
                to='academics.classroom'
            ),
        ),
        migrations.AddField(
            model_name='student',
            name='promoted_to',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='promoted_students',
                to='academics.classroom'
            ),
        ),

        # 3️⃣ Data migration
        migrations.RunPython(migrate_classroom_data, reverse_migration),

        # 4️⃣ Drop old varchar columns
        migrations.RemoveField(model_name='student', name='current_class_old'),
        migrations.RemoveField(model_name='student', name='promoted_to_old'),
    ]
