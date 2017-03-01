{% if error %}
{{error}}
{% else %}
{% if apps_on %}

# :white_check_mark: Running Apps:
{% for app in apps_on %}
### {{app.id.ljust(22)}} ({{app.instances}}) `{{app.container.docker.image}}`
{% endfor %}

{% endif %}

{% if apps_off %}
#:zzz: Stoped Apps:
{% for app in apps_off %}
### [{{app.instances}}] {{app.id}}
{{app.container.docker.network}} | `{{app.container.docker.image}}`
{% endfor %}
{% endif %}

{% endif %}
