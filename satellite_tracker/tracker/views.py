from django.shortcuts import render, get_object_or_404
import requests
from django.http import JsonResponse
from sgp4.api import Satrec, jday
import datetime
from datetime import datetime as dt
import math

# Dictionary of popular satellites with their TLE data
SATELLITES = {
    'iss': {
        'name': 'International Space Station (ISS)',
        'tle_url': 'https://celestrak.com/NORAD/elements/stations.txt',
    },
    'hubble': {
        'name': 'Hubble Space Telescope',
        'tle_url': 'https://celestrak.com/NORAD/elements/active.txt',
        'tle_id': 'HST'
    },
    'starlink': {
        'name': 'Starlink Satellite',
        'tle_url': 'https://celestrak.com/NORAD/elements/starlink.txt',
    },
    'gps': {
        'name': 'GPS Satellite',
        'tle_url': 'https://celestrak.com/NORAD/elements/gps-ops.txt',
    },
    'meteosat': {
        'name': 'Meteosat Weather Satellite',
        'tle_url': 'https://celestrak.com/NORAD/elements/weather.txt',
    },
    'isro': {
        'name': 'ISRO Satellites',
        'tle_url': 'https://celestrak.com/NORAD/elements/active.txt',
        'tle_id': 'ISRO',
        'is_isro': True
    },
    'chandrayaan': {
        'name': 'Chandrayaan-3',
        'tle_url': 'https://celestrak.com/NORAD/elements/active.txt',
        'tle_id': 'CHANDRAYAAN-3'
    },
    'aditya': {
        'name': 'Aditya-L1',
        'tle_url': 'https://celestrak.com/NORAD/elements/active.txt',
        'tle_id': 'ADITYA-L1'
    },
    'gsat': {
        'name': 'GSAT Series',
        'tle_url': 'https://celestrak.com/NORAD/elements/active.txt',
        'tle_id': 'GSAT'
    }
}

# Fallback TLE data in case of network issues
FALLBACK_TLE = {
    'iss': [
        'ISS (ZARYA)             ',
        '1 25544U 98067A   25236.34583333  .00016717  00000+0  25030-3 0  9997',
        '2 25544  51.6416  32.7813 0006900  35.6891  46.3283 15.50000000 10001'
    ],
    'hubble': [
        'HST                     ',
        '1 20580U 90037B   25236.40000000  .00000100  00000+0  00000+0 0  9999',
        '2 20580  28.4700 288.6000 0001000 330.5000  29.5000 15.10000000 10001'
    ],
    'isro': [
        'CARTOSAT-2B             ',
        '1 36795U 10035A   25236.50000000  .00000100  00000+0  00000+0 0  9999',
        '2 36795  97.4000 100.0000 0010000 270.0000  90.0000 15.20000000 10001'
    ]
}

