from rdflib import Dataset, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD, FOAF
from datetime import datetime, timezone
import urllib.parse
import nanopub
from nanopub import Nanopub, NanopubConf, load_profile
from pathlib import Path

PUBLISHER = "https://sciencelive4all.org/"

# Namespace to publish. We can use our own namespace
TEMP_NP = Namespace("https://w3id.org/np/temp") 

TEMP_NP = Namespace("https://w3id.org/sciencelive/np") 


# Namespaces ad defined in Nanodash
NP = Namespace("http://www.nanopub.org/nschema#")
DCT = Namespace("http://purl.org/dc/terms/")
NT = Namespace("https://w3id.org/np/o/ntemplate/")
NPX = Namespace("http://purl.org/nanopub/x/")
PROV = Namespace("http://www.w3.org/ns/prov#")
ORCID = Namespace("https://orcid.org/")
HYCL = Namespace("http://purl.org/petapico/o/hycl#")
CITO = Namespace("http://purl.org/spar/cito/")
SCHEMA = Namespace("http://schema.org/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
AIDA = Namespace("http://purl.org/aida/")

# Template URIs
AIDA_TEMPLATE = URIRef("https://w3id.org/np/RALmXhDw3rHcMveTgbv8VtWxijUHwnSqhCmtJFIPKWVaA")
PROV_TEMPLATE = URIRef("https://w3id.org/np/RA7lSq6MuK_TIC6JMSHvLtee3lpLoZDOqLJCLXevnrPoU")
PUBINFO_TEMPLATE_1 = URIRef("https://w3id.org/np/RA0J4vUn_dekg-U1kK3AOEt02p9mT2WO03uGxLDec1jLw")
PUBINFO_TEMPLATE_2 = URIRef("https://w3id.org/np/RAukAcWHRDlkqxk7H2XNSegc1WnHI569INvNr-xdptDGI")

# AIDA-specific constants
HYCL_AIDA_SENTENCE = URIRef("http://purl.org/petapico/o/hycl#AIDA-Sentence")
HYCL_NS = URIRef("http://purl.org/petapico/o/hycl")

profile = load_profile("./profile.yml")
print(f"Loaded profile: \n{profile.name}\n{profile.orcid_id}")

def create_aida_nanopub(logger, claim):
    """
    Create an AIDA sentence nanopublication using rdflib Dataset.
    
    Args:
        np_config: dict with AIDA sentence configuration
        metadata: dict with author and part_of info
    
    Returns:
        tuple: (Dataset, label)
    """
    # CRITICAL: Use temporary namespace that gets replaced when signing

    logger.info("Creating nanopublication")
    
    creator_orcid = "https://orcid.org/0000-0003-4112-6825"
    creator_name = "Esteban Gonzalez"
    AUTHOR_ORCID = creator_orcid
    AUTHOR_NAME = creator_name


    this_np = URIRef(TEMP_NP)
    head_graph = URIRef(TEMP_NP + "/Head")
    assertion_graph = URIRef(TEMP_NP + "/assertion")
    provenance_graph = URIRef(TEMP_NP + "/provenance")
    pubinfo_graph = URIRef(TEMP_NP + "/pubinfo")

    author_uri = URIRef(creator_orcid)


    # Create AIDA sentence URI (URL-encoded)
    aida_sentence = claim["claim"]
    logger.info("Add claim: "+str(aida_sentence))
    aida_uri = URIRef(f"http://purl.org/aida/{urllib.parse.quote(aida_sentence, safe='')}")
    
    # Create Dataset
    ds = Dataset()
    
    # Bind prefixes
    ds.bind("this", TEMP_NP)
    ds.bind("sub", TEMP_NP)
    ds.bind("np", NP)
    ds.bind("dct", DCT)
    ds.bind("nt", NT)
    ds.bind("npx", NPX)
    ds.bind("xsd", XSD)
    ds.bind("rdfs", RDFS)
    ds.bind("orcid", ORCID)
    ds.bind("prov", PROV)
    ds.bind("foaf", FOAF)
    ds.bind("hycl", HYCL)
    ds.bind("cito", CITO)
    ds.bind("schema", SCHEMA)
    ds.bind("skos", SKOS)
    
    # HEAD graph
    head = ds.graph(head_graph)
    head.add((this_np, RDF.type, NP.Nanopublication))
    head.add((this_np, NP.hasAssertion, assertion_graph))
    head.add((this_np, NP.hasProvenance, provenance_graph))
    head.add((this_np, NP.hasPublicationInfo, pubinfo_graph))
    
    # ASSERTION graph
    assertion = ds.graph(assertion_graph)
    assertion.add((aida_uri, RDF.type, HYCL_AIDA_SENTENCE))
    
     # PROVENANCE graph
    provenance = ds.graph(provenance_graph)
    provenance.add((assertion_graph, PROV.wasAttributedTo, author_uri))
    
   
    # PUBINFO graph
    pubinfo = ds.graph(pubinfo_graph)
    pubinfo.add((author_uri, FOAF.name, Literal(creator_name)))
    
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    pubinfo.add((this_np, DCT.created, Literal(now, datatype=XSD.dateTime)))
    pubinfo.add((this_np, DCT.creator, author_uri))
    pubinfo.add((this_np, DCT.license, URIRef("https://creativecommons.org/licenses/by/4.0/")))
    pubinfo.add((this_np, NPX.wasCreatedAt, URIRef(PUBLISHER)))
    
    # Nanopub types
    pubinfo.add((this_np, NPX.hasNanopubType, HYCL_AIDA_SENTENCE))
    pubinfo.add((this_np, NPX.hasNanopubType, HYCL_NS))
    
    # Introduces
    pubinfo.add((this_np, NPX.introduces, aida_uri))
    
    # Label
    label_text = aida_sentence[:100] + "..." if len(aida_sentence) > 100 else aida_sentence
    label = f"AIDA sentence: {label_text}"
    pubinfo.add((this_np, RDFS.label, Literal(label)))
    
    # Template references
    pubinfo.add((this_np, NT.wasCreatedFromTemplate, AIDA_TEMPLATE))
    pubinfo.add((this_np, NT.wasCreatedFromProvenanceTemplate, PROV_TEMPLATE))
    pubinfo.add((this_np, NT.wasCreatedFromPubinfoTemplate, PUBINFO_TEMPLATE_1))
    pubinfo.add((this_np, NT.wasCreatedFromPubinfoTemplate, PUBINFO_TEMPLATE_2))
    
    return ds, label



def publish_nanopublication2(logger, nanopub_data:dict):

    logger.info(nanopub_data)

    logger.info("Nanopublication:"+nanopub_data["label"])

    with open("example.trig", 'r') as f:
        print(f.read())

    conf = NanopubConf(profile=profile)

    #trig_text = Path("example.trig").read_text(encoding="utf-8")

    np_obj = Nanopub(rdf="example_anne.trig", conf=conf)
    np_obj.sign()
        
    np_obj.publish()
    print(f"✓ Published: {np_obj.source_uri}")

def publish_nanopublication(logger, nanopub_data:dict):

    logger.info(nanopub_data)

    logger.info("Nanopublication:"+nanopub_data["label"])
    logger.info(nanopub_data["nanopublication"])

    conf = NanopubConf(profile=profile)

    np_obj = Nanopub(rdf=nanopub_data["nanopublication"], conf=conf)
    #np_obj.check()
    np_obj.sign()
        
    np_obj.publish()
    print(f"✓ Published: {np_obj.source_uri}")