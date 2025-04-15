"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields  # Namespace, fields
from flask_cors import CORS

import data.people as ppl
import data.text as txt
import data.manuscripts as manu
import data.roles as rls
import data.users as usr


import werkzeug.exceptions as wz

# import pytest

app = Flask(__name__)
CORS(app)
api = Api(app)

DATE = 'October 16 2024'
DATE_RESP = 'Date'
EDITOR = 'editor@nyu.edu'
EDITOR_RESP = 'Editor'
ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
PEOPLE_EP = '/people'
MANU_EP = '/manuscripts'
MESSAGE = 'Message'
DEL_COUNT = 'Deleted Count'
PUBLISHER = 'Springer'
PUBLISHER_RESP = 'Publisher'
RETURN = 'return'
# Endpoint that returns journal title
JOURNAL_EP = '/journalTitle'
JOURNAL_RESP = 'Journal Title'
TITLE = "SWEtastic-journal"
TXT_EP = '/text'
ROLE_EP = '/role'
ROLES_EP = '/roles'


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(JOURNAL_EP)
class JournalTitle(Resource):
    """
    This class handles creating, reading, updating
    and deleting the journal title
    """
    def get(self):
        """
        Displays the journal's title
        """
        return {JOURNAL_RESP: TITLE}


@api.route(ROLES_EP)
class Roles(Resource):
    """
    This class handles reading person roles
    """
    def get(self):
        """
        Retrieve the journal person's roles.
        """
        return rls.read()


@api.route(PEOPLE_EP)
class People(Resource):
    """
    This class handles creating, reading, updating
    and deleting journal people.
    """
    def get(self):
        """
        Retrieve the journal people.
        """
        return ppl.read()


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLES: fields.String,
})


@api.route(f'{PEOPLE_EP}/<email>')
class Person(Resource):
    """
    This class handles creating, reading, updating
    and deleting journal people.
    """
    def get(self, email):
        """
        Retrieve a journal person.
        """
        person = ppl.read_one(email)
        if person:
            return person
        else:
            raise wz.NotFound(f'No such record: {email}')

    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such person.')
    def delete(self, email):
        # The number of people deleted
        ret = ppl.delete(email)
        if ret != 0:
            return {
                MESSAGE: f'Successfully deleted {email}',
                DEL_COUNT: ret
            }
        else:
            raise wz.NotFound(f'No such person: {email}')


@api.route(f'{PEOPLE_EP}/create')
class PeopleCreate(Resource):
    """
    Add a person to the journal database
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.expect(PEOPLE_CREATE_FLDS)
    def put(self):
        """
        Add a person.
        """
        try:
            name = request.json.get(ppl.NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            email = request.json.get(ppl.EMAIL)
            roles = request.json.get(ppl.ROLES)

            # validate required fields
            if not name or not affiliation or not email:
                raise ValueError(
                    "Missing required fields"
                    + "name, email or affiliation"
                )

            # check for duplicate person by email
            if ppl.exists(email):
                raise ValueError(
                    f"A person with email '{email}' already exists."
                )

            # create new person
            ret = ppl.create(name, affiliation, email, roles)

        except ValueError as val_err:
            return {'message': str(val_err)}, HTTPStatus.NOT_ACCEPTABLE
        except Exception as err:
            raise wz.NotAcceptable(
                f"This person could not be added: {err=}"
            )
        return {
            MESSAGE: 'This person has been successfully added!',
            RETURN: ret,
        }


@api.route(f'{PEOPLE_EP}/updateAffiliation/<email>/<new_affiliation>')
class PeopleAffiliationUpdate(Resource):
    """
    Update a person's affiliation given their email and the _new_affiliation
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self, email, new_affiliation):
        """
        Update an affiliation
        """
        try:
            ret = ppl.update_affiliation(email, new_affiliation)
        except Exception as err:
            raise wz.NotAcceptable(f'Error updating affiliation {err}')
        if ret:
            msg = f'Affiliation has been updated to {new_affiliation}!'
        else:
            msg = "Failed to update affiliation"
        return {
            'EMAIL': ret,
            MESSAGE: msg

        }


