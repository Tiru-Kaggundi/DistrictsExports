import marimo

__generated_with = "0.10.12"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def _(mo, pd):
    # Correct way to load the CSV
    try: 
        dataset_path = mo.notebook_location() / "state_exp_by_ports_and_countries.csv"
        data = pd.read_csv(dataset_path)
        print("Columns loaded:", data.columns.tolist())  # Debug column names
    except:
        print(f"Error loading CSV: {e}")
        raise
    # # Define the relative path to the dataset
    # dataset_path = "state_exp_by_ports_and_countries.csv"

    # # Read the dataset
    # data = pd.read_csv(dataset_path)
    # Convert AM24_USD to millions and AM24_INR to crores
    data['AM24_USD_million'] = (data['AM24_USD'] / 1_000_000).round(2)  # Convert to USD million
    data['AM24_INR_Cr'] = (data['AM24_INR'] / 10_000_000).round(2)  # Convert to INR crore

    # Drop the old columns as they are no longer needed
    data = data.drop(columns=['AM24_USD', 'AM24_INR'])

    # Display the dataset to verify it was read correctly
    #data.head()
    return data, dataset_path


@app.cell
def _():
    #data.columns
    return


@app.cell
def _(data):
    states = data['State '].unique().tolist()
    return (states,)


@app.cell
def _(mo, states):
    # Create a dropdown for selecting a state
    state_dropdown = mo.ui.dropdown(label="Select State", options=states, value=states[0])
    state_dropdown
    return (state_dropdown,)


@app.cell
def _(state_dropdown):
    f'state selected is {state_dropdown.value}'
    return


@app.cell
def _(mo):
    options = ["Export destinations with values", "Top Ports of Exports from the State", "Total Exports from the state"]
    radio = mo.ui.radio(options=options)
    return options, radio


@app.cell
def _(mo, radio):
    mo.hstack([radio, mo.md(f"Selected option: {radio.value}")])
    return


@app.cell
def _(mo):
    mo.md(r"""We will create the first visualisation for when the "Top Ports of Exports from the state" is selected in radio button above""")
    return


@app.cell
def _(data, radio, state_dropdown):
    # Function to filter data and create the top 15 ports DataFrame
    def update_table():
        if radio.value == "Top Ports of Exports from the State":
            selected_state = state_dropdown.value
            # Filter data for the selected state
            filtered_data = data[data['State '] == selected_state]

            # Aggregate export values by port and sort in descending order
            port_exports = (
                filtered_data.groupby('Port', as_index=False)
                .agg({"AM24_USD_million": "sum"})
                .sort_values(by="AM24_USD_million", ascending=False)
                .head(15)  # Get top 15 ports
            )

            # Return the top 20 ports DataFrame
            return port_exports.reset_index(drop=True)
        else:
            return None

    # Get the resulting table and display it
    result_table = update_table()
    result_table
    return result_table, update_table


@app.cell
def _(data, radio, state_dropdown):
    # Function to filter data and create the top 15 countries DataFrame
    def update_table_country():
        if radio.value == "Export destinations with values":
            selected_state = state_dropdown.value
            # Filter data for the selected state
            filtered_data = data[data['State '] == selected_state]

            # Aggregate export values by country and sort in descending order
            country_exports = (
                filtered_data.groupby('Country', as_index=False)
                .agg({"AM24_USD_million": "sum"})
                .sort_values(by="AM24_USD_million", ascending=False)
                .head(15)  # Get top 15 countries
            )

            # Return the top 15 countries DataFrame
            return country_exports.reset_index(drop=True)
        else:
            return None

    # Get the resulting table and display it
    result_table_country = update_table_country()
    result_table_country
    return result_table_country, update_table_country


@app.cell
def _(data, radio, state_dropdown):
    # Function to calculate total exports and return text
    def update_table_total():
        if radio.value == "Total Exports from the state":
            selected_state = state_dropdown.value
            # Filter data for the selected state
            filtered_data = data[data['State '] == selected_state]

            # Calculate total exports in INR and USD
            total_inr = filtered_data['AM24_INR_Cr'].sum()
            total_usd = filtered_data['AM24_USD_million'].sum()

            # Return the result as text
            return f"### Total Exports from {selected_state}\n- **INR:** {total_inr:.1f} Crore\n- **USD:** {total_usd:.1f} Million"
        else:
            return None

    # Get the resulting text and display it
    result_text = update_table_total()
    result_text

    return result_text, update_table_total


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
