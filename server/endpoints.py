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
# import data.roles as rls

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
            ret = ppl.create(name, affiliation, email, roles)
        except Exception as err:
            raise wz.NotAcceptable(f'This person could not be added: '
                                   f'{err=}')
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
