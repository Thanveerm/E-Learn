from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from . models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth
from django.contrib.auth.hashers import make_password
import pytz
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail






def home(request):
    sdd = Subject.objects.all()
    sd = []
    count = 0
    for i in sdd:
        if i.Subject_title not in sd:
            sd.append(i.Subject_title)
            count += 1
    return render(request,'home.html',{'sd':sd,'count':count})

def reg_msg(request):
    messages.success(request, 'Please register to access course contents')
    return redirect('home')




def news(request):
    page = requests.get('https://www.indiatoday.in/education-today')
    soup = BeautifulSoup(page.content,'html.parser')
    week = soup.find(class_ = 'special-top-news')
    wm = week.find(class_ = 'itg-listing')
    w = wm.find_all('a')
    ww = []
    for x in w:
        ww.append(x.get_text())
    #print(ww)
    #return HttpResponse(ww)
    x = datetime.datetime.now()
    return render(request,'news.html',{'ww':ww,'x':x})



def about(request):
    df = Registration.objects.get(User_role = 'admin')
    gt = Registration.objects.filter(User_role = 'teacher')
    return render(request,'about.html',{'df':df,'gt':gt})


def add_blog(request):
    if request.method == 'POST':
        nam = request.POST.get('nam')
        c_b = request.POST.get('c_b')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        date1 = request.POST.get('date1')
        b = Blogs()
        b.Name = nam
        b.Blog_content = c_b
        b.Image = photo
        b.Date_blog = date1
        b.Approval_status = 'Rejected'
        b.save()
        messages.success(request, 'Blog added successfully. Please wait for approval')
        return redirect('home')
    return render(request,'add_blog.html')



def admin_rg(request):
    if request.method == 'POST':
        lk = Registration.objects.all()

        for t in lk:
            if t.User_role == 'admin':
                messages.success(request, 'You are not allowed to be registered as admin')
                return redirect('home')
        x = datetime.datetime.now()
        z = x.strftime("%Y-%m-%d")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        admin = request.POST.get('adminn1')
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.Email == email:
                messages.success(request, 'User already exists')
                return render(request, 'register_admin.html')

        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'register_admin.html')

        user = User.objects.create_user(username=user_name, email=email, password=psw)
        user.save()

        t = Registration()
        t.First_name = first_name
        t.Last_name = last_name
        t.Email = email
        t.Password = psw
        t.Registration_date = z
        t.Qualification = 'Nil'
        t.Introduction_brief = 'Nil'
        t.Image = photo
        t.Num_of_enrolled_students = 0
        t.Average_review_rating = 0
        t.Num_of_reviews = 0
        t.About_website = 'Nil'
        t.User_role = admin
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered as admin')
        return redirect('home')
    else:
        return render(request, 'register_admin.html')


def register_tr(request):
    if request.method == 'POST':
        x = datetime.datetime.now()
        y = x.strftime("%Y-%m-%d")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        qual = request.POST.get('qual')
        intro = request.POST.get('intro')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.Email == email:
                messages.success(request, 'User already exists')
                return render(request, 'register_teacher.html')

        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'register_teacher.html')

        user = User.objects.create_user(username=user_name, email=email, password=psw)
        user.save()

        t = Registration()
        t.First_name = first_name
        t.Last_name = last_name
        t.Email = email
        t.Password = psw
        t.Registration_date = y
        t.Qualification = qual
        t.Introduction_brief = intro
        t.Image = photo
        t.Num_of_enrolled_students = 0
        t.Average_review_rating = 0
        t.Num_of_reviews = 0
        t.About_website = 'Nil'
        t.User_role = 'teacher'
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered')
        return redirect('home')
    else:
        return render(request, 'register_teacher.html')



def register_st(request):
    if request.method == 'POST':
        x = datetime.datetime.now()
        y = x.strftime("%Y-%m-%d")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.Email == email and i.User_role == 'student':
                messages.success(request, 'User already exists')
                return render(request, 'student_reg.html')

        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'student_reg.html')

        user = User.objects.create_user(username=user_name, email=email, password=psw)
        user.save()

        t = Registration()
        t.First_name = first_name
        t.Last_name = last_name
        t.Email = email
        t.Password = psw
        t.Registration_date = y
        t.Qualification = 'Nil'
        t.Introduction_brief = 'Nil'
        t.Image = photo
        t.Num_of_enrolled_students = 0
        t.Average_review_rating = 0
        t.Num_of_reviews = 0
        t.About_website = 'Nil'
        t.User_role = 'student'
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered as stu dent')
        return redirect('home')
    else:
        return render(request, 'student_reg.html')


def logout(request):
    auth.logout(request)
    return redirect('home')



def login(request):
    if request.method == 'POST':
        username = request.POST.get("user_name")
        password = request.POST.get("pword")
        user = auth.authenticate(username = username, password = password)
        if user is None:
            messages.success(request, 'Invalid credentials')
            return render(request, 'login.html')
        auth.login(request, user)
        if Registration.objects.filter(user = user, Password = password).exists():
            logs = Registration.objects.filter(user = user, Password = password)
            for value in logs:
                user_id = value.id
                usertype  = value.User_role
                teacher_email = value.Email
                if usertype == 'admin':
                    request.session['logg'] = user_id
                    g = Enrollment.objects.all()
                    for i in g:
                        delta = datetime.datetime.now().date() - i.Enrollment_date
                        d = int(delta.days)
                        mkn = Registration.objects.get(Email=i.Teacher_email)
                        df = Subject.objects.filter(Subject_title=i.Subject_name, Course_title=i.Course_name,Sub_reg=mkn)
                        for u in df:
                            st = int(u.Course_duration)
                            st1 = st - d
                            i.Pending_days = st1
                            i.save()
                            break
                    return redirect('admin_home')

                elif usertype == 'teacher':
                    request.session['logg'] = user_id
                    request.session['teacher'] = teacher_email
                    cm = Registration.objects.get(id = request.session['logg'])
                    fpr = Subject.objects.all()
                    for y in fpr:
                        kwd = Subject.objects.filter(Subject_title = y.Subject_title, Course_title = y.Course_title, Sub_reg = cm)
                        mk = 0
                        for w in kwd:
                            mk += 1
                        for d in kwd:
                            d.Num_of_chapters = mk
                            d.save()
                    g = Enrollment.objects.all()
                    count = 0
                    for i in g:
                        if i.Teacher_email == cm.Email:
                            count += 1
                    cm.Num_of_enrolled_students = count
                    mb = Feedback.objects.filter(Teacher_email = cm.Email)
                    cnn = 0
                    avs = []
                    for t in mb:
                        cnn += 1
                        avs.append(t.Rating_score)
                    aa = avs.count(5)
                    bb = avs.count(4)
                    cc = avs.count(3)
                    dd = avs.count(2)
                    ee = avs.count(1)
                    ff = [aa,bb,cc,dd,ee]
                    gg = max(ff)
                    if int(gg) == int(aa):
                        cm.Average_review_rating = 5
                    if int(gg) == int(bb):
                        cm.Average_review_rating = 4
                    if int(gg) == int(cc):
                        cm.Average_review_rating = 3
                    if int(gg) == int(dd):
                        cm.Average_review_rating = 2
                    if int(gg) == int(ee):
                        cm.Average_review_rating = 1
                    cm.Num_of_reviews = cnn
                    cm.save()
                    for i in g:
                        delta = datetime.datetime.now().date() - i.Enrollment_date
                        d = int(delta.days)
                        mkn = Registration.objects.get(Email=i.Teacher_email)
                        df = Subject.objects.filter(Subject_title=i.Subject_name, Course_title=i.Course_name,Sub_reg=mkn)
                        for u in df:
                            st = int(u.Course_duration)
                            st1 = st - d
                            i.Pending_days = st1
                            i.save()
                            break
                    return redirect('teacher_home')

                elif usertype == 'student':
                    request.session['logg'] = user_id
                    g = Enrollment.objects.all()
                    mhp = Registration.objects.get(id = request.session['logg'])
                    dt = Enrollment.objects.filter(enrol_reg = mhp)
                    pas = Learning_progress.objects.filter(Learn_p_reg = mhp)
                    pasq = []
                    for e in pas:
                        pasq.append(e.Course_name)
                    cxz = []
                    for x in pas:
                        if (x.Status == 'P') and (x.Course_name not in cxz):
                            cxz.append(x.Course_name)
                    for u in dt:
                        if (u.Course_name not in cxz) and (u.Course_name not in pasq):
                            cxz.append(u.Course_name)
                    cbx = []
                    for h in dt:
                        if (h.Course_name not in cxz) and (h.Course_name not in cbx):
                            cbx.append(h.Course_name)
                    cuz = 0
                    for z in cbx:
                        cuz += 1
                    mhp.Num_of_courses_completed = cuz
                    fdt = 0
                    for s in dt:
                        fdt += 1
                    mhp.Num_of_courses_enrolled = fdt
                    mhp.save()
                    for i in g:
                        delta = datetime.datetime.now().date() - i.Enrollment_date
                        d = int(delta.days)
                        mkn = Registration.objects.get(Email = i.Teacher_email)
                        df = Subject.objects.filter(Subject_title = i.Subject_name, Course_title = i.Course_name, Sub_reg = mkn.id)
                        for u in df:
                            st = int(u.Course_duration)
                            st1 = st - d
                            i.Pending_days = st1
                            i.save()
                            break
                    return redirect('student_home')
                else:
                    messages.success(request, 'Your access to the website is blocked. Please contact admin')
                    return render(request, 'login.html')
        else:
            messages.success(request, 'Username or password entered is incorrect')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')




def student(request) :
    return render(request,'student_home.html')


def teacher_home(request):
    return render(request,'teacher_home.html')


@login_required
def admin_home(request) :
    return render(request, 'admin_home.html')



def approval_reject(request) :
    return render(request, 'approval_reject')


def blogs_admin(request):
    dm = Blogs.objects.all()
    return render(request,'blogs_admin.html',{'dm':dm})


def blog_approves(request,ds):
    sas = Blogs.objects.get(id=ds)
    sas.Approval_status = 'Approved'
    sas.save()
    dm = Blogs.objects.all()
    return render(request, 'blogs_admin.html', {'dm': dm})


