% Solution Writeup: GCD of Fibonacci Subsets


# GCD of Fibonacci Subsets  
## Solution Writeup

**Contest:** [TAMa 2023](https://noi.ph/tama-2023/)  
**Problem Idea:** Cisco Ortega  
**Testing:** Amanda Lim, Cassidy Tan  
**Statement:** Cisco Ortega  
**Test Data Preparation:** Kevin Atienza  
**Solution Writeup:** Cisco Ortega, Kevin Atienza  



<details class="editorial-section"><summary class="h2">Subtask 1</summary>

Let&rsquo;s build some intuition.  Here are the first $n=12$ Fibonacci numbers:
$$
    1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233
$$
Maybe you then get the feeling that: most of these subsets would yield a gcd of $1$!  

To formalize this, we note that if $x$ and $y$ have a gcd of $1$, then **any** subset that contains $x$ and $y$ will automatically have a gcd of $1$ as well!  A single pair of coprime $x$ and $y$ will &ldquo;contaminate&rdquo; the entire subset.  So, as a necessary condition for some subset $A$ to have a gcd greater than $1$, each _pair_ of elements in $A$ must already have a gcd greater than $1$.

But looking at the first $12$ Fibonacci numbers, most pairs seem to be coprime!

We note the following subsets of the first $12$ Fibonacci numbers:

- Divisible by $2$: $\{2, 8, 34, 144\}$
- Divisible by $3$: $\{3, 21, 144\}$
- Divisible by $5$: $\{5, 55\}$

and from there we can compute the answer (even by hand!) with the following series of steps:

- The gcd of a singleton set $\{x\}$ is $x$.
- All subsets of $\{2, 8, 34, 144\}$ with at least $2$ elements have a gcd of $2$ (\textbf{except for} $\{8, 144\}$, whose gcd is $8$)
- All subsets of $\{3, 21, 144\}$ with at least $2$ elements have a gcd of $3$
- $\{5, 55\}$ has a gcd of $5$
- **All** other subsets of the first $12$ Fibonacci numbers have a gcd of $1$.

We have now reduced the problem to counting the number of subsets of some set, which is classic in combinatorics.

</details>



<details class="editorial-section"><summary class="h2">Subtask 2</summary>

First, note that $2^{54} \approx 1.8 \times 10^{16} \gg 10^8$, so it is not feasible to brute force over all subsets.  We need something a little smarter.  To solve subtask 2, I expect most solutions will still leverage the insight of: _these Fibonacci numbers seem to often not share common factors with that many other Fibonacci numbers_.  

There are many possible approaches that use this insight.  Here are some solutions.  Let the first $n$ Fibonacci numbers be indexed $S = \{f_1, f_2, f_3, \dots, f_{n}\}$.[^1]


### Summing based on the minimum element

All non-empty subsets of $S$ have a minimum element.  _Fix_ an index $i$, and suppose we _only_ consider subsets whose minimum element is $f_i$ (thus the &ldquo;minimum index&rdquo; is $i$).

- Because $f_i$ is the minimum, it&rsquo;s always in the subsets we&rsquo;re considering
-  Let $S' = \{f_j \mid i < j ~\text{and}~ \gcd(f_i, f_j) > 1\}$, i.e., we filter out _only_ the larger Fibonacci numbers that share a common factor with $f_i$ (a necessary condition for the gcd to be greater than $1$)
-  First, consider subsets with $f_i$ as the minimum, such that all other elements are in $S'$ (i.e., all share a common factor with $f_i$)
    -  **Brute force** all subsets $A'$ of $S'$
    -  For each one, compute $\gcd(\{f_i\} \cup A')$ and add that gcd to the total.
    -  There are $2^{|S'|}$ such subsets that we need to consider, and if $S'$ is usually small, then this is okay.
-  Next, consider subsets with $f_i$ as the minimum that contain an element _not_ in $S'$ (i.e., share _no_ common factors with $S'$)
    -  Any subset that contains $f_i$ and a number it shares no common factors with will _automatically_ have a gcd of $1$!
    -  Among $f_1$ to $f_n$, there are $n-i$ numbers greater than $f_i$
    -  Thus, there are $2^{n-i}$ subsets that have $f_i$ as the minimum element
    -  Thus, there are $2^{n-i} - 2^{|S'|}$ subsets that have $f_i$ as the minimum element and contain at least one other element not in $S'$.
    -  Since each of these subsets yields a gcd of $1$, we add $2^{n-i} - 2^{|S'|}$ to our total.

This solves the problem for a fixed $i$; so, to solve the full problem, we run this solution across all $i$ from $1$ to $n$ (i.e., consider all possible minimum elements) and sum up all the subtotals.

If $n=54$, then we can check that this solution is fast enough, because $\sum_i 2^{S'} = 2935312 \ll 10^8$.

<div class="remarks">
Some final notes:

-  To easily enumerate all subsets of some universal set, consider **bitmasking**
-  To easily find the gcd of a pair of numbers, use the **Euclidean algorithm**
</div>


### Producing gcds of sets recursively

This solution produces the gcds of the sets recursively, and makes use of the fact that the values of gcd are all divisors of some $f_i \in S$. For simplicity, we include the empty set in our enumeration and say that the empty set has gcd $0$; note that $\gcd(0, n) = n$ for any $n$ in the usual definition of $\gcd$, so this won&rsquo;t affect our sum.

Every subset of $S_n := \{f_1, \ldots, f_n\}$ is formed by taking a subset of $S_{n-1} := \{f_1, \ldots, f_{n-1}\}$, and then either inserting or not inserting $f_n$ to it. (Note that $S_{n-1}$ has $2^{n-1}$ subsets.) Now, suppose we have a subset $T \subseteq S_{n-1}$ whose gcd is $g$. If we insert $f_n$ to $T$, the new gcd will clearly be $\gcd(g, f_n)$. (Check!) Therefore, if the list of gcds of all subsets of $S_{n-1}$ is $(g_1, g_2, \ldots, g_{2^{n-1}})$, then the list of gcds of all subsets of $S_n$ is
$$(g_1, g_2, \ldots, g_{2^{n-1}}, h_1, h_2, \ldots, h_{2^{n-1}})$$
where $h_i = \gcd(g_i, f_n)$. Thus, we can build the list of all gcds with recursion.

So far, this still isn&rsquo;t that much better than the usual brute force&mdash;we&rsquo;re still essentially going through all subsets. However, we can dramatically speed this up by only listing the *distinct* values of the gcd, and keeping track of their *counts*. (In other words, we&rsquo;re keeping a &ldquo;frequency table&rdquo; of the gcds.) This is okay because we don&rsquo;t really need the subsets themselves, but only their *gcds*, and subsets with the same gcd behave pretty much identically as far as we&rsquo;re concerned, so it makes sense to handle them all simultaneously.

Doing it this way, the size of our data is no longer proportional to $2^n$, but to the number of *distinct* gcd values (which are all divisors of all $f_i \in S$). Finally, once we have the counts of the gcds of $S$, we can simply sum them all up by weighting each distinct gcd value by its count!

A possible implementation in Python now looks like the following. Here `gs`{.python} represents the frequency table. In Python, the most natural way to make a frequency table would be to use the [`Counter`{.python}](https://docs.python.org/3/library/collections.html#collections.Counter) class (from the [`collections`{.python}](https://docs.python.org/3/library/collections.html) library).[^2]
```python
from collections import Counter
from math import gcd

mod = 998_244_353

def insert_value(gs, f):
    for g, c in [*gs.items()]:
        g = gcd(g, f)
        gs[g] = (gs[g] + c) % mod

def solve(n):
    gs = Counter([0])
    a, b = 0, 1
    for it in range(n):
        a, b = b, a + b
        insert_value(gs, b)
    return sum(g * c for g, c in gs.items()) % mod
```
Now, what&rsquo;s the running time of this solution? Clearly it depends a lot on the number of *distinct* possible gcds. We have an upper bound, which is the total number of distinct divisors of all $f_i \in S$. Well, this is somewhat hard to compute...

...But actually, we don&rsquo;t have to compute a bound at all! We can simply run the algorithm for increasing values of $n$ to see whether the number of distinct gcds grows too fast for the computer to handle, or grows reasonably tamely. And as it turns out, for $n = 54$ it&rsquo;s pretty much instantaneous!

<div class="task">
**Exercise:** You can actually see how many distinct gcd values there are by simply printing the size of `gs`{.python} at the end of each loop iteration! In other words, simply insert the line `print(len(gs))`{.python} at the end of the `for`{.python} loop above.

Do this and see for yourself that there really are only a few distinct values of the gcd.

In fact, if you go ahead and do this, **you&rsquo;ll actually notice something quite peculiar...**
</div>

</details>



<details class="editorial-section"><summary class="h2">Subtask 3</summary>

<div class="remarks">
*Construction ongoing!* &nbsp;&nbsp; &#127959; &#128679; &#128679; &#128679; &#128679; &#128679; &#128679; &#128679; &#128679; &#128679; &#128679; &#128679; &#129521;
</div>

</details>


[^1]: Note that $f_1 = 1$ and $f_2 = 2$, which differs from the usual indexing of Fibonacci numbers (where $F_1 = 1$ and $F_2 = 1$).

[^2]: Here, `gs.items()`{.python} enumerates all key-value pairs (which in this case is the gcd value and the count), and `[*x]` creates a copy of the list. Note that it&rsquo;s important that we make a copy of the list to not mess up the calculations! (Why?)
