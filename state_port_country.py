import marimo

__generated_with = "0.10.12"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def _(pd):
    # Define the relative path to the dataset
    dataset_path = "data/state_exp_by_ports_and_countries.csv"

    # Read the dataset
    data = pd.read_csv(dataset_path)

    # Display the dataset to verify it was read correctly
    data.head()
    return data, dataset_path


@app.cell
def _(data):
    states = data['State '].unique().tolist()
    print(states)
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


if __name__ == "__main__":
    app.run()
