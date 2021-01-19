from app.api import bp
from flask import jsonify, url_for
from app.models import Peptoid
from app import limiter


@bp.route('/peptoids/<code>', methods=['GET'])
@limiter.limit("10 per minute")
def get_peptoid(code):
    return jsonify(Peptoid.query.get_or_404(code).to_dict())


@bp.route('/peptoids', methods=['GET'])
@limiter.limit("10 per minute")
def get_peptoids():
    data = {}
    for p in Peptoid.query.all():
        data[p.code] = url_for('api.get_peptoid', code=p.code)
    return jsonify(data)


@bp.route('/peptoids/<code>/residues', methods=['GET'])
@limiter.limit("10 per minute")
def get_residues(code):
    dict = {}
    i = 1
    for r in Peptoid.query.get_or_404(code).peptoid_residue:
        dict[f'Residue {i}'] = r.to_dict()
        i += 1
    return jsonify(dict)


@bp.route('/peptoids/<code>/authors', methods=['GET'])
@limiter.limit("10 per minute")
def get_authors(code):
    dict = {}
    i = 1
    for a in Peptoid.query.get_or_404(code).peptoid_author:
        dict[f'Author {i}'] = a.to_dict()
        i += 1
    return jsonify(dict)
