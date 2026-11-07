import templates

PyCharmMiscProject/

├─script5.py
└─templates/base.html<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Multitâches Cloud</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #121212; color: white; }
        .card { background: #1e1e1e; }
        .btn-primary { background: #4e73df; border: none; }
    </style>
</head>
<body>

<nav class="navbar navbar-dark bg-dark px-3">
    <span class="navbar-brand">🚀 Multitâches Cloud</span>
    {% if current_user.is_authenticated %}
        <a href="/dashboard" class="btn btn-outline-light btn-sm">Dashboard</a>
        <a href="/logout" class="btn btn-danger btn-sm">Déconnexion</a>
    {% endif %}
</nav>

<div class="container mt-5">
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for msg in messages %}
                <div class="alert alert-warning">{{ msg }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    {% block content %}{% endblock %}
</div>

</body>
</html>

    ├── base.html
    ├── login.html{% extends "base.html" %}
{% block content %}
<div class="card p-4 mx-auto" style="max-width:400px;">
    <h3>Connexion</h3>
    <form method="POST">
        <input name="username" class="form-control mb-3" placeholder="Utilisateur">
        <input name="password" type="password" class="form-control mb-3" placeholder="Mot de passe">
        <button class="btn btn-primary w-100">Connexion</button>
    </form>
    <a href="/register" class="btn btn-link text-light">Créer un compte</a>
</div>
{% endblock %}

    ├── register.html{% extends "base.html" %}
{% block content %}
<div class="card p-4 mx-auto" style="max-width:400px;">
    <h3>Créer un compte</h3>
    <form method="POST">
        <input name="username" class="form-control mb-3" placeholder="Utilisateur">
        <input name="password" type="password" class="form-control mb-3" placeholder="Mot de passe">
        <button class="btn btn-success w-100">Créer</button>
    </form>
</div>
{% endblock %}

    ├── dashboard.html{% extends "base.html" %}
{% block content %}
<h2>📊 Tableau de bord</h2>

<div class="row mt-4">
    <div class="col-md-4">
        <div class="card p-3 text-center">
            <h4>Victoires</h4>
            <h2>{{ stats[0] }}</h2>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card p-3 text-center">
            <h4>Défaites</h4>
            <h2>{{ stats[1] }}</h2>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card p-3 text-center">
            <h4>Matchs nuls</h4>
            <h2>{{ stats[2] }}</h2>
        </div>
    </div>
</div>

<div class="mt-5">
    <a href="/tictactoe" class="btn btn-primary">❌ Morpion</a>
    <a href="/notes" class="btn btn-secondary">📝 Notes</a>
    <a href="/cts" class="btn btn-info">🗺️ Plan CTS</a>
</div>
{% endblock %}

    ├── notes.html{% extends "base.html" %}
{% block content %}
<h2>📝 Notes</h2>

<form method="POST">
    <textarea name="notes" class="form-control mb-3" rows="10">{{ note }}</textarea>
    <button class="btn btn-success">Sauvegarder</button>
</form>
{% endblock %}

    ├── cts.html{% extends "base.html" %}
{% block content %}
<h2>🗺️ Plan CTS Strasbourg</h2>

<img src="https://upload.wikimedia.org/wikipedia/commons/5/55/Strasbourg_tramway_map.png"
     class="img-fluid rounded shadow">
{% endblock %}

    └── tictactoe.html

