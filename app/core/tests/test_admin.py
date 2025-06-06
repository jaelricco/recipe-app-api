"""
Test for Django Admin modifications. 
"""
from django.test import TestCase
from django.contrib.auth import get_user_model  # Import a function that returns the currently active User model.
from django.urls import reverse  # Import reverse to generate admin URLs dynamically by name.
from django.test import Client  # Import Django's test client to simulate browser requests in tests.


class AdminSiteTest(TestCase):  # Create a test class that inherits from Django's TestCase.
    """Test for Django Admin."""

    def setUp(self):  # This method runs before each test method.
        """Create user and client."""
        self.client = Client()  # Create a test client to simulate admin login and requests.

        self.admin_user = get_user_model().objects.create_superuser(  # Create a superuser (admin) so we can log into the admin area.
            email='admin@example.com',
            password='testpass123'
        )
        self.client.force_login(self.admin_user)  # Force login as the admin user using the test client.

        self.user = get_user_model().objects.create_user(  # Create a regular user to check if they appear in the admin list.

            email='user@example.com',
            password='testpass123',
            name='Test User'  # Assuming the User model has a 'name' field.
        )

    def test_users_list(self):
        """Test that users are listed on page."""

        # Generate the URL for the user list page in the admin (e.g., /admin/core/user/)
        # The name 'admin:core_user_changelist' comes from Django's admin URL naming convention.
        url = reverse('admin:core_user_changelist')

        res = self.client.get(url)  # Send a GET request to the admin user list page.

        self.assertContains(res, self.user.name)  # Check that the user's name is shown in the response (i.e., on the page).
        self.assertContains(res, self.user.email)  # Check that the user's email is shown as well.

    def test_edit_user_page(self):
        """Test the edit user page works."""

        # Generate the URL for the Django admin "edit user" page for a specific user.
        # 'admin:core_user_change' is the URL name Django uses for editing an existing user.
        url = reverse('admin:core_user_change', args=[self.user.id])  # We pass the user's ID as an argument so the URL points to that user's edit page.
        res = self.client.get(url)  # Use the test client (logged in as an admin) to send a GET request to the edit user page.

        self.assertEqual(res.status_code, 200)  # Check that the page loads successfully (status code 200 = OK).

    def test_create_user_page(self):
        """Test the create user page works."""

        # Generate the URL for the Django admin "add user" page.
        # 'admin:core_user_add' is the URL name Django uses for the create page of the User model.
        url = reverse('admin:core_user_add')
        res = self.client.get(url)  # Use the test client (which is logged in as an admin user) to send a GET request to the page.
        self.assertEqual(res.status_code, 200)  # Check that the page loaded successfully (HTTP status code 200 = OK).

