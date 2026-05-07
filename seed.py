from django.contrib.auth.models import User
from blog.models import Auteur, Categorie, Article, Commentaire
from django.utils import timezone

# 1. Creer des utilisateurs
users_data = [
    {'username': 'mamadou_d', 'first_name': 'Mamadou', 'last_name': 'Diallo', 'email': 'mamadou@blog.sn'},
    {'username': 'fatou_s',   'first_name': 'Fatou',   'last_name': 'Sow',    'email': 'fatou@blog.sn'},
    {'username': 'ousmane_n', 'first_name': 'Ousmane', 'last_name': 'Ndiaye', 'email': 'ousmane@blog.sn'},
]
users = []
for d in users_data:
    u, _ = User.objects.get_or_create(username=d['username'], defaults=d)
    u.set_password('password123')
    u.save()
    users.append(u)

# 2. Creer les profils auteurs
auteurs = []
bios = ['Developpeur web passionne.', 'Designer UX/UI.', 'Journaliste tech.']
for u, bio in zip(users, bios):
    a, _ = Auteur.objects.get_or_create(user=u, defaults={'bio': bio})
    auteurs.append(a)

# 3. Creer des categories
cats_data = [
    ('Django',     'django',     '#2563EB', 'Tutoriels Django'),
    ('Python',     'python',     '#16A34A', 'Tutoriels Python'),
    ('React',      'react',      '#0D9488', 'Tutoriels React'),
    ('Actualites', 'actualites', '#D97706', 'Actualites tech'),
]
cats = {}
for nom, slug, couleur, desc in cats_data:
    c, _ = Categorie.objects.get_or_create(slug=slug, defaults={
        'nom': nom, 'couleur': couleur, 'description': desc
    })
    cats[slug] = c

# 4. Creer des articles
articles_data = [
    ('Debuter avec Django',      'debuter-avec-django',      auteurs[0], ['django', 'python']),
    ('Les modeles Django',        'les-modeles-django',        auteurs[0], ['django']),
    ('Introduction a React',     'introduction-a-react',     auteurs[1], ['react']),
    ('Django et React ensemble', 'django-et-react-ensemble', auteurs[2], ['django', 'react']),
]
articles = []
for titre, slug, auteur, cat_slugs in articles_data:
    a, _ = Article.objects.get_or_create(slug=slug, defaults={
        'titre': titre,
        'auteur': auteur,
        'contenu': f'Contenu complet de l article : {titre}.',
        'extrait': f'Extrait court de : {titre}.',
        'statut': 'publie',
        'date_publication': timezone.now(),
    })
    a.categories.set([cats[s] for s in cat_slugs])
    articles.append(a)

# 5. Creer des commentaires
for article in articles:
    for user in users[:2]:
        Commentaire.objects.get_or_create(
            article=article, auteur=user,
            defaults={'contenu': f'Super article sur {article.titre} !', 'approuve': True}
        )

print(f'OK : {User.objects.count()} users, {Auteur.objects.count()} auteurs,')
print(f'     {Categorie.objects.count()} categories, {Article.objects.count()} articles,')
print(f'     {Commentaire.objects.count()} commentaires.')