from gensim.models.keyedvectors import KeyedVectors
from DocSim import DocSim

googlenews_model_path = 'y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article Collation/Data/DocSim/GoogleNews-vectors-negative300.bin'
stopwords_path = "y:/New Volume/Work & School/School/University of York/Year 4/Fake News/Code/Fake-News-Project/Article Collation/Data/DocSim/stopwords_en.txt"
model = KeyedVectors.load_word2vec_format(googlenews_model_path, binary=True)
with open(stopwords_path, 'r') as fh:
    stopwords = fh.read().split(",")
ds = DocSim(model,stopwords=stopwords)

source = 'Matt Hancock owns shares in NHS-approved firm'
target = ['Matt Hancock: links to firm used by NHS fuels Tory cronyism row']



result = ds.calculate_similarity(source, target)
print(result)














""" The Conservative government is “infected with widespread cronyism”, Labour has claimed, amid reports the health secretary’s family firm won contracts from the NHS.

It has emerged that Matt Hancock failed to declare his interest in the company Topwood to parliamentary authorities for more than two months and had never previously declared his family’s longstanding involvement with it.

“It is now clear this Conservative government has been infected with widespread cronyism and is unable to identify where the line is drawn between personal and departmental interests. It’s one rule for them, another for everybody else,” said the shadow health minister Justin Madders.

He spoke after it emerged that Topwood won a tender competition to secure a place as an approved contractor with the NHS in Wales in early 2019. At the time, the firm was owned by Hancock’s sister and other family members. Health Service Journal, which first reported the story, said he had not declared this, despite having considered a sibling’s position with a separate firm worthy of declaration.

Documents lodged with Companies House show that on 1 February a minority stake in the firm was transferred to Hancock. According to a report on the Guido Fawkes blog, the firm won contracts with the NHS in Wales the following month, though this is not the responsibility of the UK government.

It was not until 12 April that Hancock declared his interest in the firm.

“There are serious questions to answer from Matt Hancock and there needs to be a full inquiry and immediate publication of all documents relating to Topwood’s acceptance on to the framework contract in 2019,” Madders said.

The Department of Health and Social Care has not yet responded to a request for comment.

A government spokesperson said: “Mr Hancock has acted entirely properly in these circumstances. All declarations of interest have been made in accordance with the ministerial code. Ministers have no involvement in the awarding of these contracts, and no conflict of interest arises.”

The news emerged as the government came under increasing pressure over the access afforded to the Australian financier Lex Greensill, for whom the former prime minister David Cameron went on to work.

Bob Kerslake, a former head of the civil service, said he had little faith in any investigation of the Greensill affair led by No 10, saying the prime minister had sat on the report into bullying allegations against the home secretary.

Lord Kerslake said there needed to be enforceable rules to govern interactions between the public and private sectors. “But it’s also about principles. We do have the Nolan principles of public life and they are a pretty good guide to how you should behave,” he told BBC Radio 4’s Today programme on Friday.

“Even if you fit within the rules technically, ask yourself the question do you meet those principles and it’s hard to see how what’s happened here meets those principles.”

Kerslake called for a “proper investigation” and added: “There is a place for unpaid advisers and some have been very helpful. But it has to be completely transparent and above board and no question whatsoever of conflict. I think here we can see the significant issues of conflict and it is very odd indeed that [Greensill] seems to have been given a business card without being clear on the process.”

Asked if he felt the review set up by Downing Street would get to the bottom of the issue, he said: “I’m unsure. I have to say, I have slightly lost confidence in prime ministerial-led inquiries because of how Priti Patel was handled.

“I believed that would be a fair and robust process. In the end, the prime minister sat on the report and then issued a bowdlerised version and took no action.” """