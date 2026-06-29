import json, sys
from datetime import datetime, timezone
data = json.load(sys.stdin)
visits = data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']
now = datetime.now(timezone.utc)
out = {'updated_at': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'departures': []}
for v in visits[:4]:
    dt_str = v['MonitoredVehicleJourney']['MonitoredCall']['ExpectedDepartureTime']
    dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    out['departures'].append({'time': dt.strftime('%H:%M'), 'minutes': max(0, int((dt - now).total_seconds() // 60))})
print(json.dumps(out, indent=2))
