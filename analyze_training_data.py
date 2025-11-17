#!/usr/bin/env python3
"""
Analyze Training Data Distribution
Identify class imbalance and data quality issues
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.chatbot_training_data import get_all_training_samples, TRAINING_DATA

def analyze_data_distribution():
    """Analyze training data for class imbalance and quality issues"""

    print("="*70)
    print("TRAINING DATA DISTRIBUTION ANALYSIS")
    print("="*70)
    print()

    # Count samples per intent
    intent_counts = {}
    for intent, samples in TRAINING_DATA.items():
        intent_counts[intent] = len(samples)

    # Sort by count
    sorted_intents = sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)

    total_samples = sum(intent_counts.values())

    print(f"Total Training Samples: {total_samples}")
    print(f"Number of Intent Classes: {len(intent_counts)}")
    print(f"Average Samples per Intent: {total_samples / len(intent_counts):.1f}")
    print()

    print("="*70)
    print("PER-INTENT DISTRIBUTION")
    print("="*70)
    print(f"{'Intent':<25} {'Count':<10} {'Percentage':<12} {'Status'}")
    print("-"*70)

    max_count = max(intent_counts.values())
    min_count = min(intent_counts.values())
    avg_count = total_samples / len(intent_counts)

    for intent, count in sorted_intents:
        percentage = (count / total_samples) * 100

        # Determine status
        if count < avg_count * 0.5:
            status = "⚠️  SEVERELY UNDERREPRESENTED"
        elif count < avg_count * 0.8:
            status = "⚠️  Underrepresented"
        elif count > avg_count * 1.5:
            status = "⚠️  Overrepresented"
        else:
            status = "✓ Balanced"

        print(f"{intent:<25} {count:<10} {percentage:>6.2f}%      {status}")

    print()
    print("="*70)
    print("CLASS IMBALANCE METRICS")
    print("="*70)
    print(f"Largest class: {max_count} samples")
    print(f"Smallest class: {min_count} samples")
    print(f"Imbalance ratio: {max_count / min_count:.2f}x")
    print()

    if max_count / min_count > 3:
        print("⚠️  SEVERE CLASS IMBALANCE DETECTED!")
        print("   This will cause poor performance on underrepresented classes.")
        print()

    # Identify classes needing more samples
    print("="*70)
    print("RECOMMENDATIONS TO REACH 90%+ ACCURACY")
    print("="*70)

    target_samples = 80  # Target at least 80 samples per intent
    needs_improvement = []

    for intent, count in sorted_intents:
        if count < target_samples:
            deficit = target_samples - count
            needs_improvement.append((intent, count, deficit))

    if needs_improvement:
        print(f"\nIntents needing more training examples (target: {target_samples} samples):")
        print()
        for intent, current, needed in needs_improvement:
            print(f"  {intent:<25} Current: {current:>3}  →  Add {needed:>3} more examples")

        total_needed = sum(n[2] for n in needs_improvement)
        print()
        print(f"Total additional examples needed: {total_needed}")
    else:
        print("\n✓ All intents have sufficient training examples!")

    print()
    print("="*70)
    print("CRITICAL INSIGHTS")
    print("="*70)
    print()
    print("1. Class Imbalance Impact:")
    print(f"   - {max_count / min_count:.1f}x difference between largest and smallest class")
    print("   - This causes model bias toward larger classes")
    print("   - Explains CV fold scores as low as 66-68%")
    print()
    print("2. To Achieve 90%+ Accuracy:")
    print(f"   - Balance ALL intents to {target_samples}-120 samples each")
    print("   - Focus on quality, diverse examples (not duplicates)")
    print("   - Ensure examples cover edge cases and variations")
    print()
    print("3. GridSearchCV will help, but data quality is key!")
    print()

if __name__ == '__main__':
    analyze_data_distribution()
