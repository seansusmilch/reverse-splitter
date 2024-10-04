import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

PROMPT = ' '.join([
    "-- This is an article about a stock reverse split.\n",
    "--- Summarize the information about fractional shares into one or two sentences.",
    # "If the article says fractional shares will be rounded up to the nearest whole share, respond with 'Fractional shares will be rounded up.'",
    # "If the article does not contain information about fractional shares, respond with 'No information about fractional shares.'",
    "Use simple language.",
    "Read carefully.",
    "Do not hallucinate.",
    "Keep it concise.",
    "Do not include any information that is not in the article.",
    "Do not include any examples.",
    "Do not include any explanations."
    "Start the summary with a yes or no answer to the question: 'Will fractional shares be rounded up?'",
])

def summarize_article(article:str):
    response = model.generate_content(f'{article}\n{PROMPT}')
    return response.text.strip()

if __name__ == '__main__':
    article = '''
Stockhouse Logo
Join today and have your say! It’s FREE!
Join Now Sign In
Home
Community
Markets
News
Portfolio
DealRoom
Search Companies, etc

News   Press Releases
AgEagle Aerial Systems Inc. Announces Reverse Stock Split
UAVS | 18 hours ago
Wichita, Kansas, Oct. 03, 2024 (GLOBE NEWSWIRE) -- AgEagle Aerial Systems Inc. (NYSE American: UAVS) (“AgEagle” or the “Company”), an industry-leading provider of full stack flight hardware, sensors and software for commercial and government use, announced today a reverse stock split of its authorized, issued and outstanding common stock, par value $0.001 per share, at a ratio of one (1) share of common stock for every fifty (50) shares of common stock, effective as of 5:00 p.m. (Eastern Time) on October 14, 2024 (the “Effective Date”). The Company’s common stock will begin trading on a split-adjusted basis when the market opens on October 15, 2024. The reverse stock split was authorized by the Company’s Board of Directors on October 3, 2024. Pursuant to the laws of the State of Nevada, the Company’s state of incorporation, the Company’s Board of Directors has the authority to effect a reverse stock split without shareholder approval if the number of authorized shares of common stock and the number of outstanding shares of common stock are proportionally reduced. The Company will file a certificate of change to its articles of incorporation, as amended, with the Secretary of State of Nevada to effect the reverse stock split. The Company’s common stock will continue to trade on the NYSE American under the stock ticker “UAVS” but will trade under the new CUSIP number 00848K 309.

As a result of the reverse split, each fifty (50) pre-split shares of common stock outstanding will automatically combine into one (1) new share of common stock without any action on the part of the holders, and the number of outstanding common shares will be reduced from 39,720,458 shares to approximately 850,409 shares without taking into account fractional shares.

The reverse stock split is being effected to ensure that the Company can meet the per share price requirements of the NYSE American, the Company's current listing exchange.

No fractional shares will be issued as a result of the reverse stock split. Shareholders who otherwise would be entitled to a fractional share because they hold a number of shares not evenly divisible by the 1 (one) for fifty (50) reverse split ratio, will automatically be entitled to receive an additional fractional share of the Company’s common stock to round up to the next whole share.

The Company’s transfer agent, Equiniti Trust Company, which is also acting as the exchange agent for the reverse split, will send instructions to stockholders of record who hold stock certificates regarding the exchange of their old certificates for new certificates, should they wish to do so. Stockholders who hold their shares in brokerage accounts or “street name” are not required to take action to effect the exchange of their shares.

This press release does not constitute an offer to sell or the solicitation of an offer to buy, nor will there be any sales of these securities in any jurisdiction in which such offer, solicitation or sale would be unlawful prior to registration or qualification under the securities laws of such jurisdiction. For more detailed information relating to this transaction, please refer to the related Form 8-K to be filed by the Company with the U.S. Securities and Exchange Commission.

About AgEagle Aerial Systems Inc.

Through its three centers of excellence, AgEagle is actively engaged in designing and delivering best-in-class flight hardware, sensors and software that solve important problems for its customers. Founded in 2010, AgEagle was originally formed to pioneer proprietary, professional-grade, fixed-winged drones and aerial imagery-based data collection and analytics solutions for the agriculture industry. Today, AgEagle is a leading provider of full stack drone solutions for customers worldwide in the energy, construction, agriculture, and government verticals. For additional information, please visit our website at www.ageagle.com.

Forward-Looking Statement

This press release may contain “forward-looking statements” within the meaning of Section 27A of the Securities Act of 1933 and Section 21E of the Securities Exchange Act of 1934, each as amended. Forward-looking statements include all statements that do not relate solely to historical or current facts, including without limitation statements regarding the Company’s product development and business prospects, and can be identified by the use of words such as “may,” “will,” “expect,” “project,” “estimate,” “anticipate,” “plan,” “believe,” “potential,” “should,” “continue” or the negative versions of those words or other comparable words. Forward-looking statements are not guarantees of future actions or performance. These forward-looking statements are based on information currently available to the Company and its current plans or expectations and are subject to a number of risks and uncertainties that could significantly affect current plans. Should one or more of these risks or uncertainties materialize, or the underlying assumptions prove incorrect, actual results may differ significantly from those anticipated, believed, estimated, expected, intended, or planned. Although the Company believes that the expectations reflected in the forward-looking statements are reasonable, the Company cannot guarantee future results, performance, or achievements. Except as required by applicable law, including the securities laws of the United States, the Company does not intend to update any of the forward-looking statements to conform these statements to actual results.

AgEagle Aerial Systems Contacts

Investor Relations Email: UAVS@ageagle.com

Media Email: media@ageagle.com



Primary Logo

Tags:
INDUSTRIALS

 0
Related News
@ the Bell: TSX keeps holding pattern as Mideast conflicts intensify
18 hours ago
@ the Bell: TSX flat as market figures out latest Middle East conflict
1 day ago
@ the Bell: TSX and Wall Street September trading defies the odds
2 days ago
Recent U.S. Press Releases
HII Hosts Chairman of the Joint Chiefs of Staff at Newport News Shipbuilding
12 minutes ago
AEROSPACE-DEFENSE | INDUSTRIALS
Compass Therapeutics Announces Upcoming Poster Presentation at the 39th Society for Immunotherapy...
25 minutes ago
BIOTECHNOLOGY | HEALTHCARE
Apollo Silver Announces Upsizing of Private Placement
53 minutes ago
SILVER
More Press Releases »
Featured News Links
Uranium Powerhouse: The $126M Deal to Supercharge U.S. Nuclear Production
Eastern Platinum Announces Commissioning Of PGM Processing Facility At Crocodile River Mine
Alphamin Announces Interim Dividend increase, Record Quarterly Tin Production & Q3 EBITDA Guidance of US$91.5 Million
Get the latest news and updates from Stockhouse on social media

facebook twitter linkedin
Follow STOCKHOUSE Today

USER FEEDBACK SURVEY
×
Be the voice that helps shape the content on site!
At Stockhouse, we’re committed to delivering content that matters to you. Your insights are key in shaping our strategy. Take a few minutes to share your feedback and help influence what you see on our site!

The Market Online in partnership with Stockhouse
Later
Participate
Not interested

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