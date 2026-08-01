from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def build_graph(name, auctions, bid_ma, profit_ma, bid_pcts, profit_pcts, sample_idx, window):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax2 = ax.twinx()

    scale_min = -100
    scale_max = 100

    ax.set_ylim(scale_min, scale_max)
    ax2.set_ylim(scale_min, scale_max)
    ax2.set_yticks(ax.get_yticks())

    ax.plot(auctions, bid_ma, color='tab:blue', linewidth=2, label=f'Bid % (MA{window})')
    ax2.plot(auctions, profit_ma, color='tab:orange', linewidth=2, label=f'Profit % (MA{window})')
    ax.scatter([auctions[i] for i in sample_idx], [bid_pcts[i] for i in sample_idx], color='tab:blue', alpha=0.15, s=10, label='Exploring bid %')
    ax2.scatter([auctions[i] for i in sample_idx], [profit_pcts[i] for i in sample_idx], color='tab:orange', alpha=0.15, s=10)
    ax.set_xlabel('Auction')
    ax.set_ylabel('Bid % Adjustment', color='tab:blue')
    ax2.set_ylabel('Profit %', color='tab:orange')
    ax.set_title(f"graphs/{name}")
    ax.tick_params(axis='y', labelcolor='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:orange')
    ax.grid(True, alpha=0.4)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax.yaxis.set_major_locator(mticker.MaxNLocator(10))
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(10))
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc='upper left')
    fig.tight_layout()

    clean_name = name[:-4] if name.endswith('.png') else name
    output_dir = Path(__file__).resolve().parent / 'graphs'
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f'{clean_name}.png'
    fig.savefig(output_path, dpi=200)
    print(f'Saved plot to {output_path}')
    plt.close(fig)
    return str(output_path)
