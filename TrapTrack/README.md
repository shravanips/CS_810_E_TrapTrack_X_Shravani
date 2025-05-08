Project Flows

TrapTrack/
├── .idea
├── data
│   └── diff_output                    # Output of storage diff comparisons.
│   └── network_logs                   #  Per-domain tracker logs from MITMproxy.
│   └── storage_logs                   # Saved JSONs of local/session storage and cookies, labeled pre_ and post_.
│   └── geo_locations.json             # Stores IP-to-country mapping for all detected third-party domains.
├── screenshots                       # Screenshots captured during browser visits (before/after consent).
├── consent_diff_engine.py             # Compares pre- and post-consent storage to detect changes.
├── fingerprint_detector.py            #  Injects JavaScript to detect fingerprinting attempts in visited pages.
├── generate_html_report.py            # Creates a static HTML report with screenshots, cookie diffs, geo-data, and trapscore.
├── geo_analyzer.py                   # Maps IPs from tracker logs to countries using geo-location databases.
├── geo_simulator.py                  # Optionally mocks regional headers to simulate visits from different countries.
├── network_logger.py                 # MITMproxy-based logger to capture all network traffic (used to identify trackers).
├── persona_injector.py               # Placeholder for injecting simulated personas/user agents.
├── README.md
├── run_all.py                        # Full script that sequentially runs all modules: 
                                        site test, geo analyzer, trapscore calculator, report generator.
├── storage_audit.py                  # Captures localStorage, sessionStorage, and cookies before and after consent actions.
├── test_sites.csv                    # CSV file listing websites to test and their consent types
├── trapscore.py                      # Calculates a normalized privacy risk score based on trackers, geos, storage, and fingerprinting.
├── TrapTrack.py                      # Main site tester script that drives browser visits, 
                                        captures cookies, screenshots, injects JS, and initiates storage logging.
├── z3_model.py                       # Placeholder for symbolic privacy modeling using Z3



                           +------------------+
                           |   run_all.py     |  ← Master
                           +------------------+
                                     |
          ┌──────────────────────────┼────────────────────────────┐
          ↓                          ↓                            ↓
+------------------+    +---------------------+      +----------------------+
|  TrapTrack.py    |    |  geo_analyzer.py    |      |  trapscore.py        |
| (main site visit |    | (GeoIP enrichment)  |      | (privacy score calc) |
|  + JS injection) |    +---------------------+      +----------------------+
+------------------+               ↓                          ↓
          |                        Reads:                 Returns:
          ↓                    data/network_logs/       Normalized score (0–100)
+-----------------------+                             
| fingerprint_detector.py |                            
| (Injects JS for        |
| canvas/audio sniffing) |
+-----------------------+                              
          ↓
+-------------------------+
| storage_audit.py        |
| (Captures pre/post      |
| localStorage/session)   |
+-------------------------+
          ↓
+-----------------------------+
| consent_diff_engine.py      |
| (Compares pre/post storage) |
+-----------------------------+

          ↓
+-----------------------------+
| generate_html_report.py     |
| (Generates static HTML)     |
+-----------------------------+

          ↓

# Supporting tools
+------------------------+   +----------------------+
| geo_simulator.py       |   | persona_injector.py  |
| (Region header spoof)  |   | (User agent mockups) |
+------------------------+   +----------------------+




| Technique                         | Modules Involved                          | Purpose                         |
|-----------------------------------| ----------------------------------------- | ------------------------------- |
| **Dynamic Instrumentation**       | `TrapTrack.py`, `fingerprint_detector.py` | Inject JS, monitor DOM/runtime  |
| **Network Traffic Logging**       | `network_logger.py`                       | Capture third-party calls       |
| **Geo Enrichment**                | `geo_analyzer.py`                         | Location-based domain profiling |
| **Heuristic Scoring**             | `trapscore.py`                            | Rule-based risk classification  |
| **Differential State Comparison** | `consent_diff_engine.py`                  | Detect storage/cookie shifts    |
| **Symbolic Modeling**             | `z3_model.py`                             | Formalize behavioral policies   |
