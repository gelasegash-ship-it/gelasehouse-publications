from backend.app.security import hash_password, verify_password


def test_password_hash_round_trip():
    stored = hash_password("secret-123")
    assert stored != "secret-123"
    assert verify_password("secret-123", stored)
    assert not verify_password("wrong", stored)
