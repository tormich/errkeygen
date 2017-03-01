{% if error %}
{{error}}
{% else %}
{% if apps_on %}
#:white_check_mark: Running services:
    {% for app in apps_on %}
    {{app.instances}} | {{app.id}} | {{app.container.docker.network}} | `{{app.container.docker.image}}`{% endfor %}
{% endif %}

{% if apps_off %}
#:zzz: Stoped services:
    {% for app in apps_off %}
    {{app.instances}} | {{app.id}} | {{app.container.docker.network}} | `{{app.container.docker.image}}`{% endfor %}
{% endif %}

{% endif %}
