from django import forms
from django.utils.text import slugify
from .models import Article, Categorie, Auteur, Commentaire, Like


# ── Formulaire Article ─────────────────────────────────────────
class ArticleForm(forms.ModelForm):
    class Meta:
        model  = Article
        fields = ['titre', 'categories', 'contenu', 'extrait',
                  'image_couverture', 'statut']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de l article',
            }),
            'categories': forms.CheckboxSelectMultiple(),  # Cases a cocher
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
            }),
            'extrait': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Courte description visible dans la liste...',
            }),
            'statut': forms.Select(attrs={'class': 'form-select'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Generer le slug automatiquement depuis le titre
        if not instance.slug:
            instance.slug = slugify(instance.titre)
        if commit:
            instance.save()
            self.save_m2m()   # OBLIGATOIRE pour sauvegarder ManyToMany
        return instance


# ── Formulaire Categorie ───────────────────────────────────────
class CategorieForm(forms.ModelForm):
    class Meta:
        model  = Categorie
        fields = ['nom', 'description', 'couleur']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'couleur': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.nom)
        if commit:
            instance.save()
        return instance


# ── Formulaire Profil Auteur ───────────────────────────────────
class AuteurForm(forms.ModelForm):
    class Meta:
        model  = Auteur
        fields = ['bio', 'photo', 'site_web']
        widgets = {
            'bio':      forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'site_web': forms.URLInput(attrs={'class': 'form-control'}),
        }


# ── Formulaire Commentaire ─────────────────────────────────────
class CommentaireForm(forms.ModelForm):
    class Meta:
        model  = Commentaire
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Votre commentaire...',
            })
        }
        labels = {'contenu': 'Votre commentaire'}
# class LikeForm(forms.ModelForm):
#     class Meta:
#         model = Like
        