def blog_rejects(request, df):
    sas = Blogs.objects.get(id=df)
    sas.Approval_status = 'Rejected'
    sas.save()
    dm = Blogs.objects.all()
    return render(request, 'blogs_admin.html', {'dm': dm})


def blog_delete(request, dg):
    Blogs.objects.get(id=dg).delete()
    dm = Blogs.objects.all()
    return render(request, 'blogs_admin.html', {'dm': dm})

def view_blog(request):
    dc = Blogs.objects.filter(Approval_status = 'Approved')
    return render(request,'display_blog.html',{'dc':dc})


def contact(request):
    m = Registration.objects.get(User_role = 'admin')
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        t_a = request.POST.get('t_a')
        g = Messages()
        g.Category = 'guest'
        g.Name = name
        g.From_email = email
        g.To_email = m.Email
        g.Message_content = t_a
        g.save()
        messages.success(request, 'Message sent successfully')
        return redirect('home')
    return render(request,'contact.html')


def g_m(request):
    bb = Messages.objects.filter(Category = 'guest')
    return render(request,'guest_message.html',{'bb':bb})


def delete_g_msg(request,k):
    Messages.objects.get(id=k).delete()
    bb = Messages.objects.filter(Category = 'guest')
    messages.success(request, 'Message deleted successfully')
    return render(request, 'guest_message.html',{'bb':bb})



def update_pr_tr(request):
    bb = Registration.objects.get(id = request.session['logg'])
    um = User.objects.get(email = bb.Email)
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pasw = request.POST.get('psw')
        qual = request.POST.get('qual')
        intro = request.POST.get('intro')
        user_name = request.POST.get('user_name')
        m = User.objects.all().exclude(username = um.username)

        for t in m:
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'update_pr_tr.html', {'bb': bb,'um':um})


        passwords = make_password(pasw)
        u = User.objects.get(email = bb.Email)
        u.password = passwords
        u.username = user_name
        u.email = email
        u.save()

        user = auth.authenticate(username=user_name, password=pasw)
        auth.login(request, user)

        if Enrollment.objects.filter(Teacher_email = bb.Email).exists():
            kj = Enrollment.objects.filter(Teacher_email = bb.Email)
            for t in kj:
                t.Teacher_email = email
                t.Teacher_name = f_name+' '+l_name
                t.save()
        nbn = bb.First_name+' '+bb.Last_name
        if Exam.objects.filter(Teacher_name = nbn).exists():
            kj = Exam.objects.filter(Teacher_name = nbn)
            for t in kj:
                t.Teacher_name = f_name+' '+l_name
                t.save()
        if Exam_results.objects.filter(Teacher_name = nbn).exists():
            kj = Exam_results.objects.filter(Teacher_name = nbn)
            for t in kj:
                t.Teacher_name = f_name+' '+l_name
                t.save()
        if Feedback.objects.filter(Teacher_email = bb.Email).exists():
            kj = Feedback.objects.filter(Teacher_email = bb.Email)
            for t in kj:
                t.Teacher_name = f_name+' '+l_name
                t.Teacher_email = email
                t.save()
        kj = Messages.objects.all()
        for t in kj:
            if t.From_email == bb.Email:
                t.From_email = email
                t.save()
            if t.To_email == bb.Email:
                t.To_email = email
                t.save()
        kj = Requests.objects.all()
        for t in kj:
            if t.Email == bb.Email:
                t.Email = email
                t.save()

        b = bb.id
        m = int(b)
        request.session['logg'] = m

        try:
            imgg1 = request.FILES['imgg1']
            fs = FileSystemStorage()
            fs.save(imgg1.name,imgg1)
            enrol = request.POST.get('enrol')
            bb.First_name = f_name
            bb.Last_name = l_name
            bb.Email = email
            bb.Password = pasw
            bb.Qualification = qual
            bb.Introduction_brief = intro
            bb.Image = imgg1
            bb.Num_of_enrolled_students = enrol
            bb.user = u
            bb.save()
            messages.success(request, 'Updated successfully')
            return redirect('teacher_home')
        except:
            imgg2 = request.POST.get('imgg2')
            enrol = request.POST.get('enrol')
            bb.First_name = f_name
            bb.Last_name = l_name
            bb.Email = email
            bb.Password = pasw
            bb.Qualification = qual
            bb.Introduction_brief = intro
            bb.Image = imgg2
            bb.Num_of_enrolled_students = enrol
            bb.user = u
            bb.save()
            messages.success(request, 'Updated successfully')
            return redirect('teacher_home')
    return render(request, 'update_pr_tr.html', {'bb': bb,'um':um})



def update_pr_st(request):
    bb = Registration.objects.get(id = request.session['logg'])
    um = User.objects.get(email = bb.Email)
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pasw = request.POST.get('psw')
        qual = request.POST.get('qual')
        intro = request.POST.get('intro')
        user_name = request.POST.get('user_name')
        m = User.objects.all().exclude(username = um.username)

        for t in m:
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'update_pr_st.html', {'bb': bb,'um':um})


        passwords = make_password(pasw)
        u = User.objects.get(email = bb.Email)
        u.password = passwords
        u.username = user_name
        u.email = email
        u.save()

        user = auth.authenticate(username=user_name, password=pasw)
        auth.login(request, user)

        if Enrollment.objects.filter(Teacher_email = bb.Email).exists():
            kj = Enrollment.objects.filter(Teacher_email = bb.Email)
            for t in kj:
                t.Teacher_email = email
                t.Teacher_name = f_name+' '+l_name
                t.save()
        nbn = bb.First_name+' '+bb.Last_name
        if Exam.objects.filter(Teacher_name = nbn).exists():
            kj = Exam.objects.filter(Teacher_name = nbn)
            for t in kj:
                t.Teacher_name = f_name+' '+l_name
                t.save()
        if Exam_results.objects.filter(Teacher_name = nbn).exists():
            kj = Exam_results.objects.filter(Teacher_name = nbn)
            for t in kj:
                t.Teacher_name = f_name+' '+l_name
                t.save()
        if Feedback.objects.filter(Teacher_email = bb.Email).exists():
            kj = Feedback.objects.filter(Teacher_email = bb.Email)
            for t in kj:
                t.Teacher_name = f_name+' '+l_name
                t.Teacher_email = email
                t.save()
        kj = Messages.objects.all()
        for t in kj:
            if t.From_email == bb.Email:
                t.From_email = email
                t.save()
            if t.To_email == bb.Email:
                t.To_email = email
                t.save()
        kj = Requests.objects.all()
        for t in kj:
            if t.Email == bb.Email:
                t.Email = email
                t.save()

        b = bb.id
        m = int(b)
        request.session['logg'] = m

        try:
            imgg1 = request.FILES['imgg1']
            fs = FileSystemStorage()
            fs.save(imgg1.name,imgg1)
            enrol = request.POST.get('enrol')
            bb.First_name = f_name
            bb.Last_name = l_name
            bb.Email = email
            bb.Password = pasw
            bb.Qualification = qual
            bb.Introduction_brief = intro
            bb.Image = imgg1
            bb.Num_of_enrolled_students = enrol
            bb.user = u
            bb.save()
            messages.success(request, 'Updated successfully')
            return redirect('teacher_home')
        except:
            imgg2 = request.POST.get('imgg2')
            enrol = request.POST.get('enrol')
            bb.First_name = f_name
            bb.Last_name = l_name
            bb.Email = email
            bb.Password = pasw
            bb.Qualification = qual
            bb.Introduction_brief = intro
            bb.Image = imgg2
            bb.Num_of_enrolled_students = enrol
            bb.user = u
            bb.save()
            messages.success(request, 'Updated successfully')
            return redirect('teacher_home')
    return render(request, 'update_pr_st.html', {'bb': bb,'um':um})




def adm_prof(request):
    gtt = Registration.objects.filter(User_role = 'admin')
    return render(request, 'update_admin.html',{'gtt':gtt})


def del_admin(request, dk):
    Registration.objects.get(id = dk).delete()
    messages.success(request, 'You have successfully resigned from administration')
    return redirect('home')

def edit_admin(request):
    bb1 = Registration.objects.get(User_role = 'admin')
    um = User.objects.get(email=bb1.Email)
    return render(request, 'update_admin1.html',{'bb1':bb1,'um':um})

def bnb(request):
    bb1 = Registration.objects.get(User_role='admin')
    um = User.objects.get(email=bb1.Email)
    if request.method == 'POST':
        first = request.POST.get('first')
        last = request.POST.get('last')
        em = request.POST.get('em')
        psw = request.POST.get('psw')

        user_name = request.POST.get('user_name')
        m = User.objects.all().exclude(username = um.username)

        for t in m:
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'update_admin1.html',{'bb1':bb1,'um':um})

        passwor = make_password(psw)
        df = Registration.objects.get(id=request.session['logg'])
        kmk = df.user.pk
        kmk = User.objects.get(id=kmk)
        kmk.password = passwor
        kmk.email = em
        kmk.save()

        dcd = Registration.objects.get(User_role = 'admin')
        dcd.Email = em
        dcd.Password = psw
        dcd.First_name = first
        dcd.Last_name = last
        dcd.user = kmk
        dcd.save()
        gtt = Registration.objects.filter(User_role='admin')
        messages.success(request, 'You have successfully updated your profile')
        return render(request, 'update_admin.html', {'gtt': gtt})
    else:
        return render(request, "admin_home.html")



def subject_tr(request):
   dd = Subject.objects.filter(Sub_reg = request.session['logg'])
   a = []
   b = []
   c = []
   d = []
   e = []
   f = []
   g = []
   h = []
   for i in dd:
       if i.Course_title not in a:
           a.append(i.Course_title)
           b.append(i.Subject_title)
           c.append(i.Course_brief)
           d.append(i.Course_duration)
           e.append(i.Num_of_chapters)
           f.append(i.Course_fee)
           g.append(i.Language)
           h.append(i.id)
   hh = zip(a,b,c,d,e,f,g,h)

   return render(request,'sub_tr.html',{'hh':hh})


