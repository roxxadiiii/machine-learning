

art="""
░█▀▀░█▀█░█▀█░█▀▄░▀█▀░█▀▄░█▀█░▀█▀░█▀▀        
░█░░░█▀█░█░█░█░█░░█░░█░█░█▀█░░█░░█▀▀        
░▀▀▀░▀░▀░▀░▀░▀▀░░▀▀▀░▀▀░░▀░▀░░▀░░▀▀▀        
░█▀▀░█░░░▀█▀░█▄█░▀█▀░█▀█░█▀█░▀█▀░▀█▀░█▀█░█▀█
░█▀▀░█░░░░█░░█░█░░█░░█░█░█▀█░░█░░░█░░█░█░█░█
░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀░▀░▀░▀░░▀░░▀▀▀░▀▀▀░▀░▀
"""
notesMD="""
 Candidate elimination is a supervised learning algorithm that searches the hypothesis space by maintaining two boundaries the most specific (S) and most general (G) consistent hypotheses and shrinks the space between them with each training example until only the target concept remains.


eli5:Imagine we are trying to guess a secret rule for which days are "good days to play outside." You start with two guesses: 

- one ridiculously strict ("only sunny, warm, weekend mornings with no wind")
- one ridiculously loose ("every single day is good")

Every time someone shows you a day that IS a good day, you relax your strict guess a little to include it.
Every time they show you a day that is NOT good, you tighten your loose guess to exclude it. You keep adjusting both ends until they agree — and whatever's left in between is the rule.

candidate elimination in the context of concept learning — the problem of inferring a general rule (a concept) from a set of labeled training examples. A concept is a boolean function over instances: for each instance, is it a member of the concept or not?

The key insight is that rather than searching through individual hypotheses one at a time, you can represent the entire set of hypotheses that are consistent with all training examples seen so far. Mitchell calls this set the version space with respect to hypothesis space H and training set D. The version space is defined precisely: it is the subset of all hypotheses in H that correctly classify every example in D.

The algorithm represents this version space implicitly using two boundary sets, rather than listing every consistent hypothesis explicitly. The specific boundary S contains the maximally specific hypotheses — the hypotheses that classify the fewest instances as positive while still being consistent with all positive examples. The general boundary G contains the maximally general hypotheses those that classify the most instances as positive while still being consistent with all negative examples. Every consistent hypothesis lies between these two boundaries: it is more general than or equal to some member of S, and more specific than or equal to some member of G.

The update rules, per Mitchell, are as follows. For each positive training example d: remove from G any hypothesis inconsistent with d; for each hypothesis s in S that is inconsistent with d, remove it and replace it with its minimal generalizations h such that h is consistent with d and some member of G is more general than h; then remove from S any hypothesis more general than another member of S. For each negative training example d: remove from S any hypothesis inconsistent with d; for each hypothesis g in G that is inconsistent with d, remove it and replace it with its minimal specializations h such that h is consistent with d and some member of S is more specific than h; then remove from G any hypothesis less general than another member of G.

When the algorithm converges, if S and G collapse to the same single hypothesis, that hypothesis is the target concept. If S and G become empty, the training data was inconsistent. If the version space still spans multiple hypotheses, then the training data was insufficient to uniquely identify the concept.

An important property established by Mitchell: the version space representation theorem states that a hypothesis h is in the version space if and only if it is more general than or equal to some member of S, and more specific than or equal to some member of G. This means S and G together fully and compactly represent the entire version space.

"""
tldr = """

## Candidate elimination algorithm

Searches the hypothesis space by maintaining two boundary sets:
S (maximally specific consistent hypotheses) and G (maximally general).
Together S and G implicitly represent the version space — all hypotheses
consistent with every training example seen so far.

Update rules (Mitchell):
- Positive example → generalise S minimally to cover; prune G of inconsistents.
- Negative example → specialise G minimally to exclude; prune S of inconsistents.

Convergence: if S = G = one hypothesis → target concept found.
If version space empty → inconsistent training data.
If multiple hypotheses remain → insufficient data to determine concept.

No inductive bias: the algorithm will not commit beyond what the data supports.

"""
algo = """
CANDIDATE-ELIMINATION Algorithm

Initialize G to the set of maximally general hypotheses in H
    G = { ('?', '?', '?', ..., '?') }

Initialize S to the set of maximally specific hypotheses in H
    S = { ('0', '0', '0', ..., '0') }

For each training example d, do:

    If d is a POSITIVE example:
        1. Remove from G any hypothesis inconsistent with d
        2. For each hypothesis s in S that is NOT consistent with d:
               a. Remove s from S
               b. Add to S all minimal generalizations h of s such that:
                      - h is consistent with d, AND
                      - some member of G is more general than h
               c. Remove from S any hypothesis more general than
                  another hypothesis in S

    If d is a NEGATIVE example:
        1. Remove from S any hypothesis inconsistent with d
        2. For each hypothesis g in G that is NOT consistent with d:
               a. Remove g from G
               b. Add to G all minimal specializations h of g such that:
                      - h is consistent with d, AND
                      - some member of S is more specific than h
               c. Remove from G any hypothesis less general than
                  another hypothesis in G

Return S, G
"""

