import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

PROMPT = ' '.join([
    "-- This is an article about a stock reverse split.\n",
    "--- Summarize the information about fractional shares into two sentences.",
    # "If the article says fractional shares will be rounded up to the nearest whole share, respond with 'Fractional shares will be rounded up.'",
    # "If the article does not contain information about fractional shares, respond with 'No information about fractional shares.'",
    "Use simple language.",
    "Read carefully.",
    "Do not hallucinate.",
    "Keep it concise.",
    "Start the summary with a yes or no answer to the question: 'Will fractional shares be rounded up?'",
])

def summarize_article(article:str):
    response = model.generate_content(f'{article}\n{PROMPT}')
    return response.text.strip()

if __name__ == '__main__':
    article = '''
Stockhouse.com uses cookies on this site. By continuing to use our service, you agree to our use of cookies. Cookies are used to offer you a better browsing experience and to analyze our traffic. We also use them to share usage information with our partners. See full details.
I Agree
×
Stockhouse Logo
Join today and have your say! It’s FREE!

    Home
    Community
    Markets
    News
    Portfolio
    DealRoom 

News   Press Releases
ZW Data Action Technologies Inc. Announces Reverse Stock Split
CNET | 23 hours ago

BEIJING, Sept. 25, 2024 (GLOBE NEWSWIRE) -- ZW Data Action Technologies Inc. (Nasdaq: CNET) (“ZW Data” or the “Company”), an integrated online advertising, precision marketing, data analytics, and other value-added services company, announced today that its Board of Directors has approved a reverse stock split of its common stock, par value $0.001 per share (the “Common Stock”) at a ratio of 1-for-4 (the “Reverse Stock Split”). The Reverse Stock Split will take effect on September 30, 2024, and the shares of the Company will trade on a post-split basis on Nasdaq under the Company’s existing trading symbol “CNET,” at the market open on September 30, 2024, upon Nasdaq’s approval. The new CUSIP number following the Reverse Stock Split will be 98880R 307.

Under Nevada Revised Statutes (“NRS”) Section 78.207, the Company may decrease its authorized shares of Common Stock and correspondingly decrease the number of issued and outstanding shares of Common Stock by resolution adopted by the Board of Directors, without obtaining the approval of the stockholders. The Reverse Stock Split will be effected by the Company filing a Certificate of Change (the “Certificate”) pursuant to NRS Section 78.209 with the Secretary of State of the State of Nevada. As a result of the filing of the Certificate, the number of shares of the Company’s authorized Common Stock will be reduced from 50,000,000 shares to 12,500,000 shares and the issued and outstanding number of shares of the Common Stock will be correspondingly decreased.

When the Reverse Stock Split becomes effective, the total number of shares of Common Stock held by each stockholder of the Company will be converted automatically into the number of shares of Common Stock equal to (i) the number of issued and outstanding shares of Common Stock held by each such stockholder immediately prior to the Reverse Stock Split, divided by (ii) 4, with such resulting number of shares rounded up to the nearest whole share. The Company will issue one whole share of the post-Reverse Stock Split Common Stock to any stockholder who otherwise would have received a fractional share as a result of the Reverse Stock Split. As a result, no fractional shares will be issued in connection with the Reverse Stock Split and no cash or other consideration will be paid in connection with any fractional shares that would otherwise have resulted from the Reverse Stock Split.

The Reverse Stock Split has no effect on the par value of the Company’s Common Stock or authorized shares of preferred stock. Immediately after the Reverse Stock Split, each stockholder’s percentage ownership interest in the Company and proportional voting power will remain unchanged, except for minor changes and adjustments that will result from the treatment of fractional shares. The rights and privileges of the holders of shares of Common Stock will be substantially unaffected by the Reverse Stock Split.

The Reverse Stock Split is primarily being effected to regain compliance with the $1.00 minimum bid price required for continued listing on The Nasdaq Capital Market under Nasdaq Listing Rule 5550(a)(2).

Stockholders who are holding their shares in electronic form at brokerage firms do not need to take any action, as the effect of the Reverse Stock Split will automatically be reflected in their brokerage accounts. Stockholders holding paper certificates may (but are not required to) send the certificates to the Company’s transfer agent and registrar, Empire Stock Transfer. Empire Stock Transfer will issue a new stock certificate reflecting the Reverse Stock Split to each requesting stockholder.

About ZW Data Action Technologies Inc.

Established in 2003 and headquartered in Beijing, China, ZW Data Action Technologies Inc. (the “Company”) offers online advertising, precision marketing, data analytics and other value-added services for enterprise clients. Leveraging its fully integrated services platform, proprietary database, and cutting-edge algorithms, ZW Data Action Technologies delivers customized, result-driven business solutions for small and medium-sized enterprise clients in China. The Company also develops blockchain and artificial intelligence enabled web/mobile applications and software solutions for clients. More information about the Company can be found at: http://www.zdat.com/.

Forward-looking Statement

This release includes “forward-looking statements” within the meaning of Section 27A of the Securities Act of 1933, as amended, and Section 21E of the Securities Exchange Act of 1934, as amended. Forward-looking statements give our current expectations, opinion, belief or forecasts of future events and performance. A statement identified by the use of forward-looking words including “will,” “may,” “expects,” “projects,” “anticipates,” “plans,” “believes,” “estimate,” “should,” and certain of the other foregoing statements may be deemed forward-looking statements. These forward-looking statements are subject to a number of risks, uncertainties and assumptions, including market and other conditions. More detailed information about the Company and the risk factors that may affect the realization of forward-looking statements is set forth in the Company’s filings with the SEC. Investors and security holders are urged to read these documents free of charge on the SEC’s web site at http://www.sec.gov. The Company undertakes no obligation to update any such forward-looking statements after the date hereof to conform to actual results or changes in expectations, except as required by law.

For more information, please contact:
ZW Data Action Technologies Inc.
Email: wanmeng@chinanet-online.com
Phone: +86 13522831530

Primary Logo
Tags:
COMMUNICATION SERVICES
0
Related News

    @ the Bell: TSX scores another fresh record high
    11 minutes ago
    @ the Bell: TSX rally takes a pause
    23 hours ago
    @ the Bell: TSX rises as gold continues record run
    2 days ago

Recent U.S. Press Releases

    Cue Biopharma Announces Proposed Public Offering
    1 minute ago
    BIOTECHNOLOGY | HEALTHCARE
    Wabash and Steel Dynamics Forge 10-Year Strategic Partnership
    11 minutes ago
    INDUSTRIALS
    Scorpio Tankers Inc. Announces Purchase of Call Options by the President of the Company
    12 minutes ago
    OIL-GAS-MIDSTREAM | ENERGY

More Press Releases »
Featured News Links
Where to find Educational Resources for Beginner and Intermediate Investors
Red Cloud: Fall Mining Showcase 2024 Starting October 16 – Register Here
Topgolf Takes Fortnite by Storm – Gamers Can Now Swing, Score, and Win Big in the Virtual World

Get the latest news and updates from Stockhouse on social media

    facebook twitter linkedin 

Follow STOCKHOUSE Today

Stockhouse Logo

    About Us
    Careers
    Contribute
    Contact Us

Support

    Help

Legal

    Disclaimer
    Privacy Policy

Follow Us
Stockhouse.com is owned by Stockhouse Publishing Ltd. © 2019 Stockhouse Publishing Ltd. All rights reserved. Financial Market Data powered by Refinitiv. All rights reserved. Quotes and other data delayed by 15 minutes for NYSE/AMEX/NASDAQ, 20 minutes for TSX/TSX-V unless otherwise indicated. Google Play and the Google Play logo are trademarks of Google Inc. The Apple logo and iTunes are trademarks of Apple Inc., registered in the U.S. and other countries.
'''
    print(summarize_article(article))