def edit_subject(request, id, idd, idm):
    idm = int(idm)
    id = str(id)
    idd = str(idd)
    gh = Subject.objects.get(id = idm)
    ddr = Subject.objects.filter(Sub_reg = request.session['logg'], Subject_title = id, Course_title = idd)
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_b = request.POST.get('c_b')
        c_d = request.POST.get('c_d')
        n_c = request.POST.get('n_c')
        c_f = request.POST.get('c_f')
        lan = request.POST.get('lan')
        for w in ddr:
            w.Subject_title = sub
            w.Course_title = cou
            w.Course_brief = c_b
            w.Course_duration = c_d
            w.Num_of_chapters = n_c
            w.Course_fee  = c_f
            w.Language  = lan
            w.save()
        dd = Subject.objects.filter(Sub_reg = request.session['logg'])
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        g = []
        h = []
        for i in dd:
            if i.Course_title not in a:
                a.append(i.Course_title)
                b.append(i.Subject_title)
                c.append(i.Course_brief)
                d.append(i.Course_duration)
                e.append(i.Num_of_chapters)
                f.append(i.Course_fee)
                g.append(i.Language)
                h.append(i.id)
        hh = zip(a, b, c, d, e, f, g, h)
        messages.success(request, 'Subject edited successfully')
        return render(request, 'sub_tr.html', {'hh': hh})
    return render(request,'edit_subject.html',{'gh':gh})


def delete_subject(request, id, idd, idm):
    idm = int(idm)
    id = str(id)
    idd = str(idd)
    dd = Subject.objects.filter(Sub_reg=request.session['logg'])
    Subject.objects.filter(Sub_reg=request.session['logg'], Subject_title=id, Course_title=idd).delete()

    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    g = []
    h = []
    for i in dd:
        if i.Course_title not in a:
            a.append(i.Course_title)
            b.append(i.Subject_title)
            c.append(i.Course_brief)
            d.append(i.Course_duration)
            e.append(i.Num_of_chapters)
            f.append(i.Course_fee)
            g.append(i.Language)
            h.append(i.id)
    hh = zip(a, b, c, d, e, f, g, h)
    messages.success(request, 'Subject deleted successfully')
    return render(request, 'sub_tr.html', {'hh': hh})


def add_subject(request):
    if request.method == 'POST':
        sub_tit = request.POST.get('sub_tit')
        cou_tit = request.POST.get('cou_tit')
        rt = Subject.objects.filter(Sub_reg = request.session['logg'])
        for u in rt:
            if u.Subject_title == sub_tit and u.Course_title == cou_tit:
                dd = Subject.objects.filter(Sub_reg = request.session['logg'])
                a = []
                b = []
                c = []
                d = []
                e = []
                f = []
                g = []
                h = []
                for i in dd:
                    if i.Course_title not in a:
                        a.append(i.Course_title)
                        b.append(i.Subject_title)
                        c.append(i.Course_brief)
                        d.append(i.Course_duration)
                        e.append(i.Num_of_chapters)
                        f.append(i.Course_fee)
                        g.append(i.Language)
                        h.append(i.id)
                hh = zip(a, b, c, d, e, f, g, h)
                messages.success(request, 'Subject already exists')
                return render(request, 'sub_tr.html', {'hh': hh})
        c_b1 = request.POST.get('c_b1')
        c_d1 = request.POST.get('c_d1')
        n_c1 = request.POST.get('n_c1')
        c_f1 = request.POST.get('c_f1')
        lang = request.POST.get('lang')
        pk = Registration.objects.get(id = request.session['logg'])
        cdt = Subject()
        cdt.Subject_title = sub_tit
        cdt.Course_title = cou_tit
        cdt.Course_brief = c_b1
        cdt.Course_duration = c_d1
        cdt.Num_of_chapters = n_c1
        cdt.Course_fee = c_f1
        cdt.Chapter_title = 'Nil'
        cdt.Num_of_videos = 0
        cdt.Num_of_paragraphs = 0
        cdt.Num_of_images = 0
        cdt.Num_of_assignments = 0
        cdt.Chapter_Content_name = 'Nil'
        cdt.Chapter_Content_type = 'Nil'
        cdt.Chapter_Content_Is_mandatory = 0
        cdt.Chapter_Content_Time_required_in_sec = 0
        cdt.Chapter_Content_Is_open_for_free = 0
        cdt.Language = lang
        cdt.Sub_reg = pk
        cdt.save()
        dd = Subject.objects.filter(Sub_reg=request.session['logg'])
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        g = []
        h = []
        for i in dd:
            if i.Course_title not in a:
                a.append(i.Course_title)
                b.append(i.Subject_title)
                c.append(i.Course_brief)
                d.append(i.Course_duration)
                e.append(i.Num_of_chapters)
                f.append(i.Course_fee)
                g.append(i.Language)
                h.append(i.id)
        hh = zip(a, b, c, d, e, f, g, h)
        messages.success(request, 'Added subject successfully')
        return render(request, 'sub_tr.html', {'hh': hh})
    return render(request,'add_subject.html')


def chapter_tr(request):
    dm = Subject.objects.filter(Sub_reg = request.session['logg'])
    a = []
    b = []
    c = []
    d = []
    e = []
    for i in dm:
        if i.Chapter_title not in c:
            a.append(i.Subject_title)
            b.append(i.Course_title)
            c.append(i.Chapter_title)
            d.append(i.Num_of_assignments)
            e.append(i.id)
    lenn = len(a)
    for z in range(lenn):
        kpk = len(a)
        r = int(z)
        r += 1
        try:
            aa = a[z]
        except:
            break
        bb = b[z]
        cc = c[z]
        for k in range(lenn):
            if int(r) >= int(kpk):
                continue
            try:
                if a[r] == aa and b[r] == bb and c[r] == cc:
                    del a[r]
                    del b[r]
                    del c[r]
                    del d[r]
                    del e[r]
                    r -= 1
                r += 1
            except:
                break
    hh = zip(a, b, c, d, e)
    return render(request, 'chap_tr.html', {'hh': hh})


def edit_chapter(request, id, idd, idk, idm):
    idm = int(idm)
    id = str(id)
    idd = str(idd)
    idk = str(idk)
    dmr = Subject.objects.filter(Sub_reg = request.session['logg'], Subject_title = id, Course_title = idd, Chapter_title = idk)
    gh = Subject.objects.get(id = idm)
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_tt = request.POST.get('c_tt')
        n_s = request.POST.get('n_s')
        for m in dmr:
            m.Subject_title = sub
            m.Course_name = cou
            m.Chapter_title = c_tt
            m.Num_of_assignments = n_s
            m.save()

        dm = Subject.objects.filter(Sub_reg=request.session['logg'])
        a = []
        b = []
        c = []
        d = []
        e = []
        for i in dm:
            if i.Chapter_title not in c:
                a.append(i.Subject_title)
                b.append(i.Course_title)
                c.append(i.Chapter_title)
                d.append(i.Num_of_assignments)
                e.append(i.id)
        hh = zip(a, b, c, d, e)
        messages.success(request, 'Chapter edited successfully')
        return render(request, 'chap_tr.html', {'hh': hh})
    return render(request,'edit_chapter.html',{'gh':gh})


def delete_chapter(request, id, idd, idk, idm):
    idm = int(idm)
    id = str(id)
    idd = str(idd)
    idk = str(idk)
    Subject.objects.filter(Sub_reg = request.session['logg'], Subject_title = id, Course_title = idd, Chapter_title = idk).delete()
    dm = Subject.objects.filter(Sub_reg = request.session['logg'])
    a = []
    b = []
    c = []
    d = []
    e = []
    for i in dm:
        if i.Chapter_title not in c:
            a.append(i.Subject_title)
            b.append(i.Course_title)
            c.append(i.Chapter_title)
            d.append(i.Num_of_assignments)
            e.append(i.id)
    hh = zip(a, b, c, d, e)
    messages.success(request, 'Chapter deleted successfully')
    return render(request, 'chap_tr.html', {'hh': hh})

def add_chapter(request):
    dm = Subject.objects.filter(Sub_reg = request.session['logg'])
    rr = Registration.objects.get(id = request.session["logg"])
    kk = []
    for i in dm:
        if i.Subject_title not in kk:
            kk.append(i.Subject_title)
    if request.method == 'POST':
        cou_tit = request.POST.get('cou_tit1')
        sub_tit = request.session['subj_n']
        ch_tit1 = request.POST.get('ch_tit1')
        assi = request.POST.get('assi')
        cdt = Subject()
        for u in dm:
            if u.Subject_title == sub_tit and u.Course_title == cou_tit and u.Chapter_title == ch_tit1:
                a = []
                b = []
                c = []
                d = []
                e = []
                for i in dm:
                    if i.Chapter_title not in c:
                        a.append(i.Subject_title)
                        b.append(i.Course_title)
                        c.append(i.Chapter_title)
                        d.append(i.Num_of_assignments)
                        e.append(i.id)
                hh = zip(a, b, c, d, e)
                messages.success(request, 'Chapter already exists')
                return render(request, 'chap_tr.html', {'hh': hh})




        cdt.Subject_title = sub_tit
        cdt.Course_title = cou_tit
        cdt.Course_brief = 'Nil'
        cdt.Course_duration = 0
        cdt.Num_of_chapters = 0
        cdt.Course_fee = 0.0
        cdt.Language = 'Nil'
        cdt.Chapter_title  = ch_tit1
        cdt.Num_of_assignments = assi
        cdt.Chapter_Content_name = 'Nil'
        cdt.Chapter_Content_type = 'Nil'
        cdt.Chapter_Content_Is_mandatory = 0
        cdt.Chapter_Content_Time_required_in_sec = 0
        cdt.Chapter_Content_Is_open_for_free = 0
        cdt.Sub_reg = rr
        cdt.save()
        dm = Subject.objects.filter(Sub_reg=request.session['logg'])

        a = []
        b = []
        c = []
        d = []
        e = []
        for i in dm:
            if i.Chapter_title not in c:
                a.append(i.Subject_title)
                b.append(i.Course_title)
                c.append(i.Chapter_title)
                d.append(i.Num_of_assignments)
                e.append(i.id)
        hh = zip(a, b, c, d, e)
        messages.success(request, 'Chapter added successfully')
        return render(request, 'chap_tr.html', {'hh': hh})
    return render(request,'add_chapter.html',{'kk':kk})


