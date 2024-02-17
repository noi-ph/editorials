% Solution Writeup: Parañastack


# Parañastack  
## Solution Writeup

**Contest:** [NOI.PH 2024 Online Elimination Round](https://noi.ph/2024-national-eliminations/)  
**Problem Idea:** CJ Quines  
**Testing:** Dylan Dalida  
**Statement:** CJ Quines  
**Test Data Preparation:** CJ Quines  
**Solution Writeup:** CJ Quines  



<details class="editorial-section"><summary class="h2">Subtask 1</summary>

When $|T| = 0$, Abra takes the first move, and then the game immediately ends. The answer is always $1$.

</details>



<details class="editorial-section"><summary class="h2">Subtask 2</summary>

When $|S| + |T| \le 10^3$, the input is small enough that we can simulate the game directly.

Relatively unoptimized Python solutions using [`collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque) would work.

</details>



<details class="editorial-section"><summary class="h2">Subtask 3</summary>

We use our solution from Subtask 2 to make some observations when $|S| = 0$.

<div class="task">

**Exercise:** What's the answer when the elements of $T$ are:

- all equal?
- sorted in ascending order?
- sorted in descending order?
- almost sorted in ascending order?

What's the general answer?

</div>

<details class="answer"><summary class="h4">Answer</summary>

When the elements of $T$ are:

- all equal, the answer is always $|T| + 1$.
- sorted in ascending order, the answer is always $|T| + 1$.
- sorted in descending order, the answer is always $2\binom{|T|}{2} + |T| + 1$.
- almost sorted in ascending order, it depends. Let's say $T$ is sorted, except for one swap, like `[1, 2, 4, 3, 5]`. If there's one swap, the answer is always $|T| + 3$. Similarly, if there are two swaps, the answer is $|T| + 5$.

In general, the answer is twice the number of [inversions](https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics)), plus $|T| + 1$. There's standard algorithms for counting the number of inversions in an array.

We leave the proof as an exercise to the reader.

</details>

</details>



<details class="editorial-section"><summary class="h2">Subtask 4</summary>

To go from Subtask 3 to the general case, we try adding elements to $S$, one-by-one.

<div class="task">

**Exercise:** Let $T$ be `[2, 4, 6, 8, 10]`. What's the answer when $S$ is:

- `[1]`? `[3]`? `[5]`? `[7]`? `[9]`? `[11]`?
- `[1, 3]`? `[1, 3, 5]`? `[1, 5, 3, 7, 11, 9]`?
- `[1, 1]`? `[3, 1]`? `[3, 1, 5]`? `[3, 1, 5, 7, 11, 9]`? `[5, 1]`?
- `[3, 5, 1]`? `[3, 7, 1]`? `[5, 3, 1]`? `[5, 7, 1]`?

What's the general answer? Does your answer hold if $T$ isn't `[2, 4, 6, 8, 10]`?

</div>

<details class="answer"><summary class="h4">Answer</summary>

When $S$:

- is a single element $s$, we see it's twice the position of $s$ in the list $T$, plus $6$. This suggests something like the inversions, where the answer is somehow related to the number of inversions when we put $s$ in front of $T$.
- starts with $1$, then the answer is always $6$. That means the elements after $1$ are ignored. We can guess that elements less than everything in $T$ are somehow special.
- has $1$ as the second element, then it's like the first case: twice the position of the first element, plus $6$. That maybe means that everything after the minimum element is ignored.
- is some $S'$ followed by $1$, then it's twice the inversions of $\mathit{reversed}(S') + T$, plus $6$.

This suggests the general answer:

- Let $s$ be the first element in $S$ smaller than everything in $T$.
- Let $S'$ be the prefix of $S$ going from the start to the element $s$. If $s$ doesn't exist, $S' = S$.
- The answer is twice the inversions of $\mathit{reversed}(S') + T$, plus $|T| + 1$.

We leave the proof as an exercise to the reader, though we leave some hints below.

</details>

<details class="task"><summary class="h4">Hints for proof</summary>

The reverse thing suggests that we should look not at two separate stacks $S$ and $T$, but an array $\mathit{reversed}(S) + T$.

If we print what's happening to the array with each step, it looks like the array is being sorted by swapping inversions.

</details>

<details class="remarks"><summary class="h4">Remarks</summary>

The algorithm described here is [gnome sort](https://en.wikipedia.org/wiki/Gnome_sort), but with two stacks instead of an array.

</details>

</details>



