% Solution Writeup: Hit the Griddy


# Hit the Griddy  
## Solution Writeup

**Contest:** [TAMa 2023](https://noi.ph/tama-2023/)  
**Problem Idea:** Kevin Atienza  
**Testing:** Vincent dela Cruz, Dan Baterisna  
**Statement:** Cisco Ortega  
**Test Data Preparation:** Kevin Atienza  
**Solution Writeup:** Kevin Atienza  



<details class="editorial-section"><summary class="h2">Subtask 1</summary>

**Disclaimer:** The first solution we&rsquo;ll describe is the simplest one conceptually, but is not necessarily the easiest one to implement. Nonetheless, we&rsquo;re covering it anyway because the ideas we&rsquo;ll encounter will be useful for later.


### A straightforward approach

Anyway, the most straightforward solution would be to *just do it* as stated, a.k.a., *brute force*: enumerate all $2^{rc}$ grids, compute $B(G)$ for each of them, and then sum up all these $B(G)^3$. Enumerating grids is relatively straightforward with backtracking, and for the first subtask, $2^{rc} = 2^{25} = 33554432$ which is quite manageable for a computer. The only missing ingredient to fully implement this solution is being able to compute $B(G)$ for a given grid $G$.


### Computing $B(G)$

We are given a grid with $r$ rows and $c$ columns, and we want to make it *based*, i.e., change it so that every row and every column has an even number of cringe memes.

Let&rsquo;s convert a cool meme (&#128511;) into a $0$ and a cringe meme (&#128556;) into a $1$, so the condition translates to: the sum of every row and every column is even.

Now, the effect of flipping a cell is to flip the <span class="definition" data-bs-toggle="tooltip" data-bs-placement="bottom" title="The parity of a number is whether it&rsquo;s odd or even. (The word &ldquo;parity&rdquo; itself is related to the word &ldquo;pair&rdquo;.)">parity</span> of exactly one row and exactly one column, namely the row and column containing the cell. Thus, if there are $R$ odd rows, then you need at least $R$ flips to make all these odd rows even. Similarly, if there are $C$ odd columns, then you need at least $C$ flips. Combining these tells us that we need $\max(R, C)$ or more moves to make the grid based.

On the other hand, for every move, we can choose the row and column to flip *independently*. Thus, it seems intuitive that $\max(R, C)$ moves are enough. And indeed, it is:
<div class="theorem">
**Theorem 1:** If the grid $G$ has exactly $R$ odd rows and exactly $C$ odd columns, then $B(G) = \max(R, C)$.
</div>

<details class="proof"><summary>Proof</summary>
Without loss of generality, assume $R \le C$ (we can rotate the grid otherwise), so our goal is to show that $B(G) = C$. Using our earlier argument, at least $\max(R, C) = C$ moves are needed, so all that remains is to show that $C$ moves are enough.

With a greedy strategy, we can turn $R$ odd rows and odd columns even with just $R$ moves; we end up with $0$ odd rows and $C - R$ odd columns. Then, for each of the $C - R$ remaining odd columns, we flip its topmost cell. This makes all columns even, and also all rows even, except potentially the topmost row.

Let&rsquo;s figure out what happens with the topmost row. After the $R$th move, it was even, and each of the final $C - R$ moves flipped it. Thus, it&rsquo;s even if and only if $C - R$ is even, which is equivalent to saying that $R$ and $C$ have the same parity.

But $R$ and $C$ clearly have the same parity, since $R \bmod 2$ is basically the sum of the *whole* grid modulo $2$ (why?), which is also $C \bmod 2$ for a similar reason, so we indeed have $(R \bmod 2) = (C \bmod 2)$. Thus, the topmost row is even after all $C$ moves, and $C$ moves are enough.
</details>

With this formula, we can now easily compute $B(G)$ by computing the parities of all rows and columns, computing $R$ and $C$ from those, and finally computing $B(G)$ as $\max(R, C)$.


### Implementation

Here&rsquo;s an implementation in C++.

**Note:** It looks quite a bit involved, mostly because of the backtracking, so if you can&rsquo;t grok this yet, I suggest skipping it for now and proceeding to the following sections which will describe solutions that are simpler to implement. Understanding this is *not* required to understand the following solutions.
<details class="code"><summary class="h4">Code (C++)</summary>

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll mod = 998'244'353;

ll solve(int r, int c) {
    vector<vector<int>> G(r, vector<int>(c));

    // this function computes B(G)
    auto B = [&]() {
        // compute parities of rows and columns
        vector<int> odd_row(r), odd_col(c);
        for (int i = 0; i < r; i++) {
            for (int j = 0; j < c; j++) {
                odd_row[i] ^= G[i][j];
                odd_col[j] ^= G[i][j];
            }
        }

        // compute the number of odd_ rows and columns
        int odd_row_count = 0, odd_col_count = 0;
        for (int odd : odd_row) odd_row_count += odd;
        for (int odd : odd_col) odd_col_count += odd;

        // return the larger
        return max(odd_row_count, odd_col_count);
    };

    // this function computes the sum of B(G)^3 across all
    // grids G, assuming all cells before cell (i, j) have
    // already been chosen.
    ll ans = 0;
    function<void(int,int)> sum_grids = [&](int i, int j) {
        if (i >= r) {
            // we're past the last row, so just compute B(G)^3
            ll b = B() % mod;
            (ans += b * b % mod * b) %= mod;
        } else if (j >= c) {
            // we're past the current row, so go to the next row
            sum_grids(i + 1, 0);
        } else {
            // try G[i][j] = 0 and G[i][j] = 1
            for (int v : {0, 1}) {
                G[i][j] = v;
                // ... then go to the next cell
                sum_grids(i, j + 1);
            }
        }
    };
    sum_grids(0, 0);
    
    return ans % mod;
}

int main() {
    int r, c;
    scanf("%d%d", &r, &c);
    printf("%lld\n", (solve(r, c) % mod + mod) % mod);
}
```
</details>
Running this with the input `5 5` gives the answer in \~3 seconds in my computer (when the program is compiled with the `-O3` optimization flag of `g++`).

As for the running time, we can write it as
$$\mathcal{O}((\text{number of grids})\times (\text{time to compute $B(G)$)}).$$
There are $2^{rc}$ grids, and we can compute $B(G)$ in $\mathcal{O}(rc)$ (why?), so the overall time complexity is $\mathcal{O}(2^{rc} rc)$.


### Solving via pen and paper?

This subtask can technically also be solved via pen and paper. The following sections deal with solutions to further subtasks that involve much less computation. Those computations are few enough that they can be done by hand (or with a spreadsheet) to solve this subtask.

</details>



<details class="editorial-section"><summary class="h2">Subtask 2</summary>

### A better approach

It&rsquo;s now clear that we can&rsquo;t go through all possible grids if we hope to solve the remaining subtasks within the lifetime of our sun; $2^{rc}$ is simply too large. On the other hand, the number of possible values of $B(G)$ is relatively small; it&rsquo;s always between $0$ and $\max(r, c)$. This suggests that a better approach might be to count the number of grids for each possible value of $B(G)$.

Inspired by this, let&rsquo;s define the function $\mathit{count}(r, c, b)$ to be the number of $r\times c$ grids $G$ such that $B(G) = b$. With this function, we can now write the answer as
$$\mathit{count}(r, c, 0)\cdot 0^3 + \mathit{count}(r, c, 1)\cdot 1^3 + \mathit{count}(r, c, 2)\cdot 2^3 + \ldots$$
with the sum going the way up to $b = \max(r, c)$; Written in summation notation, this is the same as
$$\sum_{b=0}^{\max(r,c)} \mathit{count}(r, c, b)\cdot b^3.$$

### Computing $\mathit{count}(r, c, b)$

Our goal now is to compute $\mathit{count}(r, c, b)$ for $0 \le b \le \max(r, c)$. There are a couple of ways to do this. In what follows, we&rsquo;ll describe an approach that&rsquo;s relatively straightforward conceptually (but not necessarily implementation-wise).

We know from earlier that $B(G) = \max(R, C)$, where $R$ and $C$ are the numbers of odd rows and columns, respectively. So we probably want to define a new function that counts the number of $r\times c$ grids with exactly $R$ odd rows and $C$ odd columns. Denoting that count by $f(r, c, R, C)$, it&rsquo;s easy to see that
$$\mathit{count}(r, c, b) = \sum_{\substack{R, C \\ \max(R, C) = b}} f(r, c, R, C).$$
So all that remains is to compute $f(r, c, R, C)$ for all $0 \le R \le r$ and $0 \le C \le c$.

Let&rsquo;s now compute $f(r, c, R, C)$. Let&rsquo;s choose which $R$ rows and $C$ columns will be odd, and after choosing these, let&rsquo;s count the number of grids. $f(r, c, R, C)$ will be the sum of these counts among all possible choices. However, since the rows are pretty much the same, as is the columns, these counts ought to be the same! In other words, we can write
$$f(r, c, R, C) = \binom{r}{R} \binom{c}{C} g(r, c, R, C),$$
where $g(r, c, R, C)$ is the number of $r\times c$ grids $G$ with a given selection of $R$ rows and $C$ columns odd, and the rest even. And as we&rsquo;ve just reasoned out, the actual choice doesn&rsquo;t matter, so let&rsquo;s say they&rsquo;re the $R$ topmost rows and the $C$ leftmost columns.


### Computing $g(r, c, R, C)$

So we want to build a grid with the $R$ topmost rows odd, and the $C$ leftmost columns even. For simplicity, let&rsquo;s assume that $0 < R < r$ and $0 < C < c$; we&rsquo;ll deal with edge cases later.

For example, if $r = 4$, $c = 9$, $R = 2$ and $C = 4$, then the grid we&rsquo;re building would look like this.
$$\begin{array}{|ccccccccc|c}
\text{odd} & \text{odd} & \text{odd} & \text{odd} & \text{even} & \text{even} & \text{even} & \text{even} & \text{even} & \\
\hline
\text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} &  \text{odd} \\
\text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} &  \text{odd} \\
\text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} &  \text{even} \\
\text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} &  \text{even} \\
\hline
\end{array}$$

A straightforward way to build a grid is to build it row by row. This can be stated recursively. First, we choose what the first row looks like. Then, we &ldquo;recursively&rdquo; construct the rest of the grid...somehow.

Let&rsquo;s now go into the details. First, because we assumed $R > 0$, the topmost row must be odd, so if it has exactly $x$ ones, then $x$ must be one of: $1, 3, 5, \ldots$. Fix such an $x$, and let&rsquo;s count the number of grids with exactly $x$ $1$s in the topmost row.

Now, the placement of these $x$ $1$s affects the parities of the columns. On the other hand, the $C$ leftmost columns are pretty much the same as each other, as is the $c - C$ rightmost columns. So if $y$ of these $x$ $1$s belong to the $C$ leftmost columns, and the $x - y$ remaining $1$s belong to the $c - C$ rightmost columns, then that means that, when looking at the &ldquo;rest of the grid&rdquo;, that is, *the grid with the first row removed*:

- $y$ of the $C$ leftmost columns are even, and the remaining $C - y$ are odd;
- $x - y$ of the $c - C$ rightmost columns are odd, and the remaining $(c - C) - (x - y)$ are even.

Thus, as far as the &ldquo;rest of the grid&rdquo; is concerned, there are exactly $C - y + x - y$ odd columns. We can now count the number of them recursively! Since the &ldquo;rest of the grid&rdquo; has $r - 1$ rows, and $R - 1$ of them must be odd, and there are $c$ columns, $C - y + x - y$ of which must be odd, there must be exactly
$$\binom{C}{y} \binom{c - C}{x - y} g(r - 1, c, R - 1, C - y + x - y)$$
such grids, where the binomial coefficients come from choosing which cells will contain the $1$s in the leftmost $C$ and the rightmost $c - C$ columns.

Now, the above count is just for a fixed choice of $x$ and $y$. To compute $g(r, c, R, C)$, we simply sum over all possible values of $x$ and $y$. We thus get the formula:
$$g(r, c, R, C) = \sum_{\substack{x=0 \\ \text{$x$ odd}}}^c \sum_{y=0}^x \binom{C}{y} \binom{c - C}{x - y} g(r - 1, c, R - 1, C - y + x - y).$$
We can now use this to compute $g(r, c, R, C)$. However, this is still incomplete, for a few reasons:

- The above only works if $R > 0$, which is how we knew that the topmost row is odd. If $R = 0$, then the topmost row is even. Well, we can still find a recursive formula similar to the above, just with a couple of changes (such as $x$ now being even, among other things). The formula we get when $R = 0$ is
$$g(r, c, R, C) = \sum_{\substack{x=0 \\ \text{$x$ even}}}^c \sum_{y=0}^x \binom{C}{y} \binom{c - C}{x - y} g(r - 1, c, R, C - y + x - y).$$

- We haven&rsquo;t discussed the base case yet! In our recursion above, the base case is $r = 0$, and the answer is pretty simple: there is only one grid with zero rows and $c$ columns, namely the *empty grid*. Each of its columns is even (because every column is empty, and $0$ is even). Therefore, we have
$$g(0, c, 0, C) = \begin{cases}
1 & \text{if $C = 0$} \\
0 & \text{otherwise.}
\end{cases}$$

- As an implementation detail, you should probably further restrict the summation formula to only those terms where $y \le C$ and $x - y \le c - C$, because $\binom{C}{y}$ or $\binom{c - C}{x - y}$ will be zero anyway. If you don&rsquo;t do this, then at first glance it seems like there won&rsquo;t be any issues since you seem to be just adding zero anyway. However, there&rsquo;s a subtle issue: the value $(C - y + x - y)$&mdash;an argument to the recursive call&mdash;has the potential to exceed $c$, which could become an off-by-one error depending on your implementation.


### Running time

With this, we now have a recursive algorithm to compute $g$, and thus an algorithm to compute $f$, $\mathit{count}$, and the answer. What is the running time? Well, for the algorithm to work, we need to be able to compute binomial coefficients. We can do that by simply building Pascal&rsquo;s triangle, which is basically a graphical manifestation of the recursive formula
$$\binom{n}{r} = \binom{n - 1}{r - 1} + \binom{n - 1}{r}$$
(with base cases $\binom{n}{0} = \binom{n}{n} = 1$). Thus, in our analysis, we can assume that we can compute any binomial coefficient we need with an $\mathcal{O}(1)$ lookup (after an $\mathcal{O}(\max(r, c)^2)$ precomputation; note that we only need up to row $\max(r, c)$ of Pascal&rsquo;s triangle).

So the algorithm consists of:

1. Computing the values $g(r, c, R, C)$ that we need.
2. Computing the values $f(r, c, R, C)$ that we need.
3. Computing the values $\mathit{count}(r, c, b)$ we need.
4. Computing the final sum to get the answer.

Now, it turns out that the first step is the bottleneck, because once we have all the $g$ values we need:

- Each of the $\mathcal{O}(rc)$ values of $f$ we need can be obtained from the corresponding value of $g$ in $\mathcal{O}(1)$ (using our formula).
- We only need the values $\mathit{count}(r, c, b)$ for $0 \le b \le \max(r, c)$. The formula for $\mathit{count}(r, c, b)$ contains at most $r + c + 1$ summands, so it can be computed in $\mathcal{O}(r + c)$ time. Thus, computing all values of $\mathit{count}$ we need takes $\mathcal{O}(\max(r, c)(r + c)) = \mathcal{O}(\max(r, c)^2)$ time.
- The final sum only has $\mathcal{O}(\max(r, c))$ summands.

So all that remains is to analyze the running time of computing the $g(r, c, R, C)$ values we need. Note that the value of the argument &ldquo;$r$&rdquo; here actually varies because of the recursion! On the other hand, notice that the value of $c$ doesn&rsquo;t change at all, so it might as well be fixed. So all in all, we want to compute $g(r', c, R, C)$ for all triples $(r', R, C)$ such that $0 \le R \le r' \le r$ and $0 \le C \le c$.

Now, in general, our formula for $g(r', c, R, C)$ involves a nested sum with $\mathcal{O}(c^2)$ summands (check), so the running time is basically
$$\mathcal{O}(c^2 \cdot (\text{number of distinct arguments})).$$
Also, there are $\mathcal{O}(r^2 c)$ distinct arguments to $g$ (why?), so this is simply $\mathcal{O}(r^2 c^3)$.

The overall running time is then $\mathcal{O}(r^2 c^3)$ since this also dominates all other steps (which are $\mathcal{O}(\max(r, c)^2)$ overall). For subtask 2, we have $r = 64$ and $c = 100$, and this might be too slow. However, we can improve the running time a bit with the following observations:

- The answer for $(r, c)$ is the same as the answer for $(c, r)$, so we may freely swap $r$ and $c$;
- The algorithm runs faster when $r > c$ (because the time complexity &ldquo;$\mathcal{O}(r^2 c^3)$&rdquo; is asymmetric with respect to $r$ and $c$).

Therefore, if $r < c$, we can simply *swap* $r$ and $c$ to make it run faster!

My Python 3 implementation of this solution, when given the input $r = 100$ and $c = 64$, runs in less than one minute.

In the next section, we&rsquo;ll discuss a solution that&rsquo;s much easier to implement and even gets you up to Subtask 3. However, even though the solution presented above is somewhat more involved (e.g., there are more nested loops), in some sense, it&rsquo;s simpler because you need less thinking to derive it; ultimately, it&rsquo;s really &ldquo;just DP&rdquo;.[^1]

</details>



<details class="editorial-section"><summary class="h2">Subtask 3</summary>

The previous solution will choke on subtask 3 because the input values are quite large. To improve on the previous solution, we need a better way to compute $\mathit{count}(r, c, b)$. Building the grid row-by-row is too slow.

It turns out that we can vastly improve our computation of $g(r, c, R, C)$ by building the grid *cell by cell* instead! (Recall that $g(r, c, R, C)$ is the number of $r \times c$ grids where the $R$ topmost rows and $C$ leftmost columns are odd.) To see what I mean, suppose we&rsquo;re choosing the values of the cells in order, left to right, then top to bottom. Now, each cell will contain $0$ or $1$, so generally, there are two choices we can make at every step.

However, things change a bit when we&rsquo;re choosing the rightmost cell of the current row. Since we know the parity of the row, there&rsquo;s really only one remaining choice for the rightmost cell that will give the row the correct parity!

For example, in the following grid, suppose we&rsquo;re now at the cell marked $X$. Since the row has to be odd, the value of $X$ must be $1$.
$$\begin{array}{|ccccccccc|c}
\text{odd} & \text{odd} & \text{odd} & \text{odd} & \text{even} & \text{even} & \text{even} & \text{even} & \text{even} & \\
\hline
1 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 1 &  \text{odd} \\
0 & 1 & 1 & 0 & 1 & 1 & 0 & 0 & X &  \text{odd} \\
\text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} &  \text{even} \\
\text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} &  \text{even} \\
\hline
\end{array}$$

Furthermore, things change again when we&rsquo;re choosing the cells at the bottommost rows. Since each column also has a fixed parity, each cell is again already determined; there&rsquo;s only one choice for each of those cells that will make the parity of the column correct.

For example, in the following grid, suppose we&rsquo;re now at $X$. Then since the column must be odd, the value of $X$ must be $0$.
$$\begin{array}{|ccccccccc|c}
\text{odd} & \text{odd} & \text{odd} & \text{odd} & \text{even} & \text{even} & \text{even} & \text{even} & \text{even} & \\
\hline
1 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 1 &  \text{odd} \\
0 & 1 & 1 & 0 & 1 & 1 & 0 & 0 & 1 &  \text{odd} \\
1 & 1 & 1 & 0 & 0 & 1 & 0 & 0 & 0 &  \text{even} \\
\text{1} & X & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} & \text{?} &  \text{even} \\
\hline
\end{array}$$


Finally, things get even more special when we reach the bottom-rightmost cell. In that case, it has to satisfy *two* conditions, one for the row, and one for the column. It turns out that both conditions are satisfiable if and only if $R$ and $C$ have the same parity (why?), and in that case, there&rsquo;s exactly one choice again!

Thus, we made exactly $(r - 1)(c - 1)$ independent binary choices, corresponding to the cells not in the rightmost column or bottommost row, and everything else is uniquely determined. Thus, we&rsquo;ve essentially proven the following:

<div class="theorem">

**Theorem 2:** For $r \ge 1$, $c \ge 1$, $0 \le R \le r$, $0 \le C \le c$, we have
$$g(r, c, R, C) = \begin{cases}
2^{(r - 1)(c - 1)} & \text{if $R$ and $C$ have the same parity;} \\
0 & \text{otherwise.}
\end{cases}$$

</div>

This formula simplifies our solution a lot! After precomputing the value of $2^{(r - 1)(c - 1)}$ (modulo $998244353$), computing all the values of $g(r, c, R, C)$ we need now only takes $\mathcal{O}(rc)$ time. And in fact, we can now compute the answer in $\mathcal{O}(rc)$ time overall, which is good enough up to subtask 3.

<div class="task">
**Exercise:** Show that this solution runs in $\mathcal{O}(rc)$ time.
</div>

</details>



<details class="editorial-section"><summary class="h2">Subtasks 4 & 5</summary>

For this subtask, $\mathcal{O}(rc)$ won&rsquo;t be enough. We want something faster.

I&rsquo;ll just leave you with a hint to get you started. (The solution of course needs more steps after this.)
<div class="task">
**Hint:** Try to count the number of grids $G$ for which $B(G) \le b$, rather than $B(G) = b$.
</div>

</details>

[^1]: DP stands for **dynamic programming**, a powerful algorithmic technique! There are training materials in the Discord server explaining it. Feel free to ask us to point you to the right direction!