def get_tle(satellite_id='iss'):
    """Get TLE data for a specific satellite with fallback to local data"""
    try:
        print(f"\n=== DEBUG: Getting TLE for satellite_id: {satellite_id} ===")
        satellite = SATELLITES.get(satellite_id, SATELLITES['iss'])
        print(f"Satellite config: {satellite}")
        
        # Try to get fresh TLE data
        try:
            print(f"Making request to: {satellite['tle_url']}")
            response = requests.get(satellite['tle_url'], timeout=5)  # Reduced timeout to 5s
            print(f"Response status: {response.status_code}")
            response.raise_for_status()
        except (requests.RequestException, Exception) as e:
            print(f"Error fetching TLE data: {e}")
            print("Using fallback TLE data")
            return FALLBACK_TLE.get(satellite_id, FALLBACK_TLE['iss'])

        
        # Clean and filter lines
        raw_lines = response.text.splitlines()
        print(f"Received {len(raw_lines)} lines of TLE data")
        
        lines = [line.strip() for line in raw_lines if line.strip()]
        print(f"After cleaning: {len(lines)} non-empty lines")
        
        if not lines or len(lines) < 3:
            print(f"ERROR: Not enough TLE data received for {satellite_id}")
            print(f"First few lines: {lines[:5]}")
            return None
            
        # For ISS (first in stations.txt)
        if satellite_id == 'iss':
            return lines[0:3]
        
        # For ISRO satellites
        if satellite_id == 'isro' or satellite.get('is_isro', False):
            print("Processing ISRO satellite data...")
            isro_sats = []
            isro_keywords = ['ISRO', 'CARTOSAT', 'OCEANSAT', 'RESOURCESAT', 'GSAT', 'INSAT', 'IRNSS', 'RISAT', 'CHANDRAYAAN', 'ADITYA', 'ASTROSAT', 'SCATSAT', 'MEGHA-TROPIQUES']
            print(f"Looking for ISRO satellites with keywords: {isro_keywords}")
            
            for i in range(0, len(lines)-2, 3):
                try:
                    if i+2 >= len(lines):
                        print(f"Skipping incomplete TLE set at index {i}")
                        continue
                        
                    line = lines[i].upper()
                    if any(keyword in line for keyword in isro_keywords):
                        print(f"Found ISRO satellite: {lines[i].strip()}")
                        isro_sats.append({
                            'name': lines[i].strip(),
                            'tle1': lines[i+1],
                            'tle2': lines[i+2]
                        })
                except Exception as e:
                    print(f"Error processing TLE at index {i}: {e}")
            
            print(f"Found {len(isro_sats)} ISRO satellites")
            
            # If we found ISRO satellites, return the first one
            if isro_sats:
                sat = isro_sats[0]  # Get first ISRO satellite found
                print(f"Returning data for: {sat['name']}")
                return [sat['name'], sat['tle1'], sat['tle2']]
            
            print("No ISRO satellites found, falling back to first available satellite")
            return lines[0:3]
            
        # For other satellites with specific IDs
        if 'tle_id' in satellite:
            for i in range(0, len(lines)-2, 3):
                if satellite['tle_id'].upper() in lines[i].upper():
                    return lines[i:i+3]
        
        # Default to first 3 lines if specific satellite not found
        return lines[0:3]
        
    except requests.exceptions.RequestException as e:
        return lines[0:3] if len(lines) >= 3 else None
    except Exception as e:
        print(f"Error fetching TLE data: {e}")
        return None

def get_satellite_position(tle_lines):
    if not tle_lines or len(tle_lines) < 3:
        print("Insufficient TLE data")
        return None
        
    try:
        # Print TLE data for debugging
        print(f"TLE Data: {tle_lines[0][:50]}...")
        print(f"TLE Line 1: {tle_lines[1]}")
        print(f"TLE Line 2: {tle_lines[2]}")
        
        # Create satellite object from TLE
        sat = Satrec.twoline2rv(tle_lines[1], tle_lines[2])
        
        # Get current UTC time
        now = dt.utcnow()
        print(f"Calculating position for time: {now}")
        
        # Convert to Julian date
        jd, fr = jday(now.year, now.month, now.day,
                     now.hour, now.minute, now.second + now.microsecond*1e-6)
        
        # Calculate position
        error_code, r, _ = sat.sgp4(jd, fr)
        
        if error_code != 0:
            print(f"Error in SGP4 calculation: {error_code}")
            return None
            
        print(f"Position calculated: x={r[0]:.2f}, y={r[1]:.2f}, z={r[2]:.2f}")
        
        # Convert ECI to lat/lng
        lat = math.degrees(math.atan2(r[2], math.sqrt(r[0]*r[0] + r[1]*r[1])))
        lng = math.degrees(math.atan2(r[1], r[0]))
        altitude = math.sqrt(r[0]**2 + r[1]**2 + r[2]**2) - 6371  # Earth's radius in km
        
        return {
            'x_km': round(r[0], 2),
            'y_km': round(r[1], 2),
            'z_km': round(r[2], 2),
            'lat': round(lat, 4),
            'lng': round(lng, 4),
            'altitude': round(altitude, 2),
            'velocity': 7.66,  # Approximate velocity in km/s
            'name': tle_lines[0].strip(),
            'timestamp': now.isoformat(),
            'is_tle': True
        }
    except Exception as e:
        print(f"Error calculating position: {e}")
    return None

