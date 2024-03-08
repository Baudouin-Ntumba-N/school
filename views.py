from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Grade
from .forms import CourseForm, GradeForm
from django.urls import reverse
import xlrd
import os





def index(request):
    if(not request.user.is_authenticated ):
        return redirect('login')
    return render(request, "school/index.html")

    
def create_class(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    form = GradeForm()
    if request.method == "POST": 
        form = GradeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("classes") 
        return redirect('create-class')
    return render(request, "school/add_class.html", {'form':form})


def check_class(request, class_id): 
    if(not request.user.is_authenticated ):
        return redirect('login') 
    classe = Grade.objects.get(pk=class_id)
    courses = Course.objects.filter(utilisateur=request.user, classe=classe)
    context = {'classe': classe, "courses": courses} 
    
    if request.method == "POST":
        if not classe.liste_eleves :
            classe.liste_eleves = request.FILES['liste_eleves']
        else:
            os.remove(classe.liste_eleves.path)
            classe.liste_eleves = request.FILES['liste_eleves']
        classe.save()
        return redirect("classes")
    return render(request, "school/check_class.html", context) 


def afficher_eleves(request, class_id): 
    if(not request.user.is_authenticated):
        return redirect('login')
    classe = get_object_or_404(Grade, pk=class_id)
    try:
        document = xlrd.open_workbook(f"media/{classe.liste_eleves}")
    except:
        return redirect("classes")
    sheet1 = document.sheet_by_index(0)
    nb_rows = sheet1.nrows
    my_list = []
    for r in range(1, nb_rows):
        eleve_id = sheet1.cell_value(rowx = r, colx = 0)
        nom = sheet1.cell_value(rowx = r, colx = 1)
        student = {}
        student["id"] = int(eleve_id)
        student["nom"] = nom
        my_list.append(student) 
    return render(request, "school/liste_eleves.html", {"classe": classe , "students": my_list}) 
   
    
def create_course(request, class_id):
    if not request.user.is_authenticated:
        return redirect('login') 
    form = CourseForm()
    if request.method == "POST": 
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('check-class', kwargs={"class_id": class_id })) 
        return redirect('create-course')
    return render(request, "school/add_course.html", {'form':form})


def check_course(request, course_id): 
    if(not request.user.is_authenticated ):
        return redirect('login')
    course = get_object_or_404(Course, pk=course_id)
    if request.method == "POST":
        if course.fiche == "fiches_cotation/default/default.xls":
            course.fiche = request.FILES['fiche']
        else:
            os.remove(course.fiche.path)
            course.fiche = request.FILES['fiche']
        course.save()
        return redirect(reverse("check-course", kwargs={"course_id": course_id}))
    return render(request, "school/check_course.html", {"course": course})

def afficher_cotes(request, course_id): 
    if(not request.user.is_authenticated):
        return redirect('login')
    course = get_object_or_404(Course, pk=course_id)
    document = xlrd.open_workbook(f"media/{course.fiche}")
    sheet1 = document.sheet_by_index(0)
    nb_rows = sheet1.nrows
    my_list = []
    for r in range(1, nb_rows):
        eleve = sheet1.cell_value(rowx = r, colx = 1)
        periode1 = sheet1.cell_value(rowx = r, colx = 2)
        periode2 = sheet1.cell_value(rowx = r, colx = 3)
        exam1 = sheet1.cell_value(rowx = r, colx = 4)
        student = {}
        student["nom"] = eleve
        try:
            student["periode1"] = int(periode1)
        except:
            student["periode1"] = ""
        
        try:
            student["periode2"] = int(periode2)
        except:
            student["periode2"] = ""
        
        try:
            student["exam1"] = int(exam1)
        except:
            student["exam1"] = ""
        
        if(periode1 and periode2 and exam1):
            student["semester"] = int(periode1) + int(periode2) + int(exam1)
            
        my_list.append(student) 
       
    return render(request, "school/fiche_cotation.html", {"cours": course, "students": my_list }) 
    
def classes_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    classes = Grade.objects.filter(createur=request.user)
    return render(request, 'school/classes.html', {'classes': classes})
    

def get_student_report(request, class_id, student_id): 
    classe = get_object_or_404(Grade, pk=class_id)
    courses = Course.objects.filter(classe=classe)
    try:
        eleves_document = xlrd.open_workbook(f"media/{classe.liste_eleves}")
    except:
        return redirect("classes")
    eleves_sheet1 = eleves_document.sheet_by_index(0)
    eleves_nb_rows = eleves_sheet1.nrows
    for r in range(1, eleves_nb_rows):
        my_eleve_id = eleves_sheet1.cell_value(rowx = r, colx = 0)
        if my_eleve_id == student_id:
            my_nom = eleves_sheet1.cell_value(rowx = r, colx = 1)
            student = {}
            student["id"] = int(my_eleve_id)
            student["nom"] = my_nom
    
    report_courses = [] 
    for course in courses: 
        document = xlrd.open_workbook(f"media/{course.fiche}")
        sheet1 = document.sheet_by_index(0)
        nb_rows = sheet1.nrows
        for r in range(1, nb_rows):
            eleve_id = sheet1.cell_value(rowx = r, colx = 0)
            if eleve_id == student_id:
                eleve = sheet1.cell_value(rowx = r, colx = 1)
                periode1 = sheet1.cell_value(rowx = r, colx = 2)
                periode2 = sheet1.cell_value(rowx = r, colx = 3)
                exam1 = sheet1.cell_value(rowx = r, colx = 4)
                my_course = {}
                my_course["course"] = course
                my_course["nom"] = course.nom
                my_course["periode1"] = int(periode1)
                my_course["periode2"] = int(periode2) 
                my_course["exam1"] = int(exam1)
                my_course["semester1"] = int(periode1) + int(periode2) + int(exam1)
                
                report_courses.append(my_course) 
    
    max_gen_p1 = 0 
    for el in report_courses:
        max_gen_p1 += el["course"].maximum
    
    total_gen_p1 = 0 
    for el in report_courses:
        total_gen_p1 += el["periode1"]
    total_gen_p2 = 0 
    for el in report_courses:
        total_gen_p2 += el["periode2"] 
    
    total_gen_exam1 = 0 
    for el in report_courses:
        total_gen_exam1 += el["exam1"]  
    
    total_gen_semester1 = 0 
    for el in report_courses:
        total_gen_semester1 += el["semester1"]  
    
    if max_gen_p1 != 0 :
    	percentage1 = round((total_gen_p1 / max_gen_p1)*100, 1)
    	percentage2 = round((total_gen_p2 / max_gen_p1)*100, 1) 
    	percentage_exam1 = round((total_gen_exam1 / (max_gen_p1*2))*100, 1)
    	percentage_semester1 = round((total_gen_semester1 / (max_gen_p1*4)*100), 1)
    else:
    	percentage1 = 0
    	percentage2 = 0
    	percentage_exam1 = 0
    	percentage_semester1 = 0

    	
    context = {
        "classe": classe,
        "report_courses": report_courses, 
        "max_gen_p1": max_gen_p1,
        "total_gen_p1": total_gen_p1,
        "total_gen_p2": total_gen_p2, 
        "max_gen_exam1": max_gen_p1 * 2,
        "total_gen_exam1": total_gen_exam1,
        "max_gen_semester1": max_gen_p1 * 4, 
        "total_gen_semester1": total_gen_semester1 ,
        "percentage1": percentage1,
        "percentage2": percentage2,
        "percentage_exam1": percentage_exam1,
        "percentage_semester1": percentage_semester1,
        "student":student
    }
    return render(request, 'school/student_report.html', context)