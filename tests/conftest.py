import pytest

from admon_connector.admon import AdmonConnector
from admon_connector.settings import Settings


@pytest.fixture
def connector():
    settings = Settings()  # type: ignore[assignment]
    return AdmonConnector(settings.admon_token)
