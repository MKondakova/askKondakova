'''
wsgi script which returns given parameters
'''
import multiprocessing

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def handler_app(environ, start_response):
    response_body = b'Works fine'
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
    ]
    start_response(status, response_headers)
    resp = []
    for f in environ:
        text = str(f) + ': ' + str(environ[f]) + "\n"
        resp.append(bytes(text,'UTF-8'))

    return resp
