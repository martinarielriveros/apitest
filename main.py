from fastapi import FastAPI
import pandas as pd
import numpy as np

app = FastAPI()

@app.get("/")
def welcome():
    return "Simple API response for machine learning tests"

@app.get("/PlayTimeGenre/{genre}")

# Example for web testing: https://test-deploy-kvdi.onrender.com/PlayTimeGenre/Strategy
# This function returns launch year with most hours played by Gender

# Parameters:
# - genre(str): The genre you want to know from
# Return:
# - The year with most hours played

def PlayTimeGenre(genre):
           
    data = pd.read_csv('function1.csv')
    data['release_date_imputed'] = pd.to_datetime(data['release_date_imputed'])
    try:
        data_frame = data[data['tags&genres'].apply(lambda x: genre in x if pd.notna(x) else False)]
        result = data_frame.\
                                groupby(data_frame['release_date_imputed'].dt.year)['hours'].sum().\
                                reset_index().\
                                iloc[0]['release_date_imputed']
        del data, data_frame
        response = {f"Launch year with most hours played by Gender {genre}":f'{result}'}
        return response
    except:
        return {'No Genre like': f'{genre}'}

@app.get("/UserForGenre/{genre}")

# Example for web testing: https://test-deploy-kvdi.onrender.com//UserForGenre/Action

# It returns the user that has the most time played in that genre. Along with it's history.

# Parameters:
# - year(int): The year for which recommendations are sought
# Return:
# - The user_id of the player
# - dict: A dictionary with the {year:time played(in hours)}


def UserForGenre(genre:str):
    try:
        data = pd.read_parquet("function2.parquet", engine="fastparquet")
        filtered_df_by_genre = data[(~pd.isna(data['tags&genres'])) & (data['tags&genres'].str.contains(genre))] # serch for genre and no NaN
        user_most_played = filtered_df_by_genre.groupby('user_id')['playtime_forever'].sum().reset_index().\
                                                sort_values(by='playtime_forever', ascending=False).iloc[0]
        
        playtime_history_for_user_most_played = user_most_played['user_id']
        
        response = data[data['user_id']==playtime_history_for_user_most_played].groupby('year')['playtime_forever'].sum().reset_index()
        response['playtime_forever'] = round(response['playtime_forever']/60,0)
        
        final_response = response.to_dict(orient='records')
        
        del data, filtered_df_by_genre, user_most_played
        return f"The user wich most played {genre} genre is {playtime_history_for_user_most_played}", final_response
    except:
        del data, filtered_df_by_genre, user_most_played
        return f'No Genre like {genre}'


@app.get("/UsersRecommend/{year}")

# Example for web testing: https://test-deploy-kvdi.onrender.com/UsersRecommend/2018

# It returns the top 3 most recommended games of the year.
# according to the criteria:
# - recommended is True
# - reviews are neutral/positive

# Parameters:
# - year(int): The year for which recommendations are sought
# Return:
# - dict: A dictionary with the top 3 most recommended games for that year

def UsersRecommend(year:int):
        
        data = pd.read_csv('function345.csv')
        data['modified_date'] = pd.to_datetime(data['modified_date'])
        try:
            reviews_true_year = data[(data['recommend']==True) & (data['modified_date'].dt.year == year) & (data['sentiment_analisys']>=1)]
            result = reviews_true_year.groupby('item_id').\
                                                agg({
                                                    'sentiment_analisys': 'sum',
                                                    'app_name&title': 'first'
                                                }).\
                                        reset_index()
            response = result.sort_values(by='sentiment_analisys', ascending=False).iloc[[0, 1, 2]]['app_name&title']
            del data, reviews_true_year, result
            return [{
                    "Puesto 1": response.iloc[0],
                    "Puesto 2": response.iloc[1],
                    "Puesto 3": response.iloc[2]
                    }]
        except:
                return {'No matching combination reviews.recommend = True & comments neutral/positive for the year': f'{year}'}

@app.get("/UsersNotRecommend/{year}")

# Example for web testing: https://test-deploy-kvdi.onrender.com/UsersNotRecommend/2015

# It returns the top 3 most unrecommended games of the year.
# according to the criteria:
# - recommended is False
# - reviews are negative

# Parameters:
# - year(int): The year for which recommendations are sought
# Return:
# - dict: A dictionary with the top 3 most unrecommended games for that year

def UsersNotRecommend(year:int):
        
        data = pd.read_csv('function345.csv')
        data['modified_date'] = pd.to_datetime(data['modified_date'])
        try:
            reviews_true_year = data[(data['recommend']==False) & (data['modified_date'].dt.year == year) & (data['sentiment_analisys']==0)]
            result = reviews_true_year.groupby('item_id').\
                                                agg({
                                                    'sentiment_analisys': 'sum',
                                                    'app_name&title': 'first'
                                                }).\
                                        reset_index()
            response = result.sort_values(by='sentiment_analisys', ascending=True).iloc[[0, 1, 2]]['app_name&title']
            del data, reviews_true_year, result
            return [{
                    "Puesto 1": response.iloc[0],
                    "Puesto 2": response.iloc[1],
                    "Puesto 3": response.iloc[2]
                    }]
        except:
                return {'No matching combination reviews.recommend = False & comments negative for the year': f'{year}'}
        
@app.get("/sentiment_analysis/{year}")

# Example for web testing: https://test-deploy-kvdi.onrender.com/sentiment_analysis/2015

