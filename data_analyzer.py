from datetime import datetime

def analyze_game(game, advanced_box_score, team):
    analysis = {
        'home_team': game.home_team,
        'away_team': game.away_team,
        'date': datetime.strptime(game.start_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%A, %B %d, %Y at %I:%M %p ET"),
        'completed': game.completed
    }
    
    if game.completed:
        team_score = game.home_points if game.home_team == team else game.away_points
        opponent_score = game.away_points if game.home_team == team else game.home_points
        
        analysis['result'] = 'won' if team_score > opponent_score else 'lost'
        analysis['score'] = f"{team_score}-{opponent_score}"
    else:
        analysis['result'] = 'upcoming'
        analysis['score'] = 'Not played yet'
    
    return analysis

def analyze_betting_data(betting_df, team):
    if betting_df.empty:
        return None

    avg_spread = betting_df['spread'].mean()
    avg_over_under = betting_df['over_under'].mean()
    is_home = betting_df.iloc[0]['home_team'] == team
    is_favored = (is_home and avg_spread < 0) or (not is_home and avg_spread > 0)

    return {
        'avg_spread': avg_spread,
        'avg_over_under': avg_over_under,
        'is_home': is_home,
        'is_favored': is_favored,
        'spread_amount': abs(avg_spread)
    }


def generate_insights(game_analysis, game_stats, betting_analysis, team):
    insights = []
    
    insights.extend([
        f"{'Upcoming' if game_analysis['result'] == 'upcoming' else 'Completed'} game: {team} vs {game_analysis['away_team'] if game_analysis['home_team'] == team else game_analysis['home_team']}",
        f"Date: {game_analysis['date']}",
    ])

    if game_analysis['result'] != 'upcoming':
        insights.append(f"Result: {game_analysis['result'].capitalize()} {game_analysis['score']}")
        
        if game_stats:
            team_stats = next((stats for stats in game_stats.teams if stats.school == team), None)
            if team_stats:
                insights.extend([
                    f"\nGame Statistics for {team}:",
                    f"Total Yards: {team_stats.stats.total_yards}",
                    f"Passing Yards: {team_stats.stats.pass_yards}",
                    f"Rushing Yards: {team_stats.stats.rush_yards}",
                    f"Turnovers: {team_stats.stats.turnovers}",
                ])
    else:
        insights.append("Game has not been played yet.")
    
    if 'advanced_analysis' in locals():  # Check if advanced_analysis is defined
        if advanced_analysis:
            insights.extend([
                f"\nAdvanced Analysis:",
                f"PPA Overall: {team} {advanced_analysis['ppa']['team']['overall']:.2f} vs {advanced_analysis['opponent']} {advanced_analysis['ppa']['opponent']['overall']:.2f}",
                f"PPA Passing: {team} {advanced_analysis['ppa']['team']['passing']:.2f} vs {advanced_analysis['opponent']} {advanced_analysis['ppa']['opponent']['passing']:.2f}",
                f"PPA Rushing: {team} {advanced_analysis['ppa']['team']['rushing']:.2f} vs {advanced_analysis['opponent']} {advanced_analysis['ppa']['opponent']['rushing']:.2f}",
                f"Success Rate: {team} {advanced_analysis['success_rates']['team']:.2f} vs {advanced_analysis['opponent']} {advanced_analysis['success_rates']['opponent']:.2f}",
                f"Explosiveness: {team} {advanced_analysis['explosiveness']['team']:.2f} vs {advanced_analysis['opponent']} {advanced_analysis['explosiveness']['opponent']:.2f}",
            ])
            
            if 'rushing' in advanced_analysis:
                insights.extend([
                    f"\nRushing Analysis for {team}:",
                    f"Power Success: {advanced_analysis['rushing']['power_success']:.2f}",
                    f"Stuff Rate: {advanced_analysis['rushing']['stuff_rate']:.2f}",
                    f"Line Yards: {advanced_analysis['rushing']['line_yards']:.2f}",
                    f"Second Level Yards: {advanced_analysis['rushing']['second_level_yards']:.2f}",
                    f"Open Field Yards: {advanced_analysis['rushing']['open_field_yards']:.2f}",
                ])
            
            if 'havoc' in advanced_analysis:
                insights.extend([
                    f"\nHavoc Rates for {team}:",
                    f"Total: {advanced_analysis['havoc']['total']:.2f}",
                    f"Front Seven: {advanced_analysis['havoc']['front_seven']:.2f}",
                    f"DB: {advanced_analysis['havoc']['db']:.2f}",
                ])
        else:
            insights.append("\nAdvanced analysis data not available for this game.")

    if betting_analysis:
        insights.extend([
            f"\nBetting Insights:",
            f"Average spread: {betting_analysis['avg_spread']:.1f}",
            f"Average over/under: {betting_analysis['avg_over_under']:.1f}",
            f"{team} is the {'home' if betting_analysis['is_home'] else 'away'} team",
            f"{'Favored' if betting_analysis['is_favored'] else 'Underdog'} by {betting_analysis['spread_amount']:.1f} points"
        ])
    else:
        insights.append("\nBetting data not available for this game.")

    return "\n".join(insights)