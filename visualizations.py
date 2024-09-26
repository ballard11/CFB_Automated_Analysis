import matplotlib.pyplot as plt
import seaborn as sns

def create_detailed_quarter_visualizations(advanced_box, team):
    team_data = next((t for t in advanced_box.teams.ppa if t.team == team), None)
    opponent_data = next((t for t in advanced_box.teams.ppa if t.team != team), None)
    
    if not team_data or not opponent_data:
        print("Unable to create visualizations: missing data")
        return
    
    quarters = ['quarter1', 'quarter2', 'quarter3', 'quarter4']
    
    # PPA Breakdown
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 18))
    
    # Overall PPA
    team_overall = [getattr(team_data.overall, q) for q in quarters]
    opponent_overall = [getattr(opponent_data.overall, q) for q in quarters]
    ax1.bar(quarters, team_overall, alpha=0.7, label=team)
    ax1.bar(quarters, opponent_overall, alpha=0.7, label=opponent_data.team)
    ax1.set_title('Overall PPA by Quarter')
    ax1.set_ylabel('PPA')
    ax1.legend()
    
    # Passing PPA
    team_passing = [getattr(team_data.passing, q) for q in quarters]
    opponent_passing = [getattr(opponent_data.passing, q) for q in quarters]
    ax2.bar(quarters, team_passing, alpha=0.7, label=team)
    ax2.bar(quarters, opponent_passing, alpha=0.7, label=opponent_data.team)
    ax2.set_title('Passing PPA by Quarter')
    ax2.set_ylabel('PPA')
    ax2.legend()
    
    # Rushing PPA
    team_rushing = [getattr(team_data.rushing, q) for q in quarters]
    opponent_rushing = [getattr(opponent_data.rushing, q) for q in quarters]
    ax3.bar(quarters, team_rushing, alpha=0.7, label=team)
    ax3.bar(quarters, opponent_rushing, alpha=0.7, label=opponent_data.team)
    ax3.set_title('Rushing PPA by Quarter')
    ax3.set_ylabel('PPA')
    ax3.legend()
    
    plt.tight_layout()
    plt.savefig('ppa_breakdown.png')
    plt.close()
    
    # Success Rates
    team_success = next((t for t in advanced_box.teams.success_rates if t.team == team), None)
    opponent_success = next((t for t in advanced_box.teams.success_rates if t.team != team), None)
    
    if team_success and opponent_success:
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 18))
        
        # Overall Success Rate
        team_overall = [getattr(team_success.overall, q) for q in quarters]
        opponent_overall = [getattr(opponent_success.overall, q) for q in quarters]
        ax1.plot(quarters, team_overall, marker='o', label=team)
        ax1.plot(quarters, opponent_overall, marker='o', label=opponent_data.team)
        ax1.set_title('Overall Success Rate by Quarter')
        ax1.set_ylabel('Success Rate')
        ax1.legend()
        
        # Standard Downs Success Rate
        team_standard = [getattr(team_success.standard_downs, q) for q in quarters]
        opponent_standard = [getattr(opponent_success.standard_downs, q) for q in quarters]
        ax2.plot(quarters, team_standard, marker='o', label=team)
        ax2.plot(quarters, opponent_standard, marker='o', label=opponent_data.team)
        ax2.set_title('Standard Downs Success Rate by Quarter')
        ax2.set_ylabel('Success Rate')
        ax2.legend()
        
        # Passing Downs Success Rate
        team_passing = [getattr(team_success.passing_downs, q) for q in quarters]
        opponent_passing = [getattr(opponent_success.passing_downs, q) for q in quarters]
        ax3.plot(quarters, team_passing, marker='o', label=team)
        ax3.plot(quarters, opponent_passing, marker='o', label=opponent_data.team)
        ax3.set_title('Passing Downs Success Rate by Quarter')
        ax3.set_ylabel('Success Rate')
        ax3.legend()
        
        plt.tight_layout()
        plt.savefig('success_rates.png')
        plt.close()
    
    # Explosiveness
    team_explosiveness = next((t for t in advanced_box.teams.explosiveness if t.team == team), None)
    opponent_explosiveness = next((t for t in advanced_box.teams.explosiveness if t.team != team), None)
    
    if team_explosiveness and opponent_explosiveness:
        plt.figure(figsize=(10, 6))
        team_exp = [getattr(team_explosiveness.overall, q) for q in quarters]
        opponent_exp = [getattr(opponent_explosiveness.overall, q) for q in quarters]
        plt.plot(quarters, team_exp, marker='o', label=team)
        plt.plot(quarters, opponent_exp, marker='o', label=opponent_data.team)
        plt.title('Explosiveness by Quarter')
        plt.ylabel('Explosiveness')
        plt.legend()
        plt.savefig('explosiveness.png')
        plt.close()
    
    print("Detailed visualizations saved as 'ppa_breakdown.png', 'success_rates.png', and 'explosiveness.png'")