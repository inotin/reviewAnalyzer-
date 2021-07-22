#!/usr/bin/env python
# coding: utf-8
from IPython.core.display import display, HTML
from scipy.stats import ttest_ind
from google_images_search import GoogleImagesSearch
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from youtubesearchpython import VideosSearch
import warnings
from sklearn.preprocessing import MinMaxScaler
from collections import defaultdict
from scipy.stats import hmean
from deepsegment import DeepSegment
from nltk.corpus import stopwords
from nltk.tokenize import treebank
from nltk.sentiment import vader
from nltk.corpus import opinion_lexicon
from nltk.corpus import wordnet
import os
import sys
import time
import random
import urllib.request
import pandas as pd
import numpy as np
import charwords
import googleCreds  # Please modify goggleCredsTemplate and rename it to googleCreds
from tqdm import tqdm
from html2image import Html2Image

# Scraping packages
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
from bs4.element import Comment
# NLP packages
import nltk
nltk.download('opinion_lexicon')
nltk.download('vader_lexicon')
nltk.download('stopwords')

warnings.filterwarnings('ignore')


def getYouTubeLinksFromSearch(query, maxNumber=5):
    """
    The function returns a list of youtube urls from the query results

    Input:
    query:      str
                a string for searching youtube videos

    maxNumber:  int, default: 5
                number of urls for output,

    Output:
    list(str): list of urls

    """
    videosSearch = VideosSearch(query, limit=maxNumber, region='US')
    ids = []
    for i in videosSearch.result()['result']:
        ids.append('https://www.youtube.com/watch?v='+i['id'])
        # (i['title'])
    return ids


