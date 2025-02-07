import folium
import pandas as pd
import numpy as np
import os

def parse_coordinates(coord_str):
    try:
        coord_str = coord_str.strip('()')
        coords = coord_str.split(',')
        lat = float(coords[0].replace('np.float64(', '').strip(')'))
        lon = float(coords[1].replace('np.float64(', '').strip(')'))
        return (lat, lon)
    except Exception as e:
        print(f"Error parsing coordinates: {coord_str}")
        print(f"Error details: {e}")
        return None

def create_map_visualization(file_path, percentage_file_path, output_path='map.html'):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find the Excel file at: {file_path}")
        
    if not os.path.exists(percentage_file_path):
        raise FileNotFoundError(f"Could not find the percentage file at: {percentage_file_path}")

    df = pd.read_excel(file_path)
    percentages_df = pd.read_excel(percentage_file_path)

    print(f"Processing {len(df)} rows of data from address pairs...")
    print("Column names in the address pairs Excel file:", df.columns.tolist())
    
    print(f"Processing {len(percentages_df)} rows of data from percentage file...")
    print("Column names in the percentage Excel file:", percentages_df.columns.tolist())

    df['address1_coords'] = df['Address 1'].apply(parse_coordinates)
    df['address2_coords'] = df['Address 2'].apply(parse_coordinates)
    
    df = df.dropna(subset=['address1_coords', 'address2_coords'])
    print(f"Successfully parsed coordinates for {len(df)} rows")
    
    if len(df) == 0:
        raise ValueError("No valid coordinate pairs found after parsing")
    
    all_coordinates = df['address1_coords'].tolist() + df['address2_coords'].tolist()
    all_lats = [coords[0] for coords in all_coordinates if coords is not None]
    all_lons = [coords[1] for coords in all_coordinates if coords is not None]
    
    if not all_lats or not all_lons:
        raise ValueError("No valid coordinates found to create the map")
    
    center_lat = sum(all_lats) / len(all_lats)
    center_lon = sum(all_lons) / len(all_lons)
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
    
    fg = folium.FeatureGroup(name="Address Pairs")
    
    for idx, row in df.iterrows():
        address1_coords = row['address1_coords']
        address2_coords = row['address2_coords']

        lat1, lon1 = address1_coords
        lat2, lon2 = address2_coords

        percentage1 = percentages_df[
            (percentages_df['lat'] == lat1) & (percentages_df['lng'] == lon1)
        ]['percentage'].values

        percentage2 = percentages_df[
            (percentages_df['lat'] == lat2) & (percentages_df['lng'] == lon2)
        ]['percentage'].values
        
        percentage1_value = percentage1[0] if len(percentage1) > 0 else 'N/A'
        percentage2_value = percentage2[0] if len(percentage2) > 0 else 'N/A'
        
        icon1 = folium.DivIcon(
            html=f"""<div style="font-size: 8px; color: red; background-color: white; border-radius: 50%; width: 20px; height: 20px; text-align: center; line-height: 20px; border: 1px solid red;">{percentage1_value}%</div>"""
        )

        icon2 = folium.DivIcon(
            html=f"""<div style="font-size: 8px; color: red; background-color: white; border-radius: 50%; width: 20px; height: 20px; text-align: center; line-height: 20px; border: 1px solid red;">{percentage2_value}%</div>"""
        )

        folium.Marker(location=address1_coords, icon=icon1).add_to(fg)
        folium.Marker(location=address2_coords, icon=icon2).add_to(fg)

        line_coordinates = [address1_coords, address2_coords]
        folium.PolyLine(
            locations=line_coordinates,
            weight=2,
            color='gray',
            opacity=0.8,
            tooltip=f"Distance: {row['Distance (km)']:.1f} km\nPercentage Difference: {row['Percentage Difference (%)']:.1f}%"
        ).add_to(fg)

    fg.add_to(m)
    
    folium.LayerControl().add_to(m)
    
    m.save(output_path)
    print(f"Map visualization saved to {output_path}")
    print(f"Total pairs visualized: {len(df)}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "close_address_pairs_with_high_percentage_difference.xlsx")
    percentage_file_path = os.path.join(current_dir, "2024_parliamentary_round_1_proportional_electronic.xlsx")
    output_path = os.path.join(current_dir, "map.html")
    
    try:
        create_map_visualization(file_path, percentage_file_path, output_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease make sure your Excel file is in the correct location and named correctly.")
        print(f"Looking for file at: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        print("\nDetailed error information:")
        print(traceback.format_exc())
        
        try:
            df = pd.read_excel(file_path)
            print("\nData overview:")
            print(f"Total rows: {len(df)}")
            print("\nColumn names:")
            print(df.columns.tolist())
        except Exception as e:
            print(f"Could not read Excel file for debugging: {e}")
