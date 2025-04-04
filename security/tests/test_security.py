from flask import Flask
import security.security as sec


def test_read():
    recs = sec.read()
    assert isinstance(recs, dict)
    for feature in recs:
        assert isinstance(feature, str)
        assert len(feature) > 0


def test_require_permission_allows_user():
    app = Flask(__name__)
    sec.security_recs.clear()
    sec.security_recs.update({
        sec.PEOPLE: {
            sec.CREATE: {
                sec.USER_LIST: ['meghan@example.com'],
                sec.CHECKS: {}
            }
        }
    })

    @sec.require_permission(sec.PEOPLE, sec.CREATE)
    def dummy():
        return "ok"

    with app.test_request_context(headers={"X-User-Email": "meghan@example.com"}):
        assert dummy() == "ok"