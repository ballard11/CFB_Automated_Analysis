from config import TEAM, YEAR, WEEK
from api_client import setup_api
from data_fetcher import get_game_data, get_betting_data
from data_analyzer import analyze_game, analyze_betting_data, generate_insights

def main():
    api = setup_api()
    
    # Fetch game data
    game, game_stats = get_game_data(api, YEAR, WEEK, TEAM)
    if not game:
        print(f"No game data found for {TEAM} in week {WEEK} of {YEAR}")
        return

    # Analyze game data
    game_analysis = analyze_game(game, game_stats, TEAM)

    # Fetch and analyze betting data
    betting_df = get_betting_data(api, YEAR, WEEK, TEAM)
    betting_analysis = analyze_betting_data(betting_df, TEAM)

    # Generate insights
    insights = generate_insights(game_analysis, game_stats, betting_analysis, TEAM)
    print(insights)

    # Print detailed betting data if available
    if not betting_df.empty:
        print("\nDetailed Betting Data:")
        print(betting_df)
    else:
        print("\nNo betting data available.")

if __name__ == "__main__":
    main()