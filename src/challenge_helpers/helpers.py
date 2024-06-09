import seaborn as sns
import pandas as pd
import altair as alt


def generate_facet_plot_histogram(data, x, row, height, aspect):
    """Generates a faceted histogram plot with seaborn"""
    g = sns.FacetGrid(data, row=row, height=height, aspect=aspect)
    g.map_dataframe(sns.histplot, x=x, binwidth=1)
    g.tick_params(axis="x", rotation=45)

    return g


def generate_facet_plot_line(data, x, y, hue, row, height, aspect):
    """Generates a faceted line plot with seaborn"""
    g = sns.FacetGrid(data, row=row, height=height, aspect=aspect)
    g.map_dataframe(sns.lineplot, x=x, y=y, hue=hue)
    g.tick_params(axis="x", rotation=45)

    return g


def generate_weekly_line_plot(data):
    """Generates a faceted, interactive line chart using altair plotting library."""
    selection = alt.selection_point(encodings=["color"])
    color = alt.condition(
        selection,
        alt.Color("week:N").legend(None),
        alt.value("gray"),
    )
    opacity = alt.condition(selection, alt.value(1), alt.value(0.2))

    chart = (
        alt.Chart(data)
        .mark_line()
        .encode(
            x="weekly_ts",
            y="temperature",
            color=color,
            tooltip="week",
            opacity=opacity,
            row="property_name",
        )
        .properties(width=1000, height=300)
        .add_params(selection)
    )

    legend = (
        alt.Chart(data)
        .mark_point()
        .encode(alt.Y("week:N").axis(orient="right"), color=color)
        .add_params(selection)
        .properties(height=300)
    )

    return chart | legend


def resample_to_hours(data):
    """Groups the time series by properties week and property_name and resamples it to hourly resolution."""
    return (
        data.loc[:, ["week", "weekly_ts", "property_name", "temperature"]]
        .copy()
        .set_index(["weekly_ts"])
        .groupby(["week", "property_name"])
        .resample("1h")
        .mean()
        .reset_index()
    )


def normalize_to_start_of_week(data):
    """Adds an additional column to the dataframe that contains a time series which has year and month set to Jan 1999. The day corresponds to the weekday (0-6) of the original timestamp. The time is kept as is."""
    data["weekly_ts"] = pd.to_datetime(
        "1999-01-0"
        + (data.datetime.dt.weekday + 1).astype(str)
        + " "
        + data.datetime.dt.time.astype(str)
    )
    return data


def extract_week_number(data):
    """Adds week number of the original timeseries to the dataframe as additional column"""
    data["week"] = data.datetime.dt.isocalendar().week.astype(str)
    return data
