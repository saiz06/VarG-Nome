import asyncio
import json
import logging
from functools import wraps

from quart import Quart, request, send_from_directory
from quart_cors import cors

from similarity_neo4j import SimilarityNeo4j

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Quart(__name__)
cors(app)

config = json.load(open('config.json', 'r'))


def exception_handler(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except NotImplementedError as e:
            logger.exception(e)
            return {'error': str(e)}, 501
        except Exception as e:
            logger.exception(e)
            return {'error': str(e)}, 500

    return decorated


@app.before_serving
async def startup():
    # Verify that the database is connected and authenticated.
    SimilarityNeo4j.init_driver()
    driver = SimilarityNeo4j()
    await driver.verify()


@app.after_serving
async def graceful_shutdown():
    # Close the driver connection when the app is shut down.
    driver = SimilarityNeo4j()
    await driver.close()


@app.route('/', methods=['GET'])
async def index():
    return 'OK'


@app.route('/openapi.json', methods=['GET'])
async def openapi_doc():
    return await send_from_directory('docs', 'openapi.json')
    
@app.route('/referenceNode', methods=['POST'])
@exception_handler
async def get_reference_node():
    data = await request.get_json()#
    start = data.get('start', 1)
    end = data.get('end', 1)
    driver = SimilarityNeo4j()
    referenceNodes = await driver.ref_nodes_query(start, end)
    return referenceNodes
    
@app.route('/variantNode', methods=['POST'])
@exception_handler
async def get_variant_node():
    data = await request.get_json()#
    vartype = data.get('vartype', '')
    driver = SimilarityNeo4j()
    variantNodes = await driver.variant_nodes_query(vartype)
    return variantNodes


# @app.route('/similarity/hpo', methods=['POST'])
# @exception_handler
# async def get_similar_hpo():
#     """
#     Run similarity search on HPO terms.

#     This endpoint accepts a list of HPO terms, and a similarity threshold.
#     :return: A JSON object containing the input terms, and their similar terms.
#     """

#     data = await request.get_json()

#     hpo_terms = data.get('hpoTerms', [])
#     threshold = data.get('threshold', 1)

#     # By default, the term is not expanded.
#     expand = request.args.get('expand', default=False, type=bool)
#     result_threshold = request.args.get('resultThreshold', default=0, type=int)
#     ic = request.args.get('ic', default=False, type=bool)

#     driver = SimilarityNeo4j()

#     # Run the similarity query.
#     similar_terms = await driver.hpo_similarity_query(hpo_terms, threshold)

#     if expand:
#         # Expand the similar terms.
#         for term_set in similar_terms:
#             full_term_set = await driver.hpo_expand_multiple(term_set['similarIDs'], depth=0)
#             term_set['similarIDs'] = full_term_set[0]['children']

#     if result_threshold > 0:
#         # Trim the result list.
#         for term_set in similar_terms:
#             term_set['similarIDs'] = term_set['similarIDs'][:result_threshold]

#     if ic:
#         # TODO: Calculate the information content of the terms.
#         pass

#     return similar_terms


# @app.route('/similarity/ordo', methods=['POST'])
# @exception_handler
# async def get_similar_ordo():
#     """
#     Run similarity search on Ordo terms.

#     This endpoint accepts a list of Ordo terms, and a match scale.
#     :return: A JSON object containing the input terms, and their similar terms, as HPO terms.
#     """

#     data = await request.get_json()

#     ordo_terms = data.get('ordoTerms', [])
#     match_scale = data.get('matchScale', 1)
#     threshold = data.get('threshold', 1)
#     frequency = data.get('frequency', None)

#     # By default, the term is not expanded.
#     expand = request.args.get('expand', default=False, type=bool)
#     result_threshold = request.args.get('resultThreshold', default=0, type=int)
#     ic = request.args.get('ic', default=False, type=bool)

#     driver = SimilarityNeo4j()

#     if expand:
#         # Expand the Ordo terms.
#         expanded_ordo = await driver.ordo_expand_multiple(ordo_terms, depth=0)
#         ordo_terms = expanded_ordo[0]['children']

#     hpo_terms = await driver.map(TermType.ORDO, TermType.HPO, ordo_terms, match_scale=match_scale, frequency=frequency)

#     # Run the similarity query against all the mapped HPO terms.
#     tasks = []
#     for hpo_set in hpo_terms:
#         tasks.append(driver.hpo_similarity_query(hpo_set['hpoIDs']['Obligated'], threshold))
#         tasks.append(driver.hpo_similarity_query(hpo_set['hpoIDs']['Optional'], threshold))
#         tasks.append(driver.hpo_similarity_query(hpo_set['hpoIDs']['Excluded'], threshold))

#     results = await asyncio.gather(*tasks)

#     # Add the result to the corresponding Ordo term.
#     for i in range(len(hpo_terms)):
#         hpo_terms[i]['similarHPOs'] = {
#             'Obligated': results[i * 3],
#             'Optional': results[i * 3 + 1],
#             'Excluded': results[i * 3 + 2],
#         }

#     if expand:
#         for hpo_set in hpo_terms:
#             for term_set in hpo_set['similarHPOs']['Obligated']:
#                 full_term_set = await driver.hpo_expand_multiple(term_set['similarIDs'], depth=0)
#                 term_set['similarIDs'] = full_term_set[0]['children']
#             for term_set in hpo_set['similarHPOs']['Optional']:
#                 full_term_set = await driver.hpo_expand_multiple(term_set['similarIDs'], depth=0)
#                 term_set['similarIDs'] = full_term_set[0]['children']
#             for term_set in hpo_set['similarHPOs']['Excluded']:
#                 full_term_set = await driver.hpo_expand_multiple(term_set['similarIDs'], depth=0)
#                 term_set['similarIDs'] = full_term_set[0]['children']

#     if result_threshold > 0:
#         for hpo_set in hpo_terms:
#             for term_set in hpo_set['similarHPOs']['Obligated']:
#                 term_set['similarIDs'] = term_set['similarIDs'][:result_threshold]
#             for term_set in hpo_set['similarHPOs']['Optional']:
#                 term_set['similarIDs'] = term_set['similarIDs'][:result_threshold]
#             for term_set in hpo_set['similarHPOs']['Excluded']:
#                 term_set['similarIDs'] = term_set['similarIDs'][:result_threshold]

#     if ic:
#         # TODO: Calculate the information content of the terms.
#         pass

#     return hpo_terms


# @app.route('/expand/hpo', methods=['POST'])
# @exception_handler
# async def expand_hpo():
#     """
#     Expand HPO terms.

#     This endpoint accepts a list of HPO terms.
#     :return: A two-dimensional array of HPO terms, traversing the HPO ontology.
#     """

#     data = await request._json()

#     hpo_terms = data.get('hpoTerms', [])

#     depth = request.args.get('depth', default=3, type=int)
#     result_threshold = request.args.get('resultThreshold', default=0, type=int)
#     ic = request.args.get('ic', default=False, type=bool)

#     driver = SimilarityNeo4j()

#     result = await driver.hpo_expand_multiple(hpo_terms, depth)
#     children = result[0]['children']

#     if result_threshold > 0:
#         children = children[:result_threshold]

#     if ic:
#         # TODO: Calculate the information content of the terms.
#         pass

#     return children


# @app.route('/expand/ordo', methods=['POST'])
# @exception_handler
# async def expand_ordo():
#     """
#     Expand Ordo terms.

#     This endpoint accepts a list of Ordo terms.
#     :return: A two-dimensional array of Ordo terms, traversing the Ordo ontology.
#     """

#     data = await request.get_json()

#     ordo_terms = data.get('ordoTerms', [])

#     depth = request.args.get('depth', default=3, type=int)
#     result_threshold = request.args.get('resultThreshold', default=0, type=int)
#     ic = request.args.get('ic', default=False, type=bool)

#     driver = SimilarityNeo4j()

#     result = await driver.ordo_expand_multiple(ordo_terms, depth)
#     children = result[0]['children']

#     if result_threshold > 0:
#         children = children[:result_threshold]

#     if ic:
#         # TODO: Calculate the information content of the terms.
#         pass

#     return children


# @app.route('/map/<term_type>', methods=['POST'])
# @exception_handler
# async def map_term(term_type: str):
#     data = await request.get_json()

#     original_terms = data.get('terms', [])
#     target_type = data.get('targetType', None)

#     query_params = request.args.to_dict(flat=False)
#     parameters = {}
#     for key, value in query_params.items():
#         if value is not None:
#             # Check the length of the list
#             if len(value) == 1:
#                 parameters[key] = value[0]
#             else:
#                 parameters[key] = value

#     original_type = TermType.from_str(term_type)
#     target_type = TermType.from_str(target_type)

#     driver = SimilarityNeo4j()
#     result = await driver.map(
#         original_type=original_type,
#         target_type=target_type,
#         terms=original_terms,
#         **parameters
#     )

#     return result


if __name__ == '__main__':
    app.run(host='localhost', port=5001)
