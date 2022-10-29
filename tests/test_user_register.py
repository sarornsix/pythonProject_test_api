import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):

    data2 = [
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'}, 0),
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'}, 1),
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'}, 2),
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'}, 3),
        ({'password': '132', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'}, 4)
    ]

    @pytest.mark.parametrize('data, t', data2)
    def test_create_incomplete_data(self, data, t):
        n = ['password', 'username', 'firstName', 'lastName', 'email']
        data.pop(n[t])
        # print(data.pop(n[t]))
        response = MyRequests.post("user", data=data)
        Assertions.assert_code_status(response, 400)
        # print(response.content)
        assert response.content.decode("utf-8") == f"The following required params are missed: {n[t]}", \
            f"Unexpected response content {response.content}"
        # The following required params are missed: firstName

    m = ""

    data1 = [
        ({'password': m, 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'}),
        ({'password': '123', 'username': '', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'}),
        ({'password': '123', 'username': 'learnqa', 'firstName': '', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'}),
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': '', 'email': 'vinkotov@example.com'}),
        ({'password': '132', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': ''})
    ]

    @pytest.mark.parametrize('data', data1)
    def test_create_empty_data(self, data):
        response = MyRequests.post("user", data=data)
        Assertions.assert_code_status(response, 400)
        print(response.content)

        q = 0
        n = ['password', 'username', 'firstName', 'lastName', 'email']
        for a in n:
            if data.get(n[q]) == "":
                print(n[q], " пустое значение")
                assert response.content.decode("utf-8") == f"The value of '{a}' field is too short", \
                    f"Unexpected response content {response.content}"
            q = q + 1

            # if response.content.decode("utf-8") == f"The value of '{a}' field is too short":
            #     print(f"The value of '{a}' field is too short")


    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("user", data=data)
        # assert response.status_code == 200, f"Unexpected status code {response.status_code}"
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")


    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("user", data=data)

        print(response.status_code)
        print(response.content)
        print(response.text)

        # assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_Invalid_email_format(self):
        email = "vinkotovexample.com"
        data = {
            'password': "1234",
            'username': "learnqa",
            'firstName': "learnqa",
            'lastName': "learnqa",
            'email': email
        }

        response = MyRequests.post("user", data=data)

        # print(response.status_code)
        # print(response.content)
        # print(response.text)

        # assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format"