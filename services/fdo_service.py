import rohub
import uuid
from rdflib import URIRef, BNode, Literal
from pathlib import Path
import config

def generate_CS1_fdo(logger, doi_result):
    logger.info("Generating the FDO")

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
    ro = rohub.ros_create(title=ro_title, research_areas=ro_research_areas, description=ro_description, ros_type=ro_type, access_mode="public"  )

    logger.info ("Update editors")
    ro.editors = [config.ROHUB_EDITOR]

    logger.info ("Adding relations")
    # Add the DOI publication as an external resource
    for file in doi_result["files_involved"]:

        pub_res = ro.add_external_resource(
            res_type="Dataset",                        # or "Paper"
            input_url=file["url"],
            title=file["name"]
        )

    # optional metadata on the resource
    pub_res.title = doi_result.get("title")
    pub_res.description = doi_result.get("abstract")
    pub_res.update_metadata()

    ro_pid = ro.shared_link
    ro_id = ro.identifier

    mvp_id="https://w3id.org/ro-id/"+ro_id+"/product/1"

    new_annot=ro.add_annotations()
    annotation_id = new_annot['identifier']
    provenanve_url_value=""
    
    mvp_id_value="" 

    license_url_value="https://creativecommons.org/licenses/by/4.0/"

    # connect mvp to RO-Crate
    the_subject=ro_pid
    the_predicate=related_product
    the_object=mvp_id
    ro.add_triple(the_subject=the_subject, the_predicate=the_predicate, the_object=the_object, annotation_id=annotation_id, object_class="URIRef")

    # set mvp type
    the_subject=mvp_id
    the_predicate=has_type
    the_object=Product
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

    try:
        logger.info("Update ro")
        ro.update()
    except Exception as e:
        print(type(e))
        print(e)
    logger.info("task completed")
    return ro_pid

def generate_CS4_fdo(logger, doi_result, enrichment_result,doi):
    logger.info("Generating the FDO")

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
    ro = rohub.ros_create(title=ro_title, research_areas=ro_research_areas, description=ro_description, ros_type=ro_type, access_mode="public"  )

    logger.info ("Update editors")
    ro.editors = [config.ROHUB_EDITOR]

    logger.info ("Adding relations")
    # Add the DOI publication as an external resource
    doi_value = doi                     # e.g. 10.xxxx/xxxxx
    doi_url = f"https://doi.org/{doi_value}"

    pub_res = ro.add_external_resource(
        res_type="Publication",                        # or "Paper"
        input_url=doi_url
    )

    # optional metadata on the resource
    pub_res.title = doi_result.get("title")
    pub_res.description = doi_result.get("abstract")
    pub_res.update_metadata()

    ro_pid = ro.shared_link
    ro_id = ro.identifier

    mvp_id="https://w3id.org/ro-id/"+ro_id+"/product/1"

    new_annot=ro.add_annotations()
    annotation_id = new_annot['identifier']
    provenanve_url_value=""
    
    """
    if "error" not in enrichment_result:
        provenanve_url_value=enrichment_result["response"]["url"]
    else:
        provenanve_url_value=""
    """
    mvp_id_value="" 

    license_url_value="https://creativecommons.org/licenses/by/4.0/"

    # connect mvp to RO-Crate
    the_subject=ro_pid
    the_predicate=related_product
    the_object=mvp_id
    ro.add_triple(the_subject=the_subject, the_predicate=the_predicate, the_object=the_object, annotation_id=annotation_id, object_class="URIRef")

    # set mvp type
    the_subject=mvp_id
    the_predicate=has_type
    the_object=Product
    ro.add_triple(the_subject=the_subject, the_predicate=the_predicate, the_object=the_object, annotation_id=annotation_id, object_class="URIRef")

    # Add keywords
    keywords = "https://schema.org/keywords"

    keyword_values = enrichment_result["response"]["ke_phrases"]

    logger.info("Keywords")
    logger.info(keyword_values)

    keyword_texts = [
        item["key_element"].strip()
        for item in keyword_values
        if item.get("key_element")
    ]

    # Optional: remove duplicates while preserving order
    keyword_texts = list(dict.fromkeys(keyword_texts))

    if keyword_texts:
        ro.add_triple(
            the_subject=mvp_id,
            the_predicate=keywords,
            the_object=", ".join(keyword_texts),
            annotation_id=annotation_id
        )

    locations = enrichment_result["response"]["entity_locations"]
    logger.info("Locations")
    logger.info(locations)
    places = [item for item in locations if 'geonames' in item]

    index = 1
    for place in places:
        print(place['entity'], place['geonames'], place['appearances'])
        
        spatialCoverage_id1="https://w3id.org/ro-id/"+ro_id+"/spatial/"+str(index)

        the_subject=mvp_id
        the_predicate=spatialCoverage
        the_object=spatialCoverage_id1
        ro.add_triple(the_subject=the_subject, the_predicate=the_predicate, the_object=the_object, annotation_id=annotation_id, object_class="URIRef")

        the_subject=spatialCoverage_id1
        the_predicate=has_type
        the_object=Place
        ro.add_triple(the_subject=the_subject, the_predicate=the_predicate, the_object=the_object, annotation_id=annotation_id, object_class="URIRef")

        the_subject=spatialCoverage_id1
        the_predicate=name
        the_object=place['entity']
        ro.add_triple(the_subject=the_subject, the_predicate=the_predicate, the_object=the_object, annotation_id=annotation_id)

        the_subject=spatialCoverage_id1
        the_predicate=url
        the_object=place["geonames"]
        ro.add_triple(the_subject=the_subject, the_predicate=the_predicate, the_object=the_object, annotation_id=annotation_id, object_class="URIRef")

        index = index + 1
    """
    for location in locations:
        index = 1
        logger.info("Location detected"+location["name"])
        spatialCoverage_id1="https://w3id.org/ro-id/"+ro_id+"/spatial/"+str(index)
        the_subject=spatialCoverage_id1
        the_predicate=name
        the_object=location["name"]
        ro.add_triple(the_subject=the_subject, the_predicate=the_predicate, the_object=the_object, annotation_id=annotation_id)
        index = index+1
    """
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

    try:
        logger.info("Update ro")
        ro.update()
    except Exception as e:
        print(type(e))
        print(e)
    logger.info("task completed")
    return ro_pid

