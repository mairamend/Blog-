from django.contrib import admin
from django.utils.html import format_html
from .models import Auteur, Categorie, Article, Commentaire
# Register your models here.

# ── Auteur ─────────────────────────────────────────────────────
@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display   = ['nom_complet', 'user', 'nb_articles', 'date_inscription']
    search_fields  = ['user__username', 'user__first_name', 'user__last_name']
    raw_id_fields  = ['user']     # Evite le dropdown avec des milliers d'users


# ── Categorie ──────────────────────────────────────────────────
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'afficher_badge', 'nb_articles', 'date_creation']
    prepopulated_fields = {'slug': ('nom',)}   # Slug genere auto depuis le nom
    search_fields = ['nom']

    def afficher_badge(self, obj):
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:4px">{}</span>',
            obj.couleur, obj.nom
        )
    afficher_badge.short_description = 'Badge'


# ── Article ────────────────────────────────────────────────────
class CommentaireInline(admin.TabularInline):
    model  = Commentaire
    extra  = 0
    fields = ['auteur', 'contenu', 'approuve', 'date_creation']
    readonly_fields = ['date_creation']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display    = ['titre', 'auteur', 'statut', 'nb_vues', 'nb_commentaires', 'date_publication']
    list_filter     = ['statut', 'categories', 'date_publication']
    search_fields   = ['titre', 'contenu', 'auteur__user__username']
    prepopulated_fields = {'slug': ('titre',)}
    filter_horizontal = ['categories']    # Widget pratique pour ManyToMany
    list_editable   = ['statut']          # Modifier le statut directement dans la liste
    date_hierarchy  = 'date_publication'
    inlines         = [CommentaireInline] # Commentaires affiches dans la page article
    readonly_fields = ['nb_vues', 'date_creation', 'date_modification']
    actions         = ['publier_articles', 'archiver_articles']

    def publier_articles(self, request, queryset):
        from django.utils import timezone
        queryset.update(statut='publie', date_publication=timezone.now())
    publier_articles.short_description = 'Publier les articles selectionnes'

    def archiver_articles(self, request, queryset):
        queryset.update(statut='archive')
    archiver_articles.short_description = 'Archiver les articles selectionnes'


# ── Commentaire ────────────────────────────────────────────────
@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display   = ['auteur', 'article', 'approuve', 'date_creation']
    list_filter    = ['approuve', 'date_creation']
    list_editable  = ['approuve']
    search_fields  = ['auteur__username', 'contenu', 'article__titre']
    actions        = ['approuver_commentaires']

    def approuver_commentaires(self, request, queryset):
        queryset.update(approuve=True)
    approuver_commentaires.short_description = 'Approuver les commentaires selectionnes'