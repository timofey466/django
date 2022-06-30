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
    obj = course()
    responce = client.get(f'api/v1/courses/{obj.id}/')
    assert responce.status_code == 200


@pytest.mark.django_db
def test_get_list_course(course, admin, client):
    course(_quantity=3)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_filter_course_id(course, admin, client):
    course()
    responce = client.get(f'/api/v1/courses?id={course.id}')

    assert responce.status_code == 200


@pytest.mark.django_db
def test_filter_course_name(client, admin, course):
    course()
    responce = client.get(f'/api/v1/courses?name={course.name}')

    assert responce.status_code == 200


@pytest.mark.django_db
def test_create_course(client, admin, course):
    course()
    responce = client.post('/api/v1/courses', course())
    assert responce.status_code == 201


@pytest.mark.django_db
def test_update_course(admin, client, course):
    course()
    respon = client.put(f'/api/v1/courses/{course.id}', course())
    assert respon.status_code == 201


@pytest.mark.django_db
def test_delete_course(admin, client, course):
    course()
    responce = client.delete(f'/api/v1/courses/{course.id}/')
    assert responce.status_code == 400
