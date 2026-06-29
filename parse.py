import json, sys
from datetime import datetime, timezone, timedelta

def to_paris(dt):
    # Décalage Europe/Paris : UTC+1 hiver, UTC+2 été (approximation DST)
    import time
    offset = 2 if time.daylight and time.localtime().tm_isdst else 1
    return dt + timedelta(hours=offset)

data = json.load(sys.stdin)
visits = data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']
now = datetime.now(timezone.utc)
out = {'updated_at': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'departures': []}
for v in visits[:4]:
    dt_str = v['MonitoredVehicleJourney']['MonitoredCall']['ExpectedDepartureTime']
    dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    dt_paris = to_paris(dt)
    out['departures'].append({
        'time': dt_paris.strftime('%H:%M'),
        'minutes': max(0, int((dt - now).total_seconds() // 60))
    })
print(json.dumps(out, indent=2))
