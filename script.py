from locust import HttpLocust, TaskSet, task, between
import json

# locust -f script.py -c 1000 -r 10

# Follow, favorite and comment won't work because mongo no longer supports 'array.push(element)' after 3.4.x; Node.js -> Models -> User.js -> Line 82 ===> array = array.concat([element]);
class UserBehavior(TaskSet):

    def __init__(self, parent):
       super(UserBehavior, self).__init__(parent)
       self.headers = {}
       self.token = ''
       self.slug = 'un-titulo-creado-por-pedro-nkjgdh'

    def on_start(self):
        self.token = self.login()
        self.headers = { 'Authorization': 'Token ' + self.token }

    def login(self):
        payload = {'user': {
            'email': 'laguerapedro@gmail.com',
            'password': '1234'
        }}
        response = self.client.post('/users/login', json=payload)
        return response.json()['user']['token']

    def register(self):
        payload = {'user': {
            'username': 'pedro',
            'email': 'laguerapedro@gmail.com',
            'password': '1234'
        }}
        self.client.post('/users', json=payload)

    @task
    def user(self):
        self.client.get('/user', headers=self.headers)

    @task
    def change_username(self):
        payload = {'user': {
            'username': 'pedro'
        }}
        self.client.put('/user', headers=self.headers, json=payload)

    @task
    def profile(self):
        self.client.get('/profiles/test', headers=self.headers)

    @task
    def tags(self):
        self.client.get('/tags', headers=self.headers)

    @task
    def articles(self):
        self.client.get('/articles')

    @task
    def feed(self):
        self.client.get('/articles/feed?limit=10', headers=self.headers)

    @task
    def article(self):
        self.client.get('/articles/{}'.format(self.slug), headers=self.headers)

    @task
    def comments(self):
        self.client.get('/articles/{}/comments'.format(self.slug))

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 9)
    host = 'http://10.6.128.158/api'
