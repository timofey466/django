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
    def factory(*args, **kwargs):
        return baker.make(Student)
    return factory


@pytest.fixture
def course():
    def factory(*args, **kwargs):
        return baker.make(Course)
    return factory


@pytest.fixture
def admin():
    return User.objects.create_user('admin')


@pytest.mark.django_db
def test_get_first_course(course, admin, client):
    client.post(course(name='name', students=admin.id))
    responce = client.get(f'api/v1/courses/{course.id}/')
    assert responce.status_code == 200


@pytest.mark.django_db
def test_get_list_course(course, admin, client):
    client.post(course(name='name', students=admin.id))
    client.post(course(name='name1', students=admin.id))
    client.post(course(name='name2', students=admin.id))
    client.post(course(name='name3', students=admin.id))
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_filter_course_id(course, admin, client):
    client.post(course(name='name', students=admin.id))
    responce = client.get(f'/api/v1/courses?id={course.id}')

    assert responce.status_code == 200


@pytest.mark.django_db
def test_filter_course_name(client, admin, course):
    client.post(course(name='name', students=admin.id))
    responce = client.get(f'/api/v1/courses?name={course.name}')

    assert responce.status_code == 200


@pytest.mark.django_db
def test_create_course(client, admin, course):
    client.post('/api/v1/courses/',
                data={'user': admin.id, 'name': 'demo1', 'students': ['demo1']},
                format='json')
    responce = client.post('/api/v1/courses', data={'name': 'demo1', 'students': admin.id}, format='json')
    assert responce.status_code == 201


@pytest.mark.django_db
def test_update_course(admin, client, course):

    client.post('/api/v1/courses', course(name='name', students=admin.id))
    respon = client.put('/api/v1/courses/', course(name='name', students=admin.id))
    assert respon.status_code == 201


@pytest.mark.django_db
def test_delete_course(admin, client, course):
    client.post('/api/v1/courses/', course(name='name', students=admin.id))
    responce = client.delete(f'/api/v1/courses/{course.id}/')
    assert responce.status_code == 400
