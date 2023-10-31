% Solution Writeup: Fruity Fractions


# Fruity Fractions  
## Solution Writeup

**Contest:** [TAMa 2023](https://noi.ph/tama-2023/)  
**Problem Idea:** Kevin Atienza  
**Testing:** Vincent dela Cruz  
**Statement:** Cisco Ortega  
**Test Data Preparation:** Kevin Atienza  
**Solution Writeup:** Cisco Ortega, Kevin Atienza  



<details class="editorial-section"><summary class="h2">Subtask 1</summary>

Let the apple emoji &#127822; be $x$, the banana emoji &#127820; be $y$, and the coconut emoji &#129381; be $z$.

First, note that floating point is the devil.  So, as one normally does with rational functions, let&rsquo;s multiply through both sides by a common denominator and move everything to one side.

To be a bit less cluttered, let $s = x + 2z$ and $t = 2x - y + 3z$.  Then, we should get:
$$
    \frac{2syt + 2xyt - 3xst - xsy}{xsyt} = 0.
$$
And again, as is typical for rational functions, we know that the entire expression equals $0$ when $2syt + 2xyt - 3xst - xsy = 0$ and $x \neq 0$ and $s \neq 0$ and $y \neq 0$ and $t \neq 0$.

This can all be done using integer arithmetic!  Perfect!

A simple brute force solution is to enumerate **all** tuples of $(x, y, z)$ where $-n \leq x, y, z \leq n$ (say, using three nested for loops) and count the number of tuples for which the above criteria hold.  The total amount of work is proportional to $(2n+1)^3$, the number of tested tuples, and with $n=3^5 = 243$, this approach is fast enough for the first subtask.

</details>



<details class="editorial-section"><summary class="h2">Subtask 2</summary>

Let&rsquo;s write the numerator entirely in terms of $x$, $y$, and $z$:
$$
    2(x+2z)y(2x - y + 3z) + 2xy(2x - y + 3z) - 2x(x+2z)(2x - y + 3z) - 2x(x+2z)y = 0.
$$
If we expand this out and collect like terms, we should get an equation that looks something like this:
$$
    Ax^3 + Bx^2y + Cxy^2 + Dy^2z + Eyz^2 + Fx^2z + Gxz^2 + Hxyz = 0,
$$
where $A, B, C, D, E, F, G, H$ are some constants whose values I won&rsquo;t spell out here (you can do the algebra on pen-and-paper or using a computer algebra system to get these coefficients yourself).

However, note that once $x$ and $y$ are selected, then our choices for $z$ are &ldquo;locked in&rdquo;; when only $z$ is left to vary, we are left with a one-variable equation, which we know how to solve!  In particular:
$$
    (Ey + Gx)z^2 + (Dy^2 + Fx^2 + Hxy)z + (Ax^3 + Bx^2y + Cxy^2) = 0.
$$
If $x$ and $y$ are fixed, then this just becomes a quadratic equation in terms of $z$, and we know how to solve those!  So, precisely, we get the following solution:

- Enumerate all pairs $(x, y)$ such that $-n \leq x, y \leq n$.  For each one:
    - Use the quadratic formula to solve for what values of $z$ satisfy the equation.
    - For each distinct solution of $z$ that (a) is an integer; and (b) lies within $-n$ to $n$, add $+1$ to the answer.
        - Remember also to not count solutions which would make any of the denominators equal to $0$

You also have to handle some other edge cases, such as what to do if $Ey + Gx = 0$, but those are implementation details you can figure out yourself.  The amount of work done is now only proportional to $(2n+1)^2$ (since we only enumerate all possible $x$ and $y$).  With $n = 5^5 = 3125$, this approach is fast enough for the second subtask.

</details>



<details class="editorial-section"><summary class="h2">Subtask 3</summary>

The previous algorithm is too slow for subtasks 3 and 4. This is because the amount of work grows quadratically with respect to $n$, and for $n = 5^{10} = 9765625$, we have $(2n+1)^2 \approx 4\cdot 10^{14}$, which is quite large; a computer that can do $1$ billion operations per second (a.k.a. &ldquo;1 gigahertz&rdquo;) will take several days to solve this problem with the previous algorithm.

Anyway, for this subtask, we will just give you hints on how to proceed. But for these hints to be helpful, you probably should first know how to solve degree $1$ and degree $2$ Diophantine equations. (The current equation is of degree $3$.) There are plenty of those you can practice on in Project Euler. You could also refer to [this video (specifically Method 2)](https://www.youtube.com/watch?v=SCdDBYRrDtM&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=44) for inspiration.

<details class="task"><summary class="h4">Hint 1</summary>
If $(x, y, z)$ is an integer solution, then $(n x, n y, n z)$ is also an integer solution for any integer $n$. In fact, $(\alpha x, \alpha y, \alpha z)$ is a *rational* solution for any rational $\alpha$.

(Basically, &ldquo;$f$ is *homogeneous*.&rdquo;)

If you think about this some more, it means that if we write our equation as
$$f(x, y, z) = 0,$$
then integer solutions to this are related to rational solutions of
$$f(X, Y, 1) = 0.$$
</details>

<details class="task"><summary class="h4">Hint 2</summary>
Because $f$ is homogeneous of degree $3$, the graph of $f(X, Y, 1) = 0$ is a *cubic* curve, which renders the corresponding rational equation hard to solve. (We can generally solve up to degree $2$ easily, but degree $3$ is where dragons[^1] roam.)

However, if you actually draw/plot the graph of $f(X, Y, 1) = 0$, you should see *something curious*...
</details>

</details>

[^1]: that is, dragons known as *elliptic curves*
