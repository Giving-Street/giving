import uuid

from giving_account.domain.model import Account, AccountProvider, AccountProfile


def test_create_account_should_return_expected_object():
    new_account = Account(email="test@noreply.com", provider="google")

    assert isinstance(new_account.id_, uuid.UUID)
    assert new_account.email == "test@noreply.com"
    assert new_account.provider == AccountProvider.GOOGLE
    assert new_account.profile is None


def test_account_change_profile_should_update_updated_at_column():
    new_account = Account(email="test@noreply.com", provider="google")
    new_profile = AccountProfile(nickname="test_user", account_id=new_account.id_)
    new_account.update_profile(profile=new_profile)

    assert new_account.created_at != new_account.updated_at