def add_chapter1(request):
   gg = request.POST.get('subj')
   gg1 = Subject.objects.filter(Subject_title = gg, Sub_reg = request.session['logg'])
   mm = []
   for y in gg1:
       if y.Course_title not in mm:
           mm.append(y.Course_title)
   request.session['subj_n'] = gg
   return render(request,'add_chapter2.html',{'gg1':gg1,'mm':mm})


def ch_co_tr(request):
    mm = Registration.objects.get(id = request.session['logg'])
    mm1 = Subject.objects.filter(Sub_reg = mm)
    return render(request, 'cont_tr.html', {'mm1': mm1})


def edit_content(request, y):
    mm = Registration.objects.get(id = request.session['logg'])
    mm1 = Subject.objects.filter(Sub_reg = mm)
    gh = Subject.objects.get(id = y)
    if request.method == 'POST':
        try:
            sub = request.POST.get('sub')
            cou = request.POST.get('cou')
            c_n1 = request.POST.get('c_n')
            c_b1 = request.POST.get('c_b')
            up_cont = request.FILES['up_cont']
            fs = FileSystemStorage()
            fs.save(up_cont.name, up_cont)
            s1 = request.POST.get('s1')
            s = request.POST.get('s')
            time = request.POST.get('time')
            cont_typ = request.POST.get('cont_typ')
            gh.Subject_title = sub
            gh.Course_title = cou
            gh.Chapter_title = c_n1
            if int(cont_typ) == 1:
                gh.Chapter_Content_type = 'Image'
            if int(cont_typ) == 2:
                gh.Chapter_Content_type = 'Text'
            if int(cont_typ) == 3:
                gh.Chapter_Content_type = 'Video'
            gh.Chapter_Content_Is_mandatory  = s
            gh.Chapter_Content_Time_required_in_sec  = time
            gh.Chapter_Content_Is_open_for_free  = s1
            gh.Chapter_Content_name = up_cont
            gh.Chapter_text_content = c_b1
            gh.save()
            messages.success(request, 'Chapter content edited successfully')
            return render(request, 'cont_tr.html', {'mm1': mm1})
        except:
            sub = request.POST.get('sub')
            cou = request.POST.get('cou')
            c_n1 = request.POST.get('c_n')
            c_b1 = request.POST.get('c_b')
            u_con = request.POST.get('u_con')
            s = request.POST.get('s')
            time = request.POST.get('time')
            s1 = request.POST.get('s1')
            cont_typ = request.POST.get('cont_typ')
            gh.Subject_title = sub
            gh.Course_title = cou
            gh.Chapter_title = c_n1
            if int(cont_typ) == 1:
                gh.Chapter_Content_type = 'Image'
            if int(cont_typ) == 2:
                gh.Chapter_Content_type = 'Text'
            if int(cont_typ) == 3:
                gh.Chapter_Content_type = 'Video'
            gh.Chapter_Content_Is_mandatory = s
            gh.Chapter_Content_Time_required_in_sec = time
            gh.Chapter_Content_Is_open_for_free = s1
            gh.Chapter_Content_name = u_con
            gh.Chapter_text_content = c_b1
            gh.save()
            messages.success(request, 'Chapter content edited successfully')
            return render(request, 'cont_tr.html', {'mm1': mm1})
    return render(request, 'edit_content.html', {'gh': gh})



def delete_content(request, id):
    mm = Registration.objects.get(id = request.session['logg'])
    mm1 = Subject.objects.filter(Sub_reg = mm)
    Subject.objects.get(id = id).delete()
    messages.success(request, 'Chapter content deleted successfully')
    return render(request, 'cont_tr.html',{'mm1': mm1})

def add_ch_con(request):
    mm = Registration.objects.get(id = request.session['logg'])
    mm1 = Subject.objects.filter(Sub_reg = mm)
    kkc = Subject.objects.filter(Sub_reg = request.session['logg'])
    kk = []
    for i in kkc:
        if i.Subject_title not in kk:
            kk.append(i.Subject_title)
    if request.method == 'POST':
        sub_tit = request.session['subj_nn']
        sel_c = request.session['court0']
        tex_con = request.POST.get('tex_con')
        ch_tit1 = request.POST.get('ch_tit1')
        fg = Subject.objects.filter(Course_title=sel_c, Subject_title=sub_tit, Chapter_title = ch_tit1, Sub_reg=mm)
        up_c = request.FILES['up_c']
        fs = FileSystemStorage()
        fs.save(up_c.name, up_c)
        s1 = request.POST.get('s1')
        s = request.POST.get('s')
        time = request.POST.get('time')
        cont_typ = request.POST.get('cont_typ')
        for y in fg:
            cdt = Subject()
            cv = int(cont_typ)
            if cv == 1:
                cdt.Chapter_Content_type = 'Image'
            if cv == 2:
                cdt.Chapter_Content_type = 'Text'
            if cv == 3:
                cdt.Chapter_Content_type = 'Video'
            cdt.Subject_title = sub_tit
            cdt.Course_title = y.Course_title
            cdt.Course_brief = y.Course_brief
            cdt.Num_of_chapters = y.Num_of_chapters
            cdt.Course_fee = y.Course_fee
            cdt.Language = y.Language
            cdt.Num_of_assignments = y.Num_of_assignments
            cdt.Chapter_title  = ch_tit1
            cdt.Chapter_Content_name  = up_c
            cdt.Chapter_text_content = tex_con
            cdt.Chapter_Content_Is_mandatory = s
            cdt.Chapter_Content_Time_required_in_sec = time
            cdt.Chapter_Content_Is_open_for_free = s1
            cdt.Course_duration = time
            cdt.Sub_reg = mm
            cdt.save()
            messages.success(request, 'Chapter content added successfully')
            return render(request, 'cont_tr.html', {'mm1': mm1})
    return render(request,'add_chapter_content.html',{'kk':kk})


def add_chapter_c0(request):
    gg = request.session['subj_nn'] = request.POST.get('subj')
    bbm = Subject.objects.filter(Sub_reg=request.session['logg'], Subject_title=gg)
    bb = []
    for i in bbm:
        if i.Course_title not in bb:
            bb.append(i.Course_title)
    return render(request, 'add_chapter_c0.html', {'bb': bb})


def add_chapter_c1(request):
    gg = request.session['subj_nn']
    request.session['court0'] = request.POST.get('cou')
    gg = str(gg)
    bbm = Subject.objects.filter(Sub_reg = request.session['logg'], Subject_title = gg, Course_title = request.session['court0'])
    kk = []
    for i in bbm:
        if i.Chapter_title not in kk:
            kk.append(i.Chapter_title)
    return render(request, 'add_chapter_c2.html', {'gg': gg,'kk':kk})


def stu_sub_selnew(request):
    sne = Subject.objects.all()
    snew = []
    for i in sne:
        if i.Subject_title not in snew:
            snew.append(i.Subject_title)
    return render(request, 'st_sub_selnew1.html',{'snew':snew})


def st_sub_selnew2(request):
    d = request.POST.get('subj')
    request.session['sub_n'] = d
    sneww = Subject.objects.filter(Subject_title = d)
    snew1 = []
    for i in sneww:
        if i.Course_title not in snew1:
            snew1.append(i.Course_title)
    return render(request, 'st_sub_selnew2.html', {'snew1': snew1})


def disp_teach(request):
    couu = request.POST.get('cou')
    request.session['course'] = couu
    drt = Subject.objects.filter(Subject_title = request.session['sub_n'], Course_title = couu)
    gh = Registration.objects.filter(User_role = 'teacher')
    fir = []
    las = []
    em =[]
    qual = []
    intr_br =[]
    imgg = []
    avgg = []
    idd =[]
    co_br = []
    co_dur = []
    num_ch = []
    co_fee = []
    lan = []
    for i in drt:
        for k in gh:
            if (i.Sub_reg == k) and (k.id not in idd):
                fir.append(k.First_name)
                las.append(k.Last_name)
                em.append(k.Email)
                qual.append(k.Qualification)
                intr_br.append(k.Introduction_brief)
                imgg.append(k.Image)
                avgg.append(k.Average_review_rating)
                idd.append(k.id)
                co_br.append(i.Course_brief)
                co_dur.append(i.Course_duration)
                num_ch.append(i.Num_of_chapters)
                co_fee.append(i.Course_fee)
                lan.append(i.Language)
    ds = zip(fir,las,em,qual,intr_br,imgg,avgg,idd,co_br,co_dur,num_ch,co_fee,lan)
    return render(request,'st_sub_selnew.html',{'ds':ds})


def stu_buk_teacherr(request, d):
    request.session['paid'] = d
    return render(request,'paid.html')


def stu_buk_teacher(request):
    paidd = request.POST.get('paid')
    dh = Registration.objects.get(id = request.session['logg'])
    nm = Registration.objects.get(id = request.session['paid'])

    if Enrollment.objects.filter(Student_email=dh.Email, Subject_name=request.session['sub_n'],
                                 Course_name=request.session['course'], Teacher_email=nm.Email).exists():
        messages.success(request, 'You have already booked this course')
        return render(request, 'paid.html')

    gg = Subject.objects.filter(Sub_reg = nm.id, Course_title = request.session['course'], Subject_title = request.session['sub_n'])
    spp = Enrollment()
    spp.Student_name = dh.First_name
    spp.Student_email = dh.Email
    spp.Subject_name = request.session['sub_n']
    spp.Course_name = request.session['course']
    spp.Teacher_name = nm.First_name+' '+nm.Last_name
    spp.Teacher_email = nm.Email
    for i in gg:
        if float(i.Course_fee) > float(paidd):
            messages.success(request, 'Please pay full amount')
            return render(request,'paid.html')
    spp.Paid_amount = paidd
    spp.Attendance = 0
    spp.Pending_days = 0
    spp.Teacher_response = 'To be expected'
    spp.notify = 'new'
    for i in gg:
        if i.Course_fee > 0:
            spp.Is_paid_subscription = 'True'
        else:
            spp.Is_paid_subscription = 'False'
    spp.enrol_reg = dh
    spp.save()
    messages.success(request, 'You have successfully booked a course')
    return render(request,'student_home.html')


def stu_buk_acc(request):
    seww = Registration.objects.get(id = request.session['logg'])
    stzz = Enrollment.objects.filter(Teacher_email = seww.Email)
    return render(request,'stu_buk_acc.html',{'stzz':stzz})

