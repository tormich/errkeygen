{% if error %}
{{error}}
{% else %}
|Status  | Name                    | Network     | Image     |
|------- | ----------------------- | ------------|-----------|{% for app in apps %}
| {{app.instances}} | {{app.id}} | {{app.container.docker.network}} | `{{app.container.docker.image}}` |
{% endfor %}
{% endif %}