@api.route(f'{PEOPLE_EP}/updateName/<email>/<new_name>')
class PeopleNameUpdate(Resource):
    """
    Update a person's name given their email and the new name
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self, email, new_name):
        """
        Update a person's nane
        """
        try:
            ret = ppl.update_name(email, new_name)
        except Exception as err:
            raise wz.NotAcceptable(f'Error updating name {err}')
        if ret:
            msg = f'Name has been updated to {new_name}!'
        else:
            msg = "Failed to update name"
        return {
            'EMAIL': ret,
            MESSAGE: msg

        }


@api.route(f'{PEOPLE_EP}/<string:email>/addRole/<string:role>')
class AddRole(Resource):
    def put(self, email, role):
        try:
            person = ppl.read_one(email)
        except ValueError:
            mssg = f"{person} not found, please create the person first"
            return {"message": mssg}, 404
        try:
            ppl.add_role(email, role)
        except KeyError as err:
            raise wz.NotFound(str(err))
        except ValueError as err:
            return {"message": str(err)}, 400
        return {"message": f"Role '{role}' added to {email}"}, 200


@api.route(f'{PEOPLE_EP}/<string:email>/removeRole/<string:role>')
class RemoveRole(Resource):
    def delete(self, email, role):
        try:
            person = ppl.read_one(email)
        except ValueError:
            mssg = f"{person} not found"
            return {"message": mssg}, 404
        try:
            ppl.remove_role(email, role)
        except KeyError:
            return {"message": f"{role} doesn't exist"}, 404
        return {"message": f"Role '{role}' removed from {email}"}, 200


@api.route(f'{TXT_EP}/pages')  # Get all pages in a journal
class JournalPages(Resource):
    def get(self):
        contents = txt.read()
        return contents


# Given a journal title and new text value, update that journal's text
@api.route(f'{TXT_EP}/update/<_key>/<_val>')
class UpdateJournalText(Resource):
    # Note: _val should be one continguous string
    def put(self, _key, _val):
        journal = txt.update_text(_key, _val)
        success_msg = f"Update page {_key} with text: {_val}"
        ret_val = {"message": f"Journal '{_key}' updated to {_val}"}, 200
        if journal == success_msg:  # update was successful
            return ret_val
        return {"message": f"Failed to update {_key}"}, 400


# Define model for creating a new journal page
PAGE_CREATE_FIELDS = api.model('CreateNewPageEntry', {
    txt.KEY: fields.String(required=True,
                           description="Unique key for the page"),
    txt.TITLE: fields.String(required=True, description="Title of the page"),
    txt.TEXT: fields.String(required=True, description="Content of the page"),
})


@api.route(f'{TXT_EP}/create')
class JournalPageCreate(Resource):
    """
    Create a new journal page.
    """
    @api.response(HTTPStatus.CREATED, 'Page created successfully')
    @api.response(HTTPStatus.BAD_REQUEST, 'Invalid data provided')
    @api.expect(PAGE_CREATE_FIELDS)
    def post(self):
        """
        Add a new journal page with a unique key, title, and text.
        """
        try:
            key = request.json.get(txt.KEY)
            title = request.json.get(txt.TITLE)
            text = request.json.get(txt.TEXT)
            # Call the create function to add the page
            result = txt.create(key, title, text)
            return {"message": "Page created successfully",
                    "result": result}, HTTPStatus.CREATED
        except Exception as e:
            return {"message":
                    f"Failed to create page: {e}"}, HTTPStatus.BAD_REQUEST


@api.route(f'{TXT_EP}/delete/<string:key>')
class DeleteJournalPage(Resource):
    """
    This class handles deleting a journal page by its key.
    """
    @api.response(HTTPStatus.OK, 'Page deleted successfully')
    @api.response(HTTPStatus.NOT_FOUND, 'No page found with this key')
    def delete(self, key):
        """
        Delete a journal page by its key.
        """
        result = txt.delete(key)
        if "Deleted" in result:
            return {"message": result}, HTTPStatus.OK
        else:
            raise wz.NotFound(result)


MASTHEAD = 'Masthead'


@api.route(f'{PEOPLE_EP}/masthead')
class Masthead(Resource):
    """
    Get a journal's masthead.
    """
    def get(self):
        return {MASTHEAD: ppl.get_masthead()}


# Define model for creating a new Manuscript entry
MANU_CREATE_FLDS = api.model('CreateNewManuscriptEntry', {
    manu.TITLE: fields.String(
        required=True,
        description="Unique title for the manuscript"
    ),
    manu.AUTHOR: fields.String(
        required=True,
        description="Author of the manuscript"
    ),
})


@api.route(MANU_EP)
class Manuscripts(Resource):
    """
    This class handles retrieving all manuscripts.
    """
    def get(self):
        """
        Retrieve all manuscripts.
        """
        manuscripts = manu.read()
        if manuscripts is None:
            raise wz.NotFound("Could not retrieve manuscripts from database")
        else:
            return manuscripts, 200


@api.route(f'{MANU_EP}/<string:title>')
class ManuscriptReadOne(Resource):
    """
    This class handles retrieving a specific manuscript by title.
    """
    def get(self, title):
        """
        Retrieve a manuscript by its title.
        """
        manuscript = manu.read_one(title)
        if manuscript:
            return manuscript
        else:
            raise wz.NotFound(f'No manuscript found with title: {title}')


@api.route(f'{MANU_EP}/create')
class ManuscriptCreate(Resource):
    """
    Create a Manuscript Object
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.expect(MANU_CREATE_FLDS)
    def put(self):
        try:
            title = request.json.get(manu.TITLE)
            author = request.json.get(manu.AUTHOR)
            referees = request.json.get(manu.REFEREES)
            # validate required fields
            if not title or not author:
                raise ValueError(
                    "Missing required fields"
                    + "title or author"
                )

            # check for duplicate person by title
            if manu.exists(title):
                raise ValueError(
                    f"A manuscript with title '{title}' already exists."
                )
            # create new title
            ret = manu.create(title, author, referees)

        except ValueError as val_err:
            return {'message': str(val_err)}, HTTPStatus.NOT_ACCEPTABLE
        except Exception as err:
            return {"message":
                    f"This manuscript could not be created: err={str(err)}"
                    }, 500
        return {
            MESSAGE: 'This manuscript has been successfully created!',
            RETURN: ret,
        }, 200


