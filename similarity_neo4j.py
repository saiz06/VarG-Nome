import asyncio
import json
import logging
import re
import os
from enum import Enum
from typing import Protocol, List, Any, Awaitable

from neo4j import AsyncGraphDatabase, AsyncDriver

config = json.load(open('config.json', 'r'))

concurrency = int(os.getenv('CONCURRENCY', config['connection']['concurrency']))
sem = asyncio.Semaphore(concurrency)


# def frequency_to_string(frequency: int) -> list[str]:
#     """
#     Convert a frequency threshold to a list of frequency terms.
#     :param frequency: The frequency value, in percentage.
#     :return: The list of frequency terms.
#     """

#     frequency = int(frequency)

#     frequency_terms = [
#         'Excluded (0%)',
#         'Very rare (<4-1%)',
#         'Occasional (29-5%)',
#         'Frequent (79-30%)',
#         'Very frequent (99-80%)',
#         'Obligate (100%)',
#     ]

#     if frequency < 0:
#         raise ValueError(f'Invalid frequency value: {frequency}')
#     elif frequency == 0:
#         return frequency_terms[0:]
#     elif frequency <= 4:
#         return frequency_terms[1:]
#     elif frequency <= 29:
#         return frequency_terms[2:]
#     elif frequency <= 79:
#         return frequency_terms[3:]
#     elif frequency <= 99:
#         return frequency_terms[4:]
#     elif frequency == 100:
#         return frequency_terms[5:]
#     else:
#         raise ValueError(f'Invalid frequency value: {frequency}')


# class MappingFunction(Protocol):
#     def __call__(self, terms: List[str], **kwargs: Any) -> Awaitable:
#         ...


# class TermType(Enum):
#     HPO = 'HPO'
#     ORDO = 'ORDO'
#     OMIM = 'OMIM'
#     PATHWAY = 'PATHWAY'
#     REACTION = 'REACTION'
#     GENE = 'GENE'
#     PROTEIN_EFFECT = 'PROTEIN_EFFECT'

#     @classmethod
#     def from_str(cls, label: str):
#         label = label.upper()

#         return cls[label]

#     def regex(self):
#         """
#         Get the regex pattern for the term type.
#         :return: The regex pattern.
#         """

#         # Note: The root term of each category may not follow this pattern.
#         #       But, they should not be queried anyway.

#         if self == TermType.HPO:
#             return r'^HP:\d{7}$'
#         elif self == TermType.ORDO:
#             return r'^ORPHA:\d{1,6}$'
#         elif self == TermType.OMIM:
#             return r'^OMIM:\d{6}$'
#         elif self == TermType.PATHWAY:
#             return r'^R-HSA-\d{1,7}$'
#         elif self == TermType.REACTION:
#             return r'^R-HSA-\d{1,7}$'
#         elif self == TermType.GENE:
#             return r'^[.]{1,10}$'
#         elif self == TermType.PROTEIN_EFFECT:
#             return r'^[.]{1,10}$'
#         else:
#             raise ValueError(f'Invalid TermType: {self}')

    # def prefix(self):
    #     """
    #     Get the prefix for the term type.
    #     :return:
    #     """

    #     if self == TermType.HPO:
    #         return "HP:"
    #     elif self == TermType.ORDO:
    #         return "ORPHA:"
    #     elif self == TermType.OMIM:
    #         return "OMIM:"
    #     else:
    #         return None


