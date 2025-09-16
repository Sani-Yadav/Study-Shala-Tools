"""
ISRO Satellite Tracker
=====================
A professional application to track ISRO satellites in real-time.
"""

import webbrowser
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import folium
from skyfield.api import load, wgs84, EarthSatellite
from skyfield.timelib import Time
import pytz

# Constants
# Using a different TLE source that includes ISRO satellites
TLE_SOURCES = [
    "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle",
    "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
]
MAP_OUTPUT_FILE = "isro_satellites.html"

# ISRO satellite NORAD IDs (manually added for better tracking)
ISRO_SATELLITES = {
    'CARTOSAT-1': '28649',
    'CARTOSAT-2': '29710',
    'CARTOSAT-3': '44804',
    'OCEANSAT-2': '35931',
    'RESOURCESAT-2': '37387',
    'GSAT-30': '45026',
    'GSAT-31': '44056',
    'IRNSS-1I': '43286',
    'GSAT-7A': '43868',
    'RISAT-2B': '44238',
    'EMISAT': '44078',
    'CHANDRAYAAN-2': '44441',
    'RISAT-2BR1': '44878',
    'GSAT-30': '45026',
    'EOS-01': '46607',
    'AMAZONIA-1': '47699',
    'EOS-04': '51450',
    'EOS-06': '54234',
    'SSLV-D2': '55990',
    'CHANDRAYAAN-3': '57320',
    'ADITYA-L1': '57476',
    'XPoSat': '58694',
    'NISAR': '58695',
    'GSAT-24': '52990',
    'GSAT-7C': '57834',
    'GSAT-7R': '57835',
    'GSAT-32': '99999'  # Example ID, replace with actual
}

def get_satellite_position(satellite) -> Dict[str, float]:
    """Get current latitude and longitude of a satellite."""
    ts = load.timescale()
    t = ts.now()
    
    # Get satellite position
    geocentric = satellite.at(t)
    subpoint = wgs84.subpoint(geocentric)
    
    return {
        'lat': subpoint.latitude.degrees,
        'lon': subpoint.longitude.degrees,
        'elevation': subpoint.elevation.km
    }

def get_satellites():
    """Fetch and filter ISRO satellites from multiple sources."""
    all_satellites = []
    
    for url in TLE_SOURCES:
        try:
            print(f"🌍 Fetching data from: {url}")
            satellites = load.tle_file(url)
            print(f"✅ Found {len(satellites)} satellites")
            all_satellites.extend(satellites)
        except Exception as e:
            print(f"⚠️ Error fetching from {url}: {str(e)}")
    
    return all_satellites

def main():
    print("\n🚀 ISRO Satellite Tracker")
    print("======================\n")
    
    try:
        # Load satellite data
        print("🌍 Fetching satellite data...")
        all_satellites = get_satellites()
        
        if not all_satellites:
            print("❌ No satellite data available")
            return
        
        # First try to find satellites by name keywords
        isro_keywords = ['ISRO', 'CARTOSAT', 'OCEANSAT', 'RESOURCESAT', 'GSAT', 'INSAT', 'IRNSS', 'RISAT', 'CHANDRAYAAN', 'ADITYA']
        isro_sats = []
        
        for sat in all_satellites:
            sat_name = sat.name.upper()
            if any(keyword in sat_name for keyword in isro_keywords):
                isro_sats.append(sat)
        
        # If no satellites found by name, try by NORAD IDs
        if not isro_sats:
            print("⚠️ No ISRO satellites found by name, trying NORAD IDs...")
            sat_by_norad = {str(sat.model.satnum): sat for sat in all_satellites}
            for name, norad_id in ISRO_SATELLITES.items():
                if norad_id in sat_by_norad:
                    sat = sat_by_norad[norad_id]
                    sat.name = name  # Update name for better display
                    isro_sats.append(sat)
        
        print(f"🔍 Found {len(isro_sats)} ISRO satellites")
        
        if not isro_sats:
            print("⚠️ No ISRO satellites found. Showing all available satellites...")
            isro_sats = all_sats[:10]  # Show first 10 satellites as fallback
        
        # Get positions of all satellites
        sat_positions = []
        for sat in isro_sats:
            try:
                pos = get_satellite_position(sat)
                sat_positions.append((sat, pos))
                print(f"📍 {sat.name}: {pos['lat']:.2f}°N, {pos['lon']:.2f}°E")
            except Exception as e:
                print(f"⚠️ Could not get position for {sat.name}: {str(e)}")
        
        if not sat_positions:
            print("❌ No valid satellite positions found")
            return
            
        # Calculate map center (average of all satellite positions)
        avg_lat = sum(pos['lat'] for _, pos in sat_positions) / len(sat_positions)
        avg_lon = sum(pos['lon'] for _, pos in sat_positions) / len(sat_positions)
        
        # Create map
        m = folium.Map(
            location=[avg_lat, avg_lon],
            zoom_start=3,
            tiles='OpenStreetMap'
        )
        
        # Add observer location (India center)
        folium.Marker(
            location=[20.5937, 78.9629],
            popup='Observer (India Center)',
            icon=folium.Icon(color='blue', icon='user', prefix='fa')
        ).add_to(m)
        
        # Add satellites to map
        for sat, pos in sat_positions:
            # Custom icon
            icon = folium.Icon(
                icon='satellite',
                prefix='fa',
                color='red',
                icon_color='white'
            )
            
            # Create popup with satellite info
            popup_html = f"""
                <div style="width: 200px;">
                    <h4>{sat.name}</h4>
                    <b>Latitude:</b> {pos['lat']:.4f}°<br>
                    <b>Longitude:</b> {pos['lon']:.4f}°<br>
                    <b>Altitude:</b> {pos['elevation']:,.0f} km
                </div>
            """
            
            folium.Marker(
                location=[pos['lat'], pos['lon']],
                popup=folium.Popup(popup_html, max_width=250),
                icon=icon,
                tooltip=sat.name
            ).add_to(m)
            
            # Add line from observer to satellite
            folium.PolyLine(
                locations=[[20.5937, 78.9629], [pos['lat'], pos['lon']]],
                color='red',
                weight=1,
                opacity=0.5
            ).add_to(m)
        
        # Add a legend
        legend_html = """
            <div style="position: fixed; 
                        bottom: 50px; left: 50px; width: 180px; 
                        background: white; padding: 10px; 
                        border: 1px solid grey; z-index: 9999;
                        font-size: 14px;
                        border-radius: 5px;">
                <b>🌍 ISRO Satellite Tracker</b><br>
                <i class="fa fa-satellite" style="color: red"></i> ISRO Satellite<br>
                <i class="fa fa-user" style="color: blue"></i> Your Location<br>
                <hr style="margin: 5px 0;">
                <small>Last updated: {}</small>
            </div>
        """.format(datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S %Z'))
        
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Save and open map
        m.save(MAP_OUTPUT_FILE)
        print("\n✅ Map generated successfully!")
        print(f"📁 File saved as: {MAP_OUTPUT_FILE}")
        print("🔄 Opening in default browser...")
        webbrowser.open(f'file://{Path(MAP_OUTPUT_FILE).absolute()}')
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPlease check your internet connection and try again.")
        print("If the error persists, the satellite data source might be temporarily unavailable.")

if __name__ == "__main__":
    main()