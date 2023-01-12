from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Registration(models.Model):
    First_name = models.CharField(max_length=200)
    Last_name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    Password = models.CharField(max_length=200)
    Registration_date = models.DateField()
    Num_of_courses_enrolled = models.IntegerField(default=0)
    Num_of_courses_completed = models.IntegerField(default=0)
    Qualification = models.TextField()
    Introduction_brief = models.TextField()
    Image = models.ImageField(upload_to='media')
    Num_of_enrolled_students = models.IntegerField()
    Average_review_rating = models.IntegerField()
    Num_of_reviews = models.IntegerField()
    About_website = models.TextField()
    User_role = models.CharField(max_length=200)
    user = models.OneToOneField(User,on_delete = models.CASCADE, null = True)

    def __str__(self):
        return self.First_name


class Subject(models.Model):
    Subject_title = models.CharField(max_length=200)
    Course_title = models.CharField(max_length=200)
    Course_brief = models.TextField()
    Course_duration = models.IntegerField()
    Num_of_chapters = models.IntegerField()
    Course_fee = models.FloatField()
    Language = models.CharField(max_length=200)
    Chapter_title = models.CharField(max_length=200)
    Num_of_assignments = models.IntegerField()
    Chapter_Content_name = models.ImageField(upload_to='media', null = True)
    Chapter_text_content = models.TextField()
    Chapter_Content_type = models.CharField(max_length=200)
    Chapter_Content_Is_mandatory = models.BooleanField()
    Chapter_Content_Time_required_in_sec = models.IntegerField()
    Chapter_Content_Is_open_for_free = models.BooleanField()
    Sub_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True)

    def __str__(self):
        return self.Subject_title


class Enrollment(models.Model):
    Student_name = models.CharField(max_length=200)
    Student_email = models.EmailField()
    Subject_name = models.CharField(max_length=200)
    Course_name = models.CharField(max_length=200)
    Teacher_name = models.CharField(max_length=200)
    Teacher_email = models.EmailField()
    Attendance = models.IntegerField()
    Pending_days = models.IntegerField()
    Enrollment_date = models.DateField(auto_now_add=True)
    Teacher_response = models.CharField(max_length=200)
    Paid_amount = models.FloatField()
    Certificate = models.CharField(max_length=200)
    Is_paid_subscription = models.BooleanField()
    notify = models.CharField(max_length=200, null = True)
    enrol_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True)


class Learning_progress(models.Model):
    Student_name = models.CharField(max_length=200)
    Student_email = models.EmailField()
    Subject_name = models.CharField(max_length=200)
    Course_name = models.CharField(max_length=200)
    Course_chapter_name = models.CharField(max_length=200)
    Course_chapter_content_name = models.ImageField(upload_to='media', null = True)
    Begin_timestamp = models.DateTimeField(auto_now_add=True)
    Completion_timestamp = models.DateTimeField(auto_now=True)
    Status = models.CharField(max_length=200)
    Teacher_email = models.EmailField(max_length=200, null=True)
    Learn_p_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True)


class Feedback(models.Model):
    Student_name = models.CharField(max_length=200)
    Student_email = models.EmailField()
    Teacher_name = models.CharField(max_length=200)
    Teacher_email = models.EmailField()
    Subject_name = models.CharField(max_length=200)
    Course_name = models.CharField(max_length=200)
    Rating_score = models.IntegerField()
    Feedback_text = models.TextField(default='Nil')
    Submission_date = models.DateField()
    Feed_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True)


class Messages(models.Model):
    Category = models.CharField(max_length=200)
    Name = models.CharField(max_length=200)
    From_email = models.EmailField()
    To_email = models.EmailField()
    Message_content = models.TextField(default='Nil')


class Exam(models.Model):
    Student_name = models.CharField(max_length=200)
    Student_email = models.EmailField()
    Teacher_name = models.CharField(max_length=200)
    Subject_name = models.CharField(max_length=200)
    Course_name = models.CharField(max_length=200)
    Question = models.TextField()
    Option1 = models.TextField()
    Option2 = models.TextField()
    Option3 = models.TextField()
    Correct_answer = models.TextField()
    Lock = models.CharField(max_length=200)
    Time_start = models.DateTimeField()
    Time_stop = models.DateTimeField()
    Exam_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True)


class Exam_results(models.Model):
    Student_name = models.CharField(max_length=200)
    Student_email = models.EmailField(max_length=200)
    Teacher_name = models.CharField(max_length=200)
    Subject_name = models.CharField(max_length=200)
    Total_marks = models.IntegerField()
    Acquired_marks = models.IntegerField()
    Grade = models.CharField(max_length=200)
    Time_stop = models.DateTimeField(auto_now=True)
    Exam_res_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True)


class Blogs(models.Model):
    Name = models.CharField(max_length=200)
    Blog_content = models.TextField()
    Image = models.ImageField()
    Date_blog = models.DateField()
    Approval_status = models.CharField(max_length=200)


class Requests(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.EmailField()
    User_category = models.CharField(max_length=200)
    Old_password = models.CharField(max_length=200)
    New_password = models.CharField(max_length=200)
    Req_reg = models.ForeignKey(Registration, on_delete=models.SET_NULL, null = True)


