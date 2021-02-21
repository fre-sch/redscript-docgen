<!doctype html>
<html lang="en">
<head>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet">
  <title>{% block title %}{% endblock %}</title>
  <style>@import url("{{base_uri}}/style.css");</style>
</head>
<body>
  <div class="container-fluid">
    <div class="row">
        <nav id="sidebar" class="sticky-top col-4"></nav>
        <main class="col-8">{% block body %}{% endblock %}</main>
    </div>
  </div>
<script src="{{base_uri}}/script.js"></script>
</body>
</html>