import requests
from requests import Session



class Stream(object):
    """represent a stream in flussonic"""
    def __init__(self, data):
        self.__dict__.update(data)
        self.keys_flu = data.keys()

    def show_fields(self):
        return self.keys_flu

    def __repr__(self):
        return "<Stream '%s'>" % self.name

class Flussonic(object):
    """flussonic api"""
    def __init__(self, url, auth=None):
        """init with url and auth tuple with usr and pwd"""
        self.auth = auth
        self.url = url

    def authorize(self, usr, pwd):
        """set auth tuple with usr, pwd"""
        self.auth = (usr, pwd)

    def _get(self, endpoint, args=None, serializer_class=None):
        """wrapper around get requests with authorized tuple and uncheck verify"""
        res = requests.get(self.url + endpoint, auth=self.auth , verify=False)
        if not serializer_class:
            return res.json()
        else:
            data = res.json()
            response = []
            for stream_data in data["streams"]:
                response.append(serializer_class(stream_data))
            return response

    def server(self):
        """get server stats"""
        return self._get("server")

    def media_info(self, stream_name):
        """Get info about stream"""
        return self._get("media_info/%s" % stream_name)

    def stream_health(self, stream_name):
        """get stream health"""
        return self._get("stream_health/%s" % stream_name)

    def streams(self):
        """get data from streams"""
        return self._get("streams", serializer_class=Stream)

    def files(self):
        """get files open"""
        return self._get("files")

    def sessions(self):
        """get sessions open"""
        return self._get("sessions")

    def dvr_status(self, stream_name, year, month, day):
        """get dvr_status of a give date and stream"""
        endpoint = "dvr_status/%s/%02d/%02d/%s" % (year, month, day, stream_name)
        return self._get(endpoint)

    def get_config(self):
        """get flussonic config"""
        return self._get("get_config")

def prepare(config):
    import getpass
    endpoint = raw_input("Please fill your flussonic api endpoint: ")
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    config.add_section("FLUSSPY")
    config.set("FLUSSPY", "username", username)
    config.set("FLUSSPY", "password", password)
    config.set("FLUSSPY", "endpoint", endpoint)
    config.write(open("/etc/flusspy/flusspy.conf", "w+"))
    return True

def cmd(args):
    from ConfigParser import ConfigParser
    import os
    config = ConfigParser()
    try:
        config.readfp(open("/etc/flusspy/flusspy.conf"))
    except IOError:
        prepare(config)
        print "Configured Succesfully see /etc/flusspy/flusspy.conf"

if __name__ == "__main__":
    flu = Flussonic(URL, AUTH)
    #print flu.dvr_status("my_stream", 2015, 9, 12)
    print flu.get_config()
