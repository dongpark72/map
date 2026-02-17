"""
Direct test of the building detail endpoint
"""
import requests
import json

# Test with the PNU that Kakao Maps is actually returning (from logs)
pnu = "2620012100103180045"  # This is what worked in the logs
url = f"http://175.126.187.59:8000/proxy/building-detail/?pnu={pnu}"

output = []
output.append(f"Testing URL: {url}")
output.append("=" * 80)

try:
    response = requests.get(url, timeout=30)
    output.append(f"Status Code: {response.status_code}")
    output.append(f"Response Length: {len(response.text)} bytes")
    output.append("\nResponse Content:")
    output.append("=" * 80)
    
    data = response.json()
    output.append(json.dumps(data, indent=2, ensure_ascii=False))
    
    if 'data' in data:
        if 'floors' in data['data']:
            output.append(f"\n\n{'='*80}")
            output.append(f"FLOORS ARRAY LENGTH: {len(data['data']['floors'])}")
            if len(data['data']['floors'])==0:
                output.append("⚠️  WARNING: Floors array is EMPTY!")
            else:
                output.append(f"✓ Found {len(data['data']['floors'])} floor records")
                for idx, floor in enumerate(data['data']['floors'][:5]):
                    output.append(f"  {idx+1}. {floor}")
        else:
            output.append("\n⚠️  WARNING: 'floors' key not found in response data!")
            
except Exception as e:
    output.append(f"Error: {e}")
    import traceback
    output.append(traceback.format_exc())

# Write to file
with open('endpoint_response.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("Response saved to endpoint_response.txt")
print(f"Floors count: {len(data.get('data', {}).get('floors', []))}")
