# https://docs.python.org/2/library/basehttpserver.html
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi #common gateway interface
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from contextlib import contextmanager


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
                        output += "<a href='/restaurants/delete'>Delete</a>"
                        output += "</br></br>"
                output += "</br><a href='/restaurants/new'>Make a New Restaurant Here</a>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/'><input name="newRestaurantName" type="text" placeholder = "New Restaurant Name">'''
                output += '''<input type="submit" value="Create"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                url_path = self.path
                restaurant_id = url_path[(url_path.find('/restaurants/') + 13): url_path.find('/edit')]
                restaurant_id = int(restaurant_id)
                with get_session() as session:
                    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                    print restaurant.name
                    output = ""
                    output += "<html><body>"
                    output += "<h1>%s</h1>" % (restaurant.name)
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><input name="editRestaurantName" type="text" placeholder = "New Restaurant Name">''' % (restaurant_id)
                    output += '''<input type="submit" value="Create"> </form>'''
                    output += "</body></html>"
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)
    def do_POST(self):
        try:
            if self.path.endswith("restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                new_restaurant_name = fields.get('newRestaurantName')
                if new_restaurant_name:
                    new_restaurant = Restaurant(name = new_restaurant_name)
                    with get_session() as session:
                        session.add(new_restaurant)
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
            if self.path.endswith("/edit"):
                url_path = self.path
                restaurant_id = url_path[(url_path.find('/restaurants/') + 13): url_path.find('/edit')]
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant_name = fields.get('editRestaurantName')
                if new_restaurant_name:
                    with get_session() as session:
                        restaurant = session.query(Restaurant).filter_by(id = restaurant_id)
                        restaurant.name= new_restaurant_name
                        session.add(restaurant)
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
