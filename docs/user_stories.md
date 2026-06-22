1. As a Head of Customer Support 
I want to see overall chatbot performance metrics 
So that I can make informed decisions about resource allocation between bot and human agents.

Given a Customer Support with no technical background
When opening the dashboard for the first time
Then all metrics are labeled with plain business terms, 
not technical abbreviations

Given a Customer Support working with resulting dashboard
When sorting by category
Then seeing that category is highlighted while others are dimmed

2. As a QA analyst 
I want to identify categories with bad performance
So that I can prioritize categories for the development team to improve.

Given a QA analyst 
When opening the resulting dashboard
Then all metrics are dynamically visualised through plots and interactive

Given a QA analyst working with resulting dashboard
When clicking on specific bar on plot
Then seeing concrete number compared to the mean

3. As a chatbot developer
I want to export evaluation results
So  that I can analyze evaluation results and adjust chatbot prompts for low-performing categories.

Given a Chatbot developer working on metric improvement
When exporting evaluation results
Then downloading file in easy-to-work json format by default

Given a Chatbot developer working on metric improvement
When trying to export data that do not exist
Then seeing a an error notification

4. As a Compliance Officer, I want to see hallucination rate by category, so that I can ensure the chatbot does not provide incorrect financial information to customers.

Given a Compliance Officer reviewing chatbot quality report
When checking hallucination rate by intent category
Then hallucination rate does not exceed 5% in any category