# main.py

from simulator import simulate, plot_ev, plot_ev_comparison, plot_outcome_per_deck, create_graphs_folder #plot_outcome_comparison
from policies import policy_1, policy_2, policy_3, policy_4, policy_5


def main():
    policies = {
        "Policy 1 (>=17)": policy_1,
        "Policy 2 (hard/soft 17)": policy_2,
        "Policy 3 (always stick)": policy_3,
        "Policy 4 (soft aggressive)": policy_4,
        "Policy 5 (dealer-aware)": policy_5
    }

    deck_types = ["infinite", "single", "shoe"]
    num_games = 1000000  # reduce to 10000 first if testing graphs

    # 🔹 Store results for graphing
    results_inf = []
    results_single = []
    results_shoe = []

    for deck_type in deck_types:
        print("\n===================================")
        print(f"DECK TYPE: {deck_type.upper()}")
        print("===================================\n")

        results_table = []

        for name, policy in policies.items():
            results = simulate(policy, deck_type, num_games)

            results_table.append((name, results))

            print(f"{name}")
            print(f"  Win Rate:  {results['win_rate']:.4f}")
            print(f"  Loss Rate: {results['loss_rate']:.4f}")
            print(f"  Draw Rate: {results['draw_rate']:.4f}")
            print(f"  Expected Value: {results['expected_value']:.4f}")
            print("-----------------------------------")

        print("\nSummary complete for:", deck_type)

        # 🔹 Save results for later graphing
        if deck_type == "infinite":
            results_inf = results_table
        elif deck_type == "single":
            results_single = results_table
        elif deck_type == "shoe":
            results_shoe = results_table    

    # 🔹 Generate graphs AFTER simulations
    create_graphs_folder()

    plot_ev(results_inf, "infinite")
    plot_ev(results_single, "single")
    plot_ev(results_shoe, "shoe")

    plot_ev_comparison(results_inf, results_single, results_shoe)

    plot_outcome_per_deck(results_inf, "infinite")
    plot_outcome_per_deck(results_single, "single")
    plot_outcome_per_deck(results_shoe, "shoe")

    #plot_outcome_comparison(results_inf, results_single, results_shoe)

    print("\nGraphs saved in /graphs folder")


if __name__ == "__main__":
    main()