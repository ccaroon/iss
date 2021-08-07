import requests

class RestClient:
    """A class that encapsulates making RESTful calls"""

    def __init__(self, api, config, err_handler=None):
        self.api = api

        self.host = config.get('host', None)
        self._custom_headers = config.get('headers', {})

        self.__error_handler = err_handler

        self.__debug = False

    def debug(self, on_off=True):
        self.__debug = on_off

    def base_url(self):
        return F"{self.host}{self.api}"

    def get(self, url, qs=None):
        full_url = F"{self.base_url()}{url}"

        if self.__debug:
            self.__debug_print_req("GET", F"{full_url}?{qs}", self.__headers(), "")

        try:
            resp = requests.get(full_url, auth=self.__auth(), headers=self.__headers(), verify=False, params=qs)
            self.check_error(resp)
            return resp
        except Exception as e:
            return e

    def post(self, url, body={}):
        full_url = F"{self.base_url()}{url}"

        if self.__debug:
            self.__debug_print_req("POST", full_url, self.__headers(), body)

        resp = requests.post(full_url, json=body, auth=self.__auth(), headers=self.__headers(), verify=False)
        self.check_error(resp)
        return(resp)

    def put(self, url, body={}):
        full_url = F"{self.base_url()}{url}"

        if self.__debug:
            self.__debug_print_req("PUT", full_url, self.__headers(), body)

        resp = requests.put(full_url, json=body, headers=self.__headers())
        self.check_error(resp)
        return(resp)

    def delete(self, url, qs=None):
        full_url = F"{self.base_url()}{url}"

        if self.__debug:
            self.__debug_print_req("DELETE", F"{full_url}?{qs}", self.__headers(), "")

        resp = requests.delete(full_url, auth=self.__auth(), headers=self.__headers(), verify=False, params=qs)
        self.check_error(resp)
        return(resp)

    def update_headers(self, headers):
        self._custom_headers = headers

    def check_error(self, response):
        if self.__error_handler:
            self.__error_handler(response)
        else:
            if response.status_code >= 400:
                raise Exception(F"{response.status_code} - {response.reason} [{response.text}]")

    def __debug_print_req(self, method, url, headers, body):
        print(F"{method} {url}\n{headers}\n{body}")

    def __auth(self):
        auth = None
        if (hasattr(self, 'username')):
            auth = (self.username, self.password)

        return (auth)

    def __headers(self):
        headers = {}
        if (hasattr(self, '_custom_headers')):
            headers = self._custom_headers

        return (headers)

    def __str__(self):
        if (hasattr(self, 'username')):
            str = F"{self.username}@{self.host}/{self.api}"
        else:
            str = F"{self.host}/{self.api}"

        return str

    # --------------------------------------------------------------------------
