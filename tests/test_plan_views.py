import json
from datetime import datetime
from datetime import timedelta
from .utils import authenticate


class TestPlanListResource:
    def test_get(self, client, plan):
        authenticate(client, plan.user)

        res = client.get('/api/plans')
        assert(res.status_code == 200)

        data = json.loads(res.data.decode('utf-8'))
        assert(data)
        assert(isinstance(data, list))
        for d in data:
            assert(isinstance(d['id'], int))
            assert(isinstance(d['title'], str))
            assert(isinstance(d['user'], int))
            assert(isinstance(d['category'], str))
            assert(isinstance(d['load_unit'], str))
            assert(isinstance(d['private'], bool))
            assert(isinstance(d['active'], bool))
            assert(isinstance(d['user'], int))
            assert(isinstance(d['title'], str))
            assert(isinstance(d['description'], str))
            assert(isinstance(d['load_index'], int))
            assert((isinstance(d['total_load'], int) or
                    isinstance(d['total_load'], float)))
            assert((isinstance(d['daily_load'], int) or
                    isinstance(d['daily_load'], float)))
            assert(isinstance(d['cron'], str))
            assert(isinstance(d['start_at'], str))
            assert((isinstance(d['end_at'], str) or d['end_at'] is None))

    def test_post_with_no_stages_and_missing_total_load(
            self, session, client, user, category, unit):
        authenticate(client, user)
        payload = {
            'category': category.name,
            'load_unit': unit.name,
            'private': True,
            'active': True,
            'title': 'test title',
            'description': 'test description',
            'load_index': 0,
            'total_load': 200,
            'start_at': str(datetime.now()),
            'end_at': str(datetime.now() + timedelta(days=180)),
        }

        res = client.post(
            '/api/plans', data=json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(res.data.decode('utf-8'))

        assert(res.status_code == 200), res.data.decode('utf-8')
        for k, v in data.items():
            assert(payload[k] == v)

    def test_post_with_no_stages_and_missing_daily_load(
            self, session, client, user, category, unit):
        authenticate(client, user)
        payload = {
            'category': category.name,
            'load_unit': unit.name,
            'private': True,
            'active': True,
            'title': 'test title',
            'description': 'test description',
            'load_index': 0,
            'daily_load': 5,
            'start_at': str(datetime.now()),
            'end_at': str(datetime.now() + timedelta(days=180)),
        }

        res = client.post(
            '/api/plans', data=json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(res.data.decode('utf-8'))

        assert(res.status_code == 200), res.data.decode('utf-8')
        for k, v in data.items():
            assert(payload[k] == v)

    def test_post_with_no_stages_and_missing_end(
            self, session, client, user, category, unit):
        authenticate(client, user)
        payload = {
            'category': category.name,
            'load_unit': unit.name,
            'private': True,
            'active': True,
            'title': 'test title',
            'description': 'test description',
            'load_index': 0,
            'daily_load': 5,
            'start_at': str(datetime.now()),
            'end_at': str(datetime.now() + timedelta(days=180)),
        }

        res = client.post(
            '/api/plans', data=json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(res.data.decode('utf-8'))

        assert(res.status_code == 200), res.data.decode('utf-8')
        for k, v in data.items():
            assert(payload[k] == v)

    def test_post_with_stages(self, session, client, user, category, unit):
        authenticate(client, user)
        payload = {
            'category': category.name,
            'load_unit': unit.name,
            'private': True,
            'active': True,
            'title': 'test title',
            'description': 'test description',
            'load_index': 0,
            'total_load': 200,
            'daily_load': 3,
            'start_at': str(datetime.now()),
            'titles': ['test stage title0', 'test stage title1'],
            'loads': [1, 3],
        }

        res = client.post(
            '/api/plans', data=json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(res.data.decode('utf-8'))

        assert(res.status_code == 200), res.data.decode('utf-8')
        for k, v in data.items():
            if k in ['titles', 'loads']:
                continue
            else:
                assert(payload[k] == v)


class PlanResourceTest:
    def test_plan_resource_get(self, plan, client):
        pass

    def test_plan_resource_delete(self, plan, client):
        pass

    def test_plan_resource_put(self, plan, client):
        pass
