import pandas as pd
from math import radians, cos, sin, acos

file_path = '2024_parliamentary_round_1_proportional_electronic.xlsx'
df = pd.read_excel(file_path)
proximity_threshold_km = 1 
percentage_diff_threshold = 10 

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    cos_angle = cos(lat1) * cos(lat2) * cos(lon1 - lon2) + sin(lat1) * sin(lat2)
    cos_angle = max(-1, min(1, cos_angle)) 

    return R * acos(cos_angle)

close_pairs = []

for i in range(len(df)):
    for j in range(i + 1, len(df)):
        lat1, lon1, pct1 = df.loc[i, 'lat'], df.loc[i, 'lng'], df.loc[i, 'percentage']
        lat2, lon2, pct2 = df.loc[j, 'lat'], df.loc[j, 'lng'], df.loc[j, 'percentage']

        address1_1 = df.loc[i, 'address_1']
        address1_2 = df.loc[i, 'address_2']
        address1_3 = df.loc[i, 'address_3']
        address2_1 = df.loc[j, 'address_1']
        address2_2 = df.loc[j, 'address_2']
        address2_3 = df.loc[j, 'address_3']
        
        distance = haversine(lat1, lon1, lat2, lon2)
        pct_diff = abs(pct1 - pct2) * 100

        if distance <= proximity_threshold_km and pct_diff >= percentage_diff_threshold:
            close_pairs.append({
                'Address 1': (lat1, lon1),
                'Address 2': (lat2, lon2),
                'Distance (km)': distance,
                'Percentage Difference (%)': pct_diff,
                'Percentage 1': pct1 * 100, 
                'Percentage 2': pct2 * 100,
                'Address 1 - Part 1': address1_1,
                'Address 1 - Part 2': address1_2,
                'Address 1 - Part 3': address1_3,
                'Address 2 - Part 1': address2_1,
                'Address 2 - Part 2': address2_2,
                'Address 2 - Part 3': address2_3
            })

results_df = pd.DataFrame(close_pairs)

output_path = 'close_address_pairs_with_high_percentage_difference.xlsx'
results_df.to_excel(output_path, index=False)

print(f'Results saved to {output_path}')