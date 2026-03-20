import rohub
import uuid
from rdflib import URIRef, BNode, Literal
from pathlib import Path
import config

def generate_CS4_fdo(logger, doi_result, enrichment_result):
    logger.info("Generating FDO")

    related_product="https://schema.org/isRelatedTo"
    has_type="http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    Product="https://schema.org/Product"
    variableMeasured="https://schema.org/variableMeasured"
    Variable = "https://w3id.org/iadopt/ont/Variable"
    name="https://schema.org/name"
    url="https://schema.org/url"
    depth="https://schema.org/depth"
    value="https://schema.org/value"
    temporalCoverage="https://schema.org/temporalCoverage"
    spatialCoverage="https://schema.org/spatialCoverage"
    Place="https://schema.org/Place"
    scenarioId="https://w3id.org/ro/terms/cca/scenarioId"
    spatialResolutionAsText="http://data.europa.eu/930/spatialResolutionAsText"
    license="https://schema.org/license"
    identifier="https://schema.org/identifier"
    provenance="http://purl.org/dc/terms/provenance"

    rohub_user = config.ROHUB_USER
    rohub_pwd = config.ROHUB_PWD
    rohub.login(username=rohub_user, password=rohub_pwd)

    ro_title= doi_result["title"]
    ro_research_areas=["Environmental research"]
    ro_description= doi_result["abstract"]
    ro_type="Bibliography-centric Research Object"
    ro = rohub.ros_create(title=ro_title, research_areas=ro_research_areas, description=ro_description, ros_type=ro_type)

    ro_pid = ro.shared_link
    ro_id = ro.identifier

    mvp_id="https://w3id.org/ro-id/"+ro_id+"/product/1"

    new_annot=ro.add_annotations()
    annotation_id = new_annot['identifier']
    provenanve_url_value=enrichment_result["url"]

    mvp_id_value="" 

    license_url_value="https://creativecommons.org/licenses/by/4.0/"

    the_subject=ro_pid
    the_predicate=related_product
    the_object=mvp_id
    ro.add_triple(the_subject=the_subject, the_predicate=the_predicate, the_object=the_object, annotation_id=annotation_id, object_class="URIRef")

    the_subject=mvp_id
    the_predicate=license
    the_object=license_url_value
    ro.add_triple(the_subject=the_subject, the_predicate=the_predicate, the_object=the_object, annotation_id=annotation_id, object_class="URIRef")

    if license_url_value != "":
        the_subject=mvp_id
        the_predicate=license
        the_object=license_url_value
        ro.add_triple(the_subject=the_subject, the_predicate=the_predicate, the_object=the_object, annotation_id=annotation_id, object_class="URIRef")

    # set mvp associated identifier
    if mvp_id_value != "":
        the_subject=mvp_id
        the_predicate=identifier
        the_object=mvp_id_value
        ro.add_triple(the_subject=the_subject, the_predicate=the_predicate, the_object=the_object, annotation_id=annotation_id)

    #
    if provenanve_url_value != "":
        the_subject=mvp_id
        the_predicate=provenance
        the_object=provenanve_url_value
        ro.add_triple(the_subject=the_subject, the_predicate=the_predicate, the_object=the_object, annotation_id=annotation_id)

    logger.info("task completed")

