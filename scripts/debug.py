from app_prime_league.models import Team
from data_crawling.api import Crawler
from parsing.regex_operations import MatchHTMLParser, TeamHTMLParser


def main():
    match_id = 597487
    team_id = 105959
    crawler = Crawler(local=True)
    team, _ = Team.objects.get_or_create(id=team_id)
    match_parser = MatchHTMLParser(crawler.get_match_website(match_id), team)
    team_parser = TeamHTMLParser(crawler.get_team_website(team_id))
    match_parser.get_enemy_lineup()
    # print(match_parser.get_suggestion_confirmed())
    # sumNames = team_parser.get_summoner_names()
    # print(sumNames)
    # print(RegexOperator.get_enemy_team_id(get_website_of_match("597508")))
    # print(RegexOperator.get_summoner_names(get_website_of_team("91700")))
    # print(RegexOperator.get_game_day(get_website_of_match("597508")))
    # print(RegexOperator.get_team_name(get_website_of_team("105878")))
    # print(RegexOperator.get_enemy_team_name(get_website_of_match("597508")))
    # print(RegexOperator.get_team_tag(get_website_of_team("105878")))
    # print(RegexOperator.get_matches(get_website_of_team("105878")))
    pass


# Command to run this file:
# python manage.py runscript debug
def run():
    main()
