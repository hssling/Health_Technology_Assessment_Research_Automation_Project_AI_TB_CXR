#!/usr/bin/env python3
"""
Literature Search Module for HTA Projects
Fetches real data from PubMed using E-utilities API
"""

import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time
from pathlib import Path

class PubMedSearcher:
    def __init__(self, email="hta-research@example.com"):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.email = email

    def search_pubmed(self, query, max_results=100):
        """Search PubMed and return PMIDs"""
        search_url = f"{self.base_url}esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "email": self.email
        }

        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()

        return data.get("esearchresult", {}).get("idlist", [])

    def fetch_abstracts(self, pmids):
        """Fetch abstracts for given PMIDs"""
        if not pmids:
            return []

        fetch_url = f"{self.base_url}efetch.fcgi"
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
            "email": self.email
        }

        response = requests.get(fetch_url, params=params)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        articles = []

        for article in root.findall(".//PubmedArticle"):
            try:
                pmid_elem = article.find(".//PMID")
                pmid = pmid_elem.text if pmid_elem is not None else ""

                title_elem = article.find(".//ArticleTitle")
                title = title_elem.text if title_elem is not None else ""

                abstract_elem = article.find(".//AbstractText")
                abstract = abstract_elem.text if abstract_elem is not None else ""

                year_elem = article.find(".//PubDate/Year")
                year = year_elem.text if year_elem is not None else ""

                journal_elem = article.find(".//Journal/Title")
                journal = journal_elem.text if journal_elem is not None else ""

                doi_elem = article.find(".//ELocationID[@EIdType='doi']")
                doi = doi_elem.text if doi_elem is not None else ""

                authors = []
                for author in article.findall(".//Author"):
                    lastname = author.find("LastName")
                    firstname = author.find("ForeName")
                    if lastname is not None and firstname is not None:
                        authors.append(f"{firstname.text} {lastname.text}")

                articles.append({
                    "pmid": pmid,
                    "title": title,
                    "abstract": abstract,
                    "year": year,
                    "journal": journal,
                    "doi": doi,
                    "authors": "; ".join(authors)
                })

            except Exception as e:
                print(f"Error parsing article: {e}")
                continue

        return articles

    def search_and_fetch(self, query, max_results=100):
        """Complete search and fetch pipeline"""
        print(f"Searching PubMed for: {query}")
        pmids = self.search_pubmed(query, max_results)
        print(f"Found {len(pmids)} articles")

        if len(pmids) > 100:  # API limit
            pmids = pmids[:100]

        # Fetch in batches to avoid API limits
        articles = []
        batch_size = 20
        for i in range(0, len(pmids), batch_size):
            batch_pmids = pmids[i:i+batch_size]
            batch_articles = self.fetch_abstracts(batch_pmids)
            articles.extend(batch_articles)
            time.sleep(0.5)  # Rate limiting

        return articles

def extract_relevant_data(articles, project_type):
    """Extract relevant quantitative data from abstracts for HTA modeling"""

    extracted_data = []

    for article in articles:
        if article is None:
            continue
        abstract = (article.get("abstract") or "").lower()
        title = (article.get("title") or "").lower()

        data_point = {
            "pmid": article.get("pmid"),
            "title": article.get("title"),
            "year": article.get("year"),
            "doi": article.get("doi")
        }

        # Project-specific extraction
        if project_type == "hpv_vaccine":
            # Extract vaccine efficacy, cost, coverage, etc.
            if "efficacy" in abstract or "effectiveness" in abstract:
                data_point["efficacy"] = extract_percentage(abstract)
            if "cost" in abstract or "price" in abstract:
                data_point["cost"] = extract_cost(abstract)
            if "coverage" in abstract or "uptake" in abstract:
                data_point["coverage"] = extract_percentage(abstract)

        elif project_type == "ncd_screening":
            # Extract screening sensitivity, specificity, cost, etc.
            if "sensitivity" in abstract:
                data_point["sensitivity"] = extract_percentage(abstract)
            if "specificity" in abstract:
                data_point["specificity"] = extract_percentage(abstract)
            if "cost" in abstract:
                data_point["cost"] = extract_cost(abstract)

        elif project_type == "dialysis":
            # Extract survival rates, cost per session, etc.
            if "survival" in abstract:
                data_point["survival_rate"] = extract_percentage(abstract)
            if "cost" in abstract:
                data_point["cost_per_session"] = extract_cost(abstract)

        elif project_type == "mdrtb":
            # Extract treatment success, cost, etc.
            if "success" in abstract or "cure" in abstract:
                data_point["success_rate"] = extract_percentage(abstract)
            if "cost" in abstract:
                data_point["cost"] = extract_cost(abstract)

        elif project_type == "ai_tb_cxr":
            # Extract AI accuracy, sensitivity, specificity
            if "accuracy" in abstract:
                data_point["accuracy"] = extract_percentage(abstract)
            if "sensitivity" in abstract:
                data_point["sensitivity"] = extract_percentage(abstract)
            if "specificity" in abstract:
                data_point["specificity"] = extract_percentage(abstract)

        # Only add if we found some relevant data
        if len(data_point) > 4:  # More than just basic fields
            extracted_data.append(data_point)

    return extracted_data

def extract_percentage(text):
    """Extract percentage values from text"""
    import re
    percentages = re.findall(r'(\d+(?:\.\d+)?)%', text)
    return percentages[0] if percentages else None

def extract_cost(text):
    """Extract cost values from text"""
    import re
    # Look for currency amounts
    costs = re.findall(r'[\$₹](\d+(?:,\d+)*(?:\.\d+)?)', text)
    if costs:
        return costs[0].replace(',', '')
    return None

def perform_literature_search(project_dir):
    """Main function to perform literature search for a project"""

    # Read search strings
    search_file = project_dir / "02_search_strings.txt"
    if not search_file.exists():
        print(f"No search strings file found in {project_dir}")
        return None

    search_content = search_file.read_text()

    # Extract PubMed query - try multiple formats
    pubmed_query = None
    lines = search_content.split('\n')

    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('-'):
            continue

        # Check for PubMed header
        if 'pubmed' in line.lower():
            # Look for query in current line after colon
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) > 1 and parts[1].strip():
                    pubmed_query = parts[1].strip()
                    break
            # Or look in next few lines
            for j in range(1, min(5, len(lines) - i)):
                next_line = lines[i + j].strip()
                if next_line and not next_line.startswith('#') and not next_line.startswith('-'):
                    pubmed_query = next_line
                    break
            if pubmed_query:
                break
        # If no header found, take first substantial line
        elif not pubmed_query and len(line) > 10:
            pubmed_query = line
            break

    if not pubmed_query:
        print(f"Could not extract PubMed query from: {search_content[:200]}...")
        return None

    # Determine project type
    project_name = project_dir.name
    if "hpv" in project_name.lower():
        project_type = "hpv_vaccine"
    elif "ncd" in project_name.lower():
        project_type = "ncd_screening"
    elif "dialysis" in project_name.lower():
        project_type = "dialysis"
    elif "mdrtb" in project_name.lower():
        project_type = "mdrtb"
    elif "ai_tb" in project_name.lower():
        project_type = "ai_tb_cxr"
    else:
        project_type = "general"

    # Perform search
    searcher = PubMedSearcher()
    articles = searcher.search_and_fetch(pubmed_query, max_results=50)

    # Extract relevant data
    extracted_data = extract_relevant_data(articles, project_type)

    # Create data directory
    data_dir = project_dir / "data"
    data_dir.mkdir(exist_ok=True)

    # Save raw search results
    df_raw = pd.DataFrame(articles)
    raw_file = data_dir / "search_results_raw.csv"
    df_raw.to_csv(raw_file, index=False)

    # Save extracted data
    if extracted_data:
        df_extracted = pd.DataFrame(extracted_data)
        extracted_file = data_dir / "extracted_data.csv"
        df_extracted.to_csv(extracted_file, index=False)

    print(f"Search completed for {project_name}. Found {len(articles)} articles, extracted {len(extracted_data)} data points.")

    return extracted_data

if __name__ == "__main__":
    # Test with HPV project
    project_dir = Path("hta_project_01_hpv_vaccine")
    perform_literature_search(project_dir)
