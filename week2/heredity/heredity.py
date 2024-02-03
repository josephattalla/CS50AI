import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    
    # creates dictionary with name, mother, father, trait keys
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    print(joint_probability(people, {"Ron"}, {"Molly"}, {"Arthur"}))
    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    
    # list to hold the calculated probabilities
    probabilities = []
    # loop through people
    for person in people:

        # bool to track if person's parents data is present
        parents = True

        # if no parent data, set parents to false
        if not people[person]['mother'] and not people[person]['father']:
                parents = False
        # else calculate the probability the parent will pass the gene
        else:
            if people[person]['mother'] in one_gene:
                mother = 0.5-PROBS['mutation']
            elif people[person]['mother'] in two_genes:
                mother = 1-PROBS['mutation']
            else:
                mother = PROBS['mutation'] 
            if people[person]['father'] in one_gene:
                father = 0.5-PROBS['mutation']
            elif people[person]['father'] in two_genes:
                father = 1-PROBS['mutation']
            else:
                father = PROBS['mutation']
        
        # if person is in one_gene add the probabilities that their mother will pass the gene and their father will pass the gene
        if person in one_gene:
            gene = 1
            if parents: gene_prob = (mother*(1-father)) + (father*(1-mother))
            # if no parent data use given probability of one gene
            else: gene_prob = PROBS["gene"][1]
        
        # if person is in two_genes multiply the probabilities that their mother will pass the gene and their father will pass the gene
        elif person in two_genes:
            gene = 2
            if parents: gene_prob = mother * father
            # if no parent data use given probability of 2 genes
            else: gene_prob = PROBS["gene"][2]

        # else person has no gene, 1-prob(one or two genes)
        else:
            gene = 0
            if parents: gene_prob = 1 - ((mother + father) - (mother * father))
            # if no parent data use given probability of no gene
            else: gene_prob = PROBS['gene'][0]

        print(f"****{person}: {gene}: {gene_prob}*****")

        # if person in have_trait multiply the prob they have their gene and prob of having the trait
        if person in have_trait:
            probabilities.append(gene_prob * PROBS["trait"][gene][True])
            print(f"****{gene}: {person}: prob: {gene_prob * PROBS['trait'][gene][True]}*****")
        else:
            probabilities.append(gene_prob * PROBS["trait"][gene][False])
            print(f"****{gene}: {person}: prob: {gene_prob * PROBS['trait'][gene][False]}*****")
        
    joint = 1
    for i in probabilities:
        joint *= i

    return joint


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    # loop through probabilities
    for person in probabilities:
        
        # update the corresponding values of person in probabilities if they are in the given categories
        if person in one_gene:
            probabilities[person]['gene'][1] += p
        elif person in two_genes:
            probabilities[person]['gene'][2] += p
        else:
            probabilities[person]['gene'][0] += p
        
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    # loop through people
    for person in probabilities:

        # loop through the joint probabilities in person
        for joint_prob in probabilities[person]:

            # get values of the joint probability
            values = list(probabilities[person][joint_prob].values())

            # if they already sum to one don't do anything to it and continue 
            if sum(values) == 1:
                continue
            
            # get the number to multiply each value by and multiply each value by it
            alpha = 1 / sum(values)
            for value in probabilities[person][joint_prob]:
                probabilities[person][joint_prob][value] *= alpha
            
            


if __name__ == "__main__":
    main()
