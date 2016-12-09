import os

from django.forms.renderers.templates import (
    DjangoTemplateRenderer, Jinja2TemplateRenderer, ProjectTemplateRenderer,
)
from django.forms.widgets import Input
from django.test import SimpleTestCase
from django.utils._os import upath


class SharedTests(object):

    def test_installed_apps_template_found(self):
        """Can find a custom template in INSTALLED_APPS."""
        renderer = self.renderer()
        # Found because forms_tests is .
        tpl = renderer.get_template('forms_tests/custom_widget.html')
        expected_path = os.path.abspath(
            os.path.join(
                upath(os.path.dirname(__file__)),
                '..',
                getattr(self, 'expected_widget_dir', 'templates') + '/forms_tests/custom_widget.html',
            )
        )
        self.assertEqual(tpl.origin.name, expected_path)

    def test_override_builtin_template(self):
        # TODO: this test isn't isolated -- the built-in template is overridden
        # for all forms_tests. If it's not identical, then it will cause
        # confusion.
        renderer = self.renderer()
        tpl = renderer.get_template(Input.template_name)
        expected_path = os.path.abspath(
            os.path.join(
                upath(os.path.dirname(__file__)),
                '..',
                getattr(self, 'expected_widget_dir', 'templates') + '/django/forms/widgets/input.html',
            )
        )
        self.assertEqual(tpl.origin.name, expected_path)


class DjangoTemplateRendererTests(SharedTests, SimpleTestCase):
    renderer = DjangoTemplateRenderer


class Jinja2TemplateRendererTests(SharedTests, SimpleTestCase):
    renderer = Jinja2TemplateRenderer
    expected_widget_dir = 'jinja2'


class ProjectTemplateRendererTests(SharedTests, SimpleTestCase):
    renderer = ProjectTemplateRenderer

    def test_override_builtin_template(self):
        # Not applicable
        pass
