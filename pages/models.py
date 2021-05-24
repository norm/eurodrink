import os

from django.conf import settings
from django.template.loader import render_to_string


class StaticPage:
    template_name = None

    def generate(self):
        output = self.render_template()
        filename = self.get_filename()
        self.write_file(filename, output)

    def get_filename(self):
        return 'index.html'

    def get_context(self):
        return {}

    def get_template_name(self):
        return self.template_name

    def render_template(self):
        template_name = self.get_template_name()
        context = self.get_context()
        return render_to_string(template_name, context)

    def write_file(self, filename, content):
        full_filename = os.path.join(settings.STATIC_PAGE_DIR, filename)
        directory = os.path.dirname(full_filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(full_filename, 'w') as handle:
            handle.write(content)
        print('++', full_filename)
