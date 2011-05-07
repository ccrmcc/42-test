from models import HttpLogEntry

class HttpLogMiddleWare(object):
    def process_response(self, request, response):
        headers = [
                (name,val) 
                for name,val in request.META.items()
                if isinstance(val, basestring)
        ]
        to_log = {
                'method' : request.method,
                'headers' : headers,
                'path' : request.path,
                'cookies' : request.COOKIES,
                'params' : request.REQUEST,
                'code' : response.status_code,
        }
        entry = HttpLogEntry(data=to_log)
        entry.save()

        return response


