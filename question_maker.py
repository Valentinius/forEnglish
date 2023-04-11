import grammar_checker
#from textacy.spacier import utils
#from textacy.spacier import utils as spacy_utils
#import spacy
#import re
import difflib


#nlp = spacy.load("en_core_web_sm")


# def questioner_1(sent):
#     doc = nlp(sent)
#     stop, modal_root, form_root, root = "", "", "", ""
#     ques, child, lem, check, label = "", "", "", "", ""
#     for sentence in doc:
#         if sentence.dep_ in ['aux', 'ROOT']:
#             if sentence.lemma_ in ['must', 'shall', 'will', 'should', 'would', 'can', 'could', 'may', 'might']:
#                 modal_root = sentence
#             elif sentence.lemma_ in ['be', 'have']:
#                 form_root = sentence
#             else:
#                 root = sentence
#             for children in sentence.subtree:
#                 if children.text in ['because', 'so because']:
#                     check = children
#                 if children.dep_ in ['dobj', 'pobj', 'advmod', 'acomp']:
#                     child = children
#                     for prep in child.subtree:
#                         if prep.is_stop:
#                             stop = prep
#                     if child.ent_type_:
#                         label = child.ent_type_
#                     elif child.pos_ == "ADV":
#                         label = "QUANTITY"
#                     else:
#                         label = ""
#
#     if modal_root and form_root:
#         root = modal_root
#     elif modal_root:
#         root = modal_root
#     elif form_root:
#         root = form_root
#
#     for lemma in doc:
#         if lemma.text in ['we', 'I']:
#             lem = lemma.text
#         else:
#             lem = ""
#
#     if stop:
#         sent = doc.text.replace(str(child), "")
#         sent = sent.replace(" " + str(stop) + " ", "")
#     else:
#         sent = doc.text.replace(str(child), "")
#
#     if lem:
#         sent = sent.replace(lem, "you")
#
#     if root.lemma_ in ['be', 'have', 'must', 'shall', 'will', 'should', 'would', 'can', 'could', 'may', 'might']:
#         if label == 'PERSON':
#             ques = 'who ' + str(root) + " " + re.sub('{}'.format(" " + str(root) + " ").lower(), ' ', sent) + '?'
#         elif label in ['GPE', 'LOC']:
#             ques = 'where ' + str(root) + " " + re.sub('{}'.format(" " + str(root) + " ").lower(), ' ', sent) + '?'
#         elif label in ['TIME', 'DATE']:
#             ques = 'when ' + str(root) + " " + re.sub('{}'.format(" " + str(root) + " ").lower(), ' ', sent) + '?'
#         elif label in ['QUANTITY']:
#             ques = 'How ' + str(root) + " " + re.sub('{}'.format(" " + str(root) + " ").lower(), ' ', sent) + '?'
#         else:
#             ques = 'what ' + str(root) + " " + re.sub('{}'.format(" " + str(root) + " ").lower(), ' ', sent) + '?'
#     else:
#         if root.tag_ == 'VBD' or str(utils.get_subjects_of_verb(root)[0]).upper() in ['I', 'You', 'We', 'They', 'He',
#                                                                                       'She', 'It']:
#             if check.text in ['because', 'so because']:
#                 ques = 'Why did ' + str(utils.get_subjects_of_verb(root)[0]) + " " + root.lemma_ + '?'
#             else:
#                 ques = 'Did ' + str(utils.get_subjects_of_verb(root)[0]) + " " + root.lemma_ + '?'
#         elif str(utils.get_subjects_of_verb(root)[0]).upper() in ['I', 'You', 'We', 'They']:
#             ques = 'Do ' + str(utils.get_subjects_of_verb(root)[0]) + " " + root.lemma_ + '?'
#         elif str(utils.get_subjects_of_verb(root)[0]).upper() in ['He', 'She', 'It'] or label == "PERSON":
#             ques = 'Does ' + str(utils.get_subjects_of_verb(root)[0]) + " " + root.lemma_ + '?'
#
#     return grammar_checker.correct_grammar_sentence(ques)
#

def sentence_to_question(arg):
    hverbs = ["is", "have", "had", "was", "could", "would", "will", "do", "did", "should", "shall", "can", "are"]
    words = arg.split(" ")
    zen_sim = (0, "", "")
    for hverb in hverbs:
        for word in words:
            similarity = difflib.SequenceMatcher(None, word, hverb).ratio() * 100
            if similarity > zen_sim[0]:
                zen_sim = (similarity, hverb, word)
    if zen_sim[0] < 30:
        raise ValueError("unable to create question.")
    else:
        words.remove(zen_sim[2])
        words = " ".join(words)[0].lower() + " ".join(words)[1:]
        question = "{0} {1}?".format(zen_sim[1].capitalize(), words)
        return question#grammar_checker.correct_grammar_sentence(question)


def get_questions(sent):
    questions = []

    try:
        questions.append(sentence_to_question(sent))
    except ValueError as err:
        print(err)

    return questions
