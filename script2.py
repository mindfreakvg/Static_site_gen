import yaml
import glob
import os
from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader


navigation = []
location = 'templates'

with open('templates/nav.yaml', 'r') as f:
    navigations = yaml.safe_load(f)

yaml_files = glob.glob('pages/*.yaml')
for yaml_file in yaml_files:

    with open(yaml_file) as data_file:
        data = yaml.safe_load(data_file)

    navigation.append({
        'name': data['title'],
        'url': data['url'],
        'order': data['order']
    })
    navigation = sorted(navigation, key=lambda x: x['name'])
    with open('templates/nav.yaml', 'w') as nav:
        yaml.safe_dump(navigation, nav)
    with open('posts/footer.md') as foot:
        footer = yaml.safe_load(foot)

    with open(data['article']) as markdown_file:
        article = markdown(markdown_file.read())

    template_env = Environment(loader=FileSystemLoader(searchpath='./'))
    template = template_env.get_template('layout.html')
    with open(os.path.join(location, data['url']), 'w') as output_file:
        output_file.write(
            template.render(
                title=data['title'],
                article=article,
                navigation=navigations,
                footer=footer
            )
        )
