% Solution Writeup: The Glass Maze


# The Glass Maze  
## Solution Writeup

**Contest:** [TAMa 2023](https://noi.ph/tama-2023/)  
**Problem Idea:** Kevin Atienza  
**Testing:** Cassidy Tan, Vincent dela Cruz, JL Allas  
**Statement:** Cisco Ortega  
**Test Data Preparation:** Kevin Atienza  
**Solution Writeup:** Cisco Ortega  



<details class="editorial-section"><summary class="h2">Subtask 1</summary>

First of all, generate the entire grid $b$ by just plugging and chugging using the formula.  Use something like Python's `pow` function, or even Wolfram Alpha if you insist on doing the first subtask by hand.

From now on, let's call $W(i_s, j_s, i_t, j_t)$ the _best weak link_ between the two squares.  The weak link along any path is the _minimum_ grid value along that path.  We also say $s = (i_s, j_s)$ and $t = (i_t, j_t)$ to reduce clutter.

Consider a somewhat philosophical question: Why include the weak link at all in our path?  Why not only pick stronger tiles?  The answer must be, then, that we used the weakest link because we had no choice _but_ to use it.

So, let's endeavor to only use the strongest tiles for as long as we can help it, only choosing to use weaker tiles when it's clearly impossible with only stronger tiles, and our hand is forced. For two tiles $s$ and $t$, here is how we find their best weak link.

For each tile in the grid, call it either "to-be-used" or "to-be-avoided"; initialize all tiles to "to-be-avoided".  We say that $s$ and $t$ are  **connected** if there exists an NSEW-path between them that only uses to-be-used tiles; for now, let's not worry about how to determine connectivity with a program, since it's something that should be "clear to see" with your human eyes.  For example, in the example on the left, $(1, 2)$ and $(3, 4)$ are connected, but on the example on the right, they are not.

TODO

Our goal is to now to try to connect $s$ and $t$ while prioritizing the use of the strongest tiles.

- Start by setting $s$ and $t$ themselves as to-be-used (since any path between them necessarily includes $s$ and $t$ themselves).  Are they already connected? If so, we're done.
- If not, prioritize the strongest tile and set it as to-be-used.  Are $s$ and $t$ connected now?  If so, we're done.
- If not, prioritize the next strongest tile and set it as to-be-used.  Are $s$ and $t$ connected now?  If so, we're done.
- If not, prioritize the _next_ strongest tile and set it as to-be-used.  Are $s$ and $t$ connected now?  If so, we're done.
- ...

Repeat this until $s$ and $t$ do become connected.  The best weak link will be the value of the tile that caused $s$ and $t$ to be connected.  Its optimality comes from the fact that it is _necessary_---we showed that it is impossible to get from $s$ to $t$ using only stronger tiles.

Note that there is a bit of an edge case: technically, the weakest link is either the connecting tile _or one of $s$ and $t$ themselves_ if they happen to be weaker than it.  An easy way to fix the edge case is to just take the min grid value of $(s, t, \text{necessary connecting tile})$ when we exit.  An alternative fix is to modify the first step as follows:

- Start by setting $s$ and $t$ themselves as to-be-used, **along with all other tiles that are stronger than $s$ or $t$** (since we're forced into using $s$ and $t$ already anyway, these tiles can never make the solution worse).

In either case, just conducting this process for all $(s, t)$ pairs allows us to solve the problem for $n=4$ by hand, with a bit of effort (definitely with the help of a calculator or spreadsheet, though).

</details>



<details class="editorial-section"><summary class="h2">Subtask 2</summary>

When $n=12$, it is far too tedious to solve by hand.  Therefore, we can just use a computer and ask it to do the computation for us.  The previously described solution is pretty straightforward to directly translate into code, with **one exception**: determining if $s$ and $t$ are connected in the grid's current state.

To solve this, we turn to a standard algorithm such as **breadth first search** or **depth first search**, often called BFS or DFS in the community.  You can discover this by literally Googling "how check when two tiles in grid are connected".  Here is a screenshot of when I did; the StackOverflow link directly mentions DFS.  Now that you know the keyword, you can seek out a dedicated beginner-friendly tutorial for it (and there are many online).  May I recommend this one HYPERLINK, written by NOI.PH?

Anyway, there are $n^4 - n^2$ pairs of start and target tiles.  In each one, we perform a DFS/BFS up to $n^2$ times, once whenever we insert the next strongest tile in the grid and want to check connectivity again.  Finally, each DFS or BFS takes on the order of $\approx n^2$ operations.  

In conclusion, we have established an upper bound: our solution takes _at most_ $(n^4 - n^2) \times n^2 \times n^2$ operations (probably less, since we might achieve connectedness after a few insertions).  If you plug in $n=12$, we get a number whose order of magnitude is $\approx 10^8$, so our solution shouldn't take more than a few seconds to terminate.

</details>



<details class="editorial-section"><summary class="h2">Subtask 3</summary>

<div class="remarks">
*Construction ongoing!* &nbsp;&nbsp; &#127959; &#128679; &#128679; &#128679; &#128679; &#128679; &#128679; &#128679; &#128679; &#128679; &#128679; &#128679; &#129521;
</div>

</details>



