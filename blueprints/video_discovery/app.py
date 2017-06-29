# -*- coding: utf-8 -*-
"""This module contains the Workbench video discovery blueprint application"""
from __future__ import unicode_literals
from mmworkbench import Application
import datetime

app = Application(__name__)

GENERAL_PROMPTS = ['I can help you find movies and tv shows. What do you feel like watching today?',
                   'Tell me what you would like to watch today.',
                   'Talk to me to browse movies and tv shows.']

GENERAL_SUGGESTIONS = [{'text': 'Most popular', 'type': 'text'},
                       {'text': 'Most recent', 'type': 'text'},
                       {'text': 'Movies', 'type': 'text'},
                       {'text': 'TV Shows', 'type': 'text'},
                       {'text': 'Action', 'type': 'text'},
                       {'text': 'Dramas', 'type': 'text'},
                       {'text': 'Sci-Fi', 'type': 'text'}]


@app.handle(intent='greet')
def welcome(context, slots, responder):
    """
    When the user starts a conversation, say hi.
    """
    greetings = ['Hello', 'Hi', 'Hey']
    try:
        # Get user's name from session information in request context to personalize the greeting.
        slots['name'] = context['request']['session']['name']
        greetings = [greeting + ', {name}.' for greeting in greetings] + \
            [greeting + ', {name}!' for greeting in greetings]
    except KeyError:
        greetings = [greeting + '.' for greeting in greetings] + \
            [greeting + '!' for greeting in greetings]

    responder.reply(greetings)

    responder.prompt(GENERAL_PROMPTS)

    # Get default videos
    responder.respond(get_default_videos_action())
    responder.suggest(GENERAL_SUGGESTIONS)


@app.handle(intent='browse')
def show_content(context, slots, responder):
    # Show the video content based on the entities found.
    responder.reply("browse placeholder.")


@app.handle(intent='start_over')
def start_over(context, slots, responder):
    """
    When the user wants to start over, clear the dialogue frame and prompt for the next request.
    """
    context['frame'] = {}
    prompts = ['Sure, what do you want to watch?',
               'Let\'s start over, what would you like to watch?',
               'Okay, starting over, tell me what you want to watch.']
    responder.prompt(prompts)

    # Get default videos
    responder.respond(get_default_videos_action())
    responder.suggest(GENERAL_SUGGESTIONS)


@app.handle(intent='exit')
def say_goodbye(context, slots, responder):
    """
    When the user ends a conversation, clear the dialogue frame and say goodbye.
    """
    context['frame'] = {}
    goodbyes = ['Bye!', 'Goodbye!', 'Have a nice day.', 'See you later.']

    responder.reply(goodbyes)


@app.handle(intent='help')
def provide_help(context, slots, responder):
    """
    When the user asks for help, provide some sample queries they can try.
    """
    help_replies = ["I can help you find movies and tv shows based on your preferences."
                    " Just say want you feel like watching and I can find great options for you."]
    responder.reply(help_replies)

    help_prompts = "Here's some content for you."
    responder.prompt(help_prompts)

    # Get default videos
    responder.respond(get_default_videos_action())
    responder.suggest(GENERAL_SUGGESTIONS)


@app.handle(intent='unsupported')
def handle_unsupported(context, slots, responder):
    # Respond with a message explaining the app does not support that # query.
    unsupported = ['Sorry, I can\'t help you with that information.',
                   'Sorry, I don\'t have that information.',
                   'Sorry, I can\'t help you with that.',
                   'Sorry, I can only help you browse movies and tv shows.',
                   'Sorry, I don\'t have that information, would you like to try something else?']

    responder.reply(unsupported)

    responder.prompt(GENERAL_PROMPTS)

    # Get default videos
    responder.respond(get_default_videos_action())
    responder.suggest(GENERAL_SUGGESTIONS)


@app.handle(intent='unrelated')
def handle_unrelated(context, slots, responder):
    # Respond with a message explaining the app does not support that # query.
    responder.reply("unrelated placeholder.")


@app.handle(intent='compliment')
def say_something_nice(context, slots, responder):
    # Respond with a compliment or something nice.
    compliments = ['Thank you, you rock!',
                   'You\'re too kind.',
                   'Thanks, I try my best!',
                   'Thanks, you\'re quite amazing yourself.',
                   'Thanks, hope you\'re having a good day!']

    responder.reply(compliments)

    responder.prompt(GENERAL_PROMPTS)
    # Get default videos
    responder.respond(get_default_videos_action())
    responder.suggest(GENERAL_SUGGESTIONS)


@app.handle(intent='insult')
def handle_insult(context, slots, responder):
    # Evade the insult and come back to the app usage.
    insult_replies = ['Sorry, I do my  best!',
                      'Someone needs to watch a romantic movie.',
                      'Sorry I\'m trying!',
                      'Nobody\'s perfect!',
                      'Sorry, I\'ll try to do better next time.']

    responder.reply(insult_replies)

    responder.prompt(GENERAL_PROMPTS)

    # Get default videos
    responder.respond(get_default_videos_action())
    responder.suggest(GENERAL_SUGGESTIONS)


@app.handle()
def default(context, slots, responder):
    """
    When the user asks an unrelated question, convey the lack of understanding for the requested
    information and prompt to return to video discovery.
    """
    unrelated = ['Sorry, I didn\'t understand your request.',
                 'I\'m sorry, I\'m not sure what you mean.',
                 'Sorry, could you try a different request?',
                 'I\'m sorry, could you ask me something else related to movies or tv shows?',
                 'Sorry, I was programmed to only serve your movie and tv show requests.']

    responder.reply(unrelated)

    responder.prompt(GENERAL_PROMPTS)

    # Get default videos
    responder.respond(get_default_videos_action())
    responder.suggest(GENERAL_SUGGESTIONS)


def get_default_videos_action():
    """
    Get a client action with the most recent and popular videos.
    """
    default_videos = get_default_videos()

    videos_client_action = {'videos': []}

    for video in default_videos:
        release_date = datetime.datetime.strptime(video['release_date'], '%Y-%m-%d')
        video_summary = {'title': video['title'], 'release_year': release_date.year}
        videos_client_action['videos'].append(video_summary)

    return videos_client_action


def get_default_videos():
    """
    Retrieve the most popular and recent videos in the knowledge base.


    Returns:
        list: The list of movies.
    """
    results = app.question_answerer.get(index='video')
    return results


if __name__ == '__main__':
    app.cli()
