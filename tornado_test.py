import tornado.ioloop
import tornado.web

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        user = self.get_argument("username")
        passwd = self.get_argument("password")
        self.write("Your username is %s and password is %s" % (user, passwd))

def make_app():
    return tornado.web.Application([
        (r"/", HelloHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()