def stu_accept(request, id):
    seww = Registration.objects.get(id=request.session['logg'])
    stzz = Enrollment.objects.filter(Teacher_email = seww.Email)
    sas = Enrollment.objects.get(id = id)
    sas.Teacher_response = 'Accepted'
    sas.save()
    return render(request,'stu_buk_acc.html',{'stzz':stzz})

def stu_reject(request, id):
    seww = Registration.objects.get(id = request.session['logg'])
    stzz = Enrollment.objects.filter(Teacher_email = seww.Email)
    sas = Enrollment.objects.get(id=id)
    sas.Teacher_response = 'Rejected'
    sas.save()
    return render(request, 'stu_buk_acc.html', {'stzz': stzz})

def stu_delete(request, id):
    Enrollment.objects.get(id = id).delete()
    seww = Registration.objects.get(id=request.session['logg'])
    stzz = Enrollment.objects.filter(Teacher_email=seww.Email)
    messages.success(request, 'Enrolled student deleted successfully')
    return render(request, 'stu_buk_acc.html', {'stzz': stzz})


def notiffy(request):
    stzz = Enrollment.objects.filter(Teacher_email = request.session['teacher'])
    for y in stzz:
        if y.notify == 'new':
            y.notify = ''
            y.save()
    return redirect('teacher_home')


def st_book_courses(request):
    st = Registration.objects.get(id = request.session['logg'])
    buk = Enrollment.objects.filter(enrol_reg = st)
    return render(request, 'st_book_courses.html',{'buk':buk,'st':st})


def acc_chapter(request, id, ikm, sub):
    request.session['courss'] = str(ikm)
    request.session['subb'] = str(sub)
    gh = Enrollment.objects.get(id = id)
    if gh.Teacher_response == 'To be expected' or gh.Teacher_response == 'Rejected':
        messages.success(request, 'Please wait for approval')
        return render(request, 'student_home.html')
    nn = Registration.objects.get(Email = gh.Teacher_email)
    request.session['tch_idd'] = nn.id
    dm = Subject.objects.filter(Subject_title = request.session['subb'], Course_title = request.session['courss'], Sub_reg = nn.id)
    for i in dm:
        if i.Course_fee > gh.Paid_amount:
            messages.success(request, 'Your payment balance is pending')
            return render(request, 'student_home.html')
    fd = []
    for i in dm:
        if i.Chapter_title not in fd:
            fd.append(i.Chapter_title)
    return render(request, 'acc_chapter1.html', {'fd':fd})



def acc_chapter1(request):
    mnm = Registration.objects.get(id=request.session["logg"])
    request.session['cou_ch_nme'] = sz1 = request.POST.get('cha')
    sz = Subject.objects.filter(Subject_title = request.session['subb'], Course_title = request.session['courss'], Chapter_title = sz1, Sub_reg = request.session['tch_idd'])
    mj = Learning_progress.objects.filter(Student_name = mnm.First_name, Student_email = mnm.Email, Subject_name = request.session['subb'],Course_name = request.session['courss'], Course_chapter_name =  sz1)
    ch_con_nnme = []
    ch_txt_con_id = []
    ch_txt_con = []
    ch_cont_nmbe = []
    ch_cont_nmbe1 = []
    c_p = []
    for t in mj:
        if t.Course_chapter_content_name not in ch_con_nnme:
            ch_con_nnme.append(t.Course_chapter_content_name)
    for i in sz:
        ch_txt_con_id.append(i.id)
        ch_txt_con.append(i.Chapter_text_content)
        ch_cont_nmbe.append(i.Chapter_Content_name)
        ch_cont_nmbe1.append(i.Chapter_Content_name)
        if i.Chapter_Content_name not in ch_con_nnme:
            c_p.append('Pending')
            continue
        for m in mj:
            if i.Chapter_Content_name == m.Course_chapter_content_name:
                if m.Status == 'C':
                    c_p.append('Completed')
                else:
                    c_p.append('Pending')
    if not mj:
        c_p.append('Pending')

    ded = zip(ch_txt_con_id, ch_txt_con, ch_cont_nmbe, ch_cont_nmbe1,c_p)
    return render(request, 'acc_chapter2.html', {'ded': ded})


def compp(request):
    mnm = Registration.objects.get(id=request.session["logg"])
    idd = request.POST.getlist('id')
    comm = request.POST.getlist('comm')
    chap_cont = request.POST.getlist('chap_cont')
    ggt = zip(idd, comm, chap_cont)
    for i, h, w in ggt:
        df = Subject.objects.get(id=i)
        kmk = df.Sub_reg.pk
        kmk = Registration.objects.get(id=kmk)
        try:
            pk = Learning_progress.objects.get(Student_name=mnm.First_name, Student_email=mnm.Email,
                                               Subject_name=request.session['subb'],
                                               Course_name=request.session['courss'],
                                               Course_chapter_name=request.session['cou_ch_nme'],
                                               Teacher_email=kmk.Email, Course_chapter_content_name=w)
            pk.Status = h
            pk.save()
        except:
            pk = Learning_progress()
            pk.Student_name = mnm.First_name
            pk.Student_email = mnm.Email
            pk.Subject_name = df.Subject_title
            pk.Course_name = df.Course_title
            pk.Teacher_email = kmk.Email
            pk.Course_chapter_name = df.Chapter_title
            pk.Course_chapter_content_name = df.Chapter_Content_name
            pk.Status = h
            pk.Learn_p_reg = mnm
            pk.save()
    messages.success(request, 'Learning progress updated')
    return render(request, 'student_home.html')


def st_pr(request):
    vc = Registration.objects.get(id = request.session['logg'])
    hgh1 = Enrollment.objects.filter(Teacher_email = vc.Email)
    hgh = []
    for i in hgh1:
        if i.Student_email not in hgh:
            hgh.append(i.Student_email)
    dd = Learning_progress.objects.filter(Teacher_email = vc.Email)
    return render(request,'student_progress.html',{'dd':dd,'hgh':hgh})


def sched_test(request):
    sew = Registration.objects.get(id = request.session['logg'])
    stz = Enrollment.objects.filter(Teacher_email = sew.Email, Teacher_response = 'Accepted')
    return render(request, 'sched_test.html', {'stz': stz})

def sched_test1(request):
    numbb = request.POST.get('numbb')
    nmbb = int(numbb)
    request.session['exam_start'] = dtt = request.POST.get('dtt')
    request.session['exam_stop'] = stt = request.POST.get('stt')
    request.session['cc'] = nmbb
    k = request.POST.getlist('scd')
    request.session['stu_for_test'] = k
    return render(request,'sched_test2.html')

def sched_test3(request):
    m = request.session['stu_for_test']
    ques = request.POST.get('ques')
    op1 = request.POST.get('op1')
    op2 = request.POST.get('op2')
    op3 = request.POST.get('op3')
    ans = request.POST.get('ans')
    c = request.session['cc']
    if c>0:
        for i in m:
            stz = Enrollment.objects.get(id = i)
            fd = Exam()
            fd.Student_name = stz.Student_name
            fd.Student_email = stz.Student_email
            fd.Teacher_name = stz.Teacher_name
            fd.Subject_name = stz.Subject_name
            fd.Course_name = stz.Course_name
            fd.Option1 = op1
            fd.Option2 = op2
            fd.Option3 = op3
            fd.Correct_answer = ans
            fd.Question = ques

            drts = request.session['exam_start']
            drtd = drts.replace('T',' ')
            time_zone = pytz.timezone('Asia/Calcutta')
            drtd = datetime.datetime.strptime(drtd,"%Y-%m-%d %H:%M")
            fd.Time_start = time_zone.localize(drtd)

            drts1 = request.session['exam_stop']
            drtd1 = drts1.replace('T', ' ')
            time_zone = pytz.timezone('Asia/Calcutta')
            drtd1 = datetime.datetime.strptime(drtd1, "%Y-%m-%d %H:%M")
            fd.Time_stop = time_zone.localize(drtd1)

            dt = Registration.objects.get(id = request.session["logg"])
            fd.Exam_reg = dt
            fd.save()
        c -= 1
        request.session['cc'] = c
        if c == 0:
            messages.success(request, 'Exam scheduled successfully')
            return redirect('teacher_home')
        return render(request,'sched_test2.html')
    else:
        messages.success(request, 'Exam scheduled successfully')
        return redirect('teacher_home')

def ex_not(request):
    local_tz = pytz.timezone("Asia/Calcutta")
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Student_email = hh.Email)
    kk = []
    for i in fg:
        bb = i.Time_start
        cpp = bb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        bbn = cpp.strftime("%Y-%B-%d %H:%M:%S %p")
        if bbn not in kk:
            kk.append('Subject name')
            kk.append(i.Subject_name)
            kk.append('Course name')
            kk.append(i.Course_name)
            kk.append('Start time')
            ft = i.Time_start
            ftt = ft.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty = ftt.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty)
            kk.append('Stop time')
            fte = i.Time_stop
            ftee = fte.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty1 = ftee.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty1)
            send_mail('Exam alert','You have an exam on '+fty,'thannuksd@gmail.com',['thanveermuhammed55@gmail.com'],fail_silently=False)
    return render(request,'ex_not.html',{'kk':kk})


def start_test(request):
    local_tz = pytz.timezone("Asia/Calcutta")
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Student_email = hh.Email)
    fgc = timezone.now()
    hj = []
    for i in fg:
        zz = i.Time_start
        nb = i.Time_stop
        nbn = nb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        nbnn = nbn.strftime("%Y-%B-%d %I:%M:%S %p")
        nbnn1 = nbn.strftime("%b %d, %Y %H:%M:%S")

        mrtt = nb - zz
        mrtt = mrtt.total_seconds()
        mrtt = int(mrtt)
        mrtt *= 1000

        if fgc>zz and fgc<nb:
            nb = Exam.objects.filter(Student_email = hh.Email, Time_start__lte = fgc, Time_stop__gte = fgc)
            for i in nb:
                if i.Lock == 'locked':
                    messages.success(request, 'You have already attended the exam')
                    return render(request, 'student_home.html')
            for i in nb:
                hj.append(i.Correct_answer)
                request.session['teec'] = i.Teacher_name
                request.session['ssub'] = i.Subject_name
                request.session['student'] = i.Student_name
                request.session['student_ema'] = i.Student_email
                gg = str(nbnn)
            request.session['exam_id'] = hj
            return render(request,'start_test.html',{'nb':nb,'gg':gg,'nbnn1':nbnn1,'mrtt':mrtt})
    messages.success(request, 'No exam is scheduled now')
    return render(request, 'student_home.html')


