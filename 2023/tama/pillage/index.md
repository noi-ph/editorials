% Solution Writeup: Pillage Twilight Heroes


# Pillage Twilight Heroes  
## Solution Writeup

**Contest:** [TAMa 2023](https://noi.ph/tama-2023/)  
**Problem Idea:** Cassidy Tan  
**Testing:** Vincent dela Cruz  
**Statement:** Cassidy Tan  
**Test Data Preparation:** Kevin Atienza  
**Solution Writeup:** Kevin Atienza  



<div class="editorial-section">

## Remark: $a/b$ modulo $998244353$?

In this editorial, I'll pretend that we're *computing the full answer* (a rational number) instead of *the answer modulo $998244353$*. It turns out that many exact solutions can be adapted to compute the answer modulo something instead. A bonus section below describes how to do it.
</div>


<details class="editorial-section"><summary class="h2">Subtask 1</summary>

For Subtask 1, I'll describe a solution that doesn't use a lot of insights and essentially only uses **dynamic programming** (DP) (aside from the definition of [expected value](https://en.wikipedia.org/wiki/Expected_value)). You could also solve this subtask with *pen and paper* by using the solution for Subtask 2, which is perfectly doable by hand (and easier to implement as well).


### Expected value &#x21DD; Counting

If you have some sort of &ldquo;random variable&rdquo; $X$, then we say that the **expected value** of $X$, denoted $\operatorname{E}[X]$, is the weighted sum of the possible results of $X$, weighted by their probabilities. More formally, if the possible results are $\{x_1, x_2, \ldots, x_k\}$ with respective probabilities $p_1, p_2, \ldots, p_k$, then
$$\operatorname{E}[X] := p_1x_1 + p_2x_2 + \ldots + p_kx_k,$$
or in summation notation,
$$\operatorname{E}[X] := \sum_{i=1}^k p_ix_i.$$
The expected value of $X$ can be thought of as the *average* value of $X$, when an experiment is performed many, many times and averaging the value of $X$ across them.

Here are some examples:

- If $X$ represents the result of throwing a die, then the possible results are $\{1, 2, \ldots, 6\}$, each with probability $1/6$, so the expected value is
$$\operatorname{E}[X] = \frac{1}{6}\cdot 1 + \frac{1}{6}\cdot 2 + \ldots + \frac{1}{6}\cdot 6 = \frac{1}{6}(1 + 2 + \ldots + 6) = \frac{21}{6} = 3.5.$$
- If $Y$ represents the *sum* of the results of throwing two dice, then the possible results are $\{2, 3, 4, \ldots, 12\}$. The probabilities are no longer uniform, e.g., $7$ is much more probable than $2$ or $12$. The full table of probabilities is:
    $$\begin{array}{r|ccccccccccc}
    \text{result}      & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 & 11 & 12 \\
    \hline
    \text{probability} & \frac{1}{36} & \frac{2}{36} & \frac{3}{36} & \frac{4}{36} & \frac{5}{36} & \frac{6}{36} & \frac{5}{36} & \frac{4}{36} & \frac{3}{36} & \frac{2}{36} & \frac{1}{36}
\end{array}$$
and you can check that the expected value of $Y$ is
$$\operatorname{E}[Y] = \frac{252}{36} = 7.$$

So let's define a random variable $T$ representing the result of the process outlined in the problem statement. The process chooses $w$ numbers randomly[^1] between $1$ and $k$, and $T$ is calculated as the *sum* of the $n$ largest elements, so the possible results are between $n$ and $nk$. If we write the probability of obtaining the result $t$ as $p_t$, then the answer is
$$\operatorname{E}[T] = \sum_{t=n}^{nk}\, p_t\,t.$$
So we are done if we can compute $p_t$ for each $t$ from $n$ to $nk$.

Now, the process has $k^w$ possible outcomes&mdash;namely all the sequences of length $w$, each element of which is between $1$ and $k$&mdash;and each of those outcomes is equally likely. Therefore, we can simply *count* the number of outcomes that result in a sum of $t$, then divide by $k^w$ to get the probability. If we write the *number* of sequences whose sum of $n$ largest elements is $t$ as $c_t$, then we simply have
$$p_t = \frac{c_t}{k^w}.$$

So we've now reduced the problem to computing the $c_t$s. Now, a sum of $t$ can arise in multiple ways. For example, if $n = 3$ and $t = 10$, then the top $3$ values of the sequence (each in sorted order) could be $[2, 3, 5]$, or it could be $[2, 4, 4]$, or $[1, 1, 8]$, or something else. So, to count the number of sequences whose sum of $n$ largest elements is $t$, we need to enumerate all possible sequences of top $n$ values whose sum is $t$, and for each one, count the number of sequences of length $w$ whose sequence of top $n$ values is *that* sequence.

If that's confusing, let's formalize a bit. Let's define a **winner sequence** as a *sorted* sequence of $n$ values, each of which is between $1$ and $k$. Winner sequences are exactly the possible &ldquo;sequences of $n$ largest values&rdquo;. Now, if $W$ is a winner sequence, let's define $c(W, w)$ as the number of length-$w$ sequences whose sequence of $n$ largest values is $W$. Then you may check that the following equation holds
$$c_t = \sum_{\substack{\text{$W$ is a winner sequence} \\ \mathit{sum}(W) = t}} c(W, w).$$
Thus, we've further reduced the problem to that of computing $c(W, w)$ across all winner sequences $W$. And as it turns out, for Subtask 1, there aren't that many winner sequences. We can see this by simply enumerating them all (say with a computer). Finding a formula for the number of them isn't that hard either:
<div class="task">
**Exercise:** Show that the number of winner sequences is exactly $\binom{n + k - 1}{n}$.
</div>
For Subtask 1, $n = 5$ and $k = 5$, so $\binom{n + k - 1}{n} = 126$, so there are indeed only a few of them.


### Computing $c(W, w)$

Thinking &ldquo;DP-cally&rdquo;, we now attempt to build the length-$w$ sequence element by element. As we build the sequence, its &ldquo;sequence of $n$ largest elements&rdquo; changes as well.

Let's be more precise. For a sequence $S$, let's call the &ldquo;sequence of $n$ largest elements of $S$&rdquo; its **winning sequence,** and denote it by $W_S$. Now, suppose we insert the value $v$ to $S$. Let's denote the updated sequence by $S + [v]$. Then the winning sequence might change because of $v$. Specifically, the new winning sequence is obtained by *inserting* $v$ to $W_S$ in its proper sorted location, and then dropping the lowest element. (Can you see why?) Let's denote the process of &ldquo;inserting a value $v$ to a sequence $W$ in its proper sorted location, and then dropping the lowest element&rdquo; as a *pushpop* operation, and denote it by $\mathit{pushpop}(W, v)$. Then what we're saying is that the winning sequence of $S + [v]$ is related to the winning sequence of $S$ via a pushpop operation&mdash;specifically,
$$W_{S + [v]} = \mathit{pushpop}(W_S, v).$$

We can now think recursively, and find a recurrence for $c(W, w)$, as follows. Every sequence of length $w$ can be obtained by taking a sequence $S$ of length $w - 1$ and then appending some value $v$ (between $1$ to $k$) to it. And as described above, the new winning sequence $W_{S + [v]}$ is just $\mathit{pushpop}(W_S, v)$. Notice that this latter expression only depends on $W_S$, not on $S$ itself. Thus, for each possible *winner* sequence $W'$, we could simply collect the sequences $S$ with $W'$ as their winning sequence, and notice that the new winning sequence must be $\mathit{pushpop}(W', v)$. In other words, we have the equation
$$c(W, w) = \!\!\!\!\sum_{\substack{W'\,\,\,\, \\ \text{$W'$ is a winner sequence}}} \sum_{\substack{1 \le v \le k \,\,\,\, \\ \mathit{pushpop}(W', v) = W}} \!\!\!\!(\text{number of sequences $S$ of length $w - 1$ whose winning sequence is $W'$}).$$
But the summand is just $c(W', w - 1)$ by definition! Therefore, we obtain the recurrence
$$c(W, w) = \sum_{\substack{W'\,\,\,\, \\ \text{$W'$ is a winner sequence}}} \sum_{\substack{1 \le v \le k \,\,\,\, \\ \mathit{pushpop}(W', v) = W}} c(W', w - 1),$$
and we can use this to compute all $c(W, w')$ we need, via DP: we build a *table* of results, one for each winner sequence $W$ and each $w' \le w$. Each entry of the table can be computed using the summation above. Since our formula for $c(W, w')$ only depends on $c(W', w' - 1)$, i.e., those with a smaller $w'$ value, if we compute the table in increasing order of $w'$, those values have already been computed, and are already on the table. Thus, we'll be able to compute the final result all the way up to $w$, which is what we wanted.

Now, as for the base case, you could just directly count the sequences for, say, $w' = n$, since the winning sequence is basically the *sorted* version of the sequence itself. Alternatively, we can use $w' = 0$ as our base case, though we need to think about what the winning sequence of a sequence with less than $n$ elements should be. Well, it makes sense to say that the winning sequence must be the whole sequence as well, just sorted. And instead of a *pushpop* operation, we could simply use a *push* operation, at least while the sequence still has length less than $n$.

With this, we now have a solution! What's the running time? Well, the table has an entry for each $(W, w')$ with $W$ a winner sequence and $w' \le w$. Recall that there are $\binom{n + k - 1}{n}$ winner sequences, so there are $\approx \binom{n + k - 1}{n}w$ entries. Each entry is computed with the sum above, which clearly has at most $\binom{n + k - 1}{n}k$ summands (often much less). Therefore, the amount of steps is roughly proportional to
$$\approx \binom{n + k - 1}{n}w\cdot \binom{n + k - 1}{n}k = \binom{n + k - 1}{n}^2 wk.$$
For Subtask 1, this is good enough; my straightforward Python implementation computes the *full* answer in less than one second.

<div class="caution">
**Note:** Understanding this implementation is *not* required to understand the following sections, so you may skip it.
</div>

<details class="code"><summary class="h4">Code (Python)</summary>

```python
from fractions import Fraction as Frac
from functools import cache
from itertools import combinations_with_replacement
from math import comb

def solve(n, w, k):
    @cache
    def pushpop(W, v):
        return tuple(sorted([*W, v])[-n:])

    @cache
    def winner_sequences(n):
        return tuple(combinations_with_replacement(range(1, k+1), n))

    assert len(winner_sequences(n)) == comb(n + k - 1, n)  # sanity check

    @cache
    def c(W, w):
        assert len(W) == min(w, n)  # sanity check

        if w == 0:
            return 1
        else:
            return sum(c(WW, w - 1)
                for WW in winner_sequences(min(w - 1, n))
                for v in range(1, k+1)
                if pushpop(WW, v) == W
            )

    def c_(t):
        return sum(c(W, w) for W in winner_sequences(n) if sum(W) == t)

    def p_(t):
        return Frac(c_(t), k**w)

    return sum(p_(t) * t for t in range(n, n*k + 1))
```
</details>

<div class="remarks">
**Remark:** The implementation tries to copy our formulas above as closely as possible. As a result, it's highly unoptimized, and there are definitely several improvements that be made. But the main point is that even such unoptimized code is enough to solve the subtask.
</div>

</details>



<details class="editorial-section"><summary class="h2">Subtask 2</summary>

### Linearity of expectation

To find faster solutions, we use something called the &ldquo;**linearity of expectation**&rdquo;. Linearity of expectation means two things:

- $\operatorname{E}[\alpha X] = \alpha \operatorname{E}[X]$ for any random variable $X$ and any constant $\alpha$, and
- $\operatorname{E}[X_1 + X_2] = \operatorname{E}[X_1] + \operatorname{E}[X_2]$ for any two random variables $X_1$ and $X_2$.

The first one is quite intuitive; after all, $\alpha X$ is just $X$ with all values scaled by $\alpha$, so the *average* should just be scaled in the same way. However, the second property&mdash;additivity&mdash;may be surprising. The property could be intuitive in the case where $X_1$ and $X_2$ are *independent*, but linearity doesn't *require* them to be&mdash;it's simply *always* true!

In a bonus section below, we'll explain why this is true, but for now, let's first try to apply this to the problem. Let $T$ be the same random variable as before, so it denotes the *sum* of the $n$ largest values of the sequence produced. Now, we define $n$ new random variables $T_1, T_2, \ldots T_n$, where $T_i$ denotes the $i$th largest value of the sequence. Then clearly we have
$$T = T_1 + T_2 + \ldots + T_n = \sum_{i=1}^n T_i.$$
Now, the $T_i$'s are definitely not independent, e.g., knowing the largest value constrains the possible values of the second value, and vice versa. Regardless, *expectation is always additive*, so we have the equality
$$\operatorname{E}[T] = \operatorname{E}[T_1] + \operatorname{E}[T_2] + \ldots + \operatorname{E}[T_n] = \sum_{i=1}^n \operatorname{E}[T_i].$$
Thus, we've reduced the problem to computing $\operatorname{E}[T_i]$ for $1 \le i \le n$, which is potentially more manageable!


### Computing $\operatorname{E}[T_i]$

Let's now try to compute $\operatorname{E}[T_i]$, the expected value of the $i$th largest element of the sequence. The possible values are between $1$ and $k$, so by definition, we have
$$\operatorname{E}[T_i] = \sum_{v=1}^k \operatorname{P}[T_i = v]\cdot v,$$
where $\operatorname{P}[T_i = v]$ denotes the probability that $T_i = v$. Next, we again turn probability into counting; noting that there are $k^w$ equally likely possibilities, we have something like
$$\operatorname{P}[T_i = v] = \frac{\mathit{count}_{=v}(i)}{k^w}$$
where $\mathit{count}_{=v}(i)$ denotes the number of sequences whose $i$th largest value is $v$. Thus, we're done if we can compute $\mathit{count}_{=v}(i)$.


### Computing $\mathit{count}_{=v}(i)$

We can compute $\mathit{count}_{=v}(i)$ by noting that:

<div class="theorem">

**Theorem 1:** The $i$th largest value of a sequence is $v$ if and only if

- the sequence has $< i$ elements greater than $v$, and
- the sequence has $\le w - i$ elements less than $v$.

</div>
This is fairly intuitive, and you should try to prove it yourself &#128578;.
<details class="proof"><summary class="h4">Proof</summary>
Sort the sequence in **decreasing** order, so the $i$th element denotes the $i$th largest value.

(&rArr;) Now, suppose the $i$th largest element is $v$, i.e., the element at index $i$ is $v$. Then because the sequence is decreasing,

- only indices $1$ to $i - 1$ can have a value greater than $v$, and there are $< i$ of them; and
- only indices $i + 1$ to $w$ can have a value less than $v$, and there are $\le w - i$ of them.

(&lArr;) On the other hand,

- if the sequence has $< i$ values greater than $v$, then $> w - i$ values must be at most $v$. Since the sequence is decreasing, indices $i$ to $w$ must have values at most $v$; and
- if the sequence has $\le w - i$ values less than $v$, then $\ge i$ values must be at least $v$. Since the sequence is decreasing, indices $1$ to $i$ must have values at least $v$.

In particular, the value at index $i$ must be at most $v$ and at least $v$ at the same time, so it must be equal to $v$, i.e., the $i$th largest value is $v$.
</details>

Thus, we want to count the number of sequences with $< i$ elements greater than $v$ and $\le w - i$ elements less than $v$. Let

- $\ell$ be the number of elements $< v$, and
- $g$ be the number of elements $> v$,

so that $\ell \le w - i$ and $g < i$. Then using Theorem 1, we have the equality
$$\mathit{count}_{=v}(i) = \sum_{\ell=0}^{w-i} \sum_{g=0}^{i-1} c(\ell, g, v)$$
where $c(\ell, g, v)$ is the number of sequences with exactly $\ell$ elements $< v$ and exactly $g$ elements $> v$. Finally, counting $c(\ell, g, v)$ is easy, because to build such a sequence, we could use the following process:

1. Among the $w$ indices, we first choose which $\ell$ elements will be $< v$. There are $\binom{w}{\ell}$ ways to do this.
2. Next, among the $w - \ell$ remaining indices, we choose which $g$ elements will be $> v$. There are $\binom{w - \ell}{g}$ ways to do this, and the remaining $w - \ell - g$ indices must contain the value $v$.
3. Next, we choose the actual values of the elements $< v$. There are $\ell$ values to choose, and each one is an independent choice of a number between $1$ and $v-1$, so there are $(v-1)^{\ell}$ ways to do this.
4. Finally, we choose the actual values of the elements $> v$. There are $g$ values to choose, and each one is an independent choice of a number between $v+1$ and $k$, so there are $(k-v)^g$ ways to do this.

Thus, all in all, there are
$$c(\ell, g, v) = \binom{w}{\ell} \cdot \binom{w - \ell}{g} \cdot (v-1)^{\ell} \cdot (k-v)^g$$
such sequences.

We now have a complete solution! How fast does it run? Well, we need to compute $\operatorname{E}[T_i]$ for $1 \le i \le n$, which in turn require the values $\mathit{count}_{=v}(i)$ for $1 \le i \le n$ and $1 \le v \le k$, which in turn require the values $c(\ell, g, v)$ for $0 \le \ell \le w - 1$, $0 \le g \le n - 1$ and $1 \le v \le k$.

- Each $c(\ell, g, v)$ value is a product of some binomial coefficients and powers. The powers can all be computed with fast exponentiation, or they could just be precomputed in a table at the beginning (since all powers we need have bases less than $k$, and exponents less than $w$), and the binomial coefficients can also be precomputed in a table, either via Pascal's identity, or precomputing factorials and using
$$\binom{a}{b} = \frac{a!}{(a - b)!b!}.$$
Therefore, we could say that each $c(\ell, g, v)$ can be computed in a constant amount of steps, and since there are $\approx wnk$ of them, the total number of steps to compute them all is $\approx wnk$.

- To compute the $\mathit{count}_{=v}(i)$ values, note that there are $kn$ such values, and each one is computed with a summation with $\approx wn$ summands. Therefore, it takes $\approx wn^2 k$ steps to compute them all.

- The formula for $\operatorname{E}[T]$ has $n$ summands, each of which has a formula with $k$ summands, so this takes $\approx nk$ steps.

- Finally, we also need to account for the precomputation of factorials and powers. There are $\approx w$ factorials and $\approx kw$ powers to precompute, so their precomputation takes $\approx kw$ steps.

Thus, the running time is dominated by the computation of $\mathit{count}_{=v}(i)$. For Subtask 2, we have $wn^2 k = 6\cdot 10^9$, so the number of steps seems small enough for this to be waitable if you use a fast language and a highly optimized implementation. It may be slow though, so instead of that, let's just improve our algorithm further.


### Computing $\mathit{count}_{=v}(i)$ more quickly

Let's look at $\mathit{count}_{=v}(i)$ again. It denotes the number of sequences whose $i$th largest value is exactly $v$. It turns out that it's easier to count the number of sequences whose $i$th largest value is **at most $v$**. Even more nicely, it turns out that you can use the latter to compute the former!

To see this, let's define $\mathit{count}_{\le v}(i)$ to be the number of sequences whose $i$th largest value is at most $v$. Then we easily have:
<div class="theorem">
**Claim:** $\mathit{count}_{=v}(i) = \mathit{count}_{\le v}(i) - \mathit{count}_{\le v - 1}(i)$.
</div>
<div class="proof">

**Proof:** Left as an exercise to the reader.
</div>

So we've reduced the problem to computing $\mathit{count}_{\le v}(i)$ for $0 \le v \le k$ and $1 \le i \le n$. So what? Well, here's what. It turns out that we can find a version of Theorem 1 that applies to $\mathit{count}_{\le v}(i)$:
<div class="theorem">

**Theorem 2:** The $i$th largest value of a sequence is at most $v$ if and only if the sequence has $< i$ elements greater than $v$.
</div>
<div class="proof">

**Proof:** Left as an exercise to the reader.
</div>

And as you may notice, Theorem 2 is much simpler than Theorem 1!

We can now use a similar counting argument as before. Let $g$ be the number of elements greater than $v$, so that $g < i$, and we can again write
$$\mathit{count}_{\le v}(i) = \sum_{g=0}^{i-1} c(g, v)$$
where now, $c(g, v)$ denotes the number of sequences with *exactly* $g$ elements greater than $v$. Then we can count $c(g, v)$ similarly as before, except it's even simpler:

1. First, choose the $g$ indices that will be $> v$. There are $\binom{w}{g}$ ways to do this. The rest of the elements will be $\le v$.
2. Then, we choose the actual values of the elements $> v$. There are $g$ values to choose, and each one is an independent choice of a number between $v+1$ and $k$, so there are $(k-v)^g$ ways to do this.
3. Finally, we choose the actual values of the elements $\le v$. There are $w - g$ values to choose, and each one is an independent choice of a number between $1$ and $v$, so there are $v^{w - g}$ ways to do this.

Therefore, we have the simpler formula
$$c(g, v) = \binom{w}{g}\cdot (k - v)^g \cdot v^{w - g}.$$

We can now estimate the new running time. We now expect it to be better since the formulas are now simpler, and in particular, the double nested summations have become single summations. In fact, if we perform the same estimation, we find that the number of steps is $\approx wk + n^2 k$, which is now definitely fast enough for Subtask 2!

<div class="task">
**Bonus:** We can similarly define $\mathit{count}_{\ge v}(i)$ and write
$$\mathit{count}_{= v}(i) = \mathit{count}_{\ge v}(i) - \mathit{count}_{\ge v + 1}(i).$$
What happens to the running time when you base your algorithm on this?
</div>

</details>



<details class="editorial-section"><summary class="h2">Subtask 3</summary>

The main change from Subtask 2 to Subtask 3 is that $w$ is vastly increased, which means the portion of our previous algorithm that takes $\approx wk$ steps is now unacceptable. Let's recap what those steps are:

1. precomputing factorials up to $w$, and
2. precomputing powers up to base $k$ and up to exponent $w$.

Among these, the second one clearly dominates the running time. But we can essentially get rid of the second one by simply *not* precomputing powers, and instead just fast exponentiation to compute them when needed! This makes the running time slightly worse&mdash;fast exponentiation takes $\mathcal{O}(\lg w)$ steps for an exponent the size of $w$&mdash;but that's a very worthwhile tradeoff, because you can check that the number of steps improves from $\mathcal{O}(wk + n^2 k)$ to 
$$\mathcal{O}(w + n^2 k + nk \lg w).$$
This is now acceptable for Subtask 3 &#128578;.

Now, there's still that factor $w$ in the running time, which in the current subtask is probably ok since $w = 10^8$. However, in later subtasks, $w = 10^{16}$, which suggests that that bit can still be improved further.

How can we improve it? Well, the main reason for needing factorials up to $w$ is so that we can compute binomial coefficients. But looking closer, notice that we actually only need binomial coefficients **at exactly row $w$**. Furthermore, we actually only need the first $n$ coefficients in it. And as it turns out, there's a way to compute a row of binomial coefficients one by one, starting from the leftmost one, by using the following recurrence (which is easy to prove using the factorial formula):
$$\binom{w}{g} = \binom{w}{g - 1}\cdot \frac{w - g + 1}{g},$$
with base case simply $\binom{w}{0} = 1$. So now, instead of precomputing factorials, we may simply precompute the needed binomial coefficients using this recurrence with just $\approx n$ steps! The running time then improves to
$$\mathcal{O}(n^2 k + nk \log w),$$
which is really cool.

</details>



<details class="editorial-section"><summary class="h2">Subtasks 4 & 5</summary>

Our previous algorithm is now too slow; in particular, that $\mathcal{O}(n^2 k)$ bit in the running time is now too large. For the rest of the subtasks, I'll just give a couple of hints to guide you towards faster solutions.

<details class="task"><summary class="h4">Hint 1</summary>
Do you really have to compute the whole sum
$$\mathit{count}_{\le v}(i) = \sum_{g=0}^{i-1} c(g, v)$$
every time?
</details>

<details class="task"><summary class="h4">Hint 2</summary>
Notice that
$$(k - v)^g\cdot v^{w - g} = v^w \cdot \left(\frac{k - v}{v}\right)^g.$$
Letting $x_v := \frac{k - v}{v}$, this is the same as $v^w x_v^g$.
</details>



</details>



<details class="editorial-section"><summary class="h2">Bonus: Linearity of expectation</summary>

This section is devoted to explaining why expectation is *linear*. Recall from above that linearity means two properties:

- **Scaling:** $\operatorname{E}[\alpha X] = \alpha \operatorname{E}[X]$ for any random variable $X$ and any constant $\alpha$, and
- **Additivity:** $\operatorname{E}[X_1 + X_2] = \operatorname{E}[X_1] + \operatorname{E}[X_2]$ for any two random variables $X_1$ and $X_2$.

The first one is simple enough, and you should be able to prove it yourself &#128578;. The real surprise is the second, which holds even if $X_1$ and $X_2$ are not independent. (For independent variables, this may not be a surprise, since &ldquo;clearly&rdquo; the variables have nothing to do with each other,[^2] so the averages should &ldquo;just add up.&rdquo;)

Let's see an example of this, using our current problem itself, with $n = 2$, $w = 3$ and $k = 2$. In this case, we have
$$T = T_1 + T_2$$
where $T_i$ is the value of the $i$th largest element. Clearly, $T_1$ and $T_2$ are not independent; for example, we know that $T_1$ is at least $T_2$, so if $T_2$ is $2$, then $T_1$ must be $2$ as well.

Regardless, we will now illustrate that
$$\operatorname{E}[T] = \operatorname{E}[T_1] + \operatorname{E}[T_2]$$
by simply enumerating all $2^3 = 8$ possible sequences:

- For $[1, 1, 1]$, we have $T_1 = 1$, $T_2 = 1$ and $T = 2$;
- For $[1, 1, 2]$, we have $T_1 = 2$, $T_2 = 1$ and $T = 3$;
- For $[1, 2, 1]$, we have $T_1 = 2$, $T_2 = 1$ and $T = 3$;
- For $[1, 2, 2]$, we have $T_1 = 2$, $T_2 = 2$ and $T = 4$;
- For $[2, 1, 1]$, we have $T_1 = 2$, $T_2 = 1$ and $T = 3$;
- For $[2, 1, 2]$, we have $T_1 = 2$, $T_2 = 2$ and $T = 4$;
- For $[2, 2, 1]$, we have $T_1 = 2$, $T_2 = 2$ and $T = 4$;
- For $[2, 2, 2]$, we have $T_1 = 2$, $T_2 = 2$ and $T = 4$.

We can now compute the averages as follows:
$$\begin{align*}
\operatorname{E}[T_1] &= \frac{1 + 2 + 2 + 2 + 2 + 2 + 2 + 2}{8} = 1.875;\\
\operatorname{E}[T_2] &= \frac{1 + 1 + 1 + 2 + 1 + 2 + 2 + 2}{8} = 1.5;\\
\operatorname{E}[T]   &= \frac{2 + 3 + 3 + 4 + 3 + 4 + 4 + 4}{8} = 3.375,
\end{align*}$$
and sure enough, $3.375 = 1.875 + 1.5$, even though $T_1$ and $T_2$ are not independent.

But actually, this little calculation illustrates pretty well *why* expectation is additive; we're simply adding the same things in different ways! To illustrate this further, we can tabulate everything as follows:
$$\begin{array}{l|l|lll}
s & p_s & T_1 & T_2 & T \\
\hline
[1, 1, 1] & \frac{1}{8} & 1 & 1 & 2 \\
[1, 1, 2] & \frac{1}{8} & 2 & 1 & 3 \\
[1, 2, 1] & \frac{1}{8} & 2 & 1 & 3 \\
[1, 2, 2] & \frac{1}{8} & 2 & 2 & 4 \\
[2, 1, 1] & \frac{1}{8} & 2 & 1 & 3 \\
[2, 1, 2] & \frac{1}{8} & 2 & 2 & 4 \\
[2, 2, 1] & \frac{1}{8} & 2 & 2 & 4 \\
[2, 2, 2] & \frac{1}{8} & 2 & 2 & 4.
\end{array}$$
Now, the $T$ column is clearly the sum of the $T_1$ and $T_2$ columns. We can now *distribute* the probabilities in each row:
$$\begin{array}{l|lll}
s & p_sT_1 & p_sT_2 & p_sT \\
\hline
[1, 1, 1] & \frac{1}{8} & \frac{1}{8} & \frac{2}{8} \\
[1, 1, 2] & \frac{2}{8} & \frac{1}{8} & \frac{3}{8} \\
[1, 2, 1] & \frac{2}{8} & \frac{1}{8} & \frac{3}{8} \\
[1, 2, 2] & \frac{2}{8} & \frac{2}{8} & \frac{4}{8} \\
[2, 1, 1] & \frac{2}{8} & \frac{1}{8} & \frac{3}{8} \\
[2, 1, 2] & \frac{2}{8} & \frac{2}{8} & \frac{4}{8} \\
[2, 2, 1] & \frac{2}{8} & \frac{2}{8} & \frac{4}{8} \\
[2, 2, 2] & \frac{2}{8} & \frac{2}{8} & \frac{4}{8}.
\end{array}$$
and note that the $p_sT$ column is still the sum of the $p_sT_1$ and $p_sT_2$ columns. Finally, computing $\operatorname{E}[T]$ amounts to taking the *sum* of the $p_sT$ column, while computing $\operatorname{E}[T_1] + \operatorname{E}[T_2]$ amounts to taking the sum of the $p_sT_1$ and $p_sT_2$ columns separately, then adding them. But these are clearly the same! (And this worked even if $T_1$ and $T_2$ aren't independent.)

It should now not be too hard to formalize this argument and make it more general. If you're interested, here it is:
<details class="proof"><summary class="h4">Proof</summary>

Suppose the sample space has $k$ elements $\{\omega_1, \omega_2, \ldots, \omega_k\}$ with respective probabilities $p_1, p_2, \ldots, p_k$. Because $T = T_1 + T_2$, we must always have $T(\omega_i) = T_1(\omega_i) + T_2(\omega_i),$ for every $i$. 

Thus, by the [law of the unconscious statistician](https://en.wikipedia.org/wiki/Law_of_the_unconscious_statistician), 
$$\begin{align*}
\operatorname{E}[T]
&= \sum_{i=1}^k p_i \cdot T(\omega_i) \\
&= \sum_{i=1}^k p_i \cdot \left(T_1(\omega_i) + T_2(\omega_i)\right) \\
&= \sum_{i=1}^k p_i \cdot T_1(\omega_i) + \sum_{i=1}^k p_i \cdot T_2(\omega_i) \\
&= \operatorname{E}[T_1] + \operatorname{E}[T_2].
\end{align*}$$
</details>

Just as practice, you could try proving the *scaling* property formally yourself:
<div class="task">

**Exercise:** Prove the *scaling* property of expectation formally.
</div>

<div class="remarks">

**Remark:** Our proof of linearity depends on the fact that the sample space is finite. Indeed, our definition of random variable assumes that as well. In other settings where there may be infinitely many outcomes, it turns out expectation is still linear, but our proof (and even the definition of &ldquo;expected value&rdquo;) needs to be modified a bit.
</div>
</details>



<details class="editorial-section"><summary class="h2">Bonus: Computing rational numbers modulo $998244353$</summary>

All solutions we described above compute the *full* answer, i.e., we pretend we were working on $\mathbb{R}$ where we can add, subtract, multiply, and crucially, divide, numbers. Actually, we could also pretend we are working on $\mathbb{Q}$, i.e., the rationals, since all intermediate results are clearly rational, and we can also do the same arithmetic operations there.

Now, in many problems, we can usually convert such full-answer solutions into solutions that compute the answer mod $m$, say $m = 998244353$, because we can also add, subtract and multiply numbers mod $m$. However, division mod $m$ is more complicated; it sometimes doesn't work at all. To see this, let $m = 10$, and note that $12 \equiv 32 \pmod{10}$, but dividing by $4$ fails:
$$\frac{12}{4} = 3 \not\equiv 8 = \frac{32}{4} \pmod{10}.$$


### Computing $a/b \bmod m$ by trial and error

Before we tackle this issue, let's first see if we can compute $a/b \bmod m$ based solely on the definition given in the problem statement. Suppose you've computed the full answer as $a/b$, and let's say it's in lowest terms. Then the problem guarantees us that $a/b \bmod m$ is well-defined, and it is the unique number $q$ such that &ldquo;$a/b - q = \frac{a - qb}{b}$ is divisible by $m$&rdquo;, which by definition means that $\frac{a - qb}{b}$ can be written as a fraction whose numerator is divisible by $m$ but whose denominator is not. Now, the fraction $\frac{a - qb}{b}$ is already in lowest terms (why?), so this means two things:

- $b$ must not be divisible by $m$ (which we can check), otherwise there's no hope of $\frac{a - qb}{b}$ being divisible by $m$.
- $a - qb$ is divisible by $m$. To find such a $q$, we could simply use brute force: check each $q$ from $0$ to $m-1$ and find one where $a - qb$ is divisible by $m$. The problem statement says that such a $q$ is unique.

All in all, this takes $\approx m$ steps in the worst case to find $q$, which is the answer we're looking for. With $m = 998244353 \approx 10^9$, that isn't so bad, especially if $a/b$ doesn't have too many digits. So for Subtasks 1 and 2, that's more-or-less okay. But for the larger subtasks the numbers become too large[^3] which makes it not okay, and we clearly need to do something else.


### Working &ldquo;modulo $m$&rdquo;

You might suspect that the reason that dividing by $4$ failed modulo $10$ is that $4$ and $10$ share a common factor. And indeed, that's a good hunch. For example, dividing by $3$ seems to work modulo $10$, which you can check with lots of small examples, or maybe by using a program to do several checks for you, e.g.:
<details class="code"><summary class="h4">Code (Python)</summary>

```python
from math import gcd

def congruent(m, a, b):
    """ a == b (mod m) """
    return (a - b) % m == 0

m = 10

# try denominators coprime with m
denominators = [d for d in range(-100, 100+1) if gcd(m, d) == 1]

for den in denominators:
    print("Checking", den)

    # take several numbers divisible by den
    nums = [den * v for v in range(-1000, 1000+1)]

    for num1 in nums:
        for num2 in nums:
            # check that if num1 == num2 then (num1/den) == (num2/den), mod m
            if congruent(m, num1, num2):
                assert congruent(m, num1 // den, num2 // den)

print("All OK")
```
</details>
You can replace `m = 10`{.python} with other numbers and it still seems to work! So clearly, there seems to be some sense in which division &ldquo;kinda makes sense&rdquo;, as long as the number you're dividing with is coprime with the modulus $m$.

And as it turns out, we can prove that fact!

<div class="theorem">
**Theorem A:** If $da \equiv db \pmod{m}$ and $\gcd(m, d) = 1$, then $a \equiv b \pmod{m}$.
</div>

<div class="proof">

**Proof:** Fairly straightforward, so we leave it to the reader.
</div>

Now that's all well and good, but what we really want is to be able to *divide* modulo $m$. For this, we should answer the following question first: *what is division, really*? Well, dividing is the same as multiplying by the *multiplicative inverse*, that is, $a/b$ is the same as $ab^{-1}$, where $b^{-1} = 1/b$ is the multiplicative inverse of $b$. But what is a multiplicative inverse? Well, $b^{-1}$ is defined as the unique number such that $bb^{-1} = 1$.

Now, as it turns out, multiplicative inverses sometimes exist modulo $m$. In the mod $m$ world, the multiplicative inverse of $b$ is still denoted $b^{-1}$, but this time, it's not a fraction. Nonetheless, it's still defined analogously; $b^{-1}$ is the &ldquo;unique&rdquo; number such that
$$bb^{-1} \equiv 1 \pmod{m}.$$
Note that I put &ldquo;unique&rdquo; in quotes because if $x$ is a multiplicative inverse, then $x + m$ is also one, as is $x + 2m$, $x - m$, etc. But as it turns out, all these numbers are the same mod $m$, which is what we mean by &ldquo;unique&ldquo; here.

We can actually prove that fact, and in fact, something stronger:
<div class="theorem">

**Theorem B:** $b$ has a multiplicative inverse if and only if $b$ and $m$ and coprime, and it is unique if it exists.
</div>

<details class="proof"><summary class="h4">Proof</summary>

(&rArr;) Suppose $b$ has a multiplicative inverse $b'$, so that
$$bb' \equiv 1 \pmod{m}.$$
This is equivalent to saying that there's a $k$ such that
$$bb' - mk = 1.$$
Now, if $d$ is a common divisor of $b$ and $m$, then $d$ divides the left-hand side, so it must also divide the right-hand side, which is $1$. Thus, all common divisors of $b$ and $m$ divide $1$, which means they are coprime.

(&lArr;) Suppose $b$ and $m$ are coprime, so their gcd is $1$. By [Bézout's](https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity), there are integers $x$ and $y$ such that
$$bx + my = 1.$$
Reducing this modulo $m$ gives
$$bx \equiv 1 \pmod{m},$$
so $x$ is a multiplicative inverse of $b$.

(Uniqueness) Suppose $b'$ and $b''$ are both multiplicative inverses of $b$. Then
$$\begin{align*}
    bb' &\equiv 1 \pmod{m} \\
    bb'' &\equiv 1 \pmod{m},
\end{align*}$$
so
$$bb' \equiv bb'' \pmod{m}.$$
But $m$ and $b$ are coprime (since a multiplicative inverse exists), so by using Theorem A, $b' \equiv b'' \pmod{m}$, so any two multiplicative inverses of $b$ are the same mod $m$.

</details>

<div class="remarks">
**Remark:** The proof can actually be turned into an algorithm to compute the multiplicative inverse, since the integers $x$ and $y$ guaranteed by Bézout's identity can be computed using the **extended version of Euclid's gcd algorithm.**
</div>

So with this, we're now fairly able to &ldquo;divide modulo $m$&rdquo;, as long as the divisors are coprime with $m$. Since we're using the modulus $m = 998244353$ which is prime, most numbers are coprime! The only ones we can't divide with are those divisible by $m$ itself, but since such numbers are $\equiv 0 \pmod{m}$, it makes sense not to be able to divide with them since that's sort of equivalent to dividing by $0$.

Now, that's well and good, but we still need to relate this way of dividing modulo $m$ with the definition given in the statement. As it turns out, everything is okay; we can prove that $a/b \bmod m$, as defined in the statement, is the same as $ab^{-1} \bmod m$, using the following theorem:

<div class="theorem">

**Theorem C:** For a rational $r$, $r \bmod m$ exists if and only if $r$ can be written as $a/b$ with $b$ coprime with $m$, and if it exists, then we have the equality
$$(a/b \bmod m) = (ab^{-1} \bmod m).$$
</div>

For this theorem to work, we will amend the definitions given in the statement as follows: We say a rational is **divisible by $m$** if it can be written as $a/b$ with $a$ divisible by $m$ and $b$ *coprime* with $m$. This is equivalent to the definition in the statement when $m$ is prime, but is friendlier to nonprime moduli.

<details class="proof"><summary class="h4">Proof</summary>

(&rArr;) Suppose $r \bmod m$ exists, i.e., there's a unique $q$ such that $r - q$ is &ldquo;divisible by $m$&rdquo; (as defined above). Writing $r$ in lowest terms as $a/b$, we note that $a/b - q = \frac{a - bq}{b}$ is also in lowest terms.

By definition of divisibility, $\frac{a - qb}{b}$ can be written as $a'/b'$ with $m$ dividing $a'$ but coprime with $b'$. Since
$$\frac{a - qb}{b} = \frac{a'}{b'}$$
and the former is in lowest terms, it follows that $a - qb$ is a divisor of $a'$ and $b$ is a divisor of $b'$. But if $m$ and $b'$ are coprime and $b \mid b'$, then $m$ and $b$ must be coprime as well.

(&lArr;) Suppose $r = a/b$ with $b$ is coprime with $m$. Then I claim that
$$q := (ab^{-1} \bmod m)$$
satisfies the definition of $r \bmod m$. Note that
$$r - q = \frac{a - qb}{b},$$
and we already know $b$ is coprime with $m$, so it's sufficient to show that $a - qb$ is divisible by $m$, i.e., $a \equiv qb \pmod{m}$. That's shown as follows:
$$\begin{align*}
qb 
&\equiv (ab^{-1})b \\
&\equiv a(bb^{-1}) \\
&\equiv a\cdot(1) \\
&= a \pmod{m}.
\end{align*}$$

So $r - q$ is indeed divisible by $m$. All that remains is to show that $q$ is the unique one satisfying the definition. If $q'$ also satisfies the definition, then $\frac{a - q'b}{b}$ is also divisible by $m$, so we can write it as
$$\frac{a - q'b}{b} = \frac{a'}{b'}$$
with $m$ dividing $a'$ and coprime with $b'$. Rearranging this gives
$$(a - q'b)b' = a'b.$$
Because $m \mid a'$, $m$ must divide the left-hand side $(a - q'b)b'$ as well, but since $m$ and $b'$ are coprime, $m$ must divide $a - q'b$, i.e.,
$$a \equiv q'b \pmod{m}.$$
Multiplying both sides by $b^{-1}$, we get
$$q' \equiv ab^{-1} \equiv q \pmod{m}.$$
In other words, any other possible value $q'$ of $(r \bmod m)$ must be equal to $q = (ab^{-1} \bmod m)$, so it's unique.
</details>

<div class="theorem">

**Corollary:** Suppose $r$ cannot be written as $a/b$ with $b$ coprime with $m$. Then there is *no* integer $q$ such that $r - q$ is divisible by $m$.
</div>
Note that this doesn't follow immediately from the definition, since if $r \bmod m$ doesn't exist, then all we can say from the definition is that there isn't *exactly one* $q$ such that $r - q$ is divisible by $m$. In particular, there may be zero, or there may be more than one. This corollary rules out the latter.

<details class="proof"><summary class="h4">Proof</summary>

We prove the contrapositive.

Suppose there is a $q$ such that $r - q$ is divisible by $m$. Notice that the &ldquo;(&rArr;)&rdquo; portion of the previous proof doesn't really use the fact that $q$ is unique, so the proof also goes through here just fine, and it proves that $r$ can be written as $a/b$ with $b$ coprime with $m$.
</details>

With this, we can now completely work modulo $m = 998244353$ all throughout! All that we need now is to check that we're only ever dividing with numbers without $m$ as a prime factor. The possible divisors come from $k^w$ and the numbers coming from the computation of $\binom{w}{g}$ with $g < n$. The number $k$ is less than $m$ in all inputs, so $k^w$ is coprime with $m$. And in the first few subtasks, $w$ is also less than $m$, so all factors in $\binom{w}{g}$ are all coprime as well. Finally, in the subtasks where $w$ is very large, recall that we're only computing the first $n$ terms of row $w$ of the binomial coefficient table, and that we're using the recurrence
$$\binom{w}{g} = \binom{w}{g - 1}\cdot \frac{w - g + 1}{g},$$
so we only need to divide with numbers $g < n$. Since $n < m$ for all inputs, this is ok too.

Thus, we can safely divide whenever we need to, and all is well in the world.

<div class="remarks">

**Remark:** In math, when we're doing this idea &ldquo;working modulo $m$&rdquo; we usually say we're &ldquo;working in $\mathbb{Z}/m\mathbb{Z}$&rdquo;. Here, &ldquo;$\mathbb{Z}/m\mathbb{Z}$&rdquo; is a formalization of the &ldquo;set of integers modulo $m$&rdquo;. It is just like the integers $\mathbb{Z}$, but we make two numbers equal iff they are the same mod $m$. In this setting, we can also add, subtract, and multiply, and we can divide by any number coprime with $m$ (as shown above).

If $m$ is prime, then this means we can divide by any &ldquo;nonzero number&rdquo; (where you need to remember that &ldquo;nonzero&rdquo; means &ldquo;not divisible by $m$&rdquo;), which makes $\mathbb{Z}/m\mathbb{Z}$ a **field**, just like $\mathbb{R}$ and $\mathbb{Q}$.
</div>

</details>

[^1]: technically, we should say &ldquo;*uniformly randomly, and independently of each other*&rdquo; here...

[^2]: technically, *independent* doesn't really mean *has nothing to do with each other*; it means more like *the probabilities of one are not affected if you know the other*

[^3]: and even if it isn't, the overhead of having to compute with large numbers makes things slower, which we probably couldn't afford for later subtasks
