from fastapi import FastAPI
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

app = FastAPI()

@app.get("/")
def welcome():
    return "Simple API response for machine learning tests"

@app.get("/UserForGenre/{genre}")

def UserForGenre(genre:str):
    data = pd.read_parquet("function2.parquet", engine="pyarrow")
    data['release_date_imputed'] = pd.to_datetime(data['release_date_imputed'], format='%Y-%m-%d', errors='coerce')
    data['year'] = data['release_date_imputed'].dt.year # keep the year, drop the rest.
    data.drop('release_date_imputed', axis=1, inplace=True) # drop previous date column
    filtered_df_by_genre = data[(~pd.isna(data['tags&genres'])) & (data['tags&genres'].str.contains(genre))] # serch for genre and no NaN
    del data
    # user_most_played = filtered_df_by_genre.groupby('user_id')['playtime_forever'].sum().reset_index().sort_values(by='playtime_forever', ascending=False).iloc[0]
    # playtime_history_for_user_most_played = user_most_played['user_id']
    # response = filtered_df_by_genre[filtered_df_by_genre['user_id']==playtime_history_for_user_most_played].groupby('year')['playtime_forever'].sum().reset_index()
    # response['playtime_forever'] = round(response['playtime_forever']/60,0)
    # change_column_names_to_spanish = {'year': 'anio', 'playtime_forever': 'horas'}
    # response.rename(columns=change_column_names_to_spanish, inplace=True)
    # final_response = response.to_json(orient='records', lines=True)
    return "test ok"

@app.get("/PlayTimeGenre/{genre}") # The value of the path parameter 'genre' will be passed to your function as the argument 'genre'.

# Example for web testing: https://test-deploy-kvdi.onrender.com/PlayTimeGenre/Strategy

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
        
        data = pd.read_csv('function3and4.csv')
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
        
        data = pd.read_csv('function3and4.csv')
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

def sentiment_analysis(year:int):

# Example for web testing: https://test-deploy-kvdi.onrender.com/sentiment_analysis/2015

# It returns a list with total user reviews categorized by sentiment analisys (Negative, Neutral and Positive) for a given year

# Parameters:
# - year(int): The year for which recommendations were issued
# Return:
# - dict: A dictionary with the 3 categories for that year


    data = pd.read_csv('function3and4.csv')    
    data['modified_date'] = pd.to_datetime(data['modified_date'])
    year_condition = data[data['modified_date'].dt.year==year]

    reviews = year_condition.groupby('sentiment_analisys')['user_id'].count().reset_index()
    return {
            "negative"  : reviews['user_id'].iloc[0],
            "neutral"   : reviews['user_id'].iloc[1],
            "positive"  : reviews['user_id'].iloc[2]
            }