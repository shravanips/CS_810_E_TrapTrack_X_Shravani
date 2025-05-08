# CS810E_Project

Project by:
> Shravani Sawant
> Ayushi Gupta

Experimental Setup

Procedure:
To reproduce our experiment or run your own privacy analysis using TrapTrack, follow the steps below:

1. Install All Dependencies
Before starting, make sure you’ve set up the environment:
•	Python 3.10 or higher
•	Playwright (headless browser automation)
•	MITMproxy (for traffic interception)
•	All other packages listed in the requirements (you can use pip install -r requirements.txt if available)

2. Set Up Your Test Website
•	Open the file test_sites.csv in the project root.
•	By default, it contains:
o	https://www.amazon.co.uk, EU
•	You can replace or add more sites to this file in the same format:
o	Website URL,Consent Type (e.g., Accept All or Reject All)

 3. Start MITMproxy in Logging Mode
•	In Terminal Window 1, navigate to the TrapTrack project directory.
•	Run the following command:
o	mitmdump -s network_logger.py
•	This step is essential for logging all outbound network requests made during the browsing session.

4. Launch the TrapTrack Analysis Pipeline
•	In Terminal Window 2, also navigate to your TrapTrack folder.
•	Start the program using:
o	python run_all.py
•	This script will:
o	Verify MITMproxy is running.
o	Load URLs from test_sites.csv.
o	Open a Chromium browser via Playwright to simulate user interaction.

5. Interact with the Website Like a Real User
•	When the browser launches:
o	Wait for the cookie consent banner to appear.
o	Click Accept, Reject, or any available choice (based on your test plan).
o	Spend 30–60 seconds browsing — click on links, view product pages, scroll around.
This mimics genuine behavior and triggers any consent-based tracking scripts.

6. Continue the Analysis
•	Once you’ve explored enough, go back to Terminal 2.
•	The script will prompt:
o	🕹️ Surf manually in the browser... Press [Enter] here when done...
•	Simply press Enter to begin post-consent data capture.

7. Automated Modules Will Execute in Sequence
The following tools will now run automatically:
•	geo_analyzer.py – Maps all third-party tracker IPs to their physical countries.
•	trapscore.py – Calculates a privacy risk score based on behavior.
•	generate_html_report.py – Creates an HTML report with visuals and metrics.

8. View the Final Report
•	After processing, your browser will open a new tab showing:
o	Before & after screenshots
o	Storage differences (cookies/local/session)
o	GeoIP map of tracker countries
o	Final TrapScore with detailed breakdown


