import marimo

__generated_with = "0.10.12"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def _(mo):
    mo.md(r"""Basic data exploration to see if things are properly read or not""")
    return


@app.cell
def _(pd):
    # Load the CSV file
    file_path = "data/dist_exports_am24.csv"
    data = pd.read_csv(file_path)
    return data, file_path


@app.cell
def _(data):
    # Display the first few rows
    print(data.head())
    return


@app.cell
def _(data):
    data.shape
    return


@app.cell
def _(data):
    data.columns
    return


@app.cell
def _(data):
    # Drop unnecessary columns and rename the remaining ones
    data_cleaned = data.drop(columns=['March, 24 Value(INR)', 'March, 24 Value(US $)'])

    # Rename columns
    data_cleaned = data_cleaned.rename(columns={
        'HS Code': 'HS6',
        'Commodity Description': 'Commodity',
        'April, 23 To March, 24 Value(INR)': 'AM24_INR',
        'April, 23 To March, 24 Value(US $)': 'AM24_USD'
    })

    # Display the updated DataFrame
    print(data_cleaned.head())

    return (data_cleaned,)


@app.cell
def _(data_cleaned):
    # Count rows where AM24_USD is less than 100
    rows_less_than_100 = data_cleaned[data_cleaned['AM24_USD'] < 100].shape[0]

    print(f"Number of rows where AM24_USD is less than 100: {rows_less_than_100}")

    return (rows_less_than_100,)


@app.cell
def _(data_cleaned):
    # Group by Port and calculate the sum of AM24_USD
    port_grouped = data_cleaned.groupby('Port', as_index=False)['AM24_USD'].sum()

    # Sort the result in descending order by AM24_USD
    port_grouped_sorted = port_grouped.sort_values(by='AM24_USD', ascending=False)

    # Display the sorted result
    port_grouped_sorted.head(20)

    return port_grouped, port_grouped_sorted


@app.cell
def _(data_cleaned):
    data_cleaned.columns
    return


@app.cell
def _(data_cleaned):
    # Aggregate exports based on State, Port, and Country
    state_exports = data_cleaned.groupby(['State ', 'Port', 'Country'], as_index=False)[['AM24_INR', 'AM24_USD']].sum()

    # Save the new DataFrame to a CSV file
    state_exports.to_csv("data/state_exp_by_ports_and_countries.csv", index=False)

    print("New DataFrame saved as 'data/state_exports_summary.csv'")

    return (state_exports,)


@app.cell
def _(state_exports):
    state_exports.head()

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
