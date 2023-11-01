from reservations.models import Reservation
from flights.models import Flight
import requests

def notify_flight(flight_id=1408):
    Reservations = Reservation.objects.filter(flight=flight_id)
    flight = Flight.objects.get(pk=flight_id)
    
    notification_body = f'ستنطلق رحلتك من {flight.program.move_from} إلي {flight.program.move_to} قريبا.'
    for reservation in Reservations:
        send_notification(reservation.user.notification_token, notification_body)
        



def send_notification(to, notification_body):
    # Define the FCM API URL
    fcm_url = "https://fcm.googleapis.com/fcm/send"

    # Define your FCM server key
    fcm_server_key = "AAAAxm5MHOE:APA91bFTvcbli2I_poG2wffmnyrLSiYpFYUTpceFEq8MfCQndP3xWMmcrmNrQZuZCytXqaG9YIfsKj4SzB3D8-j9gWNFVWbB2LHJ0cIvm5qXgi1QHFhTRFNADYdQ9YaP-TDVqbjdLcPZ"

    # Define the headers for the request
    headers = {
        "Authorization": "key=" + fcm_server_key,
        "Content-Type": "application/json"
    }

    # Define the JSON payload for the POST request
    payload = {
        "to": to,
        "notification": {
            "body": notification_body,
            "title": "Momayz",
            "android_channel_id": "2"
        },
        "data": {
            "click_action": "FLUTTER_NOTIFICATION_CLICK",
            "status": "done",
            "body": "body",
            "title": "title"
        },
        "priority": "high"
    }

    # Send the POST request to FCM
    response = requests.post(fcm_url, json=payload, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("Notification sent successfully.")
    else:
        print("Failed to send notification. Status code:", response.status_code)
        print("Response content:", response.content)
        
        
