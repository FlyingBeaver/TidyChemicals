from api.tests.setup import BasicApiTest, dict_to_namedtuple
from profiles.models import Profile


class UsersApiTest(BasicApiTest):
    def test_users_read(self):
        self.billie_eilish_logs_in()
        users_response = self.client.get("/api/v1/users")
        self.assertEqual(users_response.status_code, 200)
        response_data = list(users_response.data)
        self.assertTrue(response_data)
        users_list = list(users_response.data)
        recent = users_list.pop()
        reference_users_list = []
        for prof in Profile.objects.all():
            reference_users_list.append(
                {"username": prof.user.username,
                "first_name": prof.user.first_name,
                "last_name": prof.user.last_name}
            )
        # For comparison lists they must be sorted first.
        # For sorting list values must support > and <, but dicts
        # don't. Namedtules do, so dicts will be converted to
        # namedtuples
        users_namedtuples_list = list(
            map(dict_to_namedtuple,
                users_list)
        )
        reference_users_namedtuples_list = list(
            map(dict_to_namedtuple,
                reference_users_list)
        )
        users_namedtuples_list.sort()
        reference_users_namedtuples_list.sort()
        self.assertEqual(users_namedtuples_list,
                         reference_users_namedtuples_list)
        recent_reference = self.billie_eilish.search_preferences
        recent_reference.pop("search_fields")
        self.assertEqual(
            recent,
            recent_reference
        )

    def test_users_read_unauthorized(self):
        users_response = self.client.get("/api/v1/users")
        self.assertEqual(users_response.status_code, 403)