# It returns a list with total user reviews categorized by sentiment analisys (Negative, Neutral and Positive) for a given year

# Parameters:
# - year(int): The year for which recommendations were issued
# Return:
# - dict: A dictionary with the 3 categories for that year

def sentiment_analysis(year:int):

    try:
        data = pd.read_csv('function345.csv')    
        data['modified_date'] = pd.to_datetime(data['modified_date'])
        year_condition = data[data['modified_date'].dt.year==year]

        reviews = year_condition.groupby('sentiment_analisys')['user_id'].count().reset_index()
        return [{
                "negative":reviews.iloc[0]['user_id'].tolist(),
                "neutral":reviews.iloc[1]['user_id'].tolist(),
                "positive":reviews.iloc[2]['user_id'].tolist()
                }]
    except:
            return {'No reviews for year': f'{year}'}

@app.get("/game_recommendation/{item_id}")

# Example for web testing: https://test-deploy-kvdi.onrender.com/game_recommendation/754120

# It returns the name of the game searched, and a list of 5 similar games to that game.

# Parameters:
# - item_id(int): The id of the game to match
# Return:
# - The queried item_id game name
# - dict: A dictionary with the 5 similar games names

def game_recommendation(item_id:int):
    
    from sklearn.metrics.pairwise import cosine_similarity
    data = pd.read_parquet("recommendfunc1.parquet", engine="fastparquet")
    data['item_id'] = data['item_id'].astype(int)
    games_names_df = pd.read_csv('item_id&name.csv')

    try:
        if data['item_id'].isin([item_id]).any():
            
            # Calculates the cosine similarity between the selected game (item_id) and
            # all other games in the data DataFrame. The result is stored in the 'similarity' variable.
            
            selected_item = data[data['item_id'] == item_id][data.columns[2:]]
            features_columns = data[data.columns[2:]]
            similarity = cosine_similarity(selected_item[data.columns[2:]], features_columns)

            # Get the indices of the top 6 similar items (we include the first for complete response)
            
            similar_items_indices = np.argsort(similarity[0])[::-1][0:6]
                
            # Extract 'item_ids' of the top 6 similar items
            
            top_6_similar_items = data.loc[similar_items_indices, 'item_id'].tolist()
            
            # Create a Categorical data type with the desired order. This data type is used to represent categorical data with a specified order.

            order = pd.CategoricalDtype(top_6_similar_items, ordered=True)

            # converting the 'item_id' column in the DataFrame (games_names_df) to the Categorical data type created.
            # This step is crucial for ensuring that subsequent operations take into account the desired order of the categories.

            games_names_df['item_id'] = games_names_df['item_id'].astype(order)

            # Filter the DataFrame based on the 'item_id' values in top_6_similar_items

            response = games_names_df[games_names_df['item_id'].isin(top_6_similar_items)].sort_values(by='item_id').reset_index(drop=True)
            
            objective_game = response.iloc[0]['app_name&title']
            similar_games = response.iloc[1:]['app_name&title']

            return f"Games similar to {objective_game} are:", similar_games
    except:
            return {f'No item_id like {item_id}'}

@app.get("/user_recommendation/{user_id}")

# Example for web testing: https://test-deploy-kvdi.onrender.com/user_recommendation/76561198068270286

# It returns the name of the games the user_id would like.

# Parameters:
# - user_id(str): The id user to match
# Return:
# - dict: A dictionary with the 5 recommended games for that user

def user_recommendation(user_id:str):
    
    from sklearn.metrics.pairwise import cosine_similarity
    data = pd.read_parquet("recommendfunc1.parquet", engine="fastparquet")
    user_data = pd.read_csv("recommendfunc2.csv")

    item_id = user_data.loc[user_data['user_id'] == user_id, 'item_id'].values[0]


    data['item_id'] = data['item_id'].astype(int)
    games_names_df = pd.read_csv('item_id&name.csv')

    try:
        if data['item_id'].isin([item_id]).any():
            
            # Calculates the cosine similarity between the selected game (item_id) and
            # all other games in the data DataFrame. The result is stored in the 'similarity' variable.
            
            selected_item = data[data['item_id'] == item_id][data.columns[2:]]
            features_columns = data[data.columns[2:]]
            similarity = cosine_similarity(selected_item[data.columns[2:]], features_columns)

            # Get the indices of the top 5 recommended games
            
            similar_items_indices = np.argsort(similarity[0])[::-1][0:5]
                
            # Extract 'item_ids' of the top 5 recommended games
            
            top_5_recommended_games = data.loc[similar_items_indices, 'item_id'].tolist()
            
            # Create a Categorical data type with the desired order. This data type is used to represent categorical data with a specified order.

            order = pd.CategoricalDtype(top_5_recommended_games, ordered=True)

            # converting the 'item_id' column in the DataFrame (games_names_df) to the Categorical data type created.
            # This step is crucial for ensuring that subsequent operations take into account the desired order of the categories.

            games_names_df['item_id'] = games_names_df['item_id'].astype(order)

            # Filter the DataFrame based on the 'item_id' values in top_5_recommended_games

            response = games_names_df[games_names_df['item_id'].isin(top_5_recommended_games)].sort_values(by='item_id').reset_index(drop=True)
            print(response)

            return f"Games {user_id} would like are:", response['app_name&title']
    except:
            return {f'No user_id like {user_id}'}