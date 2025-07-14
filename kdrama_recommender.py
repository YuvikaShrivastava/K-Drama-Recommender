import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import os

# Load the CSV file
df = pd.read_csv("kdramas (2).csv")
df["features"] = df["genre"] + " " + df["lead"]

# TF-IDF Model 
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["features"])

print("\n👋 Hey! Welcome to the K-Drama Recommender!🎬")
print("How would you like to search today?")
print("1. Genre\n2. Actor Name")
choice = input("Enter 1 or 2: ").strip()
recommendations = pd.DataFrame()

# Perform the search
if choice == "1":
    user_input = input("\n🎭 Enter genre: ").strip().lower()
    filtered = df[df["genre"].str.lower() == user_input]

elif choice == "2":
    user_input = input("\n⭐ Enter actor/actress name: ").strip().lower()
    filtered = df[df["lead"].str.lower().str.contains(user_input)]
else:
    print("\n❌ Invalid choice.")
    exit()

# If no results found
if filtered.empty:
    print("\n❌ Sorry! No match found.")
    see_others = input("Would you like to see dramas recommended by others? (yes/no): ").strip().lower()
    if see_others == "yes":
        if os.path.exists("user_likes.txt"):
            with open("user_likes.txt", "r") as f:
                past_likes = f.read().splitlines()
            if past_likes:
                print("\n🔥 Popular K-Dramas loved by other users:")
                most_common = Counter(past_likes).most_common(3)
                for title, count in most_common:
                    print(f"🎬 {title} ({count} votes)")
        else:
            print("\n📄 No previous user favorites found.")
        print("\n📺 Thank you! Enjoy your K-Drama marathon!💫")
    else:
        print("\n📺😢 Sorry we couldn't help you this time.")
    exit()
else:
    recommendations = filtered.sample(n=min(5, len(filtered)), random_state=None)

# Show Recommendations 
if not recommendations.empty:
    print("\n📢 Recommended K-Dramas for you:")
    print("-" * 70)
    for _, row in recommendations.iterrows():
        print(f"🎬 Title : {row['title']}")
        print(f"📅 Year  : {row['year']}")
        print(f"🎭 Genre : {row['genre']}")
        print(f"⭐ Lead  : {row['lead']}")
        print("-" * 70)

    # Ask for user recommendation 
    user_fav = input("\n🎥 Which K-Drama would you like to recommend to others? ").strip()
    with open("user_likes.txt", "a") as f:
        f.write(f"{user_fav}\n")
    print("\n💖 Thanks for sharing your recommendation!")

    # Ask to view popular k dramas recommended by th users
    see_others = input("\n👀 Would you like to see popular dramas recommended by others? (yes/no): ").strip().lower()
    if see_others == "yes":
        if os.path.exists("user_likes.txt"):
            with open("user_likes.txt", "r") as f:
                past_likes = f.read().splitlines()
            if past_likes:
                print("\n🔥Top 3 Popular K-Dramas loved by other users:")
                most_common = Counter(past_likes).most_common(3)
                for title, count in most_common:
                    print(f"🎬 {title} ({count} votes)")
        else:
            print("\n📄 No previous user favorites found.")

print("\n📺 Hope you like the recommendations. Enjoy your K-Drama marathon!💫")
