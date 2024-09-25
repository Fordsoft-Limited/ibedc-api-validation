from users.models import CustomUser
from rest_framework.test import APITestCase
from users.serializers import ( ChangePasswordSerializer)

class TestChangePasswordSerializer(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            name="odofin", username="oyejide", password="admin", role="USER"
        )

    def test_that_change_password_payload_is_valid(self):
        context = {"old_password": "admin", "new_password": "admin1233"}
        serializer = ChangePasswordSerializer(data=context, context={"user": self.user})
        self.assertTrue(serializer.is_valid())
        saved_user = serializer.save()
        self.assertTrue(saved_user.check_password('admin1233'))
    def test_that_change_password_payload_is_not_valid(self):
        context = {"old_password": "test", "new_password": "admin1233"}
        serializer = ChangePasswordSerializer(data=context, context={"user": self.user})
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors)
    def test_that_change_password_payload_require_password_and_old_password(self):
        context = {"old_password": "", "new_password": ""}
        serializer = ChangePasswordSerializer(data=context, context={"user": self.user})
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors)
        self.assertTrue("new_password" in serializer.errors)
        self.assertTrue("old_password" in serializer.errors)
    
