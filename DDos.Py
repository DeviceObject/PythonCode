import sys
import socket

def format_request_header(url_addr, uri, cookie, referer, fromlen, tolen):
    request_header = "GET " + uri + " HTTP/1.1" + "\r\n" + "Host:" + url_addr + "\r\n"
    if (referer != None):
        request_header = request_header + "Referer:" + referer + "\r\n"
    request_header = request_header + "Accept:*/*" + "\r\n"
    request_header = request_header + "User-Agent:Mozilla/4.0 (compatible; MSIE 5.00; Windows 98)" + "\r\n"
    request_header = request_header + "Connection:Keep-Alive" + "\r\n"
    if (cookie != None):
        request_header = request_header + "Set Cookie:0" + cookie + "\r\n"
    if (fromlen > 0):
        request_header = request_header + "Range: bytes=" + str(fromlen) + "-"
        if (tolen > fromlen):
            request_header = request_header + str(tolen) + "\r\n"
    request_header = request_header + "\r\n"
    return request_header

def attach_http(url_addr, port, uri):
    try:
        ip_addr = socket.gethostbyname(url_addr)
        print(ip_addr)
    except:
        print("get ip address failed")

def entry():
#    if len(sys.argv) < 3:
#        return
    format_request_header("www.baidu.com", "1.txt", None, None, 0, 0)
if __name__ == "__main__":
    entry()