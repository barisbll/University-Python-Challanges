import pytest

class HTTP_Container:

    def __init__(self, req_type, res_path, http_protocol):
        self.req_type = req_type
        self.res_path = res_path
        self.http_protocol = http_protocol


def reqstr2obj(request_string):
    if type(request_string) != str:
        raise TypeError


class BadRequestTypeError(Exception):
    pass


class BadHTTPVersion(Exception):
    pass


class ValueError(Exception):
    pass


def httpobj(request_string):

    parameters = request_string.split()

    if len(parameters) != 3 or parameters[0].isnumeric() or \
           parameters[1].isnumeric() or parameters[2].isnumeric():
        return None

    req_types = ['GET', 'POST', 'PUT', 'DELETE']
    http_versions = ['HTTP1.0', 'HTTP1.1', 'HTTP2.0.']

    try:
        if not (parameters[0] in req_types):
            raise BadRequestTypeError


        if not http_versions.__contains__(parameters[2]):
            raise BadHTTPVersion

        if not parameters[1][0] == '/':
            raise ValueError

        return HTTP_Container(parameters[0], parameters[1], parameters[2])

    except BadRequestTypeError:
        raise BadRequestTypeError('Request type does not exist error')

    except BadHTTPVersion:
        raise BadHTTPVersion('Http version does not exist')

    except ValueError:
        raise ValueError('Path must start with /')



#Test #1
def test_reqstr2obj():
    request_string = 'GET / HTTP1.1'
    with pytest.raises(TypeError):
        assert reqstr2obj(42)


#Test #2
def test_http():

    assert isinstance(httpobj('GET / HTTP1.1'), HTTP_Container)

#Test #3
def test_http3():
    if isinstance(httpobj('GET / HTTP1.1'), HTTP_Container):
        assert (httpobj('GET / HTTP1.1').http_protocol == 'HTTP1.1' and
                httpobj('GET / HTTP1.1').res_path == '/' and
                httpobj('GET / HTTP1.1').req_type == 'GET')
    else:
        None


#Test #4
def test_http4():
    assert isinstance(httpobj('GET / HTTP1.1'), HTTP_Container)


#Test #5
def test_http5():
    assert httpobj('some string to hold') == None


#Test #6
def test_http6():
    with pytest.raises(BadRequestTypeError):
        assert httpobj('DOWNLOAD /movie.mp4 HTTP1.1') == BadRequestTypeError


#Test #7
def test_http7():
    with pytest.raises(BadHTTPVersion):
        assert httpobj('GET /movie.mp4 HTTP7')


#Test #8
def test_http8():
    with pytest.raises(ValueError):
        assert httpobj('GET movie.mp4 HTTP1.1')


#Test #9
def test_http8():
    with pytest.raises(ValueError):
        assert httpobj('GET movie.mp4 HTTP1.1')

