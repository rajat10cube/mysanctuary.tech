# mysanctuary.tech

Hello Reader!

# My Sanctuary

Problem: The increasing isolation and separtaion from friends and families due to varied timezones and modern lifestyles, leaves people feeling lonely and wanting to be heard. The lack of a social person further escalates this feeling. In such a scenario, one reaches out to the 'relentlessly adicting' social media platforms which inculcates toxic coping mechanisms and other issues. The rise of echo chambers throughout online social networks is accelerating user polarization on such delicate subjects. There is little knowledge of the key players in such homogeneous groups and how echo chambers communicate with one another. As observed, over the time this leads to development of multiple wellness issues. 

Why to solve it: We frequently seek out and accept viewpoints that are consistent with our own. Strong relationships between people who share similar beliefs on online platforms are likely to be a reflection of this tendency. The development of such homogeneous societies might also be aided by feed algorithms used by websites like Twitter. Researchers have demonstrated the creation of "echo chambers" of individuals with like opinions in online social networks, which can increase polarization and extreme opinions.

Solution: Introducing a Mental Wellness oriented Safe Space 'MY SANCTUARY' which is a cloud based web app that aims to dismantle the echo chambers and maintain relevancy of the support space with an AI Chatbot, toxicity filters, sentiment analysis, emotion detection, all this while maintaining the privacy of the user. 

How we're solving it: As the name suggests, `My Sanctuary` creates a non-judgemental blog forum for users to vent out and resonate with like-minded peers. The platform incorporates several Machine Learning Models to achieve toxicity filters, sentiment analysis, emotion detection functions. 
- The web app is developed in Python using the Flask framework. 
- The conversational AI agent built using the Google Cloud subset Dialogflow, aims to be a passifier in case of need. Upon encountering a vulnerable state of mind of the user, the chatbot redirects the user to either the Mental Health Helplines or the EMergency contact given by them using Twilio . 
- To maintain the non-judgemental aspect and privacy of the users, all usernames are randomly generated for the front end but the actual identity of the user is taken in at the time of registration for authentication purposes.
- Every post given by a user is scanned using the ML algorithms for various safety parameters and if passes the checks, if displayed on the feed.
- The entity HEALER SCORE is a measure of the good activity tht the user involves in. The score increases by positive engagement with the platform.

TechStack used:
1. Python, Flask
2. MongoDB
3. Twilio
4. Google Cloud Platform, Dialogflow
5. Frontend: HTML, CSS, JS, Bootstrap
