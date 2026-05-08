from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import math
# Create your models here.

class Auteur(models.Model):
    """
    Profil etendu d'un utilisateur Django.
    OneToOneField : 1 User = 1 Auteur (jamais plus).
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,     # Si le User est supprime, l'Auteur aussi
        related_name='auteur',        # user.auteur pour acceder au profil
        verbose_name='Utilisateur',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Biographie',
        help_text='Presentation de l auteur',
    )
    photo = models.ImageField(
        upload_to='auteurs/',         # Stocke dans media/auteurs/
        blank=True,
        null=True,
        verbose_name='Photo de profil',
    )
    site_web = models.URLField(
        blank=True,
        verbose_name='Site web',
    )
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Auteur'
        verbose_name_plural = 'Auteurs'
        ordering = ['user__last_name']

    def __str__(self):
        return f'{self.user.get_full_name()} (@{self.user.username})'

    def get_absolute_url(self):
        return reverse('blog:auteur_detail', kwargs={'pk': self.pk})

    @property
    def nom_complet(self):
        return self.user.get_full_name() or self.user.username

    @property
    def nb_articles(self):
        return self.articles.filter(statut='publie').count()
    @property
    def initiales(self):
        # On récupère la première lettre du prénom et du nom en majuscules
        first = self.user.first_name[0].upper() if self.user.first_name else ""
        last = self.user.last_name[0].upper() if self.user.last_name else ""
        # Si l'utilisateur n'a ni nom ni prénom, on prend la 1ère lettre du username
        if not first and not last:
            return self.user.username[0].upper() if self.user.username else "?"
        return f"{first}{last}"
    @property
    def moi_annee_inscription(self):
        return f"{self.date_inscription.strftime("%B %Y")} "
    
class Categorie(models.Model):
    """
    Categorie d'articles. Un article peut appartenir a plusieurs categories.
    """
    nom = models.CharField(
        max_length=100,
        unique=True,           # Pas de doublons de nom
        verbose_name='Nom',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text='Identifiant URL (genere automatiquement)',
    )
    description = models.TextField(blank=True, verbose_name='Description')
    couleur = models.CharField(
        max_length=7,
        default='#3B82F6',    # Couleur hexadecimale pour le badge
        verbose_name='Couleur (hex)',
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('blog:categorie_detail', kwargs={'slug': self.slug})

    @property
    def nb_articles(self):
        return self.articles.filter(statut='publie').count()
class Article(models.Model):
    """
    Article de blog. Coeur de l'application.
    """
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie',    'Publie'),
        ('archive',  'Archive'),
    ]

    titre = models.CharField(max_length=200, verbose_name='Titre')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text='Identifiant URL unique',
    )
    auteur = models.ForeignKey(
        Auteur,
        on_delete=models.SET_NULL,    # Si l'auteur est supprime, article conserve (auteur=NULL)
        null=True,
        related_name='articles',      # auteur.articles.all() pour obtenir ses articles
        verbose_name='Auteur',
    )
    categories = models.ManyToManyField(
        Categorie,
        blank=True,
        related_name='articles',      # categorie.articles.all()
        verbose_name='Categories',
    )
    contenu = models.TextField(verbose_name='Contenu')
    extrait = models.TextField(
        blank=True,
        max_length=500,
        verbose_name='Extrait',
        help_text='Courte description pour la liste',
    )
    image_couverture = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True,
        verbose_name='Image de couverture',
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='brouillon',
        verbose_name='Statut',
    )
    date_creation  = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_publication = models.DateTimeField(null=True, blank=True)
    nb_vues = models.PositiveIntegerField(default=0, verbose_name='Nombre de vues')
    temps_de_lecture = models.PositiveBigIntegerField(editable=False,default=0)
    
    
    def save(self, *args, **kwargs):
        mots = self.contenu.split()
        nb_mots = len(mots)
        self.temps_lecture = math.ceil(nb_mots / 200)
        
        super().save(*args,**kwargs)
        

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-date_publication', '-date_creation']

    def __str__(self):
        return self.titre
    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})

    @property
    def nb_commentaires(self):
        return self.commentaires.filter(approuve=True).count()

    def incrementer_vues(self):
        self.nb_vues += 1
        self.save(update_fields=['nb_vues'])  # Update partiel : plus efficace


class Commentaire(models.Model):
    """
    Commentaire laisse sur un article.
    Lie a un Article (ForeignKey) et a un User Django (ForeignKey).
    """
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,     # Si l'article est supprime, commentaires aussi
        related_name='commentaires',
        verbose_name='Article',
    )
    auteur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='commentaires',
        verbose_name='Auteur',
    )
    contenu = models.TextField(
        verbose_name='Commentaire',
        max_length=2000,
    )
    approuve = models.BooleanField(
        default=False,
        verbose_name='Approuve',
        help_text='Seuls les commentaires approuves sont visibles',
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Commentaire'
        verbose_name_plural = 'Commentaires'
        ordering = ['date_creation']

    def __str__(self):
        auteur_nom = self.auteur.username if self.auteur else 'Utilisateur supprime'
        return f'Commentaire de {auteur_nom} sur "{self.article.titre[:40]}"'    
class Like(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name='like'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    date_like = models.DateTimeField(auto_now_add=True)
    
    class Meta :
        unique_together = ('article','user')
        
        def __str__(self):
            return f"{self.user.username} aime {self.article.titre} "