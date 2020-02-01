import tornado.ioloop
import tornado.web

class HTMLHandler(tornado.web.RequestHandler):
    def initialize(self, queue):
        print("HelloHandler")
        self.queue = queue

    def get(self):
        self.write("Hello bees")

    def post(self):
        id = int(self.get_argument("id"))
        dir = self.get_argument("dir")

        print("id:", id)
        print("dir:", dir)

        self.queue.put((id,dir))


def make_app(queue):
    return tornado.web.Application([
        (r"/", HTMLHandler, dict(queue=queue)),
    ])
