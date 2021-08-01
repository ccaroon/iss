import requests
# import urllib3
# urllib3.disable_warnings()

# Singleton class
class RestClient:
    """A singleton class that encapsulates making RESTful calls"""

    __instance = None

    # Singleton handling stuff
    def __init__(self, api=None, config=None):
        if not RestClient.__instance:
            if api == None or config == None:
                raise ValueError("'api' and 'config' are required to instantiate a new instance.")
            else:
                RestClient.__instance = RestClient.new_instance(api, config)

    def __getattr__(self, name):
        return getattr(RestClient.__instance, name)

    @classmethod
    def new_instance(cls, api, config):
        return RestClient.__Instance(api, config)

    @classmethod
    def error(cls, response, as_exception=True):
        """Parse out the error message from the given response if any"""
        all_msgs = []

        data = response.json()
        for result in data:
            error_msg = None
            if 'error' in result:
                error = result['error']
                error_msg = F"Status Code: [{response.status_code}] | Reason: [{response.reason}]"
                error_msg += F" | Description: [{error.get('description', '?????')}]"

                if as_exception:
                    raise Exception(error_msg)
                else:
                    all_msgs.append(error_msg)

        return ('\n'.join(all_msgs))

    # Define instance methods here
    class __Instance:
        DEBUG = False

        def __init__(self, api, config):
            self.api = api

            self.host = config.get('host', None)
            self._custom_headers = config.get('headers', {})

        def __str__(self):
            if (hasattr(self, 'username')):
                str = "%s@%s/%s" % (self.username,self.host,self.api)
            else:
                str = "%s@%s/%s" % (self.token,self.host,self.api)

            return str

        def debug(self, on_off=True):
            self.DEBUG = on_off

        def base_url(self):
            return "{0}{1}".format(self.host, self.api)

        def get(self, url, qs=None):
            full_url = "{0}{1}".format(self.base_url(), url)

            if self.DEBUG:
                self.__debug_print_req("GET", "%s?%s" % (full_url,qs), self.__headers(), "")

            try:
                resp = requests.get(full_url, auth=self.__auth(), headers=self.__headers(), verify=False, params=qs)
                return resp
            except Exception as e:
                return e

        def post(self, url, body={}):
            full_url = "{0}{1}".format(self.base_url(), url)

            if self.DEBUG:
                self.__debug_print_req("POST", full_url, self.__headers(), body)

            resp = requests.post(full_url, json=body, auth=self.__auth(), headers=self.__headers(), verify=False)
            return(resp)

        def put(self, url, body={}):
            full_url = "{0}{1}".format(self.base_url(), url)

            if self.DEBUG:
                self.__debug_print_req("PUT", full_url, self.__headers(), body)

            resp = requests.put(full_url, json=body, headers=self.__headers())
            return(resp)

        def delete(self, url, qs=None):
            full_url = "{0}{1}".format(self.base_url(), url)

            if self.DEBUG:
                self.__debug_print_req("DELETE", "%s?%s" % (full_url,qs), self.__headers(), "")

            resp = requests.delete(full_url, auth=self.__auth(), headers=self.__headers(), verify=False, params=qs)
            return(resp)

        def update_headers(self, headers):
            self._custom_headers = headers

        def __debug_print_req(self, method, url, headers, body):
            print("%s %s\n%s\n%s" % (method, url, headers, body))

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
