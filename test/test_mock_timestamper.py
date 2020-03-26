def test_mock_stamper(mock_timestamper):

    stamped_dict = mock_timestamper(None, None, {})

    assert stamped_dict["timestamp"] == mock_timestamper.timestamp
