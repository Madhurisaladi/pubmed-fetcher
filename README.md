# pubmed-fetcher
**Overview**
This Python program fetches research papers from PubMed based on a user-specified query. It identifies papers with at least one non-academic author affiliated with a pharmaceutical or biotech company and returns the results as a CSV file.

**How the Code is Organized**
The code is structured into the following sections:
1. Fetching PubMed Papers
Uses esearch API to retrieve PubMed IDs based on the search query.
Uses efetch API to get detailed paper information.
2. Filtering Non-Academic Authors
Identifies authors from pharmaceutical/biotech companies using heuristics (e.g., company keywords, email domains).
3. Command-line Interface
Supports query input, debugging mode, and output file specification.
4. Saving Results
Writes the filtered paper details to a CSV file.
5. Error Handling & Logging
Handles API failures, empty responses, and missing data.

**Installation & Execution**
1. Install Dependencies
Using Poetry (Recommended)
poetry install
Using pip
pip install requests

2. Running the Script
Run the script with a query:
python fetch_pubmed_papers.py "cancer research" -f results.csv
Command-line Options
   1. -f or --file → Specify output CSV file name.
   2. -d or --debug → Enable debug mode for more information.
   3. -h or --help → Show help menu.
Example with debug mode:
python fetch_pubmed_papers.py "biotechnology innovation" -d

**Dependencies & External Tools Used**
1. Programming Language
Python 3.8+ (Recommended)
2. Libraries Used            Library	Purpose

   1.requests         -          	To make API calls to PubMed
   2.argparse	       -           For handling command-line arguments
   3.csv	             -           To save results in CSV format
   4.re	             -           For filtering non-academic authors based on heuristics
   5.xml.etree.ElementTree  -    	For parsing XML responses from PubMed API
3. APIs Used
PubMed API (esearch & efetch)
Retrieves research papers from PubMed database.
4. Version Control & Hosting
Git & GitHub → Used for version control and collaboration.



