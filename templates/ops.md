{% if error %}
{{error}}
{% else %}
{% if apps_on %}

#Running:
{% for app in apps_on %} - *{{app.id}}* x {{app.instances}}
 -- config changed:  {{app.versionInfo.lastConfigChangeAt}}
 -- last scaling:  {{app.versionInfo.lastScalingAt}}
{% endfor %}

{% endif %}

{% if apps_off %}
#Stoped:
{% for app in apps_off %}
### [{{app.instances}}] {{app.id}}
{{app.container.docker.network}} | `{{app.container.docker.image}}`
{% endfor %}
{% endif %}

{% endif %}