def simulate_isro_satellite(satellite):
    """Simulate position for ISRO satellites"""
    try:
        now = dt.utcnow()
        name = satellite.get('name', 'ISRO Satellite')
        
        # Special handling for specific ISRO missions
        if 'CHANDRAYAAN' in name.upper():
            # Chandrayaan in lunar orbit
            altitude = 100  # km above lunar surface
            moon_radius = 1737.4  # km
            distance = moon_radius + altitude
            orbit_period = 2.1 * 3600  # 2.1 hours
            
            # Simulate orbit around moon (simplified)
            angle = (2 * math.pi * now.timestamp() / orbit_period) % (2 * math.pi)
            lat = math.degrees(math.sin(angle) * math.radians(30))  # 30° inclination
            lng = (math.degrees(angle) + (now.hour * 15)) % 360 - 180  # Rotate with time
            
            return JsonResponse({
                'lat': round(lat, 4),
                'lng': round(lng, 4),
                'altitude': round(altitude, 2),
                'velocity': 1.62,  # km/s (lunar orbital velocity)
                'name': name + ' (Lunar Orbit)',
                'is_tle': False
            })
            
        elif 'ADITYA' in name.upper():
            # Aditya-L1 at Sun-Earth L1 point
            return JsonResponse({
                'lat': 0,
                'lng': 0,
                'altitude': 1500000,  # km from Earth
                'velocity': 0,
                'name': name + ' (L1 Point)',
                'is_tle': False
            })
            
        else:
            # Default LEO simulation for other ISRO satellites
            altitude = 600  # km
            earth_radius = 6371  # km
            distance = earth_radius + altitude
            orbit_period = 96 * 60  # 96 minutes in seconds
            
            # Calculate position in orbit
            seconds = now.timestamp()
            angle = (2 * math.pi * seconds / orbit_period) % (2 * math.pi)
            
            # Add some inclination (typical for ISRO satellites)
            inclination = math.radians(45)  # 45° inclination
            
            # Calculate 3D position
            x = distance * math.cos(angle)
            y = distance * math.sin(angle) * math.cos(inclination)
            z = distance * math.sin(angle) * math.sin(inclination)
            
            # Convert to lat/lng
            lat = math.degrees(math.asin(z / distance))
            lng = math.degrees(math.atan2(y, x))
            
            # Calculate orbital velocity (km/s)
            velocity = 7.8 * math.sqrt(earth_radius / (earth_radius + altitude))
            
            return JsonResponse({
                'x_km': round(x, 2),
                'y_km': round(y, 2),
                'z_km': round(z, 2),
                'lat': round(lat, 4),
                'lng': round(lng, 4),
                'altitude': round(altitude, 2),
                'velocity': round(velocity, 2),
                'name': name + ' (Simulated Orbit)',
                'is_tle': False,
                'timestamp': now.isoformat()
            })
            
    except Exception as e:
        print(f"Error in ISRO satellite simulation: {e}")
        return JsonResponse({
            'error': 'Failed to calculate satellite position',
            'details': str(e)
        }, status=500)

def satellite_position_view(request, satellite_id='iss'):
    """API endpoint to get satellite position"""
    try:
        # Get satellite info from our dictionary
        satellite = SATELLITES.get(satellite_id, SATELLITES['iss'])
        is_isro = satellite_id == 'isro' or satellite.get('is_isro', False)
        
        # For ISRO satellites, use our simulation
        if is_isro:
            return simulate_isro_satellite(satellite)
            
        # For other satellites, try to get TLE data
        try:
            tle_lines = get_tle(satellite_id)
            
            if tle_lines and len(tle_lines) >= 3:
                position = get_satellite_position(tle_lines)
                if position:
                    position.update({
                        'is_tle': True,
                        'satellite_name': tle_lines[0].strip(),
                        'timestamp': dt.utcnow().isoformat()
                    })
                    return JsonResponse(position)
        except Exception as e:
            print(f"Error processing TLE data: {e}")
            # Fall through to simulation if TLE fails
        
        # If we get here, TLE data wasn't available or failed
        return JsonResponse({
            'error': 'Unable to calculate position - no valid TLE data available',
            'satellite_id': satellite_id,
            'name': satellite.get('name', 'Unknown Satellite')
        }, status=500)
        
    except Exception as e:
        print(f"Error in satellite_position_view: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def get_satellites_list():
    """Get list of available satellites"""
    return [{'id': sat_id, 'name': data['name']} for sat_id, data in SATELLITES.items()]

def index(request):
    """Main view with satellite tracking interface"""
    satellites_list = [
        {'id': 'iss', 'name': 'International Space Station'},
        {'id': 'hubble', 'name': 'Hubble Space Telescope'},
        {'id': 'starlink', 'name': 'Starlink Satellite'},
        {'id': 'gps', 'name': 'GPS Satellite'},
        {'id': 'chandrayaan', 'name': 'Chandrayaan-3'},
        {'id': 'aditya', 'name': 'Aditya-L1'},
    ]
    
    context = {
        'satellites': satellites_list,
        'default_satellite': request.GET.get('satellite', 'iss'),
        'STATIC_URL': '/static/'  # Make sure static URL is available in template
    }
    
    # If it's an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'satellites': satellites_list})
        
    return render(request, 'tracker/index.html', context)