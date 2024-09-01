from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

CustomUser = get_user_model()

class CustomUserTests(TestCase):
    """
    Test cases for creating CustomUser instances with various parameters.
    """

    def test_create_user_with_email(self):
        """
        Test the creation of a user with an email and password. Verify that
        the user instance has the correct email, password, and default attributes.
        """
        email = 'testuser@example.com'
        password = 'testpassword'
        user = CustomUser.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """
        Test the creation of a superuser with email and password. Verify that
        the superuser instance has the correct email, password, and is marked
        as a staff member and superuser.
        """
        email = 'superuser@example.com'
        password = 'superpassword'
        user = CustomUser.objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_without_email(self):
        """
        Test that creating a user without an email raises a ValueError. 
        Ensure that email is a required field for user creation.
        """
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email=None, password='testpassword')

class UniqueEmailTests(TestCase):
    """
    Test cases to ensure email uniqueness constraint in CustomUser model.
    """

    def test_duplicate_email_raises_error(self):
        """
        Test that attempting to create a user with a duplicate email raises 
        a ValidationError. This ensures that the email field is unique.
        """
        email = 'duplicate@example.com'
        CustomUser.objects.create_user(email=email, password='password1')
        with self.assertRaises(ValidationError):
            user = CustomUser(email=email)
            user.full_clean()  

class UserPermissionsTests(TestCase):
    """
    Test cases to verify user permissions and access control.
    """

    def setUp(self):
        """
        Set up test users: a regular user and a superuser.
        """
        self.user = CustomUser.objects.create_user(email='user@example.com', password='password')
        self.superuser = CustomUser.objects.create_superuser(email='admin@example.com', password='password')

    def test_user_has_no_permissions(self):
        """
        Test that a regular user does not have permissions or module permissions
        by default.
        """
        self.assertFalse(self.user.has_perm('some_permission'))
        self.assertFalse(self.user.has_module_perms('some_module'))

    def test_superuser_has_permissions(self):
        """
        Test that a superuser has all permissions and module permissions.
        """
        self.assertTrue(self.superuser.has_perm('some_permission'))
        self.assertTrue(self.superuser.has_module_perms('some_module'))

class UserStrMethodTests(TestCase):
    """
    Test cases to validate the string representation of the CustomUser model.
    """

    def test_user_str_method(self):
        """
        Test that the string representation of a user instance returns the email.
        """
        user = CustomUser.objects.create_user(email='strtest@example.com', password='password')
        self.assertEqual(str(user), 'strtest@example.com')

class PasswordTests(TestCase):
    """
    Test cases to verify password handling for CustomUser.
    """

    def test_password_is_hashed(self):
        """
        Test that the password is hashed in the database and not stored in plain text.
        Verify that the hashed password can still be used for authentication.
        """
        user = CustomUser.objects.create_user(email='hash@example.com', password='plaintextpassword')
        self.assertNotEqual(user.password, 'plaintextpassword')
        self.assertTrue(user.check_password('plaintextpassword'))
