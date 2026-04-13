art = """
┌┬┐┌─┐┌─┐┬┌─┐┬┌─┐┌┐┌        
 ││├┤ │  │└─┐││ ││││        
─┴┘└─┘└─┘┴└─┘┴└─┘┘└┘        
┌┬┐┬─┐┌─┐┌─┐                
 │ ├┬┘├┤ ├┤                 
 ┴ ┴└─└─┘└─┘                
┬  ┌─┐┌─┐┬─┐┌┐┌┬┌┐┌┌─┐      
│  ├┤ ├─┤├┬┘││││││││ ┬      
┴─┘└─┘┴ ┴┴└─┘└┘┴┘└┘└─┘      
┌─┐┬  ┌─┐┌─┐┬─┐┬┌┬┐┬ ┬┌┬┐┌─┐
├─┤│  │ ┬│ │├┬┘│ │ ├─┤│││└─┐
┴ ┴┴─┘└─┘└─┘┴└─┴ ┴ ┴ ┴┴ ┴└─┘
"""

noteMD="""
One-line summary: A decision tree classifies instances by sorting them down a tree of attribute tests, where each internal node tests one attribute and each leaf assigns a class label — and ID3 builds the tree by greedily choosing the attribute with the highest information gain at each step.

Imagine a game of 20 questions. You ask "Is it sunny?" — if yes, you ask "Is it humid?" — if no, you say "Go play!" You keep asking questions until you reach an answer. A decision tree is exactly this game, but the computer figures out which questions to ask first so it reaches the right answer as fast as possible — asking the most informative question each time.

Mitchell introduces decision trees as one of the most widely used and practical methods for inductive learning. A decision tree represents a disjunction of conjunctions of constraints on attribute values — which sounds complex but means simply: it is a flowchart of if-then-else rules, where each path from root to leaf encodes one rule.

The structure is precise. Each internal node in the tree represents a test on a single attribute. Each branch descending from that node corresponds to one possible value of that attribute. Each leaf node specifies the classification to be assigned — in the simplest case, a boolean class label (yes/no). To classify a new instance, you start at the root, test the attribute there, follow the branch matching the instance's value for that attribute, and repeat until you reach a leaf. Whatever label the leaf carries is the prediction.

The central question is how to build the tree from training data. Mitchell's answer is ID3 — the Iterative Dichotomiser 3 algorithm. ID3 builds the tree top-down, greedily, using a divide-and-conquer strategy. At each node, it selects the attribute that best classifies the current set of examples according to a statistical measure called information gain. The algorithm then recurses on the subsets of examples created by each branch, building subtrees until every subset is pure (all one class) or no attributes remain.

Information gain is defined using entropy, borrowed from information theory. Entropy measures the impurity of a set of examples — how mixed the class labels are. If all examples in a set belong to the same class, entropy is zero (perfectly pure). If the examples are split equally between two classes, entropy is 1 (maximally impure). Information gain for an attribute A is the reduction in entropy achieved by splitting the training set on A — how much "cleaner" the subsets become after the split. ID3 always picks the attribute with the highest information gain.

The resulting tree is guaranteed to be consistent with the training data, but it may overfit — memorising noise rather than learning the true concept. Mitchell addresses this through reduced-error pruning and rule post-pruning: converting the tree to rules and dropping conditions that do not improve accuracy on a held-out validation set. Decision trees also have a natural inductive bias: they prefer shorter trees (Occam's razor) and trees that place high-information-gain attributes near the root.
"""

tldr="""
A decision tree classifies instances by sorting them through a tree of
attribute tests. Each internal node tests one attribute; each leaf assigns
a class label.

ID3 builds the tree top-down and greedily. At each node it picks the
attribute A that maximizes information gain:

  Gain(S,A) = Entropy(S) - Σ (|Sv|/|S|) * Entropy(Sv)

  Entropy(S) = -p⊕ log₂(p⊕) - p⊖ log₂(p⊖)

Base cases: all examples same class → leaf. No attributes left → majority leaf.

Inductive bias: prefers shorter trees with high-gain attributes near the root
(implicit Occam's razor). Overfitting addressed through pruning.
"""

algo="""

ID3(Examples, Target_attribute, Attributes)

1. Create root node

2. If all Examples are positive:
       return root with label = +

3. If all Examples are negative:
       return root with label = -

4. If Attributes is empty:
       return root with label = most common value of
                                Target_attribute in Examples

5. A ← attribute in Attributes that best classifies Examples
         (i.e. highest Information Gain)

         where:

         Entropy(S)   = -p⊕ log₂(p⊕)  -  p⊖ log₂(p⊖)

         Gain(S, A)   = Entropy(S)
                        - Σ (|Sv| / |S|) × Entropy(Sv)
                          for each value v of A

6. Set decision attribute for root = A

7. For each possible value vi of A:
       a. Add a new branch below root for A = vi
       b. Sv = subset of Examples where A = vi
       c. If Sv is empty:
              Add leaf node with label = most common
              Target_attribute in Examples
          Else:
              Add subtree = ID3(Sv, Target_attribute,
                                Attributes \ {A})

8. Return root
"""
print(art)
#print(noteMD)
#print(tldr)
#print(algo)


