from backend.utils.security import verify_password, get_password_hash


class TestSecurity:
    def test_get_password_hash(self):
        password = "testpassword"
        hashed = get_password_hash(password)

        assert isinstance(hashed, str)
        assert hashed != password

    def test_verify_password_success(self):
        password = "testpassword"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed)

    def test_verify_password_failure(self):
        password = "testpassword"
        hashed = get_password_hash(password)

        assert not verify_password("wrongpassword", hashed)