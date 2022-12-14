import time
import json

with open('idfDictionary.json') as json_file:
    idf_dictionary = json.load(json_file)

with open('invertedIndex.json') as json_file:
    inverted_index = json.load(json_file)

with open('wordsCollection.json') as json_file:
    words_collection = json.load(json_file)

with open('docNameLength.json') as json_file:
    doc_name_len = json.load(json_file)

for item in doc_name_len:
    if len(item) == 0:
        doc_name_len.remove(item)

# Calculate the avergae length of the files

from gensim.parsing.preprocessing import STOPWORDS

total_words = 0

for val in words_collection.values():
    total_words += val

total_docs = len(doc_name_len)

avgFieldLen = total_words / total_docs


def calc_bm25(query):
    tokens = query.split()
    result_dict = {}

    fqid = []
    ranking = []
    result_dict = {}

    for token in tokens:

        # check if the word is in the inverted index
        if token not in inverted_index or token in STOPWORDS:
            continue

        if token in inverted_index:
            files_containing_token = []
            for key, values in inverted_index[token].items():
                files_containing_token.append(key)

                fqid.append(values)

            index = 0
            for file in files_containing_token:

                fieldLen = doc_name_len[file]

                bm25 = idf_dictionary[token] * (
                            (fqid[index] * 2.2) / (fqid[index] + 1.2 * (0.25 + 0.75 * (fieldLen / avgFieldLen))))

                if file in result_dict.keys():
                    result_dict[file] += bm25
                else:
                    result_dict[file] = bm25
                index += 1

    return result_dict


query = input("Enter the search query: ")
start_time = time.time()
result = calc_bm25(query)
if len(result) == 0:
    print("No results found")

else:
    print("\nBelow are the documents that contain the entered keywords:\n")

    sort_result = sorted(result.items(), key=lambda x: x[1], reverse=True)

    for i in sort_result:
        print(i[0])
print("--- %s seconds ---" % (time.time() - start_time))
