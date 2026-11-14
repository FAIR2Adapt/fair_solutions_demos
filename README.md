
# FAIR2Adapt – FAIR Solutions Demo

This repository contains a prototype web application developed within the **FAIR2Adapt project** to demonstrate the application of the FAIRification Framework to scientific publications.

The demonstration focuses on **Scenario 2: Literature Review and Knowledge Extraction**, developed in the context of the Portuguese National Adaptation Hub.

## Scenario implemented: Literature Review and Knowledge Extraction

Scientific publications contain valuable knowledge for climate change adaptation research. However, much of this information is available as unstructured text, limiting its discoverability, interoperability, and machine-actionability.

This scenario demonstrates how FAIRification services can transform scientific publications into machine-actionable resources by enriching their metadata and extracting structured scientific knowledge.

The FAIRification workflow includes the following activities:

1. **Publication retrieval:** Identify and retrieve relevant scientific publications.
2. **Metadata enrichment:** Extract descriptive and semantic metadata from publications.
3. **Scientific claim extraction:** Identify relevant scientific statements within publication contents.
4. **FDO generation:** Represent publications and their enriched metadata as FAIR Digital Objects.

The workflow combines automated services with human intervention when scientific interpretation or validation is required.

## Installation

The application uses Python, Poetry for dependency management, and Streamlit for its web interface.

### Requirements

- Python
- [Poetry](https://python-poetry.org/)

### Install

Clone the repository:

```bash
git clone https://github.com/FAIR2Adapt/fair_solutions_demos.git
cd fair_solutions_demos
```

Install the dependencies:

```bash
poetry install
```

## Run

Start the Streamlit web application by executing:

```bash
poetry run streamlit run app.py
```

Once the application starts, **open a web browser** and navigate to:

**http://localhost:8501**

The application provides a web-based interface to explore the FAIRification process demonstrated in Scenario 2.

Keep the terminal running while using the application. To stop the server, press `Ctrl+C` in the terminal.


## Documentation

Further information about the FAIRification Framework and its supporting services is available in the [FAIRification Framework documentation](https://w3id.org/fff).

## Acknowledgements

This prototype has been developed within the **FAIR2Adapt project**, with contributions from project partners involved in the FAIRification of climate adaptation research resources.
