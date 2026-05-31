# BTech Miniproject
##### An Intelligent and Trustworthy Social-Media–Driven Disaster Emergency Response System with Fake Content Detection and Volunteer Coordination
During continuously occurring disaster situations such as floods, earthquakes, and
landslides, social media becomes a vital platform where affected individuals share real
time updates and request urgent help. However, due to the massive volume of posts,
authorities often miss genuine requests, while fake or misleading content reduces infor
mation reliability and delays emergency response. This creates a gap between people in
need and those who can provide assistance.
Toaddress this issue, this project proposes An Intelligent and Trustworthy Social
Media–Driven Disaster Emergency Response System with Fake Content De
tection and Volunteer Coordination. The system collects real-time disaster-related
posts and processes them through a structured pipeline. A Distilled Bidirectional En
coder Representations from Transformers (DistilBERT) model analyzes disaster
relevance and generates a disaster probability. In parallel, a NewsAPI-based module
verifies events using trusted sources, while a rule-based engine evaluates textual cred
ibility. These outputs are combined using a decision engine to classify posts as real or
fake.
Only posts classified as real are further processed. A Logistic Regression model
detects genuine help requests, and the system extracts specific needs such as rescue, food,
shelter, medical aid, and emergency resources. Based on these needs, automated email
notifications are sent to relevant authorities using Simple Mail Transfer Protocol
(SMTP) for timely response.
Additionally, a Flask-based frontend displays verified posts in real time, clearly mark
ing them as real or fake. This platform enables volunteers and the public to identify af
fected individuals and provide support, effectively bridging the gap between victims and
responders.
By integrating deep learning, machine learning, external verification, and rule-based
reasoning, the system improves the accuracy, trustworthiness, and efficiency of disaster
response.
