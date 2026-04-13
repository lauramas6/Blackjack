# simulator.py --> Monte Carlo simulation

from game import BlackjackGame
from deck import Deck
import os
import matplotlib.pyplot as plt



# CORE SIMULATION
def simulate(policy, deck_type='infinite', num_games=100000):
    wins = 0
    losses = 0
    draws = 0

    deck = Deck(deck_type) if deck_type == "shoe" else None

    for _ in range(num_games):

        if deck_type != "shoe":
            deck = Deck(deck_type)

        game = BlackjackGame(deck)
        result = game.play(policy)

        if result == 1:
            wins += 1
        elif result == -1:
            losses += 1
        else:
            draws += 1

    win_rate = wins / num_games
    loss_rate = losses / num_games
    draw_rate = draws / num_games

    expected_value = win_rate - loss_rate

    return {
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "win_rate": win_rate,
        "loss_rate": loss_rate,
        "draw_rate": draw_rate,
        "expected_value": expected_value
    }


# UTIL
def create_graphs_folder():
    if not os.path.exists("graphs"):
        os.makedirs("graphs")


def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.1f}%",
            ha="center",
            va="bottom",
            fontsize=7
        )



# EV PLOT
def plot_ev(results, deck_type):
    names = [name for name, _ in results]
    evs = [res["expected_value"] for _, res in results]

    plt.figure()
    bars = plt.bar(names, evs)

    plt.title(f"Expected Value ({deck_type})")
    plt.xlabel("Policy")
    plt.ylabel("Expected Value")

    plt.xticks(rotation=30)
    plt.tight_layout()

    plt.savefig(f"graphs/{deck_type}_ev.png")
    plt.close()


# EV COMPARISON
def plot_ev_comparison(results_inf, results_single, results_shoe):
    names = [name for name, _ in results_inf]
    x = range(len(names))

    ev_inf = [res["expected_value"] for _, res in results_inf]
    ev_single = [res["expected_value"] for _, res in results_single]
    ev_shoe = [res["expected_value"] for _, res in results_shoe]

    plt.figure()

    # grouped bars
    bars1 = plt.bar([i - 0.25 for i in x], ev_inf, width=0.25, label="Infinite Deck")
    bars2 = plt.bar(x, ev_single, width=0.25, label="Single Deck")
    bars3 = plt.bar([i + 0.25 for i in x], ev_shoe, width=0.25, label="Shoe Deck (6)")

    # labels
    def add_ev_labels(bars):
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.3f}",
                ha="center",
                va="bottom",
                fontsize=7
            )

    add_ev_labels(bars1)
    add_ev_labels(bars2)
    add_ev_labels(bars3)

    plt.xticks(list(x), names, rotation=30)
    plt.title("EV Comparison: Infinite vs Single vs Shoe Deck")
    plt.ylabel("Expected Value")
    plt.legend()

    plt.tight_layout()
    plt.savefig("graphs/ev_comparison.png")
    plt.close()


# OUTCOME PER DECK
def plot_outcome_per_deck(results, deck_type):
    names = [name for name, _ in results]
    x = range(len(names))

    wins = [res["win_rate"] * 100 for _, res in results]
    losses = [res["loss_rate"] * 100 for _, res in results]
    draws = [res["draw_rate"] * 100 for _, res in results]

    plt.figure()

    bars1 = plt.bar(x, wins, width=0.25, label="Win", color="green")
    bars2 = plt.bar([i + 0.25 for i in x], losses, width=0.25, label="Loss", color="red")
    bars3 = plt.bar([i + 0.5 for i in x], draws, width=0.25, label="Draw", color="gray")

    add_labels(bars1)
    add_labels(bars2)
    add_labels(bars3)

    plt.xticks(list(x), names, rotation=30)
    plt.title(f"Outcome Rates ({deck_type} deck)")
    plt.ylabel("Percentage (%)")
    plt.ylim(0, 100)
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"graphs/{deck_type}_outcomes.png")
    plt.close()


# OUTCOME COMPARISON
""""
def plot_outcome_comparison(results_inf, results_single, results_shoe):
    names = [name for name, _ in results_inf]
    x = range(len(names))

    def extract(results, key):
        return [res[key] * 100 for _, res in results]

    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.1f}%",
                ha="center",
                va="bottom",
                fontsize=7
            )

    #  WIN RATE 
    plt.figure()

    bars1 = plt.bar([i - 0.25 for i in x], extract(results_inf, "win_rate"), width=0.2, label="Inf")
    bars2 = plt.bar(x, extract(results_single, "win_rate"), width=0.2, label="Single")
    bars3 = plt.bar([i + 0.25 for i in x], extract(results_shoe, "win_rate"), width=0.2, label="Shoe")

    add_labels(bars1)
    add_labels(bars2)
    add_labels(bars3)

    plt.xticks(list(x), names, rotation=30)
    plt.title("Win Rate Comparison")
    plt.ylabel("Percentage (%)")
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()
    plt.savefig("graphs/win_rate_comparison.png")
    plt.close()

    # LOSS RATE 
    plt.figure()

    bars1 = plt.bar([i - 0.25 for i in x], extract(results_inf, "loss_rate"), width=0.2, label="Inf")
    bars2 = plt.bar(x, extract(results_single, "loss_rate"), width=0.2, label="Single")
    bars3 = plt.bar([i + 0.25 for i in x], extract(results_shoe, "loss_rate"), width=0.2, label="Shoe")

    add_labels(bars1)
    add_labels(bars2)
    add_labels(bars3)

    plt.xticks(list(x), names, rotation=30)
    plt.title("Loss Rate Comparison")
    plt.ylabel("Percentage (%)")
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()
    plt.savefig("graphs/loss_rate_comparison.png")
    plt.close()

    # DRAW RATE 
    plt.figure()

    bars1 = plt.bar([i - 0.25 for i in x], extract(results_inf, "draw_rate"), width=0.2, label="Inf")
    bars2 = plt.bar(x, extract(results_single, "draw_rate"), width=0.2, label="Single")
    bars3 = plt.bar([i + 0.25 for i in x], extract(results_shoe, "draw_rate"), width=0.2, label="Shoe")

    add_labels(bars1)
    add_labels(bars2)
    add_labels(bars3)

    plt.xticks(list(x), names, rotation=30)
    plt.title("Draw Rate Comparison")
    plt.ylabel("Percentage (%)")
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()
    plt.savefig("graphs/draw_rate_comparison.png")
    plt.close()
"""