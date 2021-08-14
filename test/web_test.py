import requests

def test_compile():
    url = "http://localhost:8010/compile/"
    payload = {
        "workPath": "/tmp",
        "userName": "ljw",
    }
    requests.post(url, data=payload)


if __name__ == "__main__":
    test_compile()
