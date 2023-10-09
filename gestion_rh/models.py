# gestion_rh/models.py
from django.db import models
from django.contrib.auth.models import User
from auditlog.models import AuditlogHistoryField
from gestion_materiel.models import TypeMateriel
import uuid



# Modèle pour les services RH
class Services(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.nom

# Modèle pour les employés
class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=200, blank=True, null=True)
    prenom = models.CharField(max_length=200, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    sexe = models.CharField(max_length=10, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    numero_telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    poste_actuel = models.CharField(max_length=100, blank=True, null=True)
    salaire = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_embauche = models.DateField(blank=True, null=True)
    photo_profil = models.ImageField(null=True, blank=True, upload_to='employe_profiles/', default="employe_profiles/user-default.png")
    cv = models.FileField(null=True, blank=True, upload_to='employe_cv/')
    is_chef_service = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        ordering = ['created']

    @property
    def imageURL(self):
        try:
            url = self.photo_profil.url
        except:
            url = ''
        return url

# Modèle pour les postes
class Postes(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.nom

# Modèle générique pour toutes les demandes
class Demande(models.Model):
    TYPE_CHOICES = (
        ('conge', 'Demande de congé'),
        ('materiel', 'Demande de matériel'),
        # Ajoutez d'autres types de demandes au besoin
    )

    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    objet_demande = models.CharField(max_length=20, choices=TYPE_CHOICES)
    pieces_jointes = models.ManyToManyField('gestion_rh.Demande', blank=True)
    statut = models.CharField(max_length=20, default='en attente')

    # Champs spécifiques à la demande de congé
    type_conge = models.ForeignKey('TypeConge', on_delete=models.CASCADE)
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)

    # Champs spécifiques à la demande de matériel
    type_materiel = models.ForeignKey(TypeMateriel, on_delete=models.CASCADE, blank=True, null=True)
    quantite_demandee = models.PositiveIntegerField(blank=True, null=True)
    caracteristique = models.TextField()
    # Service concerné
    service_concerne = models.ForeignKey(Services, on_delete=models.CASCADE, blank=True, null=True)
    # Champ UUID pour garantir l'unicité de chaque demande
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return f"Demande ({self.get_objet_demande_display()}) de {self.employe.nom} {self.employe.prenom}"

# Modèle pour les commentaires associés aux demandes
class CommentaireDemande(models.Model):
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE)
    auteur = models.ForeignKey(Employe, on_delete=models.CASCADE)
    commentaire = models.TextField()
    date_commentaire = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.auteur} sur la demande {self.demande}"

# Modèle pour les types de congé
class TypeConge(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.nom

class EvaluationPerformance(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_evaluation = models.DateField()
    resultat = models.TextField()

    def __str__(self):
        return f"Évaluation de {self.employe.nom} {self.employe.prenom}"

# Modèle pour les formations des employés
class Formation(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    nom_formation = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField()
    competences_acquises = models.TextField()

    def __str__(self):
        return f"Formation de {self.employe.nom} {self.employe.prenom}"


class Message(models.Model):
    sender = models.ForeignKey(
        Employe, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(
        Employe, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']

