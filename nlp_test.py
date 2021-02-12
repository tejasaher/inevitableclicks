from nltk.tag import pos_tag
from nltk import word_tokenize,ne_chunk
from nltk.stem.wordnet import WordNetLemmatizer
import re, string,random
import os
from nltk.corpus import stopwords
from nltk import FreqDist, classify, NaiveBayesClassifier

with open(os.getcwd()+"/sasi_errors.txt",'r+') as f:
    content = f.readlines()
    f.close()

#text= "Failed to provision command on network element: [nsps1@PSALN02ZATCWI]:[3008]Validation of request against the XML schema failed."

#print(pos_tag(word_tokenize(text)))

# #lemmatize the string data 
# def lemmatize_sentence(tokens):
#     lemmatizer = WordNetLemmatizer()
#     lemmatized_sentence = []
#     for word, tag in pos_tag(tokens):
#         if tag.startswith('NN'):
#             pos = 'n'
#         elif tag.startswith('VB'):
#             pos = 'v'
#         else:
#             pos = 'a'
#         lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
#     return lemmatized_sentence
# for a in content:
# 	print(lemmatize_sentence(word_tokenize(a)))
def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token
def get_errors_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

#remove noise like special characters ,remove stop words
def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens
stop_words = stopwords.words('english')
positive_cleaned_tokens_list=[]
for a in content:
#print(stopwords)
	positive_cleaned_tokens_list.append(remove_noise(word_tokenize(a), stop_words))
all_pos_words = get_all_words(positive_cleaned_tokens_list)
print(all_pos_words)
freq_dist_pos = FreqDist(all_pos_words)
print(freq_dist_pos.most_common(10))
positive_tokens_for_model = get_errors_for_model(positive_cleaned_tokens_list)
positive_dataset = [(error_dict, "Positive")
                         for error_dict in positive_tokens_for_model]


dataset = positive_dataset 

random.shuffle(dataset)

train_data = dataset[:700]
test_data = dataset[700:]

classifier = NaiveBayesClassifier.train(train_data)

print("Accuracy is:", classify.accuracy(classifier, test_data))

print(classifier.show_most_informative_features(10))

custom_error = "Failed to provision command on network element: [nsps1@PSALN02ZATCWI]:Failed to X509 sign the request.: RSA private key operation failed"

custom_tokens = remove_noise(word_tokenize(custom_error))
1
print(custom_error, classifier.classify(dict([token, True] for token in custom_tokens)))



