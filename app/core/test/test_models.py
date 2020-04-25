from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """Test creating a new user with an email is successful created"""
        email = "jadoiradukunda@sigma-resources.com"
        password = "iradukunda78988@*::?!"

        user  = get_user_model().objects.create_user(
                email = email,
                password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
        """ Test if the user email passed is a normalized one(lower case)"""
        email = "jadoiradukunda@SIGMA-RESOURCES.COM";

        user = get_user_model().objects.create_user(email,"iradukunda78988&**?2")

        self.assertEqual(user.email,email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,"iradukunda90889**7")

    def test_create_new_superuser(self):
        """Test create new super user"""
        user =  get_user_model().objects.create_superuser("iradukunda@gmail.com","123")

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
