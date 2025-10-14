import matplotlib.pyplot as plt
import seaborn as sns
import pandas



dataframes = [pandas.read_csv("amazon.csv"), pandas.read_csv("microsoft.csv")]
questions = pandas.concat(dataframes)


#outputs a map of [question concept] -> question count
def generateConceptToQuestionCount(questions:pandas.DataFrame):
    
    questionCount = {}

    for row in questions.iterrows():

        topics = row[1]["Topics"].split(", ")
        addTopicsToMap(topics, questionCount)
    
    return questionCount


#Adds all the questions to the topics
def addTopicsToMap(topics, questionCount:dict):
    for topic in topics:
        if topic not in questionCount:
            questionCount[topic] = 1
        else:
            questionCount[topic] += 1
    


questionCount = generateConceptToQuestionCount(questions)

print(questionCount)

def getMinTopic(merged:dict):

    smallest = "Array"

    for key in merged:
        if merged[key] <= merged[smallest]:
            smallest = key

    return smallest


def mergeOthers(merged, questionCount):

    merged["Others"] = 0

    for key in questionCount:

        if(key not in merged.keys()):
            merged["Others"] += questionCount[key]
    

#returns a new merged map
def merge(questionCount:dict, num):
    merged = {}
    minTopic = ""

    for key in questionCount.keys():
        if minTopic == "":
            minTopic = key
            merged[key] = questionCount[key]
        elif len(merged) < num:
            if merged[minTopic] > questionCount[key]:
                minTopic = key
            merged[key] = questionCount[key]
        elif len(merged) >= num:
            if questionCount[key] > merged[minTopic]:
                merged.pop(minTopic)
                merged[key] = questionCount[key]
                minTopic = getMinTopic(merged)
    

    mergeOthers(merged, questionCount)
    return merged

def updateLabelsAndData(labels, data, questionCount):

    for key in questionCount.keys():
        labels.append(key)
        data.append(questionCount[key])


def displayPiChart(questionCount:dict):

    labels = []
    data = []
    updateLabelsAndData(labels, data, questionCount)
    sns.set_style("darkgrid")
    plt.pie(data, labels=labels)

    # Add title
    plt.title("Distribution of Leet Code Questions by Concept At Amazon")

    # Show plot
    plt.show()

merged = merge(questionCount, 15)
print("number of concepts: " + str(len(questionCount)))
print("\n")
print(merged)
displayPiChart(merged)


    
    