def save_exam(request):
    end_time = request.POST.get('end_time')
    edr = datetime.datetime.strptime(end_time, '%Y-%B-%d %I:%M:%S %p')
    b = datetime.datetime.now()
    bb = b.strftime('%Y-%B-%d %H:%M:%S ')
    edr1 = datetime.datetime.strptime(bb, '%Y-%B-%d %H:%M:%S ')
    if edr < edr1:
        messages.success(request, 'You have timed out')
        return render(request, 'student_home.html')
    correct_answers = request.POST.getlist('exx3')
    answers = request.POST.getlist('exx')
    print(correct_answers)
    print (answers)
    if len(correct_answers) != len(answers):
        messages.success(request, 'Your exam attempt failed due to selecting multiple answers')
        return render(request,'student_home.html')
    count = 0
    count1 = 0
    for i in correct_answers:
        count1 += 1
    for i,j in zip(correct_answers,answers):
        if i == j:
            count += 1
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Student_email = hh.Email)
    fgc = timezone.now()
    for i in fg:
        zz = i.Time_start
        nb = i.Time_stop
        if fgc > zz and fgc < nb:
            nb = Exam.objects.filter(Student_email = hh.Email, Time_start__lte = fgc, Time_stop__gte = fgc)
            for i in nb:
                i.Lock = 'locked'
                i.save()
    ddd = Exam_results()
    ddd.Student_name = request.session['student']
    ddd.Student_email = request.session['student_ema']
    ddd.Teacher_name = request.session['teec']
    ddd.Subject_name = request.session['ssub']
    ddd.Total_marks = count1
    ddd.Acquired_marks = count
    avg = 100 * float(count)/float(count1)
    if avg >= 80:
        ddd.Grade = 'A'
    elif avg < 80 and avg >= 50 :
        ddd.Grade = 'B'
    elif avg < 50 and avg >= 30:
        ddd.Grade = 'C'
    else:
        ddd.Grade = 'Failed'
    ddd.Time_stop = b
    ddd.Exam_res_reg = hh
    ddd.save()
    messages.success(request, 'You have successfully finished your exam')
    return render(request, 'student_home.html')


def exam_result1(request):
    gt = Exam_results.objects.all()
    hh = Registration.objects.get(id = request.session['logg'])
    return render(request,'exam_result1.html',{'hh':hh,'gt':gt})

def exam_result(request):
    hh = Registration.objects.get(id = request.session['logg'])
    mnm = hh.First_name+' '+hh.Last_name
    gt = Exam_results.objects.filter(Teacher_name = mnm)
    return render(request,'exam_result.html',{'hh':hh,'gt':gt})

def delete_ex_re(request, k):
    Exam_results.objects.get(id=k).delete()
    hh = Registration.objects.get(id=request.session['logg'])
    mnm = hh.First_name + ' ' + hh.Last_name
    gt = Exam_results.objects.filter(Teacher_name = mnm)
    return render(request, 'exam_result.html', {'hh': hh, 'gt': gt})


def delete_test(request):
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Exam_reg = hh)
    return render(request, 'delete_test.html', {'fg': fg})

def delete_test1(request, m):
    Exam.objects.get(id = m).delete()
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Exam_reg = hh)
    return render(request, 'delete_test.html', {'fg': fg})


def m_m(request):
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email).exclude(Category='guest')
    return render(request,'message.html',{'bb':bb})

def del_msg_admin(request,id):
    Messages.objects.get(id = id).delete()
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    messages.success(request, 'Message deleted successfully')
    return render(request,'message.html',{'bb':bb})

def reply_msg_admin(request,id):
    pa = Messages.objects.get(id = id)
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    if request.method == 'POST':
        f_email = request.POST.get('f_email')
        to_email = request.POST.get('to_email')
        msg_cont = request.POST.get('msg_cont')
        pa1 = Messages()
        pa1.Category = p.User_role
        pa1.From_email = to_email
        pa1.To_email = f_email
        pa1.Message_content = msg_cont
        pa1.save()
        messages.success(request, 'Message reply successful')
        return render(request, 'message.html', {'bb': bb})
    return render(request,'reply_msg_admin.html',{'pa':pa})


def sent_msg_admin(request):
    kk = Registration.objects.all()
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = str(to_em)
        gg = ddp.split()
        pnm = gg[0]
        pnm1 = gg[2]+' '+gg[3]
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Category = p.User_role
        kkp = Registration.objects.get(id = request.session['logg'])
        nm.From_email = kkp.Email
        nm.Name = pnm1
        nm.To_email = pnm
        nm.Message_content = msg_cont
        nm.save()
        messages.success(request, 'Message sent successfully')
        return render(request, 'message.html', {'bb': bb})
    return render(request,'sent_msg_admin.html',{'kk':kk})



def m_m2(request):
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email).exclude(Category='guest')
    return render(request,'message2.html',{'bb':bb})


def del_msg_student(request,id):
    Messages.objects.get(id = id).delete()
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    messages.success(request, 'Message deleted successfully')
    return render(request,'message2.html',{'bb':bb})


def reply_msg_student(request,id):
    pa = Messages.objects.get(id = id)
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    if request.method == 'POST':
        f_email = request.POST.get('f_email')
        to_email = request.POST.get('to_email')
        msg_cont = request.POST.get('msg_cont')
        km = p.First_name
        kmd = p.Last_name
        pa1 = Messages()
        pa1.Name = str(km)+' '+str(kmd)
        pa1.Category = p.User_role
        pa1.From_email = to_email
        pa1.To_email = f_email
        pa1.Message_content = msg_cont
        pa1.save()
        messages.success(request, 'Message reply successful')
        return render(request, 'message2.html', {'bb': bb})
    return render(request,'reply_msg_student.html',{'pa':pa})



def sent_msg_student(request):
    kk = Registration.objects.all()
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = str(to_em)
        gg = ddp.split()
        pnm = gg[0]
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Category = p.User_role
        kkp = Registration.objects.get(id = request.session['logg'])
        nm.From_email = kkp.Email
        nm.To_email = pnm
        nm.Message_content = msg_cont
        nm.save()
        messages.success(request, 'Message sent successfully')
        return render(request, 'message2.html', {'bb': bb})
    return render(request,'sent_msg_student.html',{'kk':kk})




def m_m3(request):
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email).exclude(Category='guest')
    return render(request,'message3.html',{'bb':bb})


def del_msg_teacher(request,id):
    Messages.objects.get(id=id).delete()
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    messages.success(request, 'Message deleted successfully')
    return render(request, 'message3.html', {'bb': bb})


def reply_msg_teacher(request,id):
    aa = Messages.objects.get(id=id)
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    if request.method == 'POST':
        f_email = request.POST.get('f_email')
        to_email = request.POST.get('to_email')
        msg_cont = request.POST.get('msg_cont')
        cat = request.POST.get('cate')
        k = p.First_name
        kk = p.Last_name
        w = Messages()
        w.Name = str(k)+' '+str(kk)
        w.Category = p.User_role
        w.From_email = f_email
        w.To_email = to_email
        w.Message_content = msg_cont
        w.save()
        messages.success(request,'message sent success fully')
        return render(request,'message3.html',{'bb':bb })
    return render(request,'reply_msg_teacher.html', {'aa':aa })


def sent_msg_teacher(request):
    kk = Registration.objects.all()
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = str(to_em)
        gg = ddp.split()
        pnm = gg[0]
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Category = p.User_role
        kkp = Registration.objects.get(id = request.session['logg'])
        nm.From_email = kkp.Email
        nm.To_email = pnm
        nm.Message_content = msg_cont
        nm.save()
        messages.success(request, 'Message sent successfully')
        return render(request, 'message3.html', {'bb': bb})
    return render(request,'sent_msg_teacher.html',{'kk':kk})



