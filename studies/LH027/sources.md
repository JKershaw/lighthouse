# LH027 sources

- **S1, selected lead:** The National Archives, `https://www.nationalarchives.gov.uk/news/issues-with-the-national-archives-website/`, search result seen 22 October 2026 before protocol. Result text said the notice was published 21 October and that some services were taken offline because of a potential PHP vulnerability. This is prior outcome knowledge, not a direct page reading.
- **S2, direct attempt:** same URL, 22 October 2026, 06:38:40 to 06:38:48 UTC. The one direct GET returned HTTP 403 and a 919-byte HTML response, retained as `data/notice-2026-10-22.html`, SHA-256 `3efdf4982c58f407c1c6b4cd635bf9f22740c5950495207f1163cbe70b7f922c`. Request metadata is `data/read-2026-10-22.json`. No original notice body was available through this instrument.
- The web reader's direct open also returned HTTP 403 before the protocol; no additional page read was made after S2. The search result was a lead, not evidence of the exact service list or current availability.
