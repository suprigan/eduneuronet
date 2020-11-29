import socket
import sys

class AbstractHTTPServer:
  def __init__(self, host, port, server_name):
    self._host = host
    self._port = port
    self._server_name = server_name

  def serve_forever(self):
    serv_sock = socket.socket(
      socket.AF_INET,
      socket.SOCK_STREAM,
      proto=0)

    try:
      serv_sock.bind((self._host, self._port))
      serv_sock.listen()

      while True:
        conn, _ = serv_sock.accept()
        try:
          self.serve_client(conn)
        except Exception as e:
          print('Client serving failed', e)
    finally:
      serv_sock.close()

  def serve_client(self, conn):
    try:
      req = self.parse_request(conn)
      resp = self.handle_request(req)
      self.send_response(conn, resp)
    except ConnectionResetError:
      conn = None
    except Exception as e:
      self.send_error(conn, e)

    if conn:
      conn.close()

  def parse_request(self, conn):
    pass  # TODO: implement me

  def handle_request(self, req):
    pass  # TODO: implement me

  def send_response(self, conn, resp):
    pass  # TODO: implement me

  def send_error(self, conn, err):
    pass  # TODO: implement me


if __name__ == '__main__':
  host = sys.argv[1]
  port = int(sys.argv[2])
  name = sys.argv[3]

  serv = AbstractHTTPServer(host, port, name)
  try:
    serv.serve_forever()
  except KeyboardInterrupt:
    pass