# mymusicproject/chatbot/views.py
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from .models import UserInteraction, Recommendation
from .chatbot_logic import generate_bot_response, analyze_tone, get_recommendation

def your_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        
        # Call your chatbot logic function to generate a response
        bot_response, sentiment = generate_bot_response(user_message)

        # Construct the response data
        response_data = {
            'message': bot_response,
            'sentiment': sentiment,
        }

        return JsonResponse(response_data)
    else:
        return HttpResponseBadRequest('Invalid request method')

def chat(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')
        user = request.POST.get('user')
        UserInteraction.objects.create(user=user, message=user_message)

        # Perform tone analysis using TextBlob
        tone = analyze_tone(user_message)

        # Get song recommendation based on tone using Last.fm
        recommendation = get_recommendation(tone)

        # Store the recommendation
        Recommendation.objects.create(user=user, **recommendation)

        return JsonResponse({'bot_message': recommendation['message']})

    interactions = UserInteraction.objects.all()
    recommendations = Recommendation.objects.all()
    return render(request, 'chatbot/chat.html', {'interactions': interactions, 'recommendations': recommendations})
