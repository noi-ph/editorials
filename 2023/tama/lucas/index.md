% Solution Writeup: Squares of Even Lucas Numbers


# Squares of Even Lucas Numbers  
## Solution Writeup

**Contest:** [TAMa 2023](https://noi.ph/tama-2023/)  
**Problem Idea:** Cisco Ortega  
**Testing:** Paolo Estavillo, Vincent dela Cruz  
**Statement:** Cisco Ortega  
**Test Data Preparation:** Kevin Atienza  
**Solution Writeup:** Cisco Ortega  



<details class="editorial-section"><summary class="h2">Subtasks 1 & 2</summary>

**Just do it.**  With $n = 10^6 + 2023 < 10^8$, we have more than enough time to simply generate all of the first $n$ Lucas numbers and add up the squares of the even ones.  Also, $n=30$ is small enough that you could do the first subtask by hand, if you feel compelled.

There is one caveat. Lucas numbers grow exponentially quickly, so we need to make sure to take mods at all intermediate steps, i.e., compute the Lucas numbers modulo $m$ as we go along, instead of only at the end:
```py
L = [2, 1]
while len(L) < n:
    L.append(
        (L[-1] + L[-2]) % m  # mod each number!!
    )
# now, add the squares of the even ones...
```
This keeps the sizes of the numbers &ldquo;reasonable&rdquo;.

The problem with this is that <span class="definition" data-bs-toggle="tooltip" data-bs-placement="bottom" title="The parity of a number is whether it&rsquo;s odd or even. (The word &ldquo;parity&rdquo; itself is related to the word &ldquo;pair&rdquo;.)">parity</span> is not necessarily preserved after taking mods.  For example:
$$
\begin{align*}
    1568397607 \bmod 998244353 &= 570153254, \\
    45537549124 \bmod 998244353 &= 616553239,
\end{align*}
$$
so there are cases where odd Lucas numbers are being turned even, and vice versa.

So, we need a way to tell us whether a pre-modded Lucas number is even or odd.  There are a few options, actually.  Here&rsquo;s two of them.

### Generate the parities separately 

_In addition_ to the values of the Lucas numbers modulo $m$, separately compute them modulo $2$ as well.  Use the value mod $2$ to determine if it is even, and if it is, add the square of the value mod $m$.
```py
L = [2, 1]
L_parity = [0, 1]
while len(L) < n:
    L.append(
        (L[-1] + L[-2]) % m  # mod each number!!
    )
    L_parity.append(
        (L_parity[-1] + L_parity[-2]) % 2
    )

total = 0
for value, parity in zip(L, L_parity):
    if parity == 0:
        total = (total + value**2) % m
```

<div class="remarks">
**Remark:** You can also just compute the Lucas numbers modulo $2m$; that way, reducing them modulo $m$ and $2$ is still valid. (Can you see why?)
</div>

### Pen-and-paper insight

It turns out that there&rsquo;s a simple criterion that gives us the parity of a Lucas number given only its index.
<div class="theorem">
**Claim:** $L_{k}$ is even if and only if $k$ is divisible by $3$.
</div>

Perhaps you might have spotted this pattern while playing around with the numbers. And actually, it&rsquo;s not that hard to prove.

<details class="proof"><summary>Proof</summary>
Perform strong induction.  Assume that $L_{3k-2}$ and $L_{3k-1}$ are odd and that $L_{3k}$ is even; use this to show that $L_{3(k+1) - 2}$ and $L_{3(k+1) - 1}$ are odd and that $L_{3(k+1)}$ is even.

 This fact directly follows from the definition of the Lucas sequence and working with it modulo $2$.  The details aren&rsquo;t too hard and are left as an exercise.
</details>

So, even more simply, you only need to add up the squares of the Lucas numbers whose index is a multiple of $3$.

</details>



<details class="editorial-section"><summary class="h2">Subtask 3</summary>

The interesting thing about the numbers modulo $m$ is that there are _finitely many of them_.  That means any infinite sequence such as the Lucas numbers will start to _repeat_ at a certain point.

In particular, the Lucas sequence is a _linear recurrence relation_&mdash;each next term is determined entirely by the previous two terms in the sequence.  So once you get two consecutive terms $(L_k, L_{k+1})$ such that this ordered pair of consecutive values already appeared previously in the sequence, we _know_ that the sequence is going to be periodic from this point on, and we know what that period will be.

For example, consider the Lucas numbers modulo $10$:
$$
    2, 1, 3, 4, 7, 1, 8, 9, 7, 6, 3, 9, \textbf{2, 1}, 3, 4, 7, 1, 8, 9, 7, 6, 3, 9, ...
$$
Note that when we see $(2, 1)$ again, it&rsquo;s the signal that the sequence devolves to just repeating the chunk $2, 1, 3, 4, 7, 1, 8, 9, 7, 6, 3, 9$ from that point on.

In fact, whenever this sequence start to repeat itself, the period _always_ begins with $2$ and $1$.  Can you see why?  **Hint:** If you know two consecutive terms in the Lucas number, you can determine the next term, but you can also determine the _previous_ term.

If this period is sufficiently small (spoiler: it _is_ for Subtask 3 :D), then you can abuse it to compute things like sums (of even squares) even for very large $n$, because the period behaves predictably.

</details>



<details class="editorial-section"><summary class="h2">Subtasks 4 & 5</summary>

Without spoiling the full details, I will remark that there are two primary approaches that you could use in solving these subtasks.  One is **far more painful** than the other.

### Painful number theory 

In one solution, you use the explicit formula of the Lucas numbers, expand it out, then use a sum-of-geometric-series formula.

The problem with this is, of course, the $\sqrt{5}$ in the explicit formula of the Lucas numbers.  To handle this, you have to:

- First, factorize the modulus into prime powers.
  - The small moduli can be brute-forced with period bashing, as in Subtask 3.
  - The large moduli are, conveniently, all prime, so we can proceed!
- Now, for each prime $p$ in the factorization, use Euler&rsquo;s criterion to determine if $x^2 \equiv 5 \pmod{p}$ has a solution.
  - If yes, solve for it using a modulo square root algorithm like Cipolla&rsquo;s.
  - If no, instead start working in the field extension with numbers of the form $a + b \sqrt{5}$ (kind of like what we do with the complex numbers)
  - Then, proceed with the rest of your solution.
- Finally, use the Chinese Remainder Theorem to stitch all your answers together into the true answer modulo $m$.

If you want to code this, go ahead!  It&rsquo;s a fun series of standard (still a bit obscure?) algorithms in number theory.  If not, you can try considering another solution...

### Using matrices to solve linear recurrence (neat, very nice) 

Using standard matrix techniques, you should be able to compute the sum of even Lucas numbers.

Does this technique also work for Lucas **squares**?  It could work if the squares of Lucas numbers also form a linear recurrence relation... do they?

</details>


