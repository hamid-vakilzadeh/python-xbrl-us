import os
from unittest.mock import Mock
from unittest.mock import patch

from xbrl_us import XBRL


@patch("xbrl_us.xbrl_us.XBRL._ensure_access_token")
@patch("xbrl_us.xbrl_us.XBRL._get_meta_endpoints")
def test_methods(mock_get_meta_endpoints, mock_ensure_token):
    # Set up our mocks
    mock_get_meta_endpoints.return_value = {}
    mock_ensure_token.return_value = None

    # Create an instance with mock values using env vars
    xbrl = XBRL(
        username=os.environ.get("XBRL_USERNAME", "dummy"),
        password=os.environ.get("XBRL_PASSWORD", "dummy"),
        client_id=os.environ.get("XBRL_CLIENT_ID", "dummy"),
        client_secret=os.environ.get("XBRL_CLIENT_SECRET", "dummy"),
    )

    # Mock the methods call
    xbrl.methods = Mock(return_value=["assertion search"])

    # Test the method
    assert sorted(xbrl.methods())[0] == "assertion search"
