from jinja2 import Template
with open('template/index.html') as file:
    template = Template(file.read())
    template.stream(title="Gravitee").dump("output.html")
