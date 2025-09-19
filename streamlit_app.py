#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from matplotlib import cm
from plotly.subplots import make_subplots
#######################
# Page configuration
st.set_page_config(
    page_title="The Rise and Fall of Somali Pirates",
    page_icon=":pirate_flag:",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# Hide Streamlit's Menu and Footer
st.markdown(
    """
    <style>
    /* Hide the three-dot menu */
    [data-testid="stToolbar"] {
        visibility: hidden;
        height: 0;
    }

    /* Hide the footer */
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)


#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


#######################
# Load data
# df_reshaped = pd.read_csv('data/us-population-2010-2019-reshaped.csv')

def load_pirate_data():
    url1 = 'https://github.com/newzealandpaul/Maritime-Pirate-Attacks/blob/main/data/csv/pirate_attacks.csv?raw=true'
    url2 = 'https://github.com/newzealandpaul/Maritime-Pirate-Attacks/blob/main/data/csv/country_indicators.csv?raw=true'
    url3 = 'https://github.com/newzealandpaul/Maritime-Pirate-Attacks/blob/main/data/csv/country_codes.csv?raw=true'

    pirate_attacks = pd.read_csv(url1)
    # country_indicators = pd.read_csv(url2)
    country_codes = pd.read_csv(url3)
    
    # Preprocessing
    pirate_attacks['date'] = pd.to_datetime(pirate_attacks['date'], errors='coerce')
    pirate_attacks = pirate_attacks.dropna(subset=['longitude', 'latitude', 'date'])
    pirate_attacks['year'] = pirate_attacks['date'].dt.year
    pirate_attacks = pirate_attacks[(pirate_attacks['year'] >= 1994) & (pirate_attacks['year'] <= 2020)]
    x= "Boarded"
    y= "Boarding"
    pirate_attacks['attack_type'] = pirate_attacks['attack_type'].replace(x, y)
    pirate_attacks['vessel_type'] = pirate_attacks['vessel_type'].fillna("Unknown")
    pirate_attacks['shore_distance'] = np.round(pirate_attacks['shore_distance'].astype(float), 2).astype(str) + ' kms'
    # pirate_attacks['attack_type'].unique()
    # Replace NaNs in nearest_country with "Unknown"
    pirate_attacks['nearest_country'] = pirate_attacks['nearest_country'].fillna("Unknown")
    return pirate_attacks,country_codes

# @st.cache
def load_ransom_data():
    ransom_data = pd.DataFrame({
        'year': [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
        'low_estimate': [1.57, 0.39, 1.03, 7.05, 20.20, 32.68, 84.42, 36.35],
        'high_estimate': [2.00, 0.40, 1.50, 8.00, 25.00, 57.16, 151.10, 40.39]
    })
    ransom_data['average_ransom'] = ransom_data[['low_estimate', 'high_estimate']].mean(axis=1)
    return ransom_data

pirate_attacks, country_codes = load_pirate_data()
ransom_data = load_ransom_data()

somalia_geojson = {
        "type": "Feature",
        "properties": {
            "name": "Somalia",
            "code": "SOM",
            "group": "Countries"
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        49.72862,
                        11.5789
                    ],
                    [
                        50.25878,
                        11.67957
                    ],
                    [
                        50.73202,
                        12.0219
                    ],
                    [
                        51.1112,
                        12.02464
                    ],
                    [
                        51.13387,
                        11.74815
                    ],
                    [
                        51.04153,
                        11.16651
                    ],
                    [
                        51.04531,
                        10.6409
                    ],
                    [
                        50.83418,
                        10.27972
                    ],
                    [
                        50.55239,
                        9.19874
                    ],
                    [
                        50.07092,
                        8.08173
                    ],
                    [
                        49.4527,
                        6.80466
                    ],
                    [
                        48.59455,
                        5.33911
                    ],
                    [
                        47.74079,
                        4.2194
                    ],
                    [
                        46.56476,
                        2.85529
                    ],
                    [
                        45.56399,
                        2.04576
                    ],
                    [
                        44.06815,
                        1.05283
                    ],
                    [
                        43.13597,
                        0.2922
                    ],
                    [
                        42.04157,
                        -0.91916
                    ],
                    [
                        41.81095,
                        -1.44647
                    ],
                    [
                        41.58513,
                        -1.68325
                    ],
                    [
                        40.993,
                        -0.85829
                    ],
                    [
                        40.98105,
                        2.78452
                    ],
                    [
                        41.855083,
                        3.918912
                    ],
                    [
                        42.12861,
                        4.23413
                    ],
                    [
                        42.76967,
                        4.25259
                    ],
                    [
                        43.66087,
                        4.95755
                    ],
                    [
                        44.9636,
                        5.00162
                    ],
                    [
                        47.78942,
                        8.003
                    ],
                    [
                        48.486736,
                        8.837626
                    ],
                    [
                        48.93813,
                        9.451749
                    ],
                    [
                        48.938233,
                        9.9735
                    ],
                    [
                        48.938491,
                        10.982327
                    ],
                    [
                        48.942005,
                        11.394266
                    ],
                    [
                        48.948205,
                        11.410617
                    ],
                    [
                        49.26776,
                        11.43033
                    ],
                    [
                        49.72862,
                        11.5789
                    ]
                ]
            ]
        },
        "_id": "somalia"
    }

custom_region_mapping = {
            "China": "South China Sea",
            "Philippines": "South China Sea",
            "Cambodia": "South China Sea",
            "Vietnam": "South China Sea",
            "Angola": "West Africa",
            "Nigeria": "West Africa",
            "Korea, Rep.": "South China Sea",
            "Pakistan": "Arabian Sea",
            "Indonesia": "Malacca Strait",
            "Brazil": "Latin America & Caribbean",
            "Japan": "South China Sea",
            "Malaysia": "Malacca Strait",
            "Sri Lanka": "Indian Ocean",
            "Colombia": "Latin America & Caribbean",
            "Congo, Dem. Rep.": "West Africa",
            "Guyana": "Latin America & Caribbean",
            "Bangladesh": "Indian Ocean",
            "Egypt, Arab Rep.": "Mediterranean Sea",
            "Jamaica": "Latin America & Caribbean",
            "Senegal": "West Africa",
            "Côte d'Ivoire": "West Africa",
            "Papua New Guinea": "South China Sea",
            "Ecuador": "Latin America & Caribbean",
            "Iran, Islamic Rep.": "Arabian Sea",
            "Russian Federation": "North Atlantic",
            "Panama": "Latin America & Caribbean",
            "Algeria": "Mediterranean Sea",
            "Turkey": "Mediterranean Sea",
            "Thailand": "South China Sea",
            "Denmark": "North Atlantic",
            "India": "Indian Ocean",
            "Peru": "Latin America & Caribbean",
            "Italy": "Mediterranean Sea",
            "Guinea": "West Africa",
            "Gabon": "West Africa",
            "Uruguay": "Latin America & Caribbean",
            "Dominican Republic": "Latin America & Caribbean",
            "Ghana": "West Africa",
            "Greece": "Mediterranean Sea",
            "Sierra Leone": "West Africa",
            "Georgia": "Mediterranean Sea",
            "Cameroon": "West Africa",
            "Myanmar": "South China Sea",
            "Albania": "Mediterranean Sea",
            "Netherlands": "North Atlantic",
            "Portugal": "Mediterranean Sea",
            "Venezuela, RB": "Latin America & Caribbean",
            "United States": "North Atlantic",
            "Solomon Islands": "South China Sea",
            "Malta": "Mediterranean Sea",
            "Singapore": "Malacca Strait",
            "France": "Mediterranean Sea",
            "Morocco": "Mediterranean Sea",
            "Mexico": "Latin America & Caribbean",
            "Guinea-Bissau": "West Africa",
            "Oman": "Arabian Sea",
            "Haiti": "Latin America & Caribbean",
            "Honduras": "Latin America & Caribbean",
            "Belize": "Latin America & Caribbean",
            "Mauritania": "West Africa",
            "Togo": "West Africa",
            "South Africa": "West Africa",
            "Equatorial Guinea": "West Africa",
            "Congo, Rep.": "West Africa",
            "São Tomé and Principe": "West Africa",
            "Trinidad and Tobago": "Latin America & Caribbean",
            "Saudi Arabia": "Arabian Sea",
            "Iraq": "Arabian Sea",
            "Bulgaria": "Mediterranean Sea",
            "United Kingdom": "North Atlantic",
            "El Salvador": "Latin America & Caribbean",
            "Costa Rica": "Latin America & Caribbean",
            "Gambia, The": "West Africa",
            "Cuba": "Latin America & Caribbean",
            "Liberia": "West Africa",
            "Barbados": "Latin America & Caribbean",
            "St. Lucia": "Latin America & Caribbean",
            "Australia": "North Atlantic",
            "Benin": "West Africa",
            "Grenada": "Latin America & Caribbean",
            "United Arab Emirates": "Arabian Sea",
            "Argentina": "Latin America & Caribbean",
            "Suriname": "Latin America & Caribbean",
            "Mauritius": "Indian Ocean",
            "Kazakhstan": "North Atlantic",
            "Maldives": "Indian Ocean",
            "Guatemala": "Latin America & Caribbean",
            "Canada": "North Atlantic",
            "Mozambique": "East Africa/Somalia",
            "Kenya": "East Africa/Somalia",
            "Eritrea": "East Africa/Somalia",
            "Yemen, Rep.": "East Africa/Somalia",
            "Madagascar": "East Africa/Somalia",
            "Djibouti": "East Africa/Somalia",
            "Somalia": "East Africa/Somalia",
            "Tanzania": "East Africa/Somalia",
            "Sudan": "East Africa/Somalia",
            "Seychelles": "East Africa/Somalia",
        }

    # Function to map countries to desired regions

def assign_custom_region(row):
    # Check country_name against the mapping
    if row['country_name'] in custom_region_mapping:
        return custom_region_mapping[row['country_name']]
    # Default to existing broader region or Unknown Region
    return "Unknown Region"

def get_incidentCounts():
    # Merge country codes to get region information
    merged_data = pd.merge(
        pirate_attacks,
        country_codes[['country_name', 'region','country']],
        left_on='nearest_country',
        right_on='country',
        how='left'
    )
    # Apply the custom mapping to assign desired regions
    merged_data['desired_region'] = merged_data.apply(assign_custom_region, axis=1)
    merged_data['desired_region'] = merged_data['desired_region'].replace("Unknown Region", "Other")

    # Group data by the desired regions and year
    desired_region_trends = merged_data.groupby(['desired_region', 'year']).size().reset_index(name='incident_count')

    # Calculate the total incidents per year
    total_incidents_per_year = desired_region_trends.groupby('year')['incident_count'].sum().reset_index(name='total_incidents')

    # Merge total incidents back with the desired region trends
    desired_region_trends = pd.merge(
        desired_region_trends,
        total_incidents_per_year,
        on='year',
        how='left'
    )

    # Calculate the percentage for each region in a given year
    desired_region_trends['percentage'] = (desired_region_trends['incident_count'] / desired_region_trends['total_incidents']) * 100

    # Replace NaN percentages with 0 for years where a region has no incidents
    desired_region_trends['percentage'] = desired_region_trends['percentage'].fillna(0)

    # Calculate all-years statistics
    all_years_stats = merged_data.groupby('desired_region').size().reset_index(name='incident_count')
    total_incidents = all_years_stats['incident_count'].sum()
    all_years_stats['total_incidents'] = total_incidents
    all_years_stats['percentage'] = (all_years_stats['incident_count'] / total_incidents) * 100
    all_years_stats['year'] = 'All Years'  # Add year column with 'All Years'

    # Combine year-wise and all-years statistics
    final_trends = pd.concat([desired_region_trends, all_years_stats], ignore_index=True)
    
    return final_trends

st.title('Somalia Pirate Attacks Dashboard '+":pirate_flag:"+" :ship:")
    
year_list = list(pirate_attacks.year.unique())
attack_types = pirate_attacks['attack_type'].unique() # need this as a variable

# with col[1]:
st.markdown('#### The Rise and Fall of Somali Pirates')
# Consistent color mapping for attack types using Viridis
attack_types = list(pirate_attacks['attack_type'].unique())
attack_types = ['unknown' if pd.isna(x) else x for x in attack_types]
color_palette = px.colors.sequential.Viridis  # Use Viridis for a uniform, colorblind-friendly palette
attack_colors = {attack: color_palette[i % len(color_palette)] for i, attack in enumerate(attack_types)}

# Ensure all attack types are represented for every year
all_years = pirate_attacks['year'].unique()
all_attack_types = pirate_attacks['attack_type'].unique()
full_combinations = pd.MultiIndex.from_product(
    [all_years, all_attack_types], names=["year", "attack_type"]
).to_frame(index=False)

# Merge with the dataset to include all combinations
pirate_attacks_full = pd.merge(
    full_combinations,
    pirate_attacks,
    on=["year", "attack_type"],
    how="left"
)

# # Fill missing data for visualization purposes
pirate_attacks_full['date'] = pirate_attacks_full['date'].fillna(pd.Timestamp("1990-01-01"))

# Slightly jitter coordinates to handle overlaps
pirate_attacks_full['latitude'] += np.random.uniform(-0.05, 0.05, pirate_attacks_full.shape[0])
pirate_attacks_full['longitude'] += np.random.uniform(-0.05, 0.05, pirate_attacks_full.shape[0])

# Generate perceptually uniform colors from Viridis palette
viridis = cm.get_cmap('plasma', len(all_attack_types))
color_scale = {attack_type: f"rgba({int(viridis(i)[0]*255)}, {int(viridis(i)[1]*255)}, {int(viridis(i)[2]*255)}, 1)"
            for i, attack_type in enumerate(all_attack_types)}

# Dynamically check for optional columns
hover_data = {"date": True, "attack_type": True}
if 'location_description' in pirate_attacks_full.columns:
    hover_data["location_description"] = True
if 'vessel_type' in pirate_attacks_full.columns:
    hover_data["vessel_type"] = True
if 'shore_distance' in pirate_attacks_full.columns:
    hover_data["shore_distance"] = True

region_percentages = get_incidentCounts()

def generate_pie_chart_data(year):
    # year_data = region_percentages[region_percentages['year'] == year]
    # top_3 = year_data.nlargest(7, 'percentage')
    # other_percentage = 100 - top_3['percentage'].sum()
    # pie_data = pd.concat([
    #     top_3[['desired_region', 'percentage']],
    #     pd.DataFrame({'desired_region': ['Others'], 'percentage': [other_percentage]})
    # ], ignore_index=True)
    if 'year' == 'All Years':
        year_data = region_percentages[region_percentages['year'] == 'All Years']
    else:
        year_data = region_percentages[region_percentages['year'] == year]
    return year_data[['desired_region', 'percentage']].copy()
    # return pie_data

region_colors = {
    "East Africa/Somalia": "#F47C7C",  # Muted Blue
    "Indian Ocean": "#93C2C6",        # Soft Cyan
    "Malacca Strait": "#F1E14B",      # Muted Yellow
    "South China Sea": "#A37B73",     # Muted Brown-Red
    "West Africa": "#B3729F",         # Muted Purple
    "Latin America & Caribbean": "#8FB46A",  # Muted Green
    "Mediterranean Sea": "#B4C5E4",   # Soft Blue
    "Others": "#D3B6E0",              # Muted Pink
    "Other": "#D3B6E0",               # Same as "Others"
    "North Atlantic": "#EBB387",      # Muted Orange
    "Arabian Sea": "#2C728E"          # Muted Red
}

# Create figure with subplots
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "pie"}, {"type": "mapbox"}]],
    column_widths=[0.3, 0.7],
)

# Add initial pie chart
initial_pie_data = generate_pie_chart_data('All Years')
fig.add_trace(
    go.Pie(
        labels=initial_pie_data['desired_region'],
        values=initial_pie_data['percentage'],
        textinfo='percent+label',
        # textposition='inside',  # Keep text inside
        insidetextorientation='radial',  # Orient text radially
        pull=[0.1 if r == "East Africa/Somalia" else 0 for r in initial_pie_data['desired_region']],
        marker_colors=[region_colors[region] for region in initial_pie_data['desired_region']],
        hole=0.4,  # Add a hole to make more space for labels
        showlegend=False,
        textfont=dict(
                size=13,  # Larger font size for better visibility
                color="black",  # White text for contrast
                family="Arial"  # Optional: Use a clean, sans-serif font
        ),
        # scalegroup='one',
        texttemplate="%{label}<br>%{percent}",
        # For values less than 5%, use outside labels with lines
        textposition=["outside" if v < 5 else "inside" for v in initial_pie_data['percentage']]
    ),
    row=1, col=1
)

# Add separate traces for each attack type
for attack_type in attack_types:
    fig.add_trace(
        go.Scattermapbox(
            lat=pirate_attacks_full[pirate_attacks_full['attack_type'] == attack_type]['latitude'],
            lon=pirate_attacks_full[pirate_attacks_full['attack_type'] == attack_type]['longitude'],
            mode='markers',
            marker=dict(
                size=10,
                color=attack_colors[attack_type],
                opacity=0.7
            ),
            text=pirate_attacks_full[pirate_attacks_full['attack_type'] == attack_type]['location_description'],
            hoverinfo='text',
            name=attack_type,
            showlegend=True,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>" +
                "Date: %{customdata[1]|%Y-%m-%d}<br>"+
                "Attack Type: %{customdata[2]}<br>" +
                "Vessel Type: %{customdata[3]}<br>" +
                "Shore Distance: %{customdata[4]}<extra></extra>"
            ),
            customdata=np.column_stack((
                pirate_attacks_full[pirate_attacks_full['attack_type'] == attack_type]['location_description'],
                pd.to_datetime(pirate_attacks_full[pirate_attacks_full['attack_type'] == attack_type]['date']).dt.strftime('%Y-%m-%d'),
                pirate_attacks_full[pirate_attacks_full['attack_type'] == attack_type]['attack_type'],
                pirate_attacks_full[pirate_attacks_full['attack_type'] == attack_type]['vessel_type'],
                pirate_attacks_full[pirate_attacks_full['attack_type'] == attack_type]['shore_distance']
            ))
        ),
        row=1, col=2
    )

# Add Somalia highlight
fig.add_trace(
    go.Choroplethmapbox(
        geojson=somalia_geojson,
        locations=["Somalia"],
        featureidkey="properties.name",
        z=[1],
        colorscale=[[0, "rgba(255, 165, 0, 0.5)"], [1, "rgba(255, 165, 0, 0.5)"]],
        showscale=False,
        marker_line_width=2,
        marker_line_color="red",
        showlegend=False
    ),
    row=1, col=2
)
# Create frames for animation
frames = []
for year in sorted(pirate_attacks_full['year'].unique()):
    year_data = pirate_attacks_full[pirate_attacks_full['year'] == year]
    # year_data
    pie_data = generate_pie_chart_data(year)
    
    frame_data = [
        go.Pie(
            labels=pie_data['desired_region'],
            values=pie_data['percentage'],
            textinfo='percent+label',
            # textposition='inside',
            insidetextorientation='radial',
            pull=[0.1 if r == "East Africa/Somalia" else 0 for r in pie_data['desired_region']],
            marker_colors=[region_colors[region] for region in pie_data['desired_region']],
            showlegend=False,
            hole=0.4,
            texttemplate="%{label}<br>%{percent}",
            # For values less than 5%, use outside labels with lines
            textposition=["outside" if v < 5 else "inside" for v in pie_data['percentage']]
        ),
    ]
    
    # Add traces for each attack type
    for attack_type in attack_types:
        frame_data.append(
            go.Scattermapbox(
                lat=year_data[year_data['attack_type'] == attack_type]['latitude'],
                lon=year_data[year_data['attack_type'] == attack_type]['longitude'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=attack_colors[attack_type],
                    opacity=0.7
                ),
                text=year_data[year_data['attack_type'] == attack_type]['location_description'],
                hoverinfo='text',
                name=attack_type,
                showlegend=True,
                hovertemplate=(
                "<b>%{customdata[0]}</b><br>" +
                "Date: %{customdata[1]|%Y-%m-%d}<br>" +
                "Attack Type: %{customdata[2]}<br>" +
                "Vessel Type: %{customdata[3]}<br>" +
                "Shore Distance: %{customdata[4]}<extra></extra>"
            ),
            customdata=np.column_stack((
                year_data['location_description'],
                pd.to_datetime(year_data['date']).dt.strftime('%Y-%m-%d'),  # Format date,
                year_data['attack_type'],
                year_data['vessel_type'],
                year_data['shore_distance']
            )),
            )
        )
    
    frame_data.append(
        go.Choroplethmapbox(
            geojson=somalia_geojson,
            locations=["Somalia"],
            featureidkey="properties.name",
            z=[1],
            colorscale=[[0, "rgba(255, 165, 0, 0.5)"], [1, "rgba(255, 165, 0, 0.5)"]],
            showscale=False,
            marker_line_width=2,
            marker_line_color="red",
            showlegend=False
        )
    )
    
    frames.append(go.Frame(data=frame_data, name=str(year)))

fig.frames = frames

# Update layout
fig.update_layout(
    title="",
    mapbox=dict(
        style="carto-positron",
        center=dict(lat=5, lon=47),
        zoom=2.25
    ),
    height=800,
    width=1200,
    showlegend=True,
    sliders=[dict(
        active=0,
        currentvalue={"prefix": "Year: "},
        pad={"t": 50},
        steps=[dict(
            method="animate",
            args=[[str(year)], {
                "frame": {"duration": 500, "redraw": True},
                "mode": "immediate",
                "transition": {"duration": 300}
            }],
            label=str(year)
        ) for year in sorted(pirate_attacks_full['year'].unique())]
    )],
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        buttons=[
            dict(label="▶️",
                 method="animate",
                 args=[None, {"frame": {"duration": 500, "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 300}}]),
            dict(label="⏸️",
                 method="animate",
                 args=[[None], {"frame": {"duration": 0, "redraw": False},
                              "mode": "immediate",
                              "transition": {"duration": 0}}]),
            dict(label="🔄",
                 method="animate",
                 args=[["1994"], {"frame": {"duration": 0, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 0}}])
        ],
        direction="left",
        pad={"r": 10, "t": 8},
        x=0.1,
        xanchor="right",
        y=0,
        yanchor="top"
    )],
    margin=dict(r=10, t=50, l=10, b=10),
    legend_title_text="Attack Type",
    # Add fixed annotations for titles
    annotations=[
        dict(
            text="Global Pirate Activity Distribution: 1994-2020",
            x=0.03,
            y=0.85,
            showarrow=False,
            font=dict(size=16,color="black",  # White text for contrast
                family="Arial",weight="bold"),
            xref='paper',
            yref='paper'
        ),
        dict(
            text="Geospatial Distribution of Pirate Attacks (1994-2020)",
            x=0.85,
            y=1.05,
            showarrow=False,
            font=dict(size=16,color="black",  # White text for contrast
                family="Arial",weight="bold"),
            xref='paper',
            yref='paper'
        ),
    ]
)

# Dynamically update the frame layout to reflect the year
for frame in frames:
    year = frame.name
    frame.layout = dict(
        annotations=[
            dict(
                text="Global Pirate Activity Distribution"+f" Year: {year}",
                x=0.03,
                y=0.85,
                showarrow=False,
                font=dict(size=16,color="black",  # White text for contrast
                family="Arial",weight="bold"),
                xref="paper",
                yref="paper"
            ),
            dict(
                text=f"Geospatial Distribution of Pirate Attacks: {year}",
                x=0.85,
                y=1.05,
                showarrow=False,
                font=dict(size=16,color="black",  # White text for contrast
                family="Arial",weight="bold"),
                xref="paper",
                yref="paper"
            ),
        ]
    )

# Assign frames to the figure
fig.frames = frames

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)


st.write("")
# st.markdown("<h4 style='text-align: center; color: black;'>No of Piracy Incidents per Year </h4>", unsafe_allow_html=True)


# Define a custom color mapping for regions
region_colors = {
    "East Africa/Somalia": "#FF0000",  # Bright red
    "Indian Ocean": "#1E90FF",  # Dodger blue
    "Arabian Sea": "#2C728E",  # Cyan (bright aqua)
    "Latin America & Caribbean": "#32CD32",  # Lime green
    "Malacca Strait": "#FF69B4",  # Hot pink
    "Mediterranean Sea": "#8A2BE2",  # Blue violet
    "North Atlantic": "#B3729F",  # Bright gold
    "Other": "#696969",  # Dim gray
    "South China Sea": "#FF8C00",  # Dark orange
    "West Africa": "#A37B73"  # Lawn green
}

final_trends = get_incidentCounts()
final_trends = final_trends[final_trends['year'] != 'All Years']

# Create the line chart with custom colors
fig_desired_regions = px.line(
    final_trends,
    x='year',
    y='incident_count',
    color='desired_region',
    title='Number of Piracy Incidents per year across regions (1994-2020)',
    labels={'year': 'Year', 'incident_count': 'Number of Incidents', 'desired_region': 'Region'},
    markers=True,
    color_discrete_map=region_colors,  # Apply custom colors
    height=500
)

# Highlight East Africa for emphasis
fig_desired_regions.for_each_trace(lambda trace: trace.update(
    line=dict(width=4, dash='solid') if trace.name == 'East Africa/Somalia' else dict(width=2, dash='dot'),
    opacity=1.0 if trace.name == 'East Africa/Somalia' else 0.9,
    marker=dict(size=8) if trace.name == 'East Africa/Somalia' else dict(size=6)
))

# Update layout for better readability
fig_desired_regions.update_layout(
    title="Annual Trends in Piracy Incidents by Region (1994-2020)",
    xaxis_title='Year',
    yaxis_title='Number of Incidents',
    template='plotly_white',
    legend_title="Region",
    font=dict(size=25),
    title_x=0.30
)

# Display the plot
st.plotly_chart(fig_desired_regions, use_container_width=True)


    
cols = st.columns((0.3,1,0.3))

with cols[1]:
    # Combined chart: Average Ransom Line + Ransom Amounts Bar Chart
    fig_combined = go.Figure()

    # Add bar chart for high/low ransom estimates
    fig_combined.add_trace(go.Bar(
        x=ransom_data['year'],
        y=ransom_data['low_estimate'],
        name='Low Estimate',
        marker_color='blue',
        opacity=0.7
    ))
    fig_combined.add_trace(go.Bar(
        x=ransom_data['year'],
        y=ransom_data['high_estimate'],
        name='High Estimate',
        marker_color='orange',
        opacity=0.7
    ))

    # Add line chart for average ransom
    fig_combined.add_trace(go.Scatter(
        x=ransom_data['year'],
        y=ransom_data['average_ransom'],
        mode='lines+markers',
        name='Average Ransom',
        line=dict(color='green', width=3),
        marker=dict(size=8)
    ))

    # Update layout
    fig_combined.update_layout(
        title='Trends in Ransom Collections by Somali Pirates (2005-2012)',
        xaxis_title='Year',
        yaxis_title='Ransom Amount (US$ millions)',
        barmode='group',  # Grouped bar chart
        template='plotly_white',
        legend_title="Ransom Type",
        height=500,
        width=1000,
        font=dict(size=25),
        title_x=0.20
    )
    st.plotly_chart(fig_combined, use_container_width=False)  # Set use_container_width to False


st.markdown(
    """
    ---
    ### Reasons for the Rise of Somali Piracy  
    - **1991 - No Government Control**: Somalia’s government **collapsed in 1991**, leaving no one to enforce laws.  
    - **1990s-2000s - Foreign Fishing**: **Illegal fishing vessels** stole fish from Somali waters, leaving locals with **no catch, income, or food**, pushing them towards desperation.  
    - **1990s-2000s - Extreme Poverty and Hunger**: With **no fishing income** and **no government support**, many Somali people faced **extreme poverty**, turning to piracy to survive.  
    - **2004 - Toxic Waste Dumping**: The **2004 tsunami** washed up toxic waste dumped off Somalia’s coast, **contaminating land and water** and causing severe health problems.  
    - **2005 - Warlord Backing**: Local **warlords funded pirates** with boats, weapons, and supplies in exchange for a share of **ransom money**, as piracy became lucrative.  
    - **2007-2011 - Organized Crime**: Piracy became highly **profitable**, attracting **organized crime** with advanced tactics and million-dollar ransom demands.  
    - **2009 - Pirate Stock Market**: A **pirate stock market** let locals **invest in hijackings**, earning shares of **ransoms** if missions succeeded.  
    """,
    unsafe_allow_html=True
)


# Add a summary at the bottom of the dashboard
st.markdown(
    """
    ---
    ### Reasons for the Fall of Somali Piracy  
    - **2011 - Naval Patrols**: Countries like the **U.S., Russia, and European nations** deployed **naval forces** to patrol Somali waters, escorting cargo ships and deterring pirate attacks.  
    - **2011 - Armed Security on Ships**: Shipping companies began hiring **armed guards** to protect vessels, making pirate attacks **riskier and less successful**.  
    - **2011 - Secure Shipping Corridors**: An **international shipping corridor** was created where cargo ships **traveled together under naval protection**, reducing pirates' chances of success.  
    - **2011 - Advanced Ship Defenses**: Ships were equipped with **barbed wire, water cannons, and surveillance systems**, making them **harder to board**.  
    - **2011-2013 - Global Awareness and Pressure**: High-profile **hijackings** involving Westerners, such as the **U.S. Navy SEAL rescue** in *Captain Phillips*, drew **global attention**, prompting stricter **security policies and legal actions** against pirates.  
    """,
    unsafe_allow_html=True
)


# Add source link to the bottom-right corner
st.markdown(
    """
    <style>
    .source-link {
        position: fixed;
        bottom: 10px;
        right: 10px;
        font-size: 14px;
        color: #1E90FF;
        text-decoration: none;
        background-color: rgba(255, 255, 255, 0.8);
        padding: 5px 10px;
        border-radius: 5px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    <a class="source-link" href="https://github.com/newzealandpaul/Maritime-Pirate-Attacks" target="_blank">
        Source: Maritime Pirate Attacks Dataset
    </a>
    """,
    unsafe_allow_html=True
)

with st.container():
    st.write("")
    st.write("")
    # st.markdown('<span style="font-size:30px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> Thank You. </span>', unsafe_allow_html=True)
    st.markdown('<span style="font-size:15px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> Developed by [Ravi Teja Rajavarapu](mailto:rrajavar@iu.edu), [Achu Jeeju](mailto:achujeej@iu.edu), [Sai Charan Reddy Kotha](mailto:saikotha@iu.edu) </span>', unsafe_allow_html=True)
