# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 22:31:44 2020

@author: Kerem's Laptop
"""

import pandas as pd
from selenium import webdriver
import spacy

executable_path = "chromedriver"


def spacy_sm_magazine_scraper(text, number):
    # Part 1 for Spectrum IEEE
    driver = webdriver.Chrome(executable_path)
    spectrum_dict = []
    driver.get(f"https://spectrum.ieee.org/searchContent?q={text}")
    driver.implicitly_wait(10)
    search = driver.find_elements_by_class_name("article-title")
    for words in search:
        spectrum_dict.append(words.text)
    spectrum = pd.Series(spectrum_dict)
    spectlabel = ['IEEE'] * len(spectrum)
    spectforlabel = pd.Series(spectlabel)
    finalspectlabel = pd.concat([spectrum, spectforlabel], axis=1)
    finalspectlabel = finalspectlabel.head(number)
    driver.close()

    # Part 2 for Popular Science
    driver2 = webdriver.Chrome(executable_path)
    popular_dict = []
    driver2.get(f"https://www.popsci.com/search-results/{text}/")
    driver2.implicitly_wait(10)
    search2 = driver2.find_elements_by_class_name("siq-partner-result")
    for words2 in search2:
        popular_dict.append(words2.text)
    popular = pd.Series(popular_dict)
    poplabel = ['PopScience'] * len(popular)
    popforlabel = pd.Series(poplabel)
    finalpoplabel = pd.concat([popular, popforlabel], axis=1)
    finalpoplabel = finalpoplabel.head(number)
    driver2.close()

    # Part 3 for Wired
    driver3 = webdriver.Chrome(executable_path=executable_path)
    wired_dict = []
    driver3.get("https://www.wired.com/search/?q=" + text + "&page=1&sort=score")
    search3 = driver3.find_elements_by_class_name("archive-item-component__title")
    for words3 in search3:
        wired_dict.append(words3.text)
    wired = pd.Series(wired_dict)
    wiredlabel = ['Wired'] * len(wired)
    wiredforlabel = pd.Series(wiredlabel)
    finalwiredlabel = pd.concat([wired, wiredforlabel], axis=1)
    finalwiredlabel = finalwiredlabel.head(number)
    driver3.close()

    # Part 4 for Scientific American
    driver4 = webdriver.Chrome(executable_path=executable_path)
    sciamerican_dict = []
    driver4.get("https://www.scientificamerican.com/search/?q=" + text)
    search4 = driver4.find_elements_by_class_name("listing__title")
    for words4 in search4:
        sciamerican_dict.append(words4.text)
    sciamerican = pd.Series(sciamerican_dict)
    sciamericanlabel = ['Scientific American'] * len(sciamerican)
    sciamericanforlabel = pd.Series(sciamericanlabel)
    finalsciamericanlabel = pd.concat([sciamerican, sciamericanforlabel], axis=1)
    finalsciamericanlabel = finalsciamericanlabel.head(number)
    driver4.close()

    # Part 5 for Science Mag
    driver5 = webdriver.Chrome(executable_path=executable_path)
    scimag_dict = []
    driver5.get("https://search.sciencemag.org/?searchTerm=" + text + "&order=tfidf&limit=textFields&pageSize=10&&")
    driver5.implicitly_wait(10)
    search5 = driver5.find_elements_by_class_name("media__headline")
    for words5 in search5:
        scimag_dict.append(words5.text)
    scimag = pd.Series(scimag_dict)
    scimaglabel = ['Science Mag'] * len(scimag)
    scimagforlabel = pd.Series(scimaglabel)
    finalscimaglabel = pd.concat([scimag, scimagforlabel], axis=1)
    finalscimaglabel = finalscimaglabel.head(number)
    driver5.close()

    # Part 6 for MIT
    driver6 = webdriver.Chrome(executable_path=executable_path)
    mit_dict = []
    driver6.get("https://www.technologyreview.com/search/?s=" + text)
    driver6.implicitly_wait(10)
    search6 = driver6.find_elements_by_class_name("teaserItem__title--32O7a")
    for words6 in search6:
        mit_dict.append(words6.text)
    mit = pd.Series(mit_dict)
    mitlabel = ['MIT Tech Review'] * len(mit)
    mitforlabel = pd.Series(mitlabel)
    finalmitlabel = pd.concat([mit, mitforlabel], axis=1)
    finalmitlabel = finalmitlabel.head(number)
    driver6.close()

    # Part 7 for American Scientist
    driver7 = webdriver.Chrome(executable_path=executable_path)
    america_dict = []
    driver7.get("https://www.americanscientist.org/search/node/" + text)
    driver7.implicitly_wait(10)
    search7 = driver7.find_elements_by_class_name("title")
    for words7 in search7:
        america_dict.append(words7.text)
    america = pd.Series(america_dict)
    americalabel = ['American Scientist'] * len(america)
    americaforlabel = pd.Series(americalabel)
    finalamericalabel = pd.concat([america, americaforlabel], axis=1)
    finalamericalabel = finalamericalabel.head(number)
    driver7.close()

    # Part 8 for New Scientist
    driver8 = webdriver.Chrome(executable_path=executable_path)
    newish_dict = []
    driver8.get("https://www.newscientist.com/search/?q=" + text)
    search8 = driver8.find_elements_by_class_name("card__heading")
    for words8 in search8:
        newish_dict.append(words8.text)
    newish = pd.Series(newish_dict)
    newishlabel = ['New Scientist'] * len(newish)
    newishforlabel = pd.Series(newishlabel)
    finalnewishlabel = pd.concat([newish, newishforlabel], axis=1)
    finalnewishlabel = finalnewishlabel.head(number)
    driver8.close()

    # Part 9 for ScienceNews
    driver9 = webdriver.Chrome(executable_path=executable_path)
    scinew_dict = []
    driver9.get("https://www.sciencenews.org/?s=" + text)
    search9 = driver9.find_elements_by_class_name("post-item-river__title___J3spU")
    for words9 in search9:
        scinew_dict.append(words9.text)
    scinew = pd.Series(scinew_dict)
    scinewlabel = ['ScienceNews'] * len(scinew)
    scinewforlabel = pd.Series(scinewlabel)
    finalscinewlabel = pd.concat([scinew, scinewforlabel], axis=1)
    finalscinewlabel = finalscinewlabel.head(number)
    driver9.close()

    # Combine Part 1, Part 2, and Part 3
    frames = [finalspectlabel, finalpoplabel, finalwiredlabel, finalsciamericanlabel, finalscimaglabel, finalmitlabel,
              finalamericalabel, finalnewishlabel, finalscinewlabel]
    result = pd.concat(frames)
    result.columns = ["Text", "Type"]

    # NER tool
    def ner(x):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(x)
        textually = []
        tags = []
        for ent in doc.ents:
            textually.append(ent.text)
            tags.append(ent.label_)
        spacy_dictionary = dict(zip(textually, tags))
        good_terms = []
        for key in spacy_dictionary:
            if spacy_dictionary[key] == "ORG":
                good_terms.append(key)
            if spacy_dictionary[key] == "GPE":
                good_terms.append(key)
            if spacy_dictionary[key] == "LOC":
                good_terms.append(key)
            if spacy_dictionary[key] == "PRODUCT":
                good_terms.append(key)
            if spacy_dictionary[key] == "DATE":
                good_terms.append(key)
            if ("PRODUCT" not in spacy_dictionary.values()) and ("ORG" not in spacy_dictionary.values()):
                good_terms.clear()
        return good_terms

    result['NER Model'] = result['Text'].apply(ner)
    return result
