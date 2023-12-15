# Individual Project 1 - ML_Ops

What follows are the results for [Henry's](https://henry.com) Proyecto Individual N1. Please go [here](https://github.com/soyHenry/PI_ML_OPS/tree/PT) to check for requirements and understand the main goal to achieve.

The project was made in three big stages.

- The ETL/EDA of data
- Functions programmig
- Github [upload](https://github.com/martinarielriveros/PI_MLops) and [Render](https://render.com) deploy

I'll go briefly on each to highlight some issues i found. For exact step by step you can go to [this repository](https://github.com/martinarielriveros/PI_MLops).

# ETL/EDA

The original dataset on what we were asked to work was Steam-Games dataset. We performed some common manipulation, although no explicitly required on this stage. We used the extended *Pandas / Seaborn / Matplotlib* to perform mostly all what follows.

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

We also stored some [*light-data*](https://github.com/martinarielriveros/PI_MLops/tree/main/light_data) that are used by required functions of the project. This was done this way, beacuse cloud memory deploy was restricted for free users. More on this ahead.

# Functions programmig

We were asked to develop 5 functions to be exectuded via API. The recommended web framework for building the API was [FastAPI](https://fastapi.tiangolo.com/), and we followed the suggestion.

As you can see functions are fairly straight, but an issue araised regarding the size of the dataset needed to run one particular function. The **`.csv`** (after merged) file was more than 1GB long, so there was no chance to upload to [GitHub](https://github.com/martinarielriveros/PI_MLops) or deploy on [Render](https://render.com).

The solution found was:

- Perform info drops as it was not needed to be used *by that paticular function*.
- Upload the dataset in **`.parquet`** format.

The drawback to the **`.parquet`** compression is that when performing that particular request, the time waiting for the server response can take up to 10 seconds. We can discuss if this is the correct approach, but i found no other solution **with no info loss** .

The endpoints are gatherd up here:

https://test-deploy-kvdi.onrender.com/docs

<p align="center">
    <img src="https://github.com/martinarielriveros/PI_MLops/images/Endpoints.png" width="60%">
</p>

Each endpoint can be tested by opening the arrow down at the far right on each. Inside, the type of data needed to be passed as **/params** are shown.

<p align="center">
    <img src=".https://github.com/martinarielriveros/PI_MLops/images/images/OneEndpoint.png">
</p>

Finally, press **Try Out** to launch the request.