class SimilarityNeo4j:
    driver: AsyncDriver | None = None

    def __init__(self,
                 semaphore: asyncio.Semaphore = sem,
                 driver: AsyncDriver = None,
                 ) -> object:
        self.semaphore = semaphore
        if driver is not None:
            self.driver = driver
        elif self.driver is None:
            raise RuntimeError('Neo4j driver is not initialized.')

    @classmethod
    def init_driver(cls, username: str = None, password: str = None, uri: str = None):
        """
        Initialize the driver as a class variable.
        :param username: The username to authenticate with.
        :param password: The password to authenticate with.
        :param uri: The URI of the database.
        :return:
        """

        if uri is None:
            uri = os.getenv('NEO4J_URI', config['neo4j']['uri'])
            username = os.getenv('NEO4J_USERNAME', config['neo4j']['username'])
            password = os.getenv('NEO4J_PASSWORD', config['neo4j']['password'])

        if cls.driver is None:
            cls.driver = AsyncGraphDatabase.driver(
                uri=uri,
                auth=(username, password),
            )

    # @staticmethod
    # def check_term(term: str, term_type: TermType) -> bool:
    #     """
    #     Check if a given string is indeed a term with the given type.
    #     :param term: The term to check.
    #     :param term_type: The type of the term.
    #     :return: True if the term is valid, False otherwise.
    #     """

    #     return re.match(term_type.regex(), term) is not None

    # @staticmethod
    # def check_terms(terms: list[str], term_type: TermType, will_raise: bool = False, auto_prefix: bool = True) -> (
    #         bool, list[str]):
    #     """
    #     Check if a list of terms are indeed terms with the given type.
    #     :param terms: The list of terms to check.
    #     :param term_type: The type of the terms.
    #     :param will_raise: Whether to raise an exception if the terms are invalid.
    #     :param auto_prefix: Whether to automatically prefix the terms with appropriate prefixes.
    #     :return: True if the terms are valid, False otherwise.
    #     """

    #     if not terms:
    #         return False

    #     if auto_prefix:
    #         # Check one term only
    #         term = terms[0]
    #         if not SimilarityNeo4j.check_term(term, term_type):
    #             # Try prefixing
    #             prefix = term_type.prefix()
    #             if prefix is not None and SimilarityNeo4j.check_term(prefix + term, term_type):
    #                 # Prefixing works, do it for all terms
    #                 terms = [prefix + term for term in terms]
    #             elif will_raise:
    #                 raise ValueError(f'Invalid term as {term_type}: {term}')
    #             else:
    #                 return False

    #     for term in terms:
    #         if not SimilarityNeo4j.check_term(term, term_type):
    #             if will_raise:
    #                 raise ValueError(f'Invalid term as {term_type}: {term}')
    #             else:
    #                 return False
    #     return True, terms

    async def verify(self) -> bool:
        """
        Verify that the database is connected and authenticated.
        :return: True if the database is connected and authenticated, False otherwise.
        """

        try:
            await self.driver.verify_connectivity()
        except Exception as e:
            logging.exception(f'Could not connect to Neo4j database: {e}')
            return False

        logging.info('Connected to Neo4j database.')

        try:
            await self.driver.verify_authentication()
        except Exception as e:
            logging.exception(f'Could not authenticate to Neo4j database: {e}')
            return False

        logging.info('Authenticated to Neo4j database.')

        return True

    async def close(self):
        """
        Close the driver connection.
        :return:
        """

        await self.driver.close()
        self.driver = None

    async def execute_query(self, query, parameters=None):
        """
        Execute a Cypher query with auto-commit.
        :param query: The Cypher query to execute.
        :param parameters: The parameters to pass to the query.
        :return: The result of the query.
        """

        async with self.semaphore:
            async with self.driver.session() as session:
                result = await session.run(query, parameters)
                return await result.data()



    async def ref_nodes_query(self, start: int = 1, end: int = 1):

        query = """
        MATCH (r:Reference) WHERE r.pos>=$start AND r.pos<=$end RETURN r.refID;
        """

        parameters = {
        'start': start,
        'end': end,
        }

        return await self.execute_query(query, parameters)
    
    async def variant_nodes_query(self, vartype: str = ""):

        query = """
        MATCH (v:Variant) WHERE v.variation=$vartype RETURN v.varID;
        """

        parameters = {
        'vartype': vartype
        }

        return await self.execute_query(query, parameters)
    
    async def ordo_expand_single(self, ordo_term: str, depth: int = 3):
        """
        Expand a single Ordo term.

        This traverse the IS_A relationship up to the specified depth, and returns all the children.
        :param ordo_term: The Ordo term to expand.
        :param depth: The depth to expand to.
        :return:
        """

        if depth > 0:
            match_query = f"MATCH (n:ORPHAterm)<-[:IS_A*0..{depth}]-(m:ORPHAterm)"
        else:
            match_query = "MATCH (n:ORPHAterm)<-[:IS_A*0..]-(m:ORPHAterm)"

        query = f"""
        {match_query}
        WHERE n.orphaid = $orphaid
        RETURN COLLECT(DISTINCT(m.orphaid)) AS children;
        """

        parameters = {
            'orphaid': ordo_term,
        }

        return await self.execute_query(query, parameters)

    
    
    
    ##############################################################################


        
    # async def hpo_similarity_query(self, hpo_terms: list[str], threshold: float = 1.0):
    #     """
    #     Run a similarity query on a list of HPO terms.
    #     :param hpo_terms: The list of HPO terms to run the query on.
    #     :param threshold: THe minimum similarity score to return.
    #     :return:
    #     """

    #     _, hpo_terms = self.check_terms(hpo_terms, TermType.HPO, will_raise=True)

    #     query = """
    #     MATCH (n:HPOterm)-[r:SIMILARITY]-(j:HPOterm)
    #     WHERE r.rel > $rel AND n.hpoid IN $hpoids
    #     RETURN DISTINCT(n.hpoid) AS id, COLLECT(j.hpoid) AS similarIDs;
    #     """

    #     parameters = {
    #         'rel': threshold,
    #         'hpoids': hpo_terms,
    #     }

    #     return await self.execute_query(query, parameters)
        

    # async def hpo_expand_single(self, hpo_term: str, depth: int = 3):
    #     """
    #     Expand a single HPO term.

    #     This traverse the IS_A relationship up to the specified depth, and returns all the children.
    #     :param hpo_term: The HPO term to expand.
    #     :param depth: The depth to expand to.
    #     :return:
    #     """

    #     if depth > 0:
    #         match_query = f"MATCH (n:HPOterm)<-[:IS_A*0..{depth}]-(m:HPOterm)"
    #     else:
    #         match_query = "MATCH (n:HPOterm)<-[:IS_A*0..]-(m:HPOterm)"

    #     query = f"""
    #     {match_query}
    #     WHERE n.hpoid = $hpoid
    #     RETURN COLLECT(DISTINCT(m.hpoid)) AS children;
    #     """

    #     parameters = {
    #         'hpoid': hpo_term,
    #     }

    #     return await self.execute_query(query, parameters)

    # async def hpo_expand_multiple(self, hpo_terms: list[str], depth: int = 3):
    #     """
    #     Expand multiple HPO terms.
    #     :param hpo_terms: The list of HPO terms to expand.
    #     :param depth: The depth to expand to.
    #     :return:
    #     """

    #     _, hpo_terms = self.check_terms(hpo_terms, TermType.HPO, will_raise=True)

    #     if depth > 0:
    #         match_query = f"MATCH (n:HPOterm)<-[:IS_A*0..{depth}]-(m:HPOterm)"
    #     else:
    #         match_query = "MATCH (n:HPOterm)<-[:IS_A*0..]-(m:HPOterm)"

    #     query = f"""
    #     {match_query}
    #     WHERE n.hpoid IN $hpoids
    #     RETURN COLLECT(DISTINCT(m.hpoid)) AS children;
    #     """

    #     parameters = {
    #         'hpoids': hpo_terms,
    #     }

    #     return await self.execute_query(query, parameters)

    # async def ordo_expand_single(self, ordo_term: str, depth: int = 3):
    #     """
    #     Expand a single Ordo term.

    #     This traverse the IS_A relationship up to the specified depth, and returns all the children.
    #     :param ordo_term: The Ordo term to expand.
    #     :param depth: The depth to expand to.
    #     :return:
    #     """

    #     if depth > 0:
    #         match_query = f"MATCH (n:ORPHAterm)<-[:IS_A*0..{depth}]-(m:ORPHAterm)"
    #     else:
    #         match_query = "MATCH (n:ORPHAterm)<-[:IS_A*0..]-(m:ORPHAterm)"

    #     query = f"""
    #     {match_query}
    #     WHERE n.orphaid = $orphaid
    #     RETURN COLLECT(DISTINCT(m.orphaid)) AS children;
    #     """

    #     parameters = {
    #         'orphaid': ordo_term,
    #     }

    #     return await self.execute_query(query, parameters)

    # async def ordo_expand_multiple(self, ordo_terms: list[str], depth: int = 3):
    #     """
    #     Expand multiple Ordo terms.
    #     :param ordo_terms: The list of Ordo terms to expand.
    #     :param depth: The depth to expand to.
    #     :return:
    #     """

    #     _, ordo_terms = self.check_terms(ordo_terms, TermType.ORDO, will_raise=True)

    #     if depth > 0:
    #         match_query = f"MATCH (n:ORPHAterm)<-[:IS_A*0..{depth}]-(m:ORPHAterm)"
    #     else:
    #         match_query = "MATCH (n:ORPHAterm)<-[:IS_A*0..]-(m:ORPHAterm)"

    #     query = f"""
    #     {match_query}
    #     WHERE n.orphaid IN $orphaid
    #     RETURN COLLECT(DISTINCT(m.orphaid)) AS children;
    #     """

    #     parameters = {
    #         'orphaid': ordo_terms,
    #     }

    #     return await self.execute_query(query, parameters)

    # async def map_ordo_hpo(self, ordo_terms: list[str], **kwargs):
    #     """
    #     Map Ordo terms to HPO terms.
    #     :param ordo_terms: The list of Ordo terms to map.
    #     :return:
    #     """

    #     match_scale = kwargs.get('match_scale', 1)
    #     frequency: int | None = kwargs.get('frequency', None)

    #     frequency_clause = ''
    #     parameters = {}

    #     if frequency is not None:
    #         frequency_clause = ' AND r.frequency IN $frequency'
    #         parameters['frequency'] = frequency_to_string(frequency)

    #     query = """
    #     MATCH (n:ORPHAterm)<-[r:PHENOTYPE_OF]-(h:HPOterm)
    #     WHERE (n.orphaid IN $orphaids""" + frequency_clause + """)
    #     WITH n, h, r
    #     ORDER BY h.ICvsORPHA DESC
    #     WITH n.orphaid AS orphaID, COLLECT({hpoid: h.hpoid, IC: h.ICvsORPHA, frequency: r.frequency}) AS hpoData
    #     WITH orphaID, hpoData[0..toInteger(floor(size(hpoData) * $matchScale))] AS cutoffData
    #     RETURN orphaID, {
    #         Obligated: [hp IN cutoffData WHERE hp.frequency = 'Obligate (100%)' | hp.hpoid],
    #         Excluded: [hp IN cutoffData WHERE hp.frequency = 'Excluded (0%)' | hp.hpoid],
    #         Optional: [hp IN cutoffData WHERE hp.frequency IN
    #             ['Very rare (<4-1%)', 'Occasional (29-5%)', 'Frequent (79-30%)', 'Very frequent (99-80%)'] | hp.hpoid]
    #     } AS hpoIDs;
    #     """

    #     parameters['orphaids'] = ordo_terms
    #     parameters['matchScale'] = match_scale

    #     return await self.execute_query(query, parameters)

    # async def map_hpo_ordo(self, hpo_terms: list[str], **kwargs):
    #     """
    #     Map HPO terms to Ordo terms.
    #     :param hpo_terms: The list of HPO terms to map.
    #     :return:
    #     """

    #     frequency: int | None = kwargs.get('frequency', None)

    #     frequency_clause = ''
    #     parameters = {}

    #     if frequency is not None:
    #         frequency_clause = ' AND r.frequency IN $frequency'
    #         parameters['frequency'] = frequency_to_string(frequency)

    #     query = f"""
    #     MATCH (n:HPOterm)-[r:PHENOTYPE_OF]->(o:ORPHAterm)
    #     WHERE (n.hpoid IN $hpoids{frequency_clause})
    #     RETURN DISTINCT(n.hpoid) AS hpoID, COLLECT(DISTINCT(o.orphaid)) AS orphaIDs;
    #     """

    #     parameters['hpoids'] = hpo_terms

    #     return await self.execute_query(query, parameters)

    # async def map_hpo_omim(self, hpo_terms: list[str], **kwargs):
    #     """
    #     Map hpo terms to omim terms.
    #     :param hpo_terms: The list of hpo terms to map.
    #     :return:
    #     """

    #     """
    #     An asterisk (*) before an entry number indicates a gene.

    #     A number symbol (#) before an entry number indicates that it
    #     is a descriptive entry, usually of a phenotype, and does not
    #     represent a unique locus. The reason for the use of the number
    #     symbol is given in the first paragraph of the entry. Discussion
    #     of any gene(s) related to the phenotype resides in another
    #     entry(ies) as described in the first paragraph.

    #     A plus sign (+) before an entry number indicates that the entry
    #     contains the description of a gene of known sequence and a phenotype.

    #     A percent sign (%) before an entry number indicates that the entry
    #     describes a confirmed mendelian phenotype or phenotypic locus for
    #     which the underlying molecular basis is not known.

    #     No symbol before an entry number generally indicates a description
    #     of a phenotype for which the mendelian basis, although suspected,
    #     has not been clearly established or that the separateness of this
    #     phenotype from that in another entry is unclear.

    #     A caret (^) before an entry number means the entry no longer exists
    #     because it was removed from the database or moved to another entry
    #     as indicated.
    #     """

    #     # TODO: Filter by prefix

    #     parameters = {}
    #     query = """
    #     MATCH (n:HPOterm)-[r:PHENOTYPE_OF]->(o:OMIMterm)
    #     WHERE n.hpoid IN $hpoids
    #     RETURN DISTINCT(n.hpoid) AS hpoID, COLLECT(DISTINCT(o.omimid)) AS omimIDs;
    #     """

    #     parameters['hpoids'] = hpo_terms

    #     return await self.execute_query(query, parameters)

    # async def map_omim_hpo(self, omim_terms: list[str], **kwargs):
    #     """
    #     Map omim terms to hpo terms.
    #     :param omim_terms: The list of omim terms to map.
    #     :return:
    #     """

    #     parameters = {}
    #     query = """
    #     MATCH (o:OMIMterm)<-[r:PHENOTYPE_OF]-(n:HPOterm)
    #     WHERE o.omimid IN $omimterms
    #     RETURN DISTINCT(o.omimid) AS omimID, COLLECT(DISTINCT(n.hpoid)) AS hpoIDs;
    #     """

    #     parameters['omimterms'] = omim_terms

    #     return await self.execute_query(query, parameters)

    # async def map_ordo_omim(self, ordo_terms: list[str], **kwargs):
    #     """
    #     Map ordo terms to omim terms.
    #     :param ordo_terms: The list of ordo terms to map.
    #     :return: Also includes the rel type in return
    #     """

    #     parameters = {}

    #     relation_types = kwargs.get('relation_types', [])

    #     if not relation_types:
    #         # No relation type filter, use all
    #         relation_types = ['BTNT', 'NTBT', 'E', 'ND']

    #     query = """
    #     MATCH (o:OMIMterm)<-[r]-(n:ORPHAterm)
    #     WHERE (n.orphaid in $ordoterms and type(r) in $reltypes)
    #     RETURN DISTINCT(n.orphaid) AS orphaID,type(r) as rel, COLLECT(DISTINCT(o.omimid)) AS omimIDs;
    #     """

    #     parameters['ordoterms'] = ordo_terms
    #     parameters['reltypes'] = relation_types

    #     return await self.execute_query(query, parameters)

    # async def map_omim_ordo(self, omim_terms: list[str], **kwargs):
    #     """
    #     Map omim terms to ordo terms.
    #     :param omim_terms: The list of omim terms to map.
    #     :return: Also includes the rel type in return
    #     """

    #     parameters = {}

    #     relation_types = kwargs.get('relation_types', [])

    #     if not relation_types:
    #         # No relation type filter, use all
    #         relation_types = ['BTNT', 'NTBT', 'E', 'ND']

    #     query = """
    #     MATCH (o:OMIMterm)<-[r]-(n:ORPHAterm)
    #     WHERE (o.omimid in $omimterms and type(r) in $reltypes)
    #     RETURN DISTINCT(o.omimid) AS omimID,type(r) as rel, COLLECT(DISTINCT(n.orphaid)) AS orphaIDs;
    #     """

    #     parameters['omimterms'] = omim_terms
    #     parameters['reltypes'] = relation_types

    #     return await self.execute_query(query, parameters)

    # async def map_pathway_reaction(self, pathway_ids: list[str], **kwargs):
    #     """
    #     Map pathways to reactions.
    #     :param pathway_ids: The list of pathways to map.
    #     :return:
    #     """

    #     query = """
    #     MATCH (n:Pathway)<-[:PART_OF_PATHWAY]-(n1:Reaction)
    #     WHERE n.ReactomePathwayID IN $pathwayids
    #     RETURN DISTINCT(n.ReactomePathwayID) AS pathwayID, collect(DISTINCT(n1.ReactomeReactionID)) AS reactionIDs;
    #     """

    #     parameters = {
    #         'pathwayids': pathway_ids,
    #     }

    #     return await self.execute_query(query, parameters)

    # async def map_reaction_pathway(self, reaction_ids: list[str], **kwargs):
    #     """
    #     Map reactions to pathways.
    #     :param reaction_ids: The list of reactions to map.
    #     :return:
    #     """

    #     query = """
    #     MATCH (n:Reaction)-[:PART_OF_PATHWAY]->(n1:Pathway)
    #     WHERE n.ReactomeReactionID IN $reactionids
    #     RETURN DISTINCT(n.ReactomeReactionID) AS reactionID, COLLECT(DISTINCT(n1.ReactomePathwayID)) AS pathwayIDs;
    #     """

    #     parameters = {
    #         'reactionids': reaction_ids,
    #     }

    #     return await self.execute_query(query, parameters)

    # async def map_reaction_gene(self, reaction_ids: list[str], **kwargs):
    #     """
    #     Map reactions to genes.
    #     :param reaction_ids: The list of reactions to map.
    #     :return:
    #     """

    #     query = """
    #     MATCH (n:Reaction)-[:USING_GENE_PRODUCT]->(n1:Gene)
    #     WHERE n.ReactomeReactionID IN $reactionids
    #     RETURN DISTINCT(n.ReactomeReactionID) AS reactionID, COLLECT(DISTINCT(n1.Symbol)) AS symbols;
    #     """

    #     parameters = {
    #         'reactionids': reaction_ids,
    #     }

    #     return await self.execute_query(query, parameters)

    # async def map_gene_reaction(self, gene_symbols: list[str], **kwargs):
    #     """
    #     Map genes to reactions.
    #     :param gene_symbols: The list of genes to map.
    #     :return:
    #     """

    #     query = """
    #     MATCH (n:Gene)<-[:USING_GENE_PRODUCT]-(n1:Reaction)
    #     WHERE n.Symbol IN $symbols
    #     RETURN DISTINCT(n.Symbol) AS symbol, COLLECT(DISTINCT(n1.ReactomeReactionID)) AS reactionIDs;
    #     """

    #     parameters = {
    #         'symbols': gene_symbols,
    #     }

    #     return await self.execute_query(query, parameters)

    # async def map_gene_protein(self, gene_symbols: list[str], **kwargs):
    #     """
    #     Map genes to protein effects.
    #     :param gene_symbols: The list of genes to map.
    #     :return:
    #     """

    #     query = """
    #     MATCH (n:Gene)-[:HAS_EFFECT]->(n1:Protein_Effect)
    #     WHERE n.Symbol IN $symbols
    #     RETURN DISTINCT(n.Symbol) AS symbol, COLLECT(DISTINCT(n1.type)) AS proteinEffects;
    #     """

    #     parameters = {
    #         'symbols': gene_symbols,
    #     }

    #     return await self.execute_query(query, parameters)

    # async def map_protein_gene(self, protein_effects: list[str], **kwargs):
    #     """
    #     Map protein effects to genes.
    #     :param protein_effects: The list of variants to map.
    #     :return:
    #     """

    #     query = """
    #     MATCH (n:Protein_Effect)<-[:HAS_EFFECT]-(n1:Gene)
    #     WHERE n.type IN $proteinEffects
    #     RETURN DISTINCT(n.type) AS variant, COLLECT(DISTINCT(n1.Symbol)) AS symbols;
    #     """

    #     parameters = {
    #         'proteinEffects': protein_effects,
    #     }

    #     return await self.execute_query(query, parameters)

    # async def map_gene_omim(self, gene_symbols: list[str], **kwargs):
    #     """
    #     Map genes to omim terms.
    #     :param gene_symbols: The list of genes to map.
    #     :return:
    #     """

    #     query = """
    #     MATCH (o:OMIMterm)<-[:ASSOCIATED_WITH]-(g:Gene) 
    #     WHERE g.Symbol IN $symbols
    #     RETURN g.Symbol as symbol,collect(DISTINCT(o.omimid)) as omimIDs
    #     """

    #     parameters = {
    #         'symbols': gene_symbols,
    #     }

    #     return await self.execute_query(query, parameters)

    # async def map_omim_gene(self, omim_terms: list[str], **kwargs):
    #     """
    #     Map omim terms to genes.
    #     :param omim_terms: The list of omim terms to map.
    #     :return:
    #     """

    #     query = """
    #     MATCH (o:OMIMterm)<-[:ASSOCIATED_WITH]-(g:Gene) 
    #     WHERE o.omimid IN $omimterms
    #     RETURN o.omimid as omimID,collect(DISTINCT(g.Symbol)) as symbols
    #     """

    #     parameters = {
    #         'omimterms': omim_terms,
    #     }

    #     return await self.execute_query(query, parameters)

    # async def map(self, original_type: TermType, target_type: TermType, terms: list[str], **kwargs):
    #     """
    #     Map terms from one ontology to another.
    #     :param original_type: The type of the original terms.
    #     :param target_type: The type of the target terms.
    #     :param terms: The list of terms to map.
    #     :return:
    #     """

    #     _, terms = self.check_terms(terms, original_type, will_raise=True)

    #     mapping_methods = {
    #         (TermType.HPO, TermType.ORDO): self.map_hpo_ordo,
    #         (TermType.ORDO, TermType.HPO): self.map_ordo_hpo,
    #         (TermType.HPO, TermType.OMIM): self.map_hpo_omim,
    #         (TermType.OMIM, TermType.HPO): self.map_omim_hpo,
    #         (TermType.ORDO, TermType.OMIM): self.map_ordo_omim,
    #         (TermType.OMIM, TermType.ORDO): self.map_omim_ordo,
    #         (TermType.PATHWAY, TermType.REACTION): self.map_pathway_reaction,
    #         (TermType.REACTION, TermType.PATHWAY): self.map_reaction_pathway,
    #         (TermType.REACTION, TermType.GENE): self.map_reaction_gene,
    #         (TermType.GENE, TermType.REACTION): self.map_gene_reaction,
    #         (TermType.GENE, TermType.PROTEIN_EFFECT): self.map_gene_protein,
    #         (TermType.PROTEIN_EFFECT, TermType.GENE): self.map_protein_gene,
    #         (TermType.GENE, TermType.OMIM): self.map_gene_omim,
    #         (TermType.OMIM, TermType.GENE): self.map_omim_gene,
    #     }

    #     mapping_function: MappingFunction = mapping_methods.get((original_type, target_type))

    #     if mapping_function is None:
    #         raise ValueError(f'Invalid mapping request: {original_type} --> {target_type}')
    #     else:
    #         return await mapping_function(terms, **kwargs)
