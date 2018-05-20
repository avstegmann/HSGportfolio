from leaderboardDAO import LeaderboardDAO

dao = LeaderboardDAO()


class Leaderboard:

    rows = []

    def get_leader(self):
        self.rows = dao.show_leader()




