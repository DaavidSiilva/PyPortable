GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"

AVAILABLE_VERSIONS = {
    "3.14": {
        "description": "Python 3.14.2 (Latest)",
        "version": "3.14.2",
        "url": "https://www.python.org/ftp/python/3.14.2/python-3.14.2-embed-amd64.zip"
    },
    "3.13": {
        "description": "Python 3.13.1 (Stable)",
        "version": "3.13.1",
        "url": "https://www.python.org/ftp/python/3.13.1/python-3.13.1-embed-amd64.zip"
    },
    "3.12": {
        "description": "Python 3.12.10 (Old Stable)",
        "version": "3.12.10",
        "url": "https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip"
    },
    "3.11": {
        "description": "Python 3.11.9 (Old Stable)",
        "version": "3.11.9",
        "url": "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
    }
}

AVAILABLE_VERSIONS["latest"] = AVAILABLE_VERSIONS["3.14"]
