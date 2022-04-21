import pytest
from models import Role
from hamcrest import assert_that, equal_to, not_none


async def test_create_role(login_user, test_client, role_create_permission):
    role_name = "test-role"
    res = await test_client.post(
        path="/rest/createrole/",
        json={
            "name": role_name
        }
    )

    role_from_db = await Role.query.where(Role.name == role_name).gino.one_or_none()
    assert_that(role_from_db, not_none())


async def test_user_lacks_permission(login_user, test_client):
    res = await test_client.post(
        path="/rest/createrole/",
        json={
            "name": "test-role"
        }
    )

    assert_that(res.status_code, equal_to(403))
