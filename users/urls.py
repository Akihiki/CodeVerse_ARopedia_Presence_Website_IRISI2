from django.contrib import admin
from django.urls import path
from users import views, PermissionsView, rolesView
from users.views import home
from django.contrib.auth.views import LoginView, LogoutView
from . import AdminViews, TeacherViews, StudentViews
from emploie import views as EmploieViews
from django.conf import settings
from django.conf.urls.static import static
from users.StudentViews import *
from face_recognition.views import video_feed

urlpatterns = [
                  # UnivIt responsable : Ettafssaoui Youssef
                  path('', home, name='users-home'),

                  # Users Login : Ettafssaoui Youssef 
                  path('login/', views.loginPage, name="login"),
                  path('doLogin/', views.doLogin, name="doLogin"),
                  path('get_user_details/', views.get_user_details, name="get_user_details"),
                  path('logout_user/', views.logout_user, name="logout_user"),
                  path('admin_home/', AdminViews.admin_home, name="admin_home"),
                  # UnivIt responsable : Ettafssaoui Youssef 
                  path('upload_csv/', AdminViews.upload_csv, name="upload_csv"),
                  path('add_professeur/', AdminViews.add_professeur, name="add_professeur"),
                  path('manage_users/', AdminViews.manage_users, name="manage_users"),
                  path('add_professeur_save/', AdminViews.add_professeur_save, name="add_professeur_save"),
                  path('manage_professeur/', AdminViews.manage_professeur, name="manage_professeur"),
                  path('edit_professeur/<professeur_id>/', AdminViews.edit_professeur, name="edit_professeur"),
                  path('edit_professeur_save/', AdminViews.edit_professeur_save, name="edit_professeur_save"),
                  path('delete_professeur/<professeur_id>/', AdminViews.delete_professeur, name="delete_professeur"),
                  # UnivIt responsable : ismail errouk
                  path('students/', StudentViews.getAllStudents, name="get_all_students"),
                  path('add_csv_file_student/', StudentViews.add_csv_file_student, name="add_csv_file_student"),
                  path('add_student/', StudentViews.add_student, name="add_student"),
                  path('add_student_save/', StudentViews.add_student_save, name="add_student_save"),
                  path('add_student_groups/<int:id>', StudentViews.add_student_groups, name="add_student_groups"),
                  path('add_student_groups_save/<int:id>', StudentViews.add_student_groups_save,
                       name="add_student_groups_save"),
                  path('edit_student/<student_id>', StudentViews.edit_student, name="edit_student"),

                  path('edit_student/video_feed/<str:id>/', video_feed, name='video_feed'),
                  path('edit_student_save/<int:id>', StudentViews.edit_student_save, name="edit_student_save"),
                  path('edit_groupe_add_save/<int:id>', StudentViews.edit_groupe_add_save, name="edit_groupe_add_save"),
                  path('edit_groupe_groupes/<int:id>', StudentViews.edit_groupe_groupes, name="edit_groupe_groupes"),
                  path('manage_student/', StudentViews.manage_student, name="manage_student"),
                  path('delete_student/<student_id>/', StudentViews.delete_student, name="delete_student"),
                  path('delete_student_groupe/<int:id1>/<int:id2>', StudentViews.delete_student_groupe,
                       name="delete_student_groupe"),

                  path('edit_student/video_feed/<str:id>/',
                       video_feed, name='video_feed'),
                  path('edit_student_save/<int:id>',
                       StudentViews.edit_student_save, name="edit_student_save"),
                  path('edit_groupe_add_save/<int:id>',
                       StudentViews.edit_groupe_add_save, name="edit_groupe_add_save"),
                  path('edit_groupe_groupes/<int:id>',
                       StudentViews.edit_groupe_groupes, name="edit_groupe_groupes"),
                  path('manage_student/', StudentViews.manage_student,
                       name="manage_student"),
                  path('delete_student/<student_id>/',
                       StudentViews.delete_student, name="delete_student"),
                  path('delete_student_groupe/<int:id1>/<int:id2>', StudentViews.delete_student_groupe,
                       name="delete_student_groupe"),

                  # UnivIt responsable : Ettafssaoui Youssef
                  path('admin_profile/', AdminViews.admin_profile,
                       name="admin_profile"),
                  path('admin_profile_update/', AdminViews.admin_profile_update,
                       name="admin_profile_update"),

                  # URLS for teacher :
                  # UnivIt responsable : Ettafssaoui Youssef
                  path('teacher_home/', TeacherViews.teacher_home,
                       name="teacher_home"),
                  # path('get_students/', TeacherViews.get_students, name="get_students"),
                  path('teacher_profile/', TeacherViews.teacher_profile,
                       name="teacher_profile"),
                  path('teacher_profile_update/', TeacherViews.teacher_profile_update,
                       name="teacher_profile_update"),

                  # URSL for Student
                  path('student_home/', StudentViews.student_home,
                       name="student_home"),
                  path('student_profile/', StudentViews.student_profile,
                       name="student_profile"),
                  path('student_profile_update/', StudentViews.student_profile_update,
                       name="student_profile_update"),

                  # Permissions
                  # UnivIt responsable : ismail errouk
                  path('add_permission/', PermissionsView.addPermission,
                       name="add_permission"),
                  path('add_permission_save/', PermissionsView.addPermissionSave,
                       name="add_permission_save"),
                  path('edit_permission/<int:id>',
                       PermissionsView.editPermission, name="edit_permission"),
                  path('edit_permission_save/<int:id>', PermissionsView.editPermissionSave,
                       name="edit_permission_save"),
                  path('delete_permission/<int:id>',
                       PermissionsView.deletePermission, name="delete_permission"),
                  path('manage_permissions', PermissionsView.managePermission,
                       name="manage_permissions"),

                  # Roles
                  # UnivIt responsable : ismail errouk
                  path('manage_roles', rolesView.manageRoles, name="manage_roles"),
                  path('add_role', rolesView.addRole, name="add_role"),
                  path('add_role_save', rolesView.addRoleSave,
                       name="add_role_save"),
                  path('edit_role/<int:id>', rolesView.editRole, name="edit_role"),
                  path('edit_role_save/<int:id>',
                       rolesView.editRoleSave, name="edit_role_save"),
                  path('delete_role/<int:id>',
                       rolesView.deleteRole, name="delete_role"),
                  path('delete_role_permission/<int:id1>/<int:id2>', rolesView.deleteRolePermission,
                       name="delete_role_permission"),
                  # Schedules
                  # CodeVerse:responsable : FIROUD Reda & OUSSAHI Salma
                  path('emploie-admin', EmploieViews.EmploieAdmin,
                       name="emploie_admin"),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
