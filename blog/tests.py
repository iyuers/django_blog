from django.test import TestCase, Client
from unittest.loader import makeSuite
import unittest


class Count(object):
    version = 2.0


# Create your tests here.
class DjangoTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_index(self):
        client = Client()
        response = client.post('/blog/login', {'username': 'admin', 'password': 'aiyue217964'})
        print(response.user.is_authenticated())
        print(response.status_code)
        print(response.META.HTTP_REFERER)
        print(response.session)
        self.assertRedirects(response, '/blog/index')
        self.client.get('/blog/index')

    @unittest.skip('not test')
    def test_login(self):
        pass

    @unittest.skipIf(Count.version > 1, '版本过低')
    def test_logout(self):
        pass

    @unittest.expectedFailure
    def test_register(self):
        pass


def get_suite():
    suite = makeSuite(DjangoTest, prefix='test')
    return suite


if __name__ == '__main__':
    s = get_suite()
    s.countTestCases()
    runner = unittest.TextTestRunner()
    runner.run(s)
