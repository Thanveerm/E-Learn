from django.contrib import admin
from django.urls import path
import learn.views


urlpatterns = [
    path('',learn.views.home, name='home'),
    path('home',learn.views.home, name='home'),
    path('news',learn.views.news, name='news'),
    path('about',learn.views.about, name='about'),
    path('admin_rg',learn.views.admin_rg, name='admin_rg'),
    path('teacher_rg',learn.views.register_tr, name='teacher_rg'),
    path('student_reg',learn.views.register_st, name='student_reg'),
    path('login',learn.views.login, name='login'),

    path('reg_msg', learn.views.reg_msg, name='reg_msg'),

    path('',learn.views.student,  name='home_student'),
    path('student_home', learn.views.student, name='student_home'),
    path('Update_profile', learn.views.student, name='Update_profile'),
    path('Booked_courses', learn.views.student, name='Booked_courses'),
    path('Book_course', learn.views.student, name='Book_course'),
    path('Download_Certificate', learn.views.student, name='Download_Certificate'),
    path('My_profile', learn.views.student, name='My_profile'),
    path('Feedback', learn.views.student, name='Feedback'),

    path('', learn.views.admin_home, name='admin_home'),
    path('admin_home', learn.views.admin_home, name='admin_home'),
    path('Update_Profile', learn.views.admin_home, name='Update_Profile'),
    path('Blogs', learn.views.admin_home, name='Blogs'),
    path('Certificate', learn.views.admin_home, name='Certificate'),
    path('About_website', learn.views.admin_home, name='About_website'),
    path('Block_member', learn.views.admin_home, name='Block_member'),
    path('Feedback ', learn.views.admin_home, name='Feedback '),
    path('Topics', learn.views.admin_home, name='Topics'),
    path('Subject', learn.views.admin_home, name='Subject'),
    path('chapter', learn.views.admin_home, name='chapter'),
    path('Chapter_content', learn.views.admin_home, name='Chapter_content'),

    path('teacher_home', learn.views.teacher_home, name='teacher_home'),
    path('Update_Profile', learn.views.teacher_home, name='Update_Profile'),
    path('Student_Progress', learn.views.teacher_home, name='Student_Progress'),
    path('Topics', learn.views.teacher_home, name='Topics'),
    path('Subject', learn.views.teacher_home, name='Subject'),
    path('Chapters', learn.views.teacher_home, name='Chapters'),
    path('Chapter_Content', learn.views.teacher_home, name='Chapter_Contents'),
    path('Student_Booked_Details', learn.views.teacher_home, name='Student_Booked_Details'),
    path('Exam', learn.views.teacher_home, name='Exam'),
    path('Student_Test', learn.views.teacher_home, name='Student_Test'),
    path('Delete_Schedule_Test', learn.views.teacher_home, name='Delete_Schedule_Test'),
    path('Exam_Result', learn.views.teacher_home, name='Exam_Result'),
    path('Messages', learn.views.teacher_home, name='Messages'),
    path('Give_Attendence', learn.views.teacher_home, name='Give_Attendence'),
    path('logout', learn.views.logout, name='logout'),

    path('stu_buk_acc', learn.views.stu_buk_acc, name='stu_buk_acc'),
    path('stu_accept/<id>', learn.views.stu_accept, name='stu_accept'),
    path('stu_reject/<id>', learn.views.stu_reject, name='stu_reject'),
    path('stu_delete/<id>', learn.views.stu_delete, name='stu_delete'),
    path('notiffy', learn.views.notiffy, name='notiffy'),

    path('add_blog', learn.views.add_blog, name='add_blog'),

    path('approval_reject',learn.views.approval_reject,name='approval_reject'),

    path('blog_admin',learn.views.blogs_admin,name='blog_admin'),
    path('blog_approves/<ds>',learn.views.blog_approves,name='blog_approves'),
    path('blog_rejects/<df>',learn.views.blog_rejects,name= 'blog_rejects'),
    path('blog_delete/<dg>',learn.views.blog_delete,name= 'blog_delete'),

    path('display_blog',learn.views.view_blog,name= 'display_blog'),


    path('contact',learn.views.contact,name= 'contact'),


    path('guest_message',learn.views.g_m,name= 'guest_message'),
    path('delete_g_msg/<k>',learn.views.delete_g_msg,name= 'delete_g_msg'),

    path('update_pr_tr',learn.views.update_pr_tr,name= 'update_pr_tr'),

    path('update_pr_st',learn.views.update_pr_st,name= 'update_pr_st'),

    path('update_admin',learn.views.adm_prof,name= 'update_admin'),
    path('del_admin/<dk>',learn.views.del_admin,name= 'del_admin'),
    path('edit_admin',learn.views.edit_admin,name= 'edit_admin'),
    path('bnb',learn.views.bnb,name= 'bnb'),


    path('sub_tr',learn.views.subject_tr,name='sub_tr'),
    path('edit_subject/<id>/<idd>/<idm>',learn.views.edit_subject,name= 'edit_subject'),
    path('delete_subject/<id>/<idd>/<idm>',learn.views.delete_subject,name= 'delete_subject'),
    path('add_subject',learn.views.add_subject,name= 'add_subject'),
    path('subject_tr',learn.views.subject_tr,name= 'subject_tr'),


    path('chapter_tr',learn.views.chapter_tr,name= 'chapter_tr'),
    path('edit_chapter/<id>/<idd>/<idk>/<idm>',learn.views.edit_chapter,name= 'edit_chapter'),
    path('delete_chapter/<id>/<idd>/<idk>/<idm>',learn.views.delete_chapter,name= 'delete_chapter'),
    path('add_chapter',learn.views.add_chapter,name= 'add_chapter'),
    path('add_chapter1',learn.views.add_chapter1,name= 'add_chapter1'),


    path('cont_tr',learn.views.ch_co_tr,name= 'cont_tr'),
    path('edit_content/<y>',learn.views.edit_content,name= 'edit_content'),
    path('delete_content/<id>',learn.views.delete_content,name= 'delete_content'),
    #path('add_chapter',learn.views.add_ch_con,name= 'add_chapter'),
    path('add_ch_con',learn.views.add_ch_con,name= 'add_ch_con'),
    path('add_chapter_c0',learn.views.add_chapter_c0,name= 'add_chapter_c0'),
    path('ch_co_tr',learn.views.ch_co_tr,name= 'ch_co_tr'),
    path('add_chapter_c1',learn.views.add_chapter_c1,name= 'add_chapter_c1'),

    
    path('st_sub_selnew1.html',learn.views.stu_sub_selnew,name= 'st_sub_selnew1.html'),
    path('st_sub_selnew2',learn.views.st_sub_selnew2,name= 'st_sub_selnew2'),
    path('disp_teach',learn.views.disp_teach,name= 'disp_teach'),
    path('paid.html',learn.views.stu_buk_teacherr,name= 'paid.html'),
    path('stu_buk_teacherr/<d>',learn.views.stu_buk_teacherr,name= 'stu_buk_teacherr'),
    path('stu_buk_teacher',learn.views.stu_buk_teacher,name= 'stu_buk_teacher'),


    path('st_book_courses',learn.views.st_book_courses,name= 'st_book_courses'),
    path('acc_chapter/<id>/<ikm>/<sub>', learn.views.acc_chapter, name='acc_chapter'),
    path('acc_chapter1', learn.views.acc_chapter1 , name='acc_chapter1'),
    path('compp', learn.views.compp , name='compp'),


    path('student_progress', learn.views.st_pr, name='student_progress'),


    path('sched_test', learn.views.sched_test, name='sched_test'),
    path('sched_test1', learn.views.sched_test1, name='sched_test1'),
    path('sched_test2', learn.views.sched_test1, name='sched_test2'),
    path('sched_test3', learn.views.sched_test3, name='sched_test3'),


    path('ex_not', learn.views.ex_not, name='ex_not'),


    path('start_test', learn.views.start_test, name='start_test'),
    path('save_exam', learn.views.save_exam, name='save_exam'),

    path('exam_result1', learn.views.exam_result1, name='exam_result1'),

    path('exam_result', learn.views.exam_result, name='exam_result'),
    path('delete_ex_re/<k>', learn.views.delete_ex_re, name='delete_ex_re'),

    path('delete_test', learn.views.delete_test, name='delete_test'),
    path('delete_test1/<m>', learn.views.delete_test1, name='delete_test1'),


    path('message', learn.views.m_m, name='message'),
    path('del_msg_admin/<id>', learn.views.del_msg_admin, name='del_msg_admin'),
    path('reply_msg_admin/<id>', learn.views.del_msg_admin, name='reply_msg_admin'),
    path('sent_msg_admin', learn.views.sent_msg_admin, name='sent_msg_admin'),


    path('message2', learn.views.m_m2, name='message2'),
    path('del_msg_student/<id>', learn.views.del_msg_student, name='del_msg_student'),
    path('reply_msg_student/<id>', learn.views.reply_msg_student, name='reply_msg_student'),
    path('sent_msg_student', learn.views.sent_msg_student, name='sent_msg_student'),


    path('message3', learn.views.m_m3, name='message3'),
    path('del_msg_teacher/<id>', learn.views.del_msg_teacher, name='del_msg_teacher'),
    path('reply_msg_teacher/<id>', learn.views.reply_msg_teacher, name='reply_msg_teacher'),
    path('sent_msg_teacher', learn.views.sent_msg_teacher, name='sent_msg_teacher'),


    path('block', learn.views.block, name='block'),
    path('blocks/<id>', learn.views.blocks, name='blocks'),
    path('blocks1/<id>', learn.views.blocks1, name='blocks1'),
    path('allows/<id>', learn.views.allows, name='allows'),
    path('allows1/<id>', learn.views.allows1, name='allows1'),


    path('upload_cert', learn.views.upl_cer, name='upload_cert'),
    path('upl_cer', learn.views.upl_cer, name='upl_cer'),


    path('do_cer', learn.views.do_cer, name='do_cer'),


    path('del_cer', learn.views.del_cer, name='del_cer'),
    path('delete_cert/<id>', learn.views.delete_cert, name='delete_cert'),


   path('feedback', learn.views.feedback, name='feedback'),


   path('feedbak', learn.views.feedbak, name='feedbak'),
   path('delete_feedback/<id>', learn.views.delete_feedback, name='delete_feedback'),




   path('edit_subject1/<id>/<idd>/<idt>/<pkm>', learn.views.edit_subject1, name='edit_subject1'),
   path('delete_subject1/<id>/<idd>/<idt>/<pkm>', learn.views.delete_subject1, name='delete_subject1'),
   path('edit_subject1', learn.views.edit_subject1, name='edit_subject1'),
   path('sub_ad', learn.views.subject_ad, name='sub_ad'),



   path('chap_ad', learn.views.chapter_ad, name='chap_ad'),
   path('edit_chapter1/<id>/<idd>/<idt>/<idk><pkm>', learn.views. edit_chapter1, name='edit_chapter1') ,
   path('delete_chapter1/<id>/<idd>/<idt>/<idk>/<pkm>', learn.views.delete_chapter1, name='delete_chapter1'),
   path('edit_chapter', learn.views. edit_subject1, name='edit_chapter'),

   path('ch_co_ad', learn.views.ch_co_ad, name='ch_co_ad'),
   path('edit_content1/<id>', learn.views.edit_content1, name='edit_content1'),
   path('delete_content1/<id>', learn.views.delete_content1, name='delete_content1'),
   path('edit_content1', learn.views.edit_content1, name='edit_content1'),



   path('pass_req', learn.views.pass_req, name='pass_req'),
   path('pass_req1/<id>', learn.views.pass_req1, name='pass_req1'),
   path('ch_p11', learn.views.ch_p11, name='ch_p11'),
   path('ch_p', learn.views.ch_p, name='ch_p'),


   path('atten', learn.views.atten, name='atten'),


   path('about_content', learn.views.abb, name='about_content'),
   path('abb', learn.views.abb, name='abb'),




]

