from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from habits.models import Action, Habit
from users.models import User


class ActionsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test1@user.com', password='123456', tg_chat_id='1234567890')
        self.otheruser = User.objects.create(email='test2@user.com', password='123456', tg_chat_id='9087654321')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.action = Action.objects.create(
            title='Тестовое действие', type_action='useful', user=self.user)

    def test_action_create(self):
        """Юниттест создания действия"""
        db_create = {'title': 'Действие для полезной привычки',
                     'type_action': 'useful',
                     'user': self.user.pk}
        url = reverse('habits:action-list')
        create_response = self.client.post(url, db_create)
        print(f'лог создания действия: {create_response, create_response.json()}')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data['title'], 'Действие для полезной привычки')
        self.assertEqual(create_response.data['type_action'], 'useful')
        print('-' * 20)

    def test_action_list_get(self):
        """Юниттест вывода списка привычек"""
        url = reverse('habits:action-list')
        list_response = self.client.get(url)
        print(f'лог вывода списка действий: {list_response, list_response.json()}')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data[0]['title'], 'Тестовое действие')
        self.assertEqual(list_response.data[0]['type_action'], 'useful')
        print('-' * 20)

    def test_action_retrieve(self):
        """Юниттест вывода детализации действия"""
        url = reverse('habits:action-detail', kwargs={'pk': self.action.pk})
        detail_response = self.client.get(url)
        print(f'лог детализации действия: {detail_response, detail_response.json()}')
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['title'], 'Тестовое действие')
        self.assertEqual(detail_response.data['type_action'], 'useful')
        print('-' * 20)

    def test_action_delete(self):
        """Юниттест удаления действия"""
        url = reverse('habits:action-detail', kwargs={'pk': self.action.pk})
        del_response = self.client.delete(url)
        print(f'лог удаления действия: {del_response}')
        self.assertEqual(del_response.status_code, status.HTTP_204_NO_CONTENT)
        print('-' * 20)

    def test_action_put(self):
        """Юниттест обновления привычки через put"""
        db_put = {'title': 'Полностью исправленное действие',
                  'type_action': 'pleasant',
                  'user': self.otheruser.pk}
        url = reverse('habits:action-detail', kwargs={'pk': self.action.pk})
        put_response = self.client.put(url, db_put)
        print(f'лог полного обновления действия: {put_response, put_response.json()}')
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.data['title'], 'Полностью исправленное действие')
        self.assertEqual(put_response.data['type_action'], 'pleasant')
        print('-' * 20)

    def test_action_patch(self):
        """Юниттест обновления действия через patch"""
        db_patch = {
            'title': 'Частично исправленное действие'
        }
        url = reverse("habits:action-detail", kwargs={'pk': self.action.pk})
        patch_response = self.client.patch(url, db_patch)
        print(f'лог частичного обновления действия: {patch_response, patch_response.json()}')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data['title'], 'Частично исправленное действие')
        print('-' * 20)


class HabitsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test1@user.com', password='123456', tg_chat_id='1234567890')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.action = Action.objects.create(
            title='Тестовое действие', type_action='useful', user=self.user)
        self.habit = Habit.objects.create(action=self.action, space='Дом', time='08:00:00', periodicity=3,
                                          runtime='00:02:00', is_public=True,
                                          last_date='2024-07-19T19:00:00+05:00', user=self.user)

    def test_habit_create(self):
        """Юниттест создания привычки"""
        db_create = {'action': self.action.pk,
                     'space': 'Дом',
                     'time': '08:00:00',
                     'periodicity': 7,
                     'runtime': '00:02:00',
                     'is_public': True,
                     'last_date': '2024-07-19T19:00:00+05:00',
                     'user': self.user.pk}
        create_response = self.client.post('/habits/habit/create/', db_create)
        print(f'лог создания привычки: {create_response, create_response.json()}')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.filter(id=1).count(), 1)
        print('-' * 20)

    def test_habits_list_get(self):
        """Юниттест вывода списка привычек"""
        get_response = self.client.get("/habits/list/")
        print(f'лог вывода списка привычек: {get_response, get_response.json()}')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 1)
        print('-' * 20)

    def test_public_habit_list_get(self):
        """Юниттест вывода списка публичны привычек"""
        get_response = self.client.get("/habits/public_list/")
        print(f'лог вывода списка публичных привычек: {get_response, get_response.json()}')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_habit_retrieve(self):
        """Юниттест вывода детализации привычки"""
        url = reverse("habits:habit_retrieve", kwargs={'pk': self.habit.pk})
        detail_response = self.client.get(url)
        print(f'лог детализации привычки: {detail_response, detail_response.json()}')
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['space'], 'Дом')
        self.assertEqual(detail_response.data['time'], '08:00:00')
        self.assertEqual(detail_response.data['runtime'], '00:02:00')
        self.assertEqual(detail_response.data['last_date'], '2024-07-19T19:00:00+05:00')
        print('-' * 20)

    def test_habit_delete(self):
        """Юниттест удаелния привычки"""
        url = reverse("habits:habit_destroy", kwargs={'pk': self.habit.pk})
        del_response = self.client.delete(url)
        print(f'лог удаления привычки: {del_response}')
        self.assertEqual(del_response.status_code, status.HTTP_204_NO_CONTENT)
        print('-' * 20)

    def test_habit_put(self):
        """Юниттест обновления привычки через put"""
        db_put = {
            'action': self.action.pk,
            'space': 'Любое место',
            'time': '19:00:00',
            'periodicity': 3,
            'runtime': '00:02:00',
            'is_public': True,
            'last_date': '2024-07-19T19:00:00+05:00',
            'user': self.user.pk
        }
        url = reverse("habits:habit_update", kwargs={'pk': self.habit.pk})
        put_response = self.client.put(url, db_put)
        print(f'лог полного обновления привычки: {put_response, put_response.json()}')
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.data['space'], 'Любое место')
        print('-' * 20)

    def test_habit_patch(self):
        """Юниттест обновления привычки через patch"""
        db_patch = {
            'is_public': False
        }
        url = reverse("habits:habit_update", kwargs={'pk': self.habit.pk})
        patch_response = self.client.patch(url, db_patch)
        print(f'лог частичного обновления привычки: {patch_response, patch_response.json()}')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data['is_public'], False)
        print('-' * 20)
