import discord

class User:
    def __init__(self, username):
        self.username = username

        # Status effects
        self.is_gagged = False

    def gag(self):
        self.is_gagged = True

    def ungag(self):
        self.is_gagged = False

USERS = {}

def get_user(member: discord.Member):
    username = str(member)

    saved_user = USERS.get(username)

    # Create a new user if we need one
    if saved_user is None:
        saved_user = User(username)
        USERS[username] = saved_user

    return saved_user
