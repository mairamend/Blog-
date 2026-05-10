from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Importation importante

app_name = 'blog'

urlpatterns = [

    # ── Accueil ───────────────────────────────────────────────
    path('', views.accueil, name='accueil'),

    # ── Articles ──────────────────────────────────────────────
    path('articles/',
         views.liste_articles,          name='article_liste'),

    path('articles/creer/',
         views.creer_article,           name='article_creer'),

    path('articles/<slug:slug>/',
         views.detail_article,          name='article_detail'),

    path('articles/<slug:slug>/modifier/',
         views.modifier_article,        name='article_modifier'),

    path('articles/<slug:slug>/supprimer/',
         views.supprimer_article,       name='article_supprimer'),

    # ── Categories ────────────────────────────────────────────
    path('categories/',
         views.liste_categories,        name='categorie_liste'),

    path('categories/creer/',
         views.creer_categorie,         name='categorie_creer'),

    path('categories/<slug:slug>/',
         views.detail_categorie,        name='categorie_detail'),

    path('categories/<slug:slug>/modifier/',
         views.modifier_categorie,      name='categorie_modifier'),

    # ── Auteurs ───────────────────────────────────────────────
    path('auteurs/',
         views.liste_auteurs,           name='auteur_liste'),

    path('auteurs/<int:pk>/',
         views.detail_auteur,           name='auteur_detail'),

    path('mon-profil/modifier/',
         views.modifier_profil,         name='auteur_modifier'),
    path('articles/<slug:slug>/commenter/',
         views.ajouter_commentaire,     name='commentaire_ajouter'),

    path('commentaires/<int:pk>/supprimer/',
         views.supprimer_commentaire,   name='commentaire_supprimer'),
#     Registration
    path('connexion/', auth_views.LoginView.as_view(template_name='blog/registration/login.html'), name='login'),
    path('deconnexion/', auth_views.LogoutView.as_view(), name='logout'),
    # systeme de like
    path('article/<slug:slug>/like/', views.liker_article, name='liker_article'),
#     Recherche globale
    path('recherche/', views.recherche_globale, name='recherche_globale'),
]
