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
PUBLISHER = 'Springer'
PUBLISHER_RESP = 'Publisher'
RETURN = 'return'
# Endpoint that returns journal title
JOURNAL_EP = '/journalTitle'
JOURNAL_RESP = 'Journal Title'
TITLE = "SWEtastic-journal"


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

    def put(self):
        """
        Updates the journal's title
        """
        global TITLE
        title = request.json.get('title')
        if title:
            TITLE = title
            return {"message": "Title updated successfully"}, 200
        return {"message": "Title required"}, 400


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
})


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
            ret = ppl.create(name, affiliation, email)
        except Exception as err:
            raise wz.NotAcceptable(f'This person could not be added: '
                                   f'{err=}')
        return {
            MESSAGE: 'This person has been successfully added!',
            RETURN: ret,
        }


@api.route(f'{PEOPLE_EP}/updateAffiliation/<_id>/<_new_affiliation>')
class PeopleAffiliationUpdate(Resource):
    """
    Update a person's affiliation given their _id and the _new_affiliation
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self, _id, _new_affiliation):
        """
        Update an affiliation
        """
        try:
            ret = ppl.update(_id, _new_affiliation)
        except Exception as err:
            raise wz.NotAcceptable(f'Error updating affiliation {err}')
        if ret:
            msg = 'This affiliation has been successfully updated!'
            ret = 200
        else:
            msg = "Failed to update affiliation"
            ret = 404
        return {
            MESSAGE: msg,
            RETURN: ret,
        }


@api.route('/people/<string:email>/addRole/<string:role>')
class AddRole(Resource):
    def put(self, email, role):
        person = ppl.get_person(email)
        if not person:
            return {"message": "Person not found"}, 404
        ppl.add_role(email, role)
        return {"message": f"Role '{role}' added to {email}"}, 200


@api.route('/people/<string:email>/removeRole/<string:role>')
class RemoveRole(Resource):
    def put(self, email, role):
        person = ppl.get_person(email)
        if not person:
            return {"message": "Person not found"}, 404
        ppl.remove_role(email, role)
        return {"message": f"Role '{role}' removed from {email}"}, 200



@api.route(f'{JOURNAL_EP}/pages') # Get all pages in a journal
class JournalPages(Resource):
    def get(self):
        contents = txt.read()
        return contents
