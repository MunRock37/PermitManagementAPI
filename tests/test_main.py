from datetime import datetime, timedelta

import pytest
from httpx import ASGITransport, AsyncClient

from app.database import SessionLocal, init_db
from app.main import app
from app.models import Permit
from tests.tasks import expire_old_permits


@pytest.fixture(autouse=True, scope="module")
def setup_db():
    init_db()


transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_permit_status_flow():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create a new permit (should be pending)
        res = await ac.post(
            "/permits",
            json={"name": "Alice", "license_plate": "ABC123", "address": "Maple St"},
            headers={"Authorization": "Bearer mocked-token"},
        )
        assert res.status_code == 200
        permit = res.json()
        assert permit["status"] == "pending"

        # Approve the permit
        res = await ac.post(
            f"/permits/{permit['id']}/approve",
            headers={"Authorization": "Bearer mocked-token"},
        )
        assert res.status_code == 200
        assert res.json()["status"] == "approved"

        # Revoke the permit
        res = await ac.post(
            f"/permits/{permit['id']}/revoke",
            headers={"Authorization": "Bearer mocked-token"},
        )
        assert res.status_code == 200
        assert res.json()["status"] == "revoked"


@pytest.mark.asyncio
async def test_expired_permit():
    # Create a pending permit with old created_at
    db = SessionLocal()
    old_permit = Permit(
        name="Bob",
        license_plate="XYZ789",
        address="Old St",
        status="pending",
        created_at=datetime.utcnow() - timedelta(days=2),
    )
    db.add(old_permit)
    db.commit()
    db.refresh(old_permit)
    db.close()

    # Run expiry task
    expire_old_permits()

    # Confirm the permit is expired
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get(
            "/permits?status=expired", headers={"Authorization": "Bearer mocked-token"}
        )
        assert res.status_code == 200
        data = res.json()
        assert any(p["id"] == old_permit.id and p["status"] == "expired" for p in data)
