import tornado.ioloop
import tornado.web

# Key Dictionary
html_dict = {
    'tl': (-1, -1),
    't': (-1, 0),
    'tr': (0, 1),
    'br': (1, 1),
    'b': (1, 0),
    'bl': (0, -1),
}

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

        xy_move = html_dict[dir]
        self.queue.put((id,xy_move))


def make_app(queue):
    return tornado.web.Application([
        (r"/", HTMLHandler, dict(queue=queue)),
    ])