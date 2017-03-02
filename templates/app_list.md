{% if error %}
{{error}}
{% else %}

{% if apps_on %}
#Running:
{% for app in apps_on %} - **{{app.id}}** x {{app.instances}}
{% endfor %}
{% endif %}

{% if apps_off %}
#Stoped:
{% for app in apps_on %} - **{{app.id}}** x {{app.instances}}
{% endfor %}
{% endif %}

{% endif %}
