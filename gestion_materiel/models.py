# gestion_materiel/models.py

from django.db import models
from auditlog.models import AuditlogHistoryField

# Modèle pour les types de matériel
class TypeMateriel(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# Modèle pour les fournisseurs
class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nom

# Modèle pour les Matériels
class Materiel(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    numero_serie = models.CharField(max_length=50, unique=True)
    type_materiel = models.ForeignKey(TypeMateriel, on_delete=models.CASCADE)
    date_acquisition = models.DateField()
    quantite_acquise = models.PositiveBigIntegerField()
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, blank=True)
    etat = models.CharField(
        max_length=20,
        choices=[("en_service", "En service"), ("en_reparation", "En réparation"), ("hors_service", "Hors service")]
    )

    def __str__(self):
        return self.nom

class Reparation(models.Model):
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    date_reparation = models.DateField()
    cout_reparation = models.DecimalField(max_digits=10, decimal_places=2)
    duree_indisponibilite = models.PositiveIntegerField()
    history = AuditlogHistoryField()

    def __str__(self):
        return f"Réparation de {self.materiel.nom}"

# Modèle pour l'affectation de matériel
class Affectation(models.Model):
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    employe = models.ForeignKey('gestion_rh.Employe', on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey('gestion_rh.Services', on_delete=models.CASCADE, null=True, blank=True)
    date_affectation = models.DateField()
    date_retour = models.DateField(null=True, blank=True)

    def __str__(self):
        if self.employe:
            return f"Affectation de {self.materiel.nom} à {self.employe.nom} {self.employe.prenom}"
        elif self.service:
            return f"Affectation de {self.materiel.nom} au service {self.service.nom}"
        else:
            return f"Affectation de {self.materiel.nom}"