print(art)
#print(notesMD)
#print(tldr)
#print(algo)

# actual code is below <3
def is_consistent(h, d):
    for i in range(len(h)):
        if h[i] == '0':
            return False
        if h[i] != '?' and h[i] != d[i]:
            return False
    return True

def is_more_general_or_equal(g, s):
    for i in range(len(g)):
        if g[i] == '?':
            continue
        if s[i] == '?' and g[i] != '?':
            return False
        if g[i] != s[i]:
            return False
    return True

def is_more_general(g, s):
    return (is_more_general_or_equal(g, s) and
            not is_more_general_or_equal(s, g))

def minimal_generalizations(s, d):
    h = list(s)
    for i in range(len(d)):
        if h[i] == '0':
            h[i] = d[i]
        elif h[i] != d[i]:
            h[i] = '?'
    return [tuple(h)]

def minimal_specializations(g, d, S, col_domains):
    specializations = []
    for i in range(len(d)):
        if g[i] == '?':
            for v in col_domains[i]:
                if v != d[i]:
                    h = list(g)
                    h[i] = v
                    ht = tuple(h)
                    if any(is_more_general_or_equal(ht, s) for s in S):
                        specializations.append(ht)
    return specializations

def candidate_elimination(training_data):
    num_attrs = len(training_data[0]) - 1

    col_domains = []
    for i in range(num_attrs):
        domain = list({row[i] for row in training_data})
        col_domains.append(domain)

    G = [tuple(['?'] * num_attrs)]
    S = [tuple(['0'] * num_attrs)]

    print(f"Initial S = {S}")
    print(f"Initial G = {G}\n")

    for idx, row in enumerate(training_data):
        d     = row[:-1]
        label = row[-1]

        print(f"--- Example {idx+1}: {d}  Label: {label} ---")

        if label == 'Yes':

            G = [g for g in G if is_consistent(g, d)]

            S_new = []
            for s in S:
                if not is_consistent(s, d):
                    for h in minimal_generalizations(s, d):
                        if (is_consistent(h, d) and
                                any(is_more_general_or_equal(g, h) for g in G)):
                            S_new.append(h)
                else:
                    S_new.append(s)

            S = [s for s in S_new
                 if not any(is_more_general(s, s2)
                            for s2 in S_new if s != s2)]

        elif label == 'No':

            S = [s for s in S if not is_consistent(s, d)]

            G_new = []
            for g in G:
                if is_consistent(g, d):
                    for h in minimal_specializations(g, d, S, col_domains):
                        if (not is_consistent(h, d) and
                                any(is_more_general_or_equal(h, s) for s in S)):
                            G_new.append(h)
                else:
                    G_new.append(g)

            G = [g for g in G_new
                 if not any(is_more_general(g2, g)
                            for g2 in G_new if g != g2)]

        print(f"S = {S}")
        print(f"G = {G}\n")

    print("=" * 60)
    print(f"Final S = {S}")
    print(f"Final G = {G}")

    return S, G


# Mitchell's EnjoySport dataset — Table 2.1
enjoysport_data = [
    #  Sky      AirTemp  Humidity   Wind      Water    Forecast   EnjoySport
    ['Sunny',  'Warm',  'Normal',  'Strong', 'Warm',  'Same',    'Yes'],
    ['Sunny',  'Warm',  'High',    'Strong', 'Warm',  'Same',    'Yes'],
    ['Rainy',  'Cold',  'High',    'Strong', 'Warm',  'Change',  'No' ],
    ['Sunny',  'Warm',  'High',    'Strong', 'Cool',  'Change',  'Yes'],
]

S_final, G_final = candidate_elimination(enjoysport_data)