# actual code yaha se shuru hain

def log2(x):
    if x == 0:
        return 0
    result = 0
    if x >= 1:
        while x >= 2:
            x /= 2
            result += 1
        x = x - 1
        ln_x = 0
        term  = x
        sign  = 1
        for n in range(1, 50):
            ln_x += sign * term / n
            term *= x
            sign *= -1
        ln2 = 0.6931471805599453
        result += ln_x / ln2
    else:
        while x < 1:
            x *= 2
            result -= 1
        x = x - 1
        ln_x = 0
        term  = x
        sign  = 1
        for n in range(1, 50):
            ln_x += sign * term / n
            term *= x
            sign *= -1
        ln2 = 0.6931471805599453
        result += ln_x / ln2
    return result

def entropy(examples):
    if not examples:
        return 0
    total  = len(examples)
    labels = [e[-1] for e in examples]
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    ent = 0.0
    for count in counts.values():
        p    = count / total
        ent -= p * log2(p)
    return ent

def information_gain(examples, attr_index):
    total        = len(examples)
    base_entropy = entropy(examples)
    values       = set(e[attr_index] for e in examples)
    weighted_ent = 0.0
    for v in values:
        subset       = [e for e in examples if e[attr_index] == v]
        weighted_ent += (len(subset) / total) * entropy(subset)
    return base_entropy - weighted_ent

def majority_label(examples):
    labels = [e[-1] for e in examples]
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    return max(counts, key=lambda k: counts[k])

def id3(examples, attributes):
    labels = [e[-1] for e in examples]

    # Base case 1: all examples same class
    if len(set(labels)) == 1:
        return {'leaf': labels[0]}

    # Base case 2: no attributes left
    if not attributes:
        return {'leaf': majority_label(examples)}

    # Pick attribute with highest information gain
    best_attr = attributes[0]
    best_gain = information_gain(examples, attributes[0])
    for a in attributes[1:]:
        gain = information_gain(examples, a)
        if gain > best_gain:
            best_gain = gain
            best_attr = a

    tree      = {'attribute': best_attr, 'branches': {}}
    remaining = [a for a in attributes if a != best_attr]

    # Branch on each value of best_attr
    values = set(e[best_attr] for e in examples)
    for v in values:
        subset = [e for e in examples if e[best_attr] == v]
        if not subset:
            tree['branches'][v] = {'leaf': majority_label(examples)}
        else:
            tree['branches'][v] = id3(subset, remaining)

    return tree

def classify(tree, instance):
    if 'leaf' in tree:
        return tree['leaf']
    val = instance[tree['attribute']]
    if val not in tree['branches']:
        return None
    return classify(tree['branches'][val], instance)

def print_tree(tree, attr_names, indent=0):
    pad = '    ' * indent
    if 'leaf' in tree:
        print(pad + '-> ' + tree['leaf'])
        return
    print(pad + '[' + attr_names[tree['attribute']] + ']')
    for val, subtree in tree['branches'].items():
        print(pad + '  ' + val + ':')
        print_tree(subtree, attr_names, indent + 1)


# Mitchell's PlayTennis dataset — Table 3.2 (exactly as in image)
attr_names = ['Outlook', 'Temperature', 'Humidity', 'Wind']

training_data = [
    #   Outlook     Temp    Humidity   Wind      PlayTennis
    ['Sunny',    'Hot',  'High',   'Weak',   'No' ],  # D1
    ['Sunny',    'Hot',  'High',   'Strong', 'No' ],  # D2
    ['Overcast', 'Hot',  'High',   'Weak',   'Yes'],  # D3
    ['Rain',     'Mild', 'High',   'Weak',   'Yes'],  # D4
    ['Rain',     'Cool', 'Normal', 'Weak',   'Yes'],  # D5
    ['Rain',     'Cool', 'Normal', 'Strong', 'No' ],  # D6
    ['Overcast', 'Cool', 'Normal', 'Strong', 'Yes'],  # D7
    ['Sunny',    'Mild', 'High',   'Weak',   'No' ],  # D8
    ['Sunny',    'Cool', 'Normal', 'Weak',   'Yes'],  # D9
    ['Rain',     'Mild', 'Normal', 'Weak',   'Yes'],  # D10
    ['Sunny',    'Mild', 'Normal', 'Strong', 'Yes'],  # D11
    ['Overcast', 'Mild', 'High',   'Strong', 'Yes'],  # D12
    ['Overcast', 'Hot',  'Normal', 'Weak',   'Yes'],  # D13
    ['Rain',     'Mild', 'High',   'Strong', 'No' ],  # D14
]

attributes = list(range(len(attr_names)))

tree = id3(training_data, attributes)

print("Decision Tree:")
print_tree(tree, attr_names)

test = ['Sunny', 'Cool', 'High', 'Strong']




