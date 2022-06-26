import pytest
from model_bakery import baker
from rest_framework.authtoken.admin import User
from rest_framework.test import APIClient

from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_fix():
    return baker.make(Student)


@pytest.fixture
def course():
    return baker.make(Course)


@pytest.fixture
def admin():
    return User.objects.create_user('admin')


@pytest.mark.django_db
def test_get_first_course():
    request = client.post('/api/v1/courses/',
                          data={'user': admin.id, 'name': 'demo1', 'students': ['demo1']},
                          format='json')
    res1 = client.post('/api/v1/courses', data={'name': 'demo1', 'students': admin.id}, format='json')

    responce = client.get('api/v1/courses/')

    assert responce.status_code == 200


@pytest.mark.django_db
def test_get_list_course():
    request = client.post('/api/v1/courses/',
                          data={'user': admin.id, 'name': 'demo1', 'students': ['demo1']},
                          format='json')
    res1 = client.post('/api/v1/courses', data={'name': 'demo1', 'students': admin.id}, format='json')
    res2 = client.post('/api/v1/courses', data={'name': 'demo2', 'students': admin.id}, format='json')
    res3 = client.post('/api/v1/courses', data={'name': 'demo3', 'students': admin.id}, format='json')
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_filter_course_id():
    res1 = client.post('/api/v1/courses', data={'name': 'demo1', 'students': admin.id}, format='json')
    res2 = client.post('/api/v1/courses', data={'name': 'demo2', 'students': admin.id}, format='json')
    res3 = client.post('/api/v1/courses', data={'name': 'demo3', 'students': admin.id}, format='json')

    responce = client.get('/api/v1/courses?id=1')

    assert responce.status_code == 200


@pytest.mark.django_db
def test_filter_course_name():
    res1 = client.post('/api/v1/courses', data={'name': 'demo1', 'students': admin.id}, format='json')
    res2 = client.post('/api/v1/courses', data={'name': 'demo2', 'students': admin.id}, format='json')
    res3 = client.post('/api/v1/courses', data={'name': 'demo3', 'students': admin.id}, format='json')

    responce = client.get('/api/v1/courses?name=demo1')

    assert responce.status_code == 200


@pytest.mark.django_db
def test_create_course(client, admin):
    request = client.post('/api/v1/courses/',
                          data={'user': admin.id, 'name': 'demo1', 'students': ['demo1']},
                          format='json')
    responce = client.post('/api/v1/courses', data={'name': 'demo1', 'students': admin.id}, format='json')
    assert responce.status_code == 201


@pytest.mark.django_db
def test_update_course(admin, client):
    request = client.post('/api/v1/courses/',
                          data={'user': admin.id, 'name': 'demo1', 'students': ['demo1']},
                          format='json')
    res = client.post('/api/v1/courses', data={'name': 'demo1', 'students': admin.id}, format='json')
    responce = client.put('/api/v1/courses/',
                          data={'user': admin.id, 'name': 'demo2', 'students': ['demo1']},
                          format='json')
    respon = client.put('/api/v1/courses/', data={'name': 'demo1', 'students': admin.id}, format='json')
    assert respon.status_code == 201


@pytest.mark.django_db
def test_delete_course():
    request = client.post('/api/v1/courses/',
                          data={'user': admin.id, 'name': 'demo1', 'students': ['demo1']},
                          format='json')
    res = client.post('/api/v1/courses', data={'name': 'demo1', 'students': admin.id}, format='json')
    responce = client.delete('/api/v1/courses/1/')
    assert responce.status_code == 400
