import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from collections import Counter
import random

RANKS = '2 3 4 5 6 7 8 9 T J Q K A'.split()
SUITS = 'spades diamonds clubs hearts'.split()


def generate_deck():
    return [(rank, suit) for rank in RANKS for suit in SUITS]


def deal_hand(deck):
    random.shuffle(deck)
    return deck[:5]


def is_royal_flush(hand):
    ranks_in_hand = [card[0] for card in hand]
    suits_in_hand = [card[1] for card in hand]
    return set(ranks_in_hand) == {'T', 'J', 'Q', 'K', 'A'} and len(set(suits_in_hand)) == 1


def is_straight_flush(hand):
    return is_straight(hand) and is_flush(hand)


def is_four_of_a_kind(hand):
    rank_counts = Counter(card[0] for card in hand)
    return 4 in rank_counts.values()


def is_full_house(hand):
    rank_counts = Counter(card[0] for card in hand)
    return set(rank_counts.values()) == {2, 3}


def is_flush(hand):
    suits_in_hand = [card[1] for card in hand]
    return len(set(suits_in_hand)) == 1


def is_straight(hand):
    ranks_in_hand = sorted(['23456789TJQKA'.index(card[0]) for card in hand])
    return ranks_in_hand == list(range(min(ranks_in_hand), min(ranks_in_hand) + 5)) or ranks_in_hand == [0, 1, 2, 3, 12]


def is_three_of_a_kind(hand):
    rank_counts = Counter(card[0] for card in hand)
    return 3 in rank_counts.values() and not is_full_house(hand)


def is_two_pair(hand):
    rank_counts = Counter(card[0] for card in hand)
    return len([count for count in rank_counts.values() if count == 2]) == 2


def is_one_pair(hand):
    rank_counts = Counter(card[0] for card in hand)
    return list(rank_counts.values()).count(2) == 1


hand_rank_checks = {
    'royal flush': is_royal_flush,
    'straight flush': is_straight_flush,
    'four of a kind': is_four_of_a_kind,
    'full house': is_full_house,
    'flush': is_flush,
    'straight': is_straight,
    'three of a kind': is_three_of_a_kind,
    'two pair': is_two_pair,
    'one pair': is_one_pair,
}


# GUI Application

