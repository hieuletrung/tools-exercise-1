from django.test import TestCase
from .models import Post

class PostModelTest(TestCase):

    def setUp(self):
        Post.objects.create(title="Test Post", content="This is a test.")

    def test_post_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.title}'
        self.assertEqual(expected_object_name, 'Test Post')

class PostListViewTest(TestCase):

    def setUp(self):
        Post.objects.create(title="Another Post", content="More content.")

    def test_view_url_exists_at_proper_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_view_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'blog/post_list.html')