MANU_ACTION_FLDS = api.model('ManuscriptAction', {
    manu.MANU_ID: fields.String,
    manu.CURR_STATE: fields.String,
    manu.ACTION: fields.String,
    manu.REFEREE: fields.String,
})


@api.route(f'{MANU_EP}/<string:title>/delete')
class ManuscriptDelete(Resource):
    def delete(self, title):
        try:
            # retrieve manuscript by title
            manu_obj = manu.read_one(title)
            if not manu_obj:
                return {"message": f"Manuscript with title '{title}'" +
                        "not found"}, 404

            # delete the manuscript
            manu.delete(title)  # delete by title
            return {"message": f"Manuscript '{title}'" +
                    "successfully deleted"}, 200

        except Exception as err:
            return {"message": f"Error: {str(err)}"}, 500


@api.route(f'{MANU_EP}/<string:title>/update/<string:new_state>')
class ManuscriptUpdateState(Resource):
    """
    Parameters:
    title -> unique title identifier to a manuscript object
    new_state -> new state to set the curr_state of a manuscript to
    """
    def put(self, title, new_state):
        try:
            # retrieve manuscript by title
            manu_obj = manu.read_one(title)
            if not manu_obj:
                return {"message": f"Manuscript with title '{title}'" +
                        "not found"}, 404
            # verify valid state
            if not manu.is_valid_state(new_state):
                return {"message": f"Manuscript: '{title}'" +
                        "attempted to change to invalid state"}, 404

            # update the manuscript
            manu.update_manuscript_state(title, new_state)
            return {"message": f"Manuscript '{title}'" +
                    "state successfully updated"}, 200

        except Exception as err:
            return {"message": f"Error: {str(err)}"}, 500


@api.route(f'{MANU_EP}/receive_action')
class ReceiveAction(Resource):
    """
    Receive an action for a manuscript.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_ACTION_FLDS)
    def put(self):
        """
        Receive an action for a manuscript.
        """
        try:
            print(request. json)
            manu_id = request.json.get(manu.MANU_ID)
            curr_state = request.json.get(manu.CURR_STATE)
            action = request. json.get(manu.ACTION)
            kwargs = {}
            kwargs[manu.REFEREE] = request.json.get(manu.REFEREE)
            ret = manu.handle_action(manu_id, curr_state, action, **kwargs)
        except Exception as err:
            raise wz.NotAcceptable(f'Bad action: ' f'{err=}')
        return {
            MESSAGE: 'Action received!',
            RETURN: ret,
        }


@api.route(f'{MANU_EP}/search')
class SearchManuscripts(Resource):
    """
    Search for manuscripts.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Query parameter is required')
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')
    def get(self):
        """
        Search for manuscripts based on a query.
        """
        query = request.args.get("query", "").strip()

        if not query:
            return {'error': 'Query parameter is required'},
        HTTPStatus.BAD_REQUEST

        try:
            print(f"Received search query: {query}")  # Debugging log
            results = manu.search_manuscripts(query)
            return results, HTTPStatus.OK
        except Exception as err:
            print(f"Search error: {err}")
            return {'error': f'Internal Server Error: {str(err)}'},
        HTTPStatus.INTERNAL_SERVER_ERROR


REGISTER_FIELDS = api.model('RegisterNewUser', {
    'name': fields.String(required=True, description='Full name of the user'),
    'email': fields.String(required=True,
                           description='User email (must be unique)'),
    'password': fields.String(required=True, description='Password for login'),
})


@api.route('/register')
class Register(Resource):
    @api.expect(REGISTER_FIELDS)
    def post(self):
        data = request.json
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not all([name, email, password]):
            return {"message": "Missing required fields."}, 400

        try:
            user = usr.create_user(email, name, password)
        except ValueError as ve:
            return {"message": str(ve)}, 400

        return {
            "user": {usr.EMAIL: user[usr.EMAIL],
                     usr.NAME: user[usr.NAME]}
        }, 201


LOGIN_FIELDS = api.model('UserLogin', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
})


@api.route('/login')
class Login(Resource):
    @api.expect(LOGIN_FIELDS)
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if usr.authenticate(email, password):
            user = usr.read_one(email)
            return {
                "message": f"Welcome back, {user[usr.NAME]}!",
                "level": user.get(usr.LEVEL, 0)
            }, 200
        else:
            return {"message": "Invalid credentials."}, 401


@api.route('/users')
class AllUsers(Resource):
    def get(self):
        users = usr.read_all()

        # Optional: exclude sensitive data like password
        sanitized_users = {
            email: {
                usr.NAME: user.get(usr.NAME),
                usr.LEVEL: user.get(usr.LEVEL)
            }
            for email, user in users.items()
        }

        return {"users": sanitized_users}, 200
