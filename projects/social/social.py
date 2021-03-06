import random

import sys
sys.path.append(r"C:\Users\Samuel\repos\Graphs\projects\graph")

from util import Queue

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def reset(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments
        Creates that number of users and a randomly distributed friendships
        between those users.
        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.reset()        

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create friendships
        possible_friendships = []

        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

            random.shuffle(possible_friendships)

        for i in range(num_users * avg_friendships // 2):
            friendships = possible_friendships[i]
            self.add_friendship(friendships[0], friendships[1])


    def get_friendships(self, user_id):
        self.users[user_id].friends = set()
        for friend in self.friendships[user_id]:
            self.users[user_id].friends.add(friend)

        return self.users[user_id].friends

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument
        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.
        The key is the friend's ID and the value is the path.
        """ 
        q = Queue()
        q.enqueue([user_id])

        visited = {}

        while q.size() > 0:
            current_path = q.dequeue()
            current_user = current_path[-1]

            if current_user not in visited:
                visited[current_user] = current_path
                
                for friend in self.friendships[current_user]:
                    path_copy = current_path[:]
                    path_copy.append(friend)
                    q.enqueue(path_copy)

        return visited


if __name__ == '__main__':
    # random.seed(84)
    sg = SocialGraph()
    print("Social Network")
    sg.populate_graph(10, 2)
    print(sg.friendships)

    user_id = 1

    print(f"\nUser {user_id}'s friend set")
    print(sg.get_friendships(1))

    print("\nConnections")
    connections = sg.get_all_social_paths(1)
    print(connections)
