import unittest
from core import collect


class TestCollect(unittest.TestCase):
    def test_if_we_get_viz_release(self):
        mock_data = {
            "name": "a",
            "img": "img",
            "link": "link",
            "publisher": "publisher",
        }
        response = collect.get_viz()
        assert response[0].keys() == mock_data.keys()

    def test_if_we_get_yen_release(self):
        mock_data = {
            "name": "a",
            "img": "img",
            "link": "link",
            "publisher": "publisher",
        }
        response = collect.get_yen()
        assert response[0].keys() == mock_data.keys()

    def test_if_we_get_sevenseas_release(self):
        mock_data = {
            "name": "a",
            "img": "img",
            "link": "link",
            "publisher": "publisher",
        }
        response = collect.get_seven_seas()
        assert response[0].keys() == mock_data.keys()

    def test_if_we_get_darkhorse_release(self):
        mock_data = {
            "name": "a",
            "img": "img",
            "link": "link",
            "publisher": "publisher",
        }
        response = collect.get_dark_horse()
        assert response[0].keys() == mock_data.keys()

    def test_if_we_get_kodansha_release(self):
        mock_data = {
            "name": "a",
            "img": "img",
            "link": "link",
            "publisher": "publisher",
        }
        response = collect.get_kodansha()
        assert response[0].keys() == mock_data.keys()
