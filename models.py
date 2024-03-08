
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth import get_user_model


#department app

User = get_user_model() 

class Option(models.Model):
    nom = models.CharField(max_length=30)
    def __str__(self):
        return self.nom

class Grade(models.Model):
    nom = models.CharField(max_length=30)
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    liste_eleves = models.FileField(null=True, upload_to=f"eleves/{createur}", verbose_name="Liste élèves")
    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Classe"

class Student(models.Model):
    class Sexe(models.TextChoices):
        MASCULIN = 'M', _('Masculin')
        FEMININ = 'F', _('Féminin')

    nom = models.CharField(max_length=50, null=False, blank=False)
    post_nom = models.CharField(max_length=50, null=False, blank=False)
    prenom = models.CharField(max_length=50, null=True)
    sexe = models.CharField(
        max_length=10,
        choices=Sexe.choices,
        default=Sexe.MASCULIN, )
    classe_del_eleve = models.ForeignKey(Grade, on_delete = models.SET_NULL, null=True, blank=True, verbose_name="Classe")
    option = models.ForeignKey(Option, on_delete = models.SET_NULL, null=True, blank=True)
    date_de_naissance  = models.DateField(null=True)
    lieu_de_naissance = models.CharField(max_length=30)
    tuteur = models.CharField(max_length=30, verbose_name="Responsable")

    class Meta:
        verbose_name = "Elève"

    def __str__(self):
        return self.nom+" "+self.post_nom+" "+self.prenom


class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "post_nom", "prenom", "sexe", "classe_del_eleve", "option")


class Prof(models.Model):
    nom = models.CharField(max_length=50, null=False, blank=False)
    post_nom = models.CharField(max_length=50, null=False, blank=False)
    prenom = models.CharField(max_length=50, null=True)
    class Sexe(models.TextChoices):
        MASCULIN = 'M', _('Masculin')
        FEMININ = 'F', _('Féminin')
    sexe = models.CharField(
        max_length=10,
        choices=Sexe.choices,
        default=Sexe.MASCULIN, )
    class Meta:
        verbose_name = "Professeur"
    def __str__(self):
        return self.nom+" "+self.post_nom+" "+self.prenom


class ProfAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "post_nom", "prenom", "sexe")


class Course(models.Model):
    nom = models.CharField(max_length=50, null=False, blank=False)
    prof = models.CharField(max_length=100, null=True, blank=True)
    classe = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, verbose_name="Classe")
    heures = models.IntegerField(default=1)
    maximum = models.IntegerField(default=10)
    fiche = models.FileField(null=True, upload_to=f"fiches_cotation", default="fiches_cotation/default/default.xls")
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Utilisateur")
 
    class Meta:
        verbose_name = "Cours"

    def __str__(self):
        return self.nom+"("+self.classe.nom+")"

    @property
    def get_half_max(self):
        return self.maximum/2
    
    @property
    def get_half_max_exam(self):
        return self.maximum 
    
    @property
    def get_max_exam(self):
        return self.maximum * 2
        
    @property
    def get_max_semester(self):
        return (self.maximum * 4) 
    
    @property
    def get_half_max_semester(self):
        return (self.maximum * 4)/2

    @property
    def get_max_annual(self):
        return (self.maximum * 8)
    


class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "prof", "classe", "heures", "utilisateur")