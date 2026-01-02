import http.client
import os
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest

BASE_URL = "http://localhost:5000"
BASE_URL_MOCK = "http://localhost:9090"
DEFAULT_TIMEOUT = 2  # in secs

@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/1/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)    # nosec B310
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3", "ERROR ADD"
        )

    def test_api_substract(self):
        url = f"{BASE_URL}/calc/substract/5/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)    # nosec B310
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3", "ERROR SUBSTRACT"
        )

    def test_api_multiply(self):
        url = f"{BASE_URL}/calc/multiply/3/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)    # nosec B310
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "9", "ERROR MULTIPLY"
        )

    def test_api_divide(self):
        url = f"{BASE_URL}/calc/divide/12/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)    # nosec B310
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "4.0", "ERROR DIVIDE"
        )

    def test_api_divide_by_zero(self):
        url = f"{BASE_URL}/calc/divide/12/0"
        with self.assertRaises(HTTPError) as context:
            urlopen(url, timeout=DEFAULT_TIMEOUT)   # nosec B310 
        self.assertEqual(context.exception.code, 406, "Se esperaba error 406 al dividir por cero")
        self.assertEqual(context.exception.read().decode(), "ERROR DIVIDE /0", "Mensaje de error incorrecto")


    def test_api_sqrt(self):
        url = f"{BASE_URL_MOCK}/calc/sqrt/64"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)    # nosec B310
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "8", "ERROR SQRT"
        )

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
