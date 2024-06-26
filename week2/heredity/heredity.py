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

    joint = 1

    # loop through people
    for person in people:

        gene = 1 if person in one_gene else 2 if person in two_genes else 0

        # if no parent data, set gene probability to given probability
        if not people[person]['mother'] and not people[person]['father']:
                gene_prob = PROBS['gene'][gene]
    
        # else calculate the probability their parents will pass the gene
        else:
            mother = 0.5 if people[person]['mother'] in one_gene else 1-PROBS['mutation'] if people[person]['mother'] in two_genes else PROBS['mutation']
            father = 0.5 if people[person]['father'] in one_gene else 1-PROBS['mutation'] if people[person]['father'] in two_genes else PROBS['mutation']
        
            # if person is in one_gene add the probabilities that their mother will pass the gene and their father will pass the gene, but not both at same time
            if gene == 1:
                gene_prob = (mother*(1-father)) + (father*(1-mother))             
            
            # if person is in two_genes multiply the probabilities that their mother will pass the gene and their father will pass the gene
            elif gene == 2:
                gene_prob = mother * father

            # else person has no gene, probality mother doesn't pass gene * probability father doesn't pass gene
            else:
                gene_prob = (1 - mother) * (1 - father)


        # multiple the joing prob by the probability current person has their gene and their trait
        joint *= gene_prob * PROBS["trait"][gene][person in have_trait] 

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