def getTextFromYoutubeCaptions(vidId):
    """
    The function gets text from captions in the YouTube video, ID of which is given as an input.

    Input:
    vidId: str
           YouTube Video ID

    Output:
    str: list of words from the captions
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(vidId)
        captions = ["NoText"]
        try:
            time.sleep(1+(0.5*random.random()))
            captions = YouTubeTranscriptApi.get_transcript(vidId, languages=['en'])
            print('english captions')
        except:
            #print("!Translating captions to English")
            transcript = transcript_list.find_transcript(['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'my', 'bs', 'bg', 'ceb', 'zh-Hant', 'zh-Hans',
                                                          'da', 'de', 'en', 'eo', 'et', 'fil', 'fi', 'fr', 'gl', 'gd', 'ka', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'ig', 'id',
                                                          'ga', 'is', 'it', 'ja', 'jv', 'yi', 'kn', 'kk', 'ca', 'km', 'rw', 'ky', 'ko', 'co', 'hr', 'ku', 'lo', 'la', 'lv', 'lt',
                                                          'lb', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mk', 'hmn', 'mn', 'ne', 'nl', 'no', 'ny', 'or', 'ps', 'fa', 'pl', 'pt', 'pa',
                                                          'ro', 'ru', 'sm', 'sv', 'sr', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'sw', 'st', 'su', 'tg', 'ta', 'tt', 'te', 'th',
                                                          'cs', 'tr', 'tk', 'ug', 'uk', 'hu', 'ur', 'uz', 'vi', 'cy', 'fy', 'xh', 'yo', 'zu'])
            captions = transcript.translate('en').fetch()
            print('translated captions')
        # print(captions)
        # input()
        text = ""

        for element in captions:
            text += element['text']+" "
        text = text.replace("\n", " ")
        # print(text)
        return text
    except:
        print('Youtube is blocking the app:( Try again later (or some other error)')
        return 'Youtube is blocking the app:( Try again later (or some other error)'


def tag_visible(element):
    """
    The function defines if element is visible

    Input:
    html element

    Output:
    bool: True if visible, False otherwise
    """

    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def getTextFromUrl(url):
    """
    The function returns visible text from html

    Input:
    html

    Output:
    str: text
    """
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)
# Testing
# getTextFromUrl('https://www.ilpost.it/2021/03/19/cina-stati-uniti-alaska-blinken/')[:1000]


# ## Scoring functions
# In this sections scoring functions are defined. They return score for a given piece of text. The higher the score the more positive text is. Further these functions will be used to assess pieces of text around keywords.

def assessPolarity(text):
    """
    Polarity assessment based on Liu and Hu opinion lexicon
    """
    stop_words = set(stopwords.words('english'))
    tokenizer = treebank.TreebankWordTokenizer()
    wordsList = [word.lower() for word in tokenizer.tokenize(text)]
    wordsList = [word for word in wordsList if not word in stop_words]
    scores = []

    for word in wordsList:
        if word in set(opinion_lexicon.positive()):
            score = 1
        elif word in set(opinion_lexicon.negative()):
            score = -1
        else:
            score = 0
        scores.append(score)
#     print(words)
#     print(scores)
    return np.sum(scores)

# Testing
# text = getTextFromYoutubeCaptions("eOW9jgCahnk")
# assessPolarity(text)


def assessPolarityVader(text, split_sentences=False):
    """
    Polarity assessment based on Vader
    """
    sia = vader.SentimentIntensityAnalyzer()
    # it's better to feed vader with phrases or sentences
    # but as soon as caption text does not contain punctuation i used deepsegment library
    # to split the caption text into sentences
    score = 0
    if split_sentences:
        segmenter = DeepSegment('en')
        sentenceList = segmenter.segment_long(text)

        for sentence in sentenceList:
            s = sia.polarity_scores(sentence)['compound']
#             print(sentence)
#             print('Score:', s)
#             print('-'*20)
            score += s
    else:
        score += sia.polarity_scores(text)['compound']
    return score

# testing
# text = getTextFromYoutubeCaptions("eOW9jgCahnk")
# assessPolarityVader(text, split_sentences = True)


def antiScore(score):
    """
    A function that returns a penalyzing score for word "not" according to the function

    Input:
    score (float): input score

    Output:
    float: a penalty to be added to the initial score if word "not" is present in the word list

    """

    return 0.58 - 1.15*score


def assessPolarityCustom(text, dictScores=None):
    """
    The function returns score for the piece of text given as input list of words according to dictScores

    Input:
    pieceOfText (list(str)): keywords to search for
    dictScores (dict): a dictionary of words and corresponding scores in form:
             {"A":[5,["very", "extremely", "surprisingly","great", "much", "incredibly"]],
              "B":[4,["pretty","good", "nice"]],
              "C":[3, ["enough","inexpensive", "cheap", "affordable","low","decent", "quite"]],
              "D":[-2,["weak","minimum","little"]]}

    Output:
    float: score
    """
    if dictScores == None:
        dictScores = {"A": [5, ["very", "extremely", "surprisingly", "great", "much", "plenty", "incredibly"]+charwords.veryWords],
                      "B": [4, ["pretty", "good", "nice"]+charwords.prettyWords],
                      "C": [3, ["enough", "affordable", "low", "decent", "quite"]+charwords.enoughWords],
                      "D": [-2, ["weak", "minimum", "little"]+charwords.weakWords]}

    stop_words = set(stopwords.words('english'))
    tokenizer = treebank.TreebankWordTokenizer()
    wordsList = [word.lower() for word in tokenizer.tokenize(text)]
    wordsList = [word for word in wordsList if not word in stop_words]

    score = 0
    lastScore = 0
    wordsList = list(set(wordsList))
    # print(wordsList)
    for word in wordsList:
        for key in dictScores:
            if word in dictScores[key][1]:
                lastScore = dictScores[key][0]
                # print(word,":",lastScore)
        if word == "not":
            lastScore = lastScore + antiScore(lastScore)
        score += lastScore
        lastScore = 0
    return score

# Testing
# text = getTextFromYoutubeCaptions("eOW9jgCahnk")
# assessPolarityCustom(text)


# ## Working with keywords
# In this section the function is defined which allows to extract a set amount of words around a key word.

def getPieceByKeyWords(text, keyWords, backward=5, forward=5):
    """
    The function returns a piece of caption text in a form of list with a given range.

    Input:
    text (str): input list of the caption text
    keyWords (list(str)): keywords to search for
    backward (int): number of words to include before found keyword
    forward (int): number of words to include before found keyword

    Output:
    list(str): list of words close to a given keyword
    """

    #stop_words = set(stopwords.words('english'))
    tokenizer = treebank.TreebankWordTokenizer()
    wordsList = [word.lower() for word in tokenizer.tokenize(text)]

    lst = []
    i = 0

    for word in wordsList:
        if word in set(keyWords):
            rear = max(0, i - backward)
            front = min(len(wordsList)-1, i+forward)
            lst.append(" ".join(wordsList[rear:front]))
        i += 1
    return lst

# Testing
# text = getTextFromYoutubeCaptions("eOW9jgCahnk")
# getPieceByKeyWords(text, ['engine'])


def getScores(dct, keyWords):
    scoresDict = defaultdict()
    dctForHist = {'product': [], 'keyword': [], 'aP': [], 'aPV': [], 'aPC': []}
    print('='*25)
    print('Scoring product: ', dct['product'])
    for url in dct['urls']:
        if 'youtube' in url:
            print('Youtube video:', url)
            text = getTextFromYoutubeCaptions(url.split('=')[1])
        else:
            text = getTextFromUrl(url)
        # print(text)
        # input()
        for keyWord in keyWords:
            textList = getPieceByKeyWords(text, [keyWord])
            aP, aPV, aPC = 0, 0, 0
            for t in textList:
                aP += assessPolarity(t)
                aPV += assessPolarityVader(t)
                aPC += assessPolarityCustom(t)
            scoresDict[keyWord] = [aP, aPV, aPC]
            dctForHist['product'].append(dct['product'])
            dctForHist['keyword'].append(keyWord)
            dctForHist['aP'].append(aP)
            dctForHist['aPV'].append(aPV)
            dctForHist['aPC'].append(aPC)
        print('-'*25)
    dfAllScores = pd.DataFrame(dctForHist)
    dfAllScores['mean'] = np.mean(dfAllScores[['aP', 'aPV', 'aPC']], axis=1)

    dfMeanScores = dfAllScores.groupby(by='keyword').mean()[['mean']].reset_index().T.reset_index()
    dfMeanScores.columns = dfMeanScores.iloc[0, :].values
    dfMeanScores = dfMeanScores.drop(columns=['keyword'])
    dfMeanScores['product'] = dct['product']
    dfMeanScores = dfMeanScores[['product']+list(dfMeanScores.columns[:-1])].iloc[1:, :]

    return dfMeanScores, dfAllScores

# Testing
# dct = {'name':"Honda CB650R",'urls':["https://www.youtube.com/watch?v=PO2uFDS1P3A",
#            "https://www.youtube.com/watch?v=GQK79vCohC4",
#            "https://www.youtube.com/watch?v=5AR5PwffLzI",
#            "https://www.youtube.com/watch?v=c0SL4pBJP4Y",
#            "https://ridermagazine.com/2020/06/05/2020-husqvarna-vitpilen-701-road-test-review/"]}

# print(getScores(dct, ['comfort','engine', 'design', 'handling']))


def getSynonimList(word):
    """
    The function returns list of synonims base on wordnet.synsets of nltk library
    for the text provide by urlList based on key words and dictScores

    Input:
    word (str): input word

    Output:
    list(str)
    """

    synonyms = []

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name().lower())
    print(synonyms)
    return (list(set(synonyms)))
# Testing
# getSynonimList('cost')


def getSetScores(productNames, productKeyWords, plot=False):
    """
    The function returns a dataframe with scores for products according to key words.

    Input:
    productNames    (list): input list of strings with product names
    productKeyWords (list): input list of strings with key words
    plot            (bool): default=False, if true plots barplots with scores and saves them to HTML ("result.html")

    Output:
    pandas dataframe with scores
    """
    productSet = []
    for product in productNames:
        dct = defaultdict()
        dct['product'] = product
        dct['urls'] = getYouTubeLinksFromSearch(product)
        productSet.append(dct)

    df = pd.DataFrame()
    for m in productSet:
        df = pd.concat([df, getScores(m, productKeyWords)])

    df['total'] = np.mean(df.iloc[:, 1:], axis=1)
    if plot:
        numOfPlots = int(np.sum([np.sum(df[x].sum() != 0) > 0 for x in df.columns[1:]]))

        fig = make_subplots(rows=numOfPlots, cols=1,
                            vertical_spacing=0.04)

        r = 1
        for n in df.columns[1:]:
            if np.sum(df[n].sum() != 0) > 0:
                fig.add_trace(go.Bar(x=df['product'], y=df[n], name=n),
                              row=r, col=1,)
                r += 1
        fig.update_layout(height=200*numOfPlots)
        fig.show()
        fig.write_html("static/reviewlyzer/result.html")

    df.to_html('static/reviewlyzer/df.html')
    return df


def getSetScoresText(productNames, productKeyWords,
                     maxNumber=15, api_key=googleCreds.GOOGLE_API_KEY2, cx=googleCreds.GOOGLE_CX, pathForOutput="results/", sep='\n'):
    """
    The function returns a dataframe with scores for products according to key words.

    Input:
    productNames    (str): input string with product names separated by sep
    productKeyWords (str): input string with key words separated by sep
    pathForOutput   (str): path for resulting htmls
    api_key         (str): Google API key for image search
    cx              (str): Google CX key for image search
    sep             (str): separator for productNames and productKeyWords ('\n' by default)

    Output:
    pandas dataframe with scores
    """
    #global fig
    # fig = None

    if not os.path.exists(pathForOutput):
        os.makedirs(pathForOutput)

    productNames = productNames.replace('\r', '')
    productKeyWords = productKeyWords.replace('\r', '')

    productNames = productNames.split(sep)
    productKeyWords = productKeyWords.lower().split(sep)
    print(productNames)
    print(productKeyWords)
    # input()
    productDictSet = []
    for product in productNames:
        dct = defaultdict()
        dct['product'] = product
        dct['urls'] = getYouTubeLinksFromSearch(product, maxNumber)
        productDictSet.append(dct)

    dfAllScores = pd.DataFrame()

    for productDict in productDictSet:
        dfTemp = getScores(productDict, productKeyWords)
        dfAllScores = pd.concat([dfAllScores, dfTemp[1]])

    dfAllScores.iloc[:, 2:] = dfAllScores.iloc[:, 2:]/np.max(dfAllScores.iloc[:, 2:])
    dfAllScores['mean'] = np.mean(dfAllScores.iloc[:, 2:], axis=1)
    print(dfAllScores.head(10))

    dfMeanScores = pd.DataFrame()
    for product in productNames:
        dfTemp = dfAllScores[dfAllScores['product'] == product]
        dfTemp = dfTemp.groupby(by='keyword').mean()[['mean']].reset_index().T.reset_index()
        dfTemp.columns = dfTemp.iloc[0, :].values
        dfTemp = dfTemp.drop(columns=['keyword'])
        dfTemp['product'] = product
        dfTemp = dfTemp[['product']+list(dfTemp.columns[:-1])].iloc[1:, :]
        dfMeanScores = pd.concat([dfMeanScores, dfTemp])
    dfMeanScores['mean'] = np.mean(dfMeanScores.iloc[:, 1:], axis=1)
    print(dfMeanScores.head(10))

    numOfPlots = int(np.sum([np.sum(dfMeanScores[x].sum() != 0)
                             > 0 for x in dfMeanScores.columns[1:]]))
    if numOfPlots != 0:
        fig = make_subplots(rows=numOfPlots, cols=1,
                            vertical_spacing=0.06)

        r = 1
        for n in dfMeanScores.columns[1:]:
            if np.sum(dfMeanScores[n].sum() != 0) > 0:
                fig.add_trace(go.Bar(x=dfMeanScores['product'], y=dfMeanScores[n], name=n),
                              row=r, col=1,)
                r += 1

        fig.update_layout(height=200*numOfPlots)
        fig.write_html(pathForOutput+"reviewlyzerBarPlots.html")
        with open(pathForOutput+"reviewlyzerBarPlots.html", 'r') as file:
            data = file.read()
        data = data.replace('<table border="1" class="dataframe">',
                            '<meta http-Equiv="Cache-Control" Content="no-cache" /> <meta http-Equiv="Pragma" Content="no-cache" /> <meta http-Equiv="Expires" Content="0" /> <table class="table">')
        data = data.replace("style=\"text-align: right;\"", "style=\"text-align: left;\"")
        data = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">\n' + data
        # with open("InstaSeerDf2.html", "w") as file:
        #      file.write("<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl\" crossorigin=\"anonymous\">")
        with open(pathForOutput+"reviewlyzerBarPlots.html", "w") as file:
            file.write(data)


    # Histograms
    px.histogram(dfAllScores[dfAllScores['mean'] != 0], x='mean', facet_col='keyword', facet_row='product', labels={
                 'mean': 'mean score'}).write_html(pathForOutput+"reviewlyzerHistograms.html")


    for n1 in dfAllScores['product'].unique():
        print("-"*10)
        print(n1)
        print(dfAllScores[dfAllScores['product'] == n1].groupby(by='keyword').mean())
        # input()

    dctPvalues = {'name_pair': [],
                  'keyword': [],
                  'result': [],
                  'pvalue': [],
                  'score1': [],
                  'score2': []}
    for k in dfAllScores['keyword'].unique():
        #     c+=1
        pvalues = []
        for n1 in dfAllScores['product'].unique():
            pv = []
            for n2 in dfAllScores['product'].unique():
                a = dfAllScores[(dfAllScores['product'] == n1) &
                                (dfAllScores['keyword'] == k)]['mean']
                b = dfAllScores[(dfAllScores['product'] == n2) &
                                (dfAllScores['keyword'] == k)]['mean']
                pv.append(ttest_ind(a, b, equal_var=False).pvalue)
                if n1 != n2:
                    dctPvalues['name_pair'].append(tuple(np.sort([n1, n2])))
                    dctPvalues['pvalue'].append(ttest_ind(a, b, equal_var=False).pvalue)
                    dctPvalues['keyword'].append(k)
                    score1 = np.mean(dfAllScores[(dfAllScores['product'] == n1) & (
                        dfAllScores['keyword'] == k)]['mean'])
                    score2 = np.mean(dfAllScores[(dfAllScores['product'] == n2) & (
                        dfAllScores['keyword'] == k)]['mean'])
                    dctPvalues['score1'].append(score1)
                    dctPvalues['score2'].append(score2)
                    if score1 > score2:
                        dctPvalues['result'].append(f'{n1} is better than {n2}')
                    else:
                        dctPvalues['result'].append(f'{n2} is better than {n1}')
            pvalues.append(pv)

    thresholdPvalue = 0.15  # threshold for p-values

    dfPvalues = pd.DataFrame(dctPvalues)
    dfPvaluesFilteredByThreshold = pd.DataFrame()
    for k in dfPvalues['keyword'].unique():
        dfPvaluesFilteredByThreshold = pd.concat(
            [dfPvaluesFilteredByThreshold, dfPvalues[dfPvalues['keyword'] == k].drop_duplicates(subset='name_pair')])
    dfPvaluesFilteredByThreshold = dfPvaluesFilteredByThreshold.sort_values(by='pvalue')
    dfPvaluesFilteredByThreshold = dfPvaluesFilteredByThreshold[
        dfPvaluesFilteredByThreshold['pvalue'] < thresholdPvalue]
    dfPvaluesFilteredByThreshold = dfPvaluesFilteredByThreshold.iloc[:, 1:]
    dfPvaluesFilteredByThreshold.to_html(pathForOutput+"reviewlyzerPvalues.html", index=False)


    # Adding piece of HTML for foramtting and so that it is not cached, which is necessary for reloading iframes (otherwise old file is loaded from cache)
    with open(pathForOutput+"reviewlyzerPvalues.html", 'r') as file:
        data = file.read()
    data = data.replace('<table border="1" class="dataframe">',
                        '<meta http-Equiv="Cache-Control" Content="no-cache" /> <meta http-Equiv="Pragma" Content="no-cache" /> <meta http-Equiv="Expires" Content="0" /> <table class="table">')
    data = data.replace("style=\"text-align: right;\"", "style=\"text-align: left;\"")
    data = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">\n' + data
    # with open("InstaSeerDf2.html", "w") as file:
    #      file.write("<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl\" crossorigin=\"anonymous\">")
    with open(pathForOutput+"reviewlyzerPvalues.html", "w") as file:
        file.write(data)

    f = px.box(dfAllScores, y='mean', facet_row='keyword', x='product', color='keyword')
    f.update_layout(height=150*len(dfAllScores['keyword'].unique()))
    f.write_html(pathForOutput+"reviewlyzerBoxPlots.html")

    dfMeanScoresWithImages = dfMeanScores.copy()
    images = []
    for i in dfMeanScoresWithImages['product']:
        gis = GoogleImagesSearch(api_key, cx)
        _search_params = {
            'q': i,
            'num': 1
        }
        try:
            gis.search(search_params=_search_params)
            images.append(gis.results()[0].url)
        except:
            images.append(
                "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg")
    dfMeanScoresWithImages = dfMeanScoresWithImages.reset_index()
    dfMeanScoresWithImages = dfMeanScoresWithImages.drop(columns='index')
    # your images
    colOrder = ['image']+list(dfMeanScoresWithImages.columns)
    dfMeanScoresWithImages['image'] = images

    # convert your links to html tags
    def path_to_image_html(path):
        return '<img src="' + path + '" width="200" >'

    pd.set_option('display.max_colwidth', None)
    dfMeanScoresWithImages = dfMeanScoresWithImages[colOrder]

    dfMeanScoresWithImages.to_html(pathForOutput+"reviewlyzerResults.html",
                                   escape=False, formatters=dict(image=path_to_image_html))

    # Adding piece of HTML so that it is not cached, which is necessary for reloading iframes (otherwise old file is loaded from cache)
    with open(pathForOutput+"reviewlyzerResults.html", 'r') as file:
        data = file.read()
    data = data.replace('<table border="1" class="dataframe">', '<head>\n<meta http-equiv="cache-control" content="max-age=0" />\n<meta http-equiv="cache-control" content="no-cache" />\n<meta http-equiv="expires" content="0" />\n<meta http-equiv="expires" content="Tue, 01 Jan 1980 1:00:00 GMT" />\n<meta http-equiv="pragma" content="no-cache" />\n</head>\n<table class="table">')
    data = data.replace("style=\"text-align: right;\"", "style=\"text-align: left;\"")
    data = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">\n' + data
    with open(pathForOutput+"reviewlyzerResults.html", "w") as file:
        file.write(data)

    return dfMeanScores

def convertHTMLtoPNG(folder):
    """
    The function converts html file in given folder to png images
    """
    for file in os.listdir(folder):
        if file.endswith(".html"):
            print(os.path.join(folder, file))
            print(os.path.join(folder, file.split('.')[0]+'.png'))
            hti = Html2Image()
            hti.screenshot(html_file=os.path.join(folder, file), save_as=file.split('.')[0]+'.png')

if __name__ == "__main__":
    getSetScoresText(sys.argv[1], sys.argv[2], sep=';')
