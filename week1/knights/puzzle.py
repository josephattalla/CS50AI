from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # AKnave or Aknight, not both
    And(Or(AKnave, AKnight), Not(And(AKnight, AKnave))),
    # AKnave implies not AKnight and AKnave
    Implication(AKnave, Not(And(AKnight, AKnave))),
    # AKnight implies AKnight and AKnave
    Implication(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # AKnave or Aknight, not both
    And(Or(AKnave, AKnight), Not(And(AKnight, AKnave))),
    # BKnave or BKnight, not both
    And(Or(BKnave, BKnight), Not(And(BKnight, BKnave))),
    # AKnave implies not AKnave and BKnave
    Implication(AKnave, Not(And(AKnave, BKnave))),
    # AKnight implies AKnave and BKnave
    Implication(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # AKnave or Aknight, not both
    And(Or(AKnave, AKnight), Not(And(AKnight, AKnave))),
    # BKnave or BKnight, not both
    And(Or(BKnave, BKnight), Not(And(BKnight, BKnave))),
    # AKnave implies not AKnave and BKnave or AKnight and BKnight
    Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),
    # BKnave implies not AKnave and BKnight or AKnight and BKnave
    Implication(BKnave, Not(Or(And(AKnave, BKnight), And(AKnight, BKnave)))),
    # AKnight implies AKnave and BKnave or AKnight and BKnight
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    # BKnight implies AKnave and BKnight or AKnight and BKnave
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # AKnave or Aknight, not both
    And(Or(AKnave, AKnight), Not(And(AKnight, AKnave))),
    # BKnave or BKnight, not both
    And(Or(BKnave, BKnight), Not(And(BKnight, BKnave))),
    # CKnave or CKnight, not both
    And(Or(CKnave, CKnight), Not(And(CKnave, CKnight))),
    # AKnight implies AKnight or AKnave
    Implication(AKnight, Or(AKnight, AKnave)),
    # AKnave implies not AKnave or AKnight
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    # BKnight implies AKnave
    Implication(BKnight, AKnave),
    # BKnave implies not AKnave
    Implication(BKnave, Not(AKnave)),
    # BKnight implies CKnave
    Implication(BKnight, CKnave),
    # BKnave implies not CKnave
    Implication(BKnave, Not(CKnave)),
    # CKnight implies AKnight
    Implication(CKnight, AKnight),
    # CKnave implies not AKnight
    Implication(CKnave, Not(AKnight))
    
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