def block(request):
    t_reg = Registration.objects.filter(Q(User_role="teacher") | Q(User_role="teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role="student") | Q(User_role="student_blocked"))
    return render(request,'block.html',{'t_reg':t_reg,'s_reg':s_reg})

def blocks(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'teacher_blocked'
    klk.save()
    t_reg = Registration.objects.filter(Q(User_role = "teacher") | Q(User_role = "teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role = "student") | Q(User_role = "student_blocked"))
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg})


def blocks1(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'student_blocked'
    klk.save()
    t_reg = Registration.objects.filter(Q(User_role = "teacher") | Q(User_role = "teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role = "student") | Q(User_role = "student_blocked"))
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg})


def allows(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'teacher'
    klk.save()
    t_reg = Registration.objects.filter(Q(User_role="teacher") | Q(User_role="teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role="student") | Q(User_role="student_blocked"))
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg})


def allows1(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'student'
    klk.save()
    t_reg = Registration.objects.filter(Q(User_role="teacher") | Q(User_role="teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role="student") | Q(User_role="student_blocked"))
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg})



def upl_cer(request):
    ss = Registration.objects.filter(User_role = 'student')
    bc = Enrollment.objects.all()
    kk = []
    kj = []
    ks = []
    ka = []
    kb = []
    kc = []
    for i in ss:
        for t in bc:
           if i.Email == t.Student_email:
               kk.append(i.First_name)
               kj.append(i.Last_name)
               ks.append(i.Email)
               ka.append(t.Subject_name)
               kb.append(t.Course_name)
               kc.append(t.Teacher_email)
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        print(stu_id)
        gg = stu_id.split(";")
        hu = gg[0]
        tq = gg[1]
        tp = gg[2]
        wx = gg[3]
        cert = request.FILES['cert']
        fs = FileSystemStorage()
        fs.save(cert.name,cert)
        cc = Enrollment.objects.get(Student_email = hu, Subject_name = tq, Course_name = tp, Teacher_email = wx)
        if cc.Certificate != '':
            messages.success(request, 'Please delete old certificates of student')
            return render(request, 'admin_home.html')
        cc.Certificate = cert
        cc.save()
        messages.success(request, 'Certificate uploaded successfully')
        return render(request,'admin_home.html')
    ms = zip(kk,kj,ks,ka,kb,kc)
    return render(request,'upload_cert.html',{'ms':ms})



def do_cer(request):
    dd = Registration.objects.get(id = request.session['logg'])
    sr = Enrollment.objects.filter(Student_name = dd.First_name, Student_email = dd.Email)
    j =[]
    for p in sr:
        if p.Certificate != "":
            j.append(p.Certificate)
    if not j:
        messages.success(request, 'No certificate available')
        return render(request, 'student_home.html')
    return render(request,'do_cer.html',{'sr':sr})



def del_cer(request):
    df = Enrollment.objects.all().exclude(Certificate = '')
    return render(request,'del_cer.html',{'df':df})

def delete_cert(request, id):
    m = Enrollment.objects.get(id = id)
    m.Certificate = ''
    m.save()
    df = Enrollment.objects.all().exclude(Certificate = '')
    messages.success(request, 'Deleted certificate')
    return render(request, 'del_cer.html', {'df': df})



def feedback(request):
    x = datetime.datetime.now()
    y = x.strftime("%Y-%m-%d")
    dd = Registration.objects.get(id = request.session['logg'])
    ds = Enrollment.objects.filter(enrol_reg = dd)
    fd = []
    for i in ds:
        if i.Course_name not in fd:
            fd.append(i.Course_name)
    fd1 = []
    for i in ds:
        if i.Subject_name not in fd1:
            fd1.append(i.Subject_name)
    fd2 = []
    fd3 = []
    for i in ds:
        if i.Teacher_email not in fd3:
            fd3.append(i.Teacher_email)
            fd2.append(i.Teacher_name)
    fd4 = zip(fd2,fd3)
    if request.method == 'POST':
        course = request.POST.get('select')
        subject = request.POST.get('select3')
        teach = request.POST.get('select4')
        teach1 = teach.split(";")
        try:
            tt = teach1[0]
            ttt = teach1[1]
        except:
            messages.success(request, 'Please register a course')
            return render(request, 'feedback.html',{'fd':fd,'fd1':fd1,'fd4':fd4})
        score = request.POST.get('select1')
        text_feed = request.POST.get('text_feed')
        qw = Feedback()
        qw.Subject_name = subject
        qw.Teacher_name = tt
        qw.Teacher_email = ttt
        for i in ds:
            qw.Student_name = i.Student_name
            qw.Student_email = i.Student_email
            break
        qw.Course_name = course
        qw.Feedback_text = text_feed
        qw.Rating_score = score
        qw.Submission_date = y
        qw.Feed_reg = dd
        qw.save()
        messages.success(request, 'Thank you for your valuable feedback')
        return render(request, 'student_home.html')
    return render(request,'feedback.html',{'fd':fd,'fd1':fd1,'fd4':fd4})


def feedbak(request):
    se = Feedback.objects.all()
    return render(request,'feedbak.html',{'se':se})

def delete_feedback(request, id):
    Feedback.objects.get(id=id).delete()
    se = Feedback.objects.all()
    return render(request, 'feedbak.html', {'se': se})




def subject_ad(request):
   dd = Subject.objects.all()
   gt = Registration.objects.all()
   sub_nam = []
   cou_nam = []
   tea_em = []
   tea_fn = []
   tea_ln = []
   cou_brf = []
   c_d = []
   c_n = []
   c_f = []
   lan = []
   c_id = []
   for i in dd:
       sub_nam.append(i.Subject_title)
       cou_nam.append(i.Course_title)
       cou_brf.append(i.Course_brief)
       c_d.append(i.Course_duration)
       c_n.append(i.Num_of_chapters)
       c_f.append(i.Course_fee)
       lan.append(i.Language)
       c_id.append(i.id)
       for t in gt:
           if t == i.Sub_reg:
               tea_em.append(t.Email)
               tea_fn.append(t.First_name)
               tea_ln.append(t.Last_name)
   lenn = len(sub_nam)
   for z in range(lenn):
       kpk = len(sub_nam)
       r = int(z)
       r += 1
       try:
           a = sub_nam[z]
       except:
           break
       b = cou_nam[z]
       c = tea_em[z]
       for k in range(lenn):
           if int(r) >= int(kpk):
               continue
           try:
               if sub_nam[r] == a and cou_nam[r] == b and tea_em[r] == c:
                   del sub_nam[r]
                   del cou_nam[r]
                   del tea_em[r]
                   del tea_fn[r]
                   del tea_ln[r]
                   del cou_brf[r]
                   del c_d[r]
                   del c_n[r]
                   del c_f[r]
                   del lan[r]
                   del c_id[r]
                   r -= 1
               r += 1
           except:
               break
   grg = zip(sub_nam,cou_nam,tea_em,tea_fn,tea_ln,cou_brf,c_d,c_n,c_f,lan,c_id)
   return render(request,'sub_ad.html',{'grg':grg})


def edit_subject1(request, id, idd, idt, pkm):
    pkm = int(pkm)
    id = str(id)
    idd = str(idd)
    idt = str(idt)
    ftf = Registration.objects.get(Email = idt)
    gh1 = Subject.objects.filter(Subject_title = id, Course_title = idd, Sub_reg = ftf)
    gh = Subject.objects.get(id = pkm)
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_b = request.POST.get('c_b')
        c_d = request.POST.get('c_d')
        n_c = request.POST.get('n_c')
        c_f = request.POST.get('c_f')
        lan = request.POST.get('lan')
        for k in gh1:
            k.Subject_title = sub
            k.Course_title = cou
            k.Course_brief = c_b
            k.Course_duration = c_d
            k.Num_of_chapters = n_c
            k.Course_fee  = c_f
            k.Language  = lan
            k.save()

        dd = Subject.objects.all()
        gt = Registration.objects.all()
        sub_nam = []
        cou_nam = []
        tea_em = []
        tea_fn = []
        tea_ln = []
        cou_brf = []
        c_d = []
        c_n = []
        c_f = []
        lan = []
        c_id = []
        for i in dd:
            sub_nam.append(i.Subject_title)
            cou_nam.append(i.Course_title)
            cou_brf.append(i.Course_brief)
            c_d.append(i.Course_duration)
            c_n.append(i.Num_of_chapters)
            c_f.append(i.Course_fee)
            lan.append(i.Language)
            c_id.append(i.id)
            for t in gt:
                if t == i.Sub_reg:
                    tea_em.append(t.Email)
                    tea_fn.append(t.First_name)
                    tea_ln.append(t.Last_name)
        lenn = len(sub_nam)
        for z in range(lenn):
            kpk = len(sub_nam)
            r = int(z)
            r += 1
            try:
                a = sub_nam[z]
            except:
                break
            b = cou_nam[z]
            c = tea_em[z]
            for k in range(lenn):
                if int(r) >= int(kpk):
                    continue
                try:
                    if sub_nam[r] == a and cou_nam[r] == b and tea_em[r] == c:
                        del sub_nam[r]
                        del cou_nam[r]
                        del tea_em[r]
                        del tea_fn[r]
                        del tea_ln[r]
                        del cou_brf[r]
                        del c_d[r]
                        del c_n[r]
                        del c_f[r]
                        del lan[r]
                        del c_id[r]
                        r -= 1
                    r += 1
                except:
                    break
        grg = zip(sub_nam, cou_nam, tea_em, tea_fn, tea_ln, cou_brf, c_d, c_n, c_f, lan, c_id)
        messages.success(request, 'Subject edited successfully')
        return render(request, 'sub_ad.html', {'grg': grg})
    return render(request,'edit_subject1.html',{'gh':gh,'ftf':ftf})



def delete_subject1(request, id, idd, idt, pkm):
    pkm = int(pkm)
    id = str(id)
    idd = str(idd)
    idt = str(idt)
    ftf = Registration.objects.get(Email=idt)
    Subject.objects.filter(Subject_title=id, Course_title=idd, Sub_reg=ftf).delete()
    gt = Registration.objects.all()
    dd = Subject.objects.all()
    sub_nam = []
    cou_nam = []
    tea_em = []
    tea_fn = []
    tea_ln = []
    cou_brf = []
    c_d = []
    c_n = []
    c_f = []
    lan = []
    c_id = []
    for i in dd:
        sub_nam.append(i.Subject_title)
        cou_nam.append(i.Course_title)
        cou_brf.append(i.Course_brief)
        c_d.append(i.Course_duration)
        c_n.append(i.Num_of_chapters)
        c_f.append(i.Course_fee)
        lan.append(i.Language)
        c_id.append(i.id)
        for t in gt:
            if t == i.Sub_reg:
                tea_em.append(t.Email)
                tea_fn.append(t.First_name)
                tea_ln.append(t.Last_name)
    lenn = len(sub_nam)
    for z in range(lenn):
        kpk = len(sub_nam)
        r = int(z)
        r += 1
        try:
            a = sub_nam[z]
        except:
            break
        b = cou_nam[z]
        c = tea_em[z]
        for k in range(lenn):
            if int(r) >= int(kpk):
                continue
            try:
                if sub_nam[r] == a and cou_nam[r] == b and tea_em[r] == c:
                    del sub_nam[r]
                    del cou_nam[r]
                    del tea_em[r]
                    del tea_fn[r]
                    del tea_ln[r]
                    del cou_brf[r]
                    del c_d[r]
                    del c_n[r]
                    del c_f[r]
                    del lan[r]
                    del c_id[r]
                    r -= 1
                r += 1
            except:
                break
    grg = zip(sub_nam, cou_nam, tea_em, tea_fn, tea_ln, cou_brf, c_d, c_n, c_f, lan, c_id)
    messages.success(request, 'Subject deleted successfully')
    return render(request, 'sub_ad.html', {'grg': grg})



def chapter_ad(request):
    dd = Subject.objects.all()
    gt = Registration.objects.all()
    sub_nam = []
    cou_nam = []
    ch_tit = []
    n_o_a = []
    tea_em = []
    tea_fn = []
    tea_ln = []
    c_id = []
    for i in dd:
        sub_nam.append(i.Subject_title)
        cou_nam.append(i.Course_title)
        ch_tit.append(i.Chapter_title)
        n_o_a.append(i.Num_of_assignments)
        c_id.append(i.id)
        for t in gt:
            if t == i.Sub_reg:
                tea_em.append(t.Email)
                tea_fn.append(t.First_name)
                tea_ln.append(t.Last_name)
    lenn = len(sub_nam)
    for z in range(lenn):
        kpk = len(sub_nam)
        r = int(z)
        r += 1
        try:
            a = sub_nam[z]
        except:
            break
        b = cou_nam[z]
        c = tea_em[z]
        d = ch_tit[z]
        for k in range(lenn):
            if int(r) >= int(kpk):
                continue
            try:
                if sub_nam[r] == a and cou_nam[r] == b and tea_em[r] == c and ch_tit[r] == d:
                    del sub_nam[r]
                    del cou_nam[r]
                    del ch_tit[r]
                    del n_o_a[r]
                    del tea_em[r]
                    del tea_fn[r]
                    del tea_ln[r]
                    del c_id[r]
                    r -= 1
                r += 1
            except:
                break
    grg1 = zip(sub_nam, cou_nam, ch_tit, n_o_a, tea_em, tea_fn, tea_ln, c_id)
    return render(request, 'chap_ad.html', {'grg1': grg1})



def edit_chapter1(request, id, idd, idt, idk, pkm):
    pkm = int(pkm)
    id = str(id)
    idd = str(idd)
    idt = str(idt)
    idk = str(idk)
    ftf = Registration.objects.get(Email=idk)
    gh1 = Subject.objects.filter(Subject_title=id, Course_title=idd, Chapter_title = idt, Sub_reg=ftf)
    gh = Subject.objects.get(id=pkm)

    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_tt = request.POST.get('c_tt')
        n_s = request.POST.get('n_s')
        for k in gh1:
            k.Subject_title = sub
            k.Course_title = cou
            k.Chapter_title = c_tt
            k.Num_of_assignments = n_s
            k.save()

        dd = Subject.objects.all()
        gt = Registration.objects.all()
        sub_nam = []
        cou_nam = []
        ch_tit = []
        n_o_a = []
        tea_em = []
        tea_fn = []
        tea_ln = []
        c_id = []
        for i in dd:
            sub_nam.append(i.Subject_title)
            cou_nam.append(i.Course_title)
            ch_tit.append(i.Chapter_title)
            n_o_a.append(i.Num_of_assignments)
            c_id.append(i.id)
            for t in gt:
                if t == i.Sub_reg:
                    tea_em.append(t.Email)
                    tea_fn.append(t.First_name)
                    tea_ln.append(t.Last_name)
        lenn = len(sub_nam)
        for z in range(lenn):
            kpk = len(sub_nam)
            r = int(z)
            r += 1
            try:
                a = sub_nam[z]
            except:
                break
            b = cou_nam[z]
            c = tea_em[z]
            d = ch_tit[z]
            for k in range(lenn):
                if int(r) >= int(kpk):
                    continue
                try:
                    if sub_nam[r] == a and cou_nam[r] == b and tea_em[r] == c and ch_tit[r] == d:
                        del sub_nam[r]
                        del cou_nam[r]
                        del ch_tit[r]
                        del n_o_a[r]
                        del tea_em[r]
                        del tea_fn[r]
                        del tea_ln[r]
                        del c_id[r]
                        r -= 1
                    r += 1
                except:
                    break
        grg1 = zip(sub_nam, cou_nam, ch_tit, n_o_a, tea_em, tea_fn, tea_ln, c_id)
        messages.success(request, 'Chapter edited successfully')
        return render(request, 'chap_ad.html', {'grg1': grg1})
    return render(request, 'edit_chapter1.html', {'gh': gh, 'ftf': ftf})


def delete_chapter1(request, id, idd, idt, idk, pkm):
    pkm = int(pkm)
    id = str(id)
    idd = str(idd)
    idt = str(idt)
    idk = str(idk)
    ftf = Registration.objects.get(Email=idk)
    Subject.objects.filter(Subject_title=id, Course_title=idd, Chapter_title=idt, Sub_reg=ftf).delete()

    dd = Subject.objects.all()
    gt = Registration.objects.all()
    sub_nam = []
    cou_nam = []
    ch_tit = []
    n_o_a = []
    n_o_v = []
    n_o_p = []
    n_o_i = []
    tea_em = []
    tea_fn = []
    tea_ln = []
    c_id = []
    for i in dd:
        sub_nam.append(i.Subject_title)
        cou_nam.append(i.Course_title)
        ch_tit.append(i.Chapter_title)
        n_o_a.append(i.Num_of_assignments)
        n_o_v.append(0)
        n_o_i.append(0)
        n_o_p.append(0)
        c_id.append(i.id)
        for t in gt:
            if t == i.Sub_reg:
                tea_em.append(t.Email)
                tea_fn.append(t.First_name)
                tea_ln.append(t.Last_name)
    lenn = len(sub_nam)
    for z in range(lenn):
        kpk = len(sub_nam)
        r = int(z)
        r += 1
        try:
            a = sub_nam[z]
        except:
            break
        b = cou_nam[z]
        c = tea_em[z]
        d = ch_tit[z]
        for k in range(lenn):
            if int(r) >= int(kpk):
                continue
            try:
                if sub_nam[r] == a and cou_nam[r] == b and tea_em[r] == c and ch_tit[r] == d:
                    del sub_nam[r]
                    del cou_nam[r]
                    del ch_tit[r]
                    del n_o_a[r]
                    del tea_em[r]
                    del tea_fn[r]
                    del tea_ln[r]
                    del c_id[r]
                    r -= 1
                r += 1
            except:
                break
    grg1 = zip(sub_nam, cou_nam, ch_tit, n_o_a, tea_em, tea_fn, tea_ln, c_id)
    messages.success(request, 'Chapter deleted successfully')
    return render(request, 'chap_ad.html', {'grg1': grg1})


def ch_co_ad(request):
    gt = Registration.objects.filter(User_role='teacher')
    dm = Subject.objects.all()
    return render(request, 'cont_ad.html', {'gt':gt,'dm':dm})

def edit_content1(request, id):
    gh1 = Subject.objects.get(id=id)
    gt = Registration.objects.filter(User_role='teacher')
    dm = Subject.objects.all()
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_n1 = request.POST.get('c_n')
        s = request.POST.get('s')
        time = request.POST.get('time')
        s1 = request.POST.get('s1')
        cont_typ = request.POST.get('cont_typ')
        textt = request.POST.get('textt')
        gh1.Subject_title = sub
        gh1.Course_title = cou
        gh1.Chapter_title = c_n1
        gh1.Chapter_text_content = textt
        if cont_typ == 1:
            gh1.Chapter_Content_type = 'Image'
        if cont_typ == 2:
            gh1.Chapter_Content_type = 'Text'
        if cont_typ == 3:
            gh1.Chapter_Content_type = 'Video'
        gh1.Chapter_Content_Is_mandatory  = s
        gh1.Chapter_Content_Time_required_in_sec  = time
        gh1.Chapter_Content_Is_open_for_free  = s1
        gh1.save()
        messages.success(request, 'Chapter content edited successfully')
        return render(request, 'cont_ad.html', {'gt':gt,'dm':dm})
    return render(request, 'edit_content1.html', {'gh1': gh1})


def delete_content1(request,id):
    Subject.objects.get(id=id).delete()
    gt = Registration.objects.filter(User_role='teacher')
    dm = Subject.objects.all()
    messages.success(request, 'Chapter content deleted successfully')
    return render(request, 'cont_ad.html', {'gt': gt, 'dm': dm})








def pass_req(request):
    dd = Requests.objects.all()
    return render(request,'pass_req.html',{'dd':dd})

def pass_req1(request, id):
    ff = Requests.objects.get(id = id)
    passwords = make_password(ff.New_password)
    print(passwords)
    u = User.objects.get(email = ff.Email)
    u.password = passwords
    u.save()

    tt = Registration.objects.get(Email=ff.Email)
    tt.Password = ff.New_password
    tt.save()
    Requests.objects.get(id=id).delete()
    dd = Requests.objects.all()
    return render(request, 'pass_req.html', {'dd': dd})


def ch_p11(request):
    th = Registration.objects.get(id = request.session['logg'])
    if request.method == 'POST':
        new_pass = request.POST.get('pssw')
        old_pass = request.POST.get('pssw_old')
        email = request.POST.get('em')
        cate = request.POST.get('usr')
        nam = request.POST.get('nam')
        g = Requests()
        g.Name = nam
        g.Email = email
        g.User_category = cate
        g.Old_password = old_pass
        g.New_password = new_pass
        g.Req_reg = th
        g.save()
        messages.success(request, 'Please wait for your password approval.. Continue to use old password')
        return redirect('teacher_home')
    return render(request, 'change_password1.html', {'th': th})



def ch_p(request):
    th = Registration.objects.get(id = request.session['logg'])
    if request.method == 'POST':
        new_pass = request.POST.get('pssw')
        old_pass = request.POST.get('pssw_old')
        email = request.POST.get('em')
        cate = request.POST.get('usr')
        nam = request.POST.get('nam')
        g = Requests()
        g.Name = nam
        g.Email = email
        g.User_category = cate
        g.Old_password = old_pass
        g.New_password = new_pass
        g.Req_reg = th
        g.save()
        messages.success(request, 'Please wait for your password approval.. Continue to use old password')
        return render(request, 'student_home.html')
    return render(request,'change_password.html',{'th':th})



def atten(request):
    h = Registration.objects.get(id = request.session['logg'])
    ss = Enrollment.objects.filter(Teacher_email = h.Email)
    if request.method == 'POST':
        atn = request.POST.get('atn')
        atn1 = request.POST.get('atn1')
        dw = Enrollment.objects.get(id = atn)
        dw.Attendance = atn1
        dw.save()
        messages.success(request, 'Attendance given')
        return redirect('teacher_home')
    return render(request,'atten.html',{'ss':ss})



def abb(request):
    amm = Registration.objects.get(User_role = 'admin')
    if request.method == 'POST':
        abbt = request.POST.get('abbt')
        idd = request.POST.get('idd')
        adc = Registration.objects.get(id = idd)
        adc.About_website = abbt
        adc.save()
        messages.success(request, 'Content added successfully')
        return render(request,'admin_home.html')
    return render(request,'about_content.html',{'amm':amm})









