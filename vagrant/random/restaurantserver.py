# https://docs.python.org/2/library/basehttpserver.html
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi #common gateway interface
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from contextlib import contextmanager
import cgitb
cgitb.enable()


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)


@contextmanager
def get_session():
    """Session helper function using context lib. Creates a session from a database connection object, and performs commits and queries using that cursor."""
    session = DBSession()
    try:
        yield session
    except:
        session.rollback()
        raise
    else:
        session.commit()
    finally:
        session.close()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant!</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='newRestaurantName' type='text' placeholder = 'New Restaurant Name'>"
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                with get_session() as session:
                    restaurants = session.query(Restaurant).all()
                    for restaurant in restaurants:
                        output += "<h2>%s</h2>" % (restaurant.name)
                        output += "<a href='/restaurants/%s/edit'>Edit</a>" % (restaurant.id)
                        output += "</br>"
                        output += "<a href='/restaurants/%s/delete'>Delete</a>" % (restaurant.id)
                        output += "</br></br>"
                output += "</br><h2><a href='/restaurants/new'>Make a New Restaurant Here</a></h2>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant_id = int(self.path.split("/")[2])
                with get_session() as session:
                    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>%s</h1>" % (restaurant.name)
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><input name="editRestaurantName" type="text" placeholder = "New Restaurant Name">''' % (restaurant_id)
                    output += '''<input type="submit" value="Rename"> </form>'''
                    output += "</body></html>"
                self.wfile.write(output)

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant_id = int(self.path.split("/")[2])
                with get_session() as session:
                    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete <b>%s</b>?</h1>" % (restaurant.name)
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % (restaurant_id)
                    output += "<input type='submit' value='Delete'>"
                    output += "</form></body></html>"
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant_name = fields.get('newRestaurantName')
                    new_restaurant = Restaurant(name=new_restaurant_name[0])

                    with get_session() as session:
                        session.add(new_restaurant)
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
            if self.path.endswith("/edit"):
                restaurant_id = int(self.path.split("/")[2])
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant_name = fields.get('editRestaurantName')
                    if new_restaurant_name[0]:
                        with get_session() as session:
                            restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                            restaurant.name = new_restaurant_name[0]
                            session.add(restaurant)
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
            if self.path.endswith("/delete"):
                restaurant_id = int(self.path.split("/")[2])
                if restaurant_id:
                    with get_session() as session:
                        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                        session.delete(restaurant)
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
        except:
            pass

def main():
    try:
        port = 9080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever() # keeps server constantly running until ctrl+c or exit the application
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()
