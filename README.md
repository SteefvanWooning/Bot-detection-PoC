# RP2 - Web of Deepfakes



## This RP is mostly about bot detection on Twitter

Online social media networks, like Twitter, are by nature vulnerable to malicious uses of text synthesis by using tools like GPT-3. Using the synthesis capabilities, automated phishing and spam campaigns can be setup to trick legitimate users of the platforms into thinking they are conversing with other legitimate users. Because of automation, malicious actors can create a number of 'inauthentic accounts' and throw out a large net and just wait until victims are made. The cost of creating an inauthentic Twitter account is a human clicking on the verify captcha button. Detecting one is more involved than that, which is why the amount of bots can grow harder than the rate at which they are removed. It is said that as little as 5\%, but as much as 30\% of the accounts on Twitter are fake or spam. Two organizations, SparkToro and Followerwonk recently did a joint Twitter analysis; their analysis found that there just under 20\% of Twitter accounts are fake, a surprising contrast to Twitter's figures of 'fewer than 5% of mDAU'(monetizable daily active users) they mention in their Q4 FY21 financial filings.

## To use the server on a local browser

The first step is to ensure all you have all required libraries for python.
then export the bearer token in your local terminal:
`export BEARER_TOKEN="your-bearer-token-here"`
`export FLASK_APP="server.py"`
`flask run`