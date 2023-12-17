# Individual Project 1 - ML_Ops

What follows are the results for [Henry's](https://soyhenry.com) Proyecto Individual N1. Please go [here](https://github.com/soyHenry/PI_ML_OPS/tree/PT) to check for requirements and understand the main goal to achieve.

The project was made in four big stages.

- The ETL/EDA of data
- Functions programmig
- Github [upload](https://github.com/martinarielriveros/PI_MLops) and [Render](https://render.com) deploy
- Machine Learning models - Render deploy

I'll go briefly on each to highlight some issues i found. For exact step by step you can go to [this repository](https://github.com/martinarielriveros/PI_MLops).

# ETL/EDA

The original dataset we were asked to work on was Steam-Games dataset. We performed some common manipulation, although no explicitly required on this stage. We used the extended *Pandas / Seaborn / Matplotlib* to perform mostly all what follows.

- Load compressed data.
- Manage all/some NaN rows/cols.
- Erase duplicates rows.
- Correct data entry ambiguities.
- *"No Price"* policy correction.
- Columns renames (for datasets matching).
- Types conversions.
- Filling missing information (other columns and *KNN Imputing*).
- Date-Time and Year conversion.
- Dataframes merging.
- Dataframes grouping, sorting and trimming.
- Users defined dataframes function appliance.
- Cell's list extraction.
- Basic graphic info plots.

We also stored some [*light-data*](https://github.com/martinarielriveros/PI_MLops/tree/main/light_data) that are used by required functions of the project. This was done this way, because cloud memory deploy was restricted for free users. More on this ahead.

# Functions programmig

We were asked to develop 5 functions to be exectuded via API. The recommended web framework for building the API was [FastAPI](https://fastapi.tiangolo.com/), and i followed the suggestion.

As you can see [here](https://github.com/martinarielriveros/apitest/blob/main/main.py), functions are fairly straight, but an issue araised regarding the size of the dataset needed to run one particular function. To run the function defined as **`def UserForGenre(genre:str):`**, the **`.csv`** file that was needed to query the info was more than 1.1 Gb, so there was no chance to upload to [GitHub](https://github.com/martinarielriveros/PI_MLops) or deploy on [Render](https://render.com).

The solution found was:

- Perform info drops as it was not needed to be used *by that paticular function*.
- Upload the dataset in **`.parquet`** format.

The drawback to the **`.parquet`** compression is that when that particular request is sent, the server response can take up to 15 seconds. We can discuss if this is the correct approach, but i found no other solution **with no info loss** . So be aware, **wait a little bit on this one**.

The endpoints are gatherd up here: https://test-deploy-kvdi.onrender.com/docs



<p align="center">
    <img src=images/Endpoints.png width=50%>
</p>

Each endpoint can be tested by opening the arrow down at the far right. Inside, the type of data needed to be passed as **`/params`** is shown.

<p align="center">
    <img src=images/OneEndpoint.png width=80%>
</p>

Finally, press **`Try it Out`** to send the request.

Server responses are shown like this:

<p align="center">
    <img src=images/ServerResponseSample.png width=50%>
</p>

# Github upload and Render deploy

Here i found no problems after taking into account issue stated above about the file size to run one particular function. To be more clear about what it is done and future modifications on repository, i divided the project in two.

- [First](https://github.com/martinarielriveros/apitest) repository has just what is needed for Render to work.
- [Second](https://github.com/martinarielriveros/PI_MLops) repository is a copy of that one, **plus** all ETL/EDA, original files, and other resorces.

<p align="center">
    <img src=images/DeployDashboard.png width=80%>
</p>


The steps to achieve the deploy were:

- Create the First Repository
- Create a virtual environment for dependencies (just the relevants to the project). This was *ignored* in repos.
- *Freeze* them into **`requirements.txt`**, so Render can *build* it.
- **In Render**: Create a Web Service, link the first repository, grant Access, set working Branch, set Runtime, set Built pip command, start uvicorn command, etc. All is done in the config Render page.

The Auto-Deploy is enabled, so each commit to the First repo triggers a new deploy.


<p align="center">
    <img src=images/AutoDeploy.png width=50%>
</p>

Finally, the **service is live**:

<p align="center">
    <img src=images/DeployLogs.png width=80%>
</p>

# Machine Learning models - Render deploy

We were asked to develop 2 ML recommendation algorithms to be exectuded via API. The recommended algorithm was **cosine similarity**, i also followed the suggestion.

You can check [this file]() for a step by step output with comments.

- First recommendation consists of a *5-item-set* similar to the **`/item-id`** param sent in the request:

https://test-deploy-kvdi.onrender.com/game_recommendation/item_id

The response is like:

<p align="center">
    <img src=images/ServerResponseML1.png width=80%>
</p>

You can also, as before, test all endpoints listed here: https://test-deploy-kvdi.onrender.com/docs