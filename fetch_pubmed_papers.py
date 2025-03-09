import argparse
import csv
import requests
import re
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
NON_ACADEMIC_KEYWORDS = ["Pharma", "Biotech", "Inc", "Corp", "Ltd", "GmbH"]

def fetch_pubmed_ids(query: str) -> List[str]:
    search_url = f"{BASE_URL}esearch.fcgi?db=pubmed&term={query}&retmode=json"
    response = requests.get(search_url)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pubmed_id: str) -> Optional[Dict]:
    fetch_url = f"{BASE_URL}efetch.fcgi?db=pubmed&id={pubmed_id}&retmode=xml"
    response = requests.get(fetch_url)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    
    title = root.find(".//ArticleTitle").text if root.find(".//ArticleTitle") else "Unknown"
    pub_date = root.find(".//PubDate/Year").text if root.find(".//PubDate/Year") else "Unknown"
    authors = root.findall(".//Author")
    
    non_academic_authors = []
    company_affiliations = []
    corresponding_email = ""
    
    for author in authors:
        affiliation = author.find("AffiliationInfo/Affiliation")
        if affiliation is not None:
            affiliation_text = affiliation.text
            if any(keyword in affiliation_text for keyword in NON_ACADEMIC_KEYWORDS):
                non_academic_authors.append(author.find("LastName").text)
                company_affiliations.append(affiliation_text)
                
            if EMAIL_REGEX.search(affiliation_text):
                corresponding_email = EMAIL_REGEX.search(affiliation_text).group(0)
    
    if not non_academic_authors:
        return None
    
    return {
        "PubmedID": pubmed_id,
        "Title": title,
        "Publication Date": pub_date,
        "Non-academic Author(s)": ", ".join(non_academic_authors),
        "Company Affiliation(s)": ", ".join(company_affiliations),
        "Corresponding Author Email": corresponding_email,
    }

def save_to_csv(data: List[Dict], filename: str):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Output filename (CSV)", default="output.csv")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    pubmed_ids = fetch_pubmed_ids(args.query)
    if args.debug:
        print(f"Found {len(pubmed_ids)} papers.")
    
    results = []
    for pubmed_id in pubmed_ids:
        details = fetch_paper_details(pubmed_id)
        if details:
            results.append(details)
    
    if results:
        save_to_csv(results, args.file)
        print(f"Results saved to {args.file}")
    else:
        print("No matching papers found.")

if __name__ == "__main__":
    main()
