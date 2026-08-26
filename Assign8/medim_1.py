POSITIVE = ["good", "great", "excellent", "love", "fast", "perfect"] 
NEGATIVE = ["bad", "terrible", "slow", "broken", "waste", "poor"] 

verdict = {
    "positive": 0,
    "negative": 0,
    "neutral": 0
}

reviews = [ 
    "excellent product I love it", 
    "terrible quality broken on arrival", 
    "delivery was fast but packaging was bad", 
    "good value great battery excellent screen", 
    "what a waste poor build slow delivery", 
    "oh great just great it broke in one day", 
] 

print("--- Keyword Sentiment Analyzer (rule-based illustration, NOT real ML) ---")

def score_review(count_1,count_2):
    strength="STRONG" if abs(count_1-count_2)>=3 else "MILD"


    if count_1>count_2:
        verdict["positive"]+=1
        
        return(f"[POSITIVE]  +{count_1} -{count_2} |{strength}")

    
    elif count_2>count_1:
        verdict["negative"]+=1
       
        return(f"[NEGATIVE] +{count_1}  -{count_2}| {strength}")

    else :
        verdict["neutral"]+=1
        return (f"[NEUTRAL] +{count_1}  -{count_2}| {strength}")

for data in reviews:
        
    count_1=0
    count_2=0

    for word in POSITIVE:
        if word in data.lower():
            count_1+=1

    for word in NEGATIVE:
        if word in data.lower():
            count_2+=1

    print(score_review(count_1,count_2),data)
print()
print(f"Summary: {verdict} ")

    