class PokerSimulator(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Poker Hand Simulator')
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height
        self.handsCount = {'royal flush': 0, 'straight flush': 0, 'four of a kind': 0, 'full house': 0, 'flush': 0,
                           'straight': 0, 'three of a kind': 0, 'two pair': 0, 'one pair': 0, 'no hand': 0}
        self.lastHand = []
        self.totalSimulations = 0
        self.lastHandByRank = {rank: [] for rank in self.handsCount}
        self.initUI()

    def initUI(self):
        # Central widget and layout
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout()

        self.batchSizeComboBox = QComboBox()
        self.batchSizeComboBox.addItems(['1', '10', '100', '1,000', '10,000', '100,000'])
        layout.addWidget(self.batchSizeComboBox)

        self.runBatchButton = QPushButton('Run Batch Simulation')
        self.runBatchButton.clicked.connect(self.runBatchSimulation)
        layout.addWidget(self.runBatchButton)

        self.resetCountsButton = QPushButton('Reset Counts')
        self.resetCountsButton.clicked.connect(self.resetCounts)
        layout.addWidget(self.resetCountsButton)

        # Hand rank selection
        self.handRankComboBox = QComboBox()
        self.handRankComboBox.addItems(
            ['royal flush', 'straight flush', 'four of a kind', 'full house', 'flush', 'straight', 'three of a kind',
             'two pair', 'one pair'])
        layout.addWidget(self.handRankComboBox)

        # Start simulation button
        self.startButton = QPushButton('Start Simulation')
        self.startButton.clicked.connect(self.startSimulation)
        layout.addWidget(self.startButton)

        # Result label
        self.resultLabel = QLabel('Results will be shown here.')
        layout.addWidget(self.resultLabel)

        self.recentHandRankLabel = QLabel('Most recent hand rank will be shown here.')
        layout.addWidget(self.recentHandRankLabel)
        # Card images
        self.cardLabels = [QLabel() for _ in range(5)]
        cardsLayout = QHBoxLayout()
        for label in self.cardLabels:
            cardsLayout.addWidget(label)
            label.setFixedSize(100, 140)  # Set a fixed size for card images
        layout.addLayout(cardsLayout)

        self.lastHandMessageLabel = QLabel('Last hand will be shown here.')
        layout.addWidget(self.lastHandMessageLabel)

        self.handRankViewComboBox = QComboBox()
        self.handRankViewComboBox.addItems(['Select rank to view last hand'] + list(self.handsCount.keys()))
        layout.addWidget(self.handRankViewComboBox)

        self.viewLastHandButton = QPushButton('View Last Hand for Rank')
        self.viewLastHandButton.clicked.connect(self.displayLastHandForRank)
        layout.addWidget(self.viewLastHandButton)

        centralWidget.setLayout(layout)

    def simulate_all_hands(self, hand_rank):
        hands_count = {'royal flush': 0, 'straight flush': 0, 'four of a kind': 0, 'full house': 0, 'flush': 0,
                       'straight': 0, 'three of a kind': 0, 'two pair': 0, 'one pair': 0, 'no hand': 0}
        total_hands_dealt = 0
        hand_achieved = False

        while not hand_achieved:
            deck = generate_deck()
            hand = deal_hand(deck)
            total_hands_dealt += 1
            hand_found = False

            for rank, check in hand_rank_checks.items():
                if check(hand):
                    hands_count[rank] += 1
                    self.lastHandByRank[rank] = hand[:]  # Update the last hand for this rank
                    if rank == hand_rank:
                        hand_achieved = True
                    hand_found = True
                    break

            if not hand_found:
                hands_count['no hand'] += 1
                self.lastHandByRank['no hand'] = hand[:]  # Update for 'no hand'

        return total_hands_dealt, hand, hands_count

    def determine_hand_rank(self, hand):
        for rank_name, check_func in hand_rank_checks.items():
            if check_func(hand):
                return rank_name
        return 'no hand'

    def startSimulation(self):
        selectedHandRank = self.handRankComboBox.currentText()
        total_hands_dealt, hand, hands_count = self.simulate_all_hands(selectedHandRank)

        result_message = f"Hand achieved after {total_hands_dealt:,} simulations.\n\nHand counts:\n"
        for rank, count in hands_count.items():
            result_message += f"{rank}: {count:,}\n"

        self.resultLabel.setText(result_message)

        # Update card images
        for i, card in enumerate(hand):
            cardRank, cardSuit = card
            cardImageFile = f'card_images/{cardRank}_of_{cardSuit}.png'
            cardImage = QPixmap(cardImageFile)
            self.cardLabels[i].setPixmap(cardImage.scaled(100, 140, Qt.KeepAspectRatio))

        for i in range(len(hand), 5):
            self.cardLabels[i].clear()

    def runBatchSimulation(self):
        batchSize = int(self.batchSizeComboBox.currentText().replace(',', ''))
        self.totalSimulations += batchSize
        for _ in range(batchSize):
            deck = generate_deck()
            hand = deal_hand(deck)
            self.updateHandCounts(hand)
        self.updateGUI()

    def updateHandCounts(self, hand):
        hand_found = False
        for rank, check in hand_rank_checks.items():
            if check(hand):
                self.handsCount[rank] += 1
                self.lastHandByRank[rank] = hand[:]  # Store a copy of the hand
                hand_found = True
                break
        if not hand_found:
            self.handsCount['no hand'] += 1
            self.lastHandByRank['no hand'] = hand[:]
        self.lastHand = hand  # Keep this to still show the last hand from any batch

        # Update the most recent hand rank display
        recent_rank = self.determine_hand_rank(hand)
        self.recentHandRankLabel.setText(f"Most recent hand rank: {recent_rank}")

    def updateGUI(self):
        # Display total simulations count
        result_message = f"Total Simulations: {self.totalSimulations:,}\n\nHand counts:\n"
        for rank, count in self.handsCount.items():
            result_message += f"{rank}: {count:,}\n"

        self.resultLabel.setText(result_message)

        # Update card images for the last hand
        for i, card in enumerate(self.lastHand):
            cardRank, cardSuit = card
            cardImageFile = f'card_images/{cardRank}_of_{cardSuit}.png'
            cardImage = QPixmap(cardImageFile)
            self.cardLabels[i].setPixmap(cardImage.scaled(100, 140, Qt.KeepAspectRatio))

        for i in range(len(self.lastHand), 5):
            self.cardLabels[i].clear()

    def resetCounts(self):
        for rank in self.handsCount:
            self.handsCount[rank] = 0
        self.totalSimulations = 0
        self.lastHandByRank = {rank: [] for rank in self.handsCount}
        self.updateGUI()
        self.lastHandMessageLabel.setText('Last hand will be shown here.')
        self.recentHandRankLabel.setText(
            'Most recent hand rank will be shown here.')  # Reset the recent hand rank display

    def displayLastHandForRank(self):
        selectedRank = self.handRankViewComboBox.currentText()
        if selectedRank == 'Select rank to view last hand' or not self.lastHandByRank[selectedRank]:
            self.lastHandMessageLabel.setText("No hand available for this rank.")
            for label in self.cardLabels:
                label.clear()
            return

        hand = self.lastHandByRank[selectedRank]
        self.lastHandMessageLabel.setText(f"Last {selectedRank} hand:")

        # Update card images for the selected rank's last hand
        for i, card in enumerate(hand):
            cardRank, cardSuit = card
            cardImageFile = f'card_images/{cardRank}_of_{cardSuit}.png'
            cardImage = QPixmap(cardImageFile)
            self.cardLabels[i].setPixmap(cardImage.scaled(100, 140, Qt.KeepAspectRatio))

        for i in range(len(hand), 5):
            self.cardLabels[i].clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PokerSimulator()
    window.show()
    sys.exit(